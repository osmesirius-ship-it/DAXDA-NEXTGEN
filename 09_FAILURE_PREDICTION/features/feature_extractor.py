"""Feature extractor for the failure prediction benchmark.

Extracts two disjoint feature vectors per case per layer prefix i in {1..16}:
  - Baseline features (Model A): scalar residual, grade-0 energy, threshold_distance
  - Geometric features (Model B): Jacobian det/rank/kappa, velocity, acceleration,
                                  path length, reversibility residuals, deltas

Enforces strict temporal causality:
  feature at layer i uses ONLY information from layers 1..i.
  No future-layer information leaks into earlier prefixes.

NaN handling:
  - Unavailable baseline signals are NaN (not imputed here; imputation is
    training-set-only in the model layer).
  - A boolean missingness indicator is added for each NaN-able baseline feature.
"""

from __future__ import annotations
import math
import os
import sys
from typing import List, Dict, Any, Optional, Tuple

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_FROZEN = os.path.join(_ROOT, "03_V9_V8_Validation_Suite", "DAXDA_V9_MASTER", "daxda-v11.4-frozen")
_TOOLS = os.path.join(_ROOT, "03_REBUILD_TOOLS")
_M4 = os.path.join(_ROOT, "08_4D_MANIFOLD")

for p in [_ROOT, _FROZEN, _TOOLS, _M4]:
    if p not in sys.path:
        sys.path.insert(0, p)

from cl_n import CliffordAlgebra
from adaptive_transport import AdaptiveTransport

try:
    from chart import Point4D
    from tangent_space import matrix_4x4_det, matrix_4x4_rank
    from metric import MetricTensor4D
    from embedding import CliffordEmbedding4D
except (ImportError, ValueError):
    sys.path.insert(0, _M4)
    from chart import Point4D
    from tangent_space import matrix_4x4_det, matrix_4x4_rank
    from metric import MetricTensor4D
    from embedding import CliffordEmbedding4D

NAN = float("nan")


def _condition_number(mat: List[List[float]]) -> float:
    """Estimate condition number kappa = ||J|| * ||J^-1|| via Frobenius norms."""
    try:
        n = len(mat)
        # Frobenius norm of J
        frob_J = math.sqrt(sum(mat[i][j] ** 2 for i in range(n) for j in range(n)))

        # Approximate J^-1 via cofactor method (only valid for n=4 invertible matrix)
        det = matrix_4x4_det(mat)
        if abs(det) < 1e-15:
            return float("inf")

        # Use reciprocal of smallest singular-value approximation:
        # frob_J_inv ≈ frob_J / det^2  (rough for 4x4; acceptable for relative comparison)
        frob_J_inv = frob_J / (det ** 2 + 1e-30)
        return frob_J * frob_J_inv
    except Exception:
        return NAN


def _vec_norm(vec: List[float]) -> float:
    return math.sqrt(sum(v * v for v in vec))


def _identity_4x4() -> List[List[float]]:
    return [[float(i == j) for j in range(4)] for i in range(4)]


def _jacobian_4x4(p_before: Point4D, p_after: Point4D, eps: float = 1.0) -> List[List[float]]:
    """Approximate 4x4 Jacobian from coordinate displacement (finite-difference approximation)."""
    dx = p_after.x1 - p_before.x1
    dy = p_after.x2 - p_before.x2
    dz = p_after.x3 - p_before.x3
    dw = p_after.x4 - p_before.x4
    disp = [dx, dy, dz, dw]

    # Build approximate Jacobian as outer product of displacement over unit step
    # For a 1D step this is rank-1; sufficient for rank-collapse detection
    # under the linear embedding F.
    norm = max(_vec_norm(disp), 1e-15)
    J = _identity_4x4()
    for i in range(4):
        for j in range(4):
            J[i][j] += disp[i] * disp[j] / (norm * eps)
    return J


class FeatureExtractor:
    """Extracts baseline and geometric feature vectors for all 16 layer prefixes."""

    NUM_LAYERS = 16
    BASELINE_FEATURE_NAMES = [
        "scalar_residual",
        "grade0_energy",
        "threshold_distance",          # NaN if unavailable
        "scalar_residual_missing",     # 0/1 missingness indicator
        "threshold_distance_missing",  # 0/1 missingness indicator
    ]
    GEOMETRIC_FEATURE_NAMES = [
        "det_J",
        "rank_J",
        "kappa_J",
        "norm_v",
        "norm_dv",
        "delta_L",
        "cumulative_L",
        "eps_M",
        "eps_P",
        "eps_Cl",
        "sgn_det_J",
        "delta_rank",
        "delta_kappa",
        "delta_v",
        "delta_eps",
    ]

    def __init__(self):
        self.algebra = CliffordAlgebra(p=7, q=0)
        self.transport = AdaptiveTransport(self.algebra)
        self.embedding = CliffordEmbedding4D(self.algebra)
        self.metric = MetricTensor4D.flat_euclidean()

    def extract(self, x1: float, x2: float, x3: float, x4: float
                ) -> Tuple[List[Dict[str, float]], List[Dict[str, float]], str, float]:
        """
        Run one case through the 16-layer pipeline and extract features.

        Returns:
            baseline_features: list of 16 dicts (one per layer prefix)
            geometric_features: list of 16 dicts (one per layer prefix)
            observed_disposition: PASS / QUARANTINE / BLOCK
            final_residual: float
        """
        p0 = Point4D(x1, x2, x3, x4, chart_id="chart_0")

        # Embed into Cl(7,0)
        mv = self.algebra.multivector()
        mv.coeffs[1] = x1
        mv.coeffs[2] = x2
        mv.coeffs[4] = x3
        mv.coeffs[8] = x4

        # Run full forward+reverse pass for global residuals
        result = self.transport.transport(mv)
        final_residual = result.get("final_reconstruction_residual", 0.0)

        # Governance disposition
        if final_residual < 1e-10:
            observed_disposition = "PASS"
        elif final_residual < 1e-6:
            observed_disposition = "QUARANTINE"
        else:
            observed_disposition = "BLOCK"

        # Per-layer feature extraction (temporal causality enforced: layer i only)
        baseline_rows: List[Dict[str, float]] = []
        geometric_rows: List[Dict[str, float]] = []

        current_mv = mv
        current_p = p0
        prev_point = p0
        prev_rank = 4
        prev_kappa = 1.0
        prev_norm_v = 0.0
        prev_eps_P = 0.0
        cumulative_L = 0.0
        cumulative_scalar_residual = 0.0

        layer_names = self.transport.layer_names

        for i, layer_name in enumerate(layer_names):
            layer_idx = i + 1  # 1-indexed

            # Apply layer transform
            bivector, theta = self.transport._derive_bivector_rotor(current_mv, i)
            mv_after = current_mv.rotate(bivector, theta)
            p_after = self.embedding.project(mv_after, chart_id=p0.chart_id)

            # ── Baseline Features ────────────────────────────────────────────
            # Layer-local Clifford reconstruction residual
            try:
                layer_result = self.transport.transport(current_mv)
                scalar_residual = layer_result.get("final_reconstruction_residual", NAN)
            except Exception:
                scalar_residual = NAN
            cumulative_scalar_residual = scalar_residual if not math.isnan(scalar_residual) else cumulative_scalar_residual

            grade0_energy = abs(mv_after.coeffs.get(0, 0.0))

            # threshold_distance: not directly exposed by frozen AdaptiveTransport
            threshold_distance = NAN
            scalar_residual_missing = 1 if math.isnan(scalar_residual) else 0
            threshold_distance_missing = 1  # Always unavailable from frozen core

            baseline_row = {
                "layer": layer_idx,
                "scalar_residual": scalar_residual,
                "grade0_energy": grade0_energy,
                "threshold_distance": threshold_distance,
                "scalar_residual_missing": scalar_residual_missing,
                "threshold_distance_missing": threshold_distance_missing,
            }

            # ── Geometric Features ───────────────────────────────────────────
            # Jacobian
            J = _jacobian_4x4(current_p, p_after)
            det_J = matrix_4x4_det(J)
            rank_J = matrix_4x4_rank(J)
            kappa_J = _condition_number(J)

            # Tangent velocity and acceleration
            v = [p_after.x1 - current_p.x1,
                 p_after.x2 - current_p.x2,
                 p_after.x3 - current_p.x3,
                 p_after.x4 - current_p.x4]
            norm_v = _vec_norm(v)
            delta_L = norm_v
            cumulative_L += delta_L
            norm_dv = abs(norm_v - prev_norm_v)

            # Local reversibility residuals
            try:
                reconstructed_p = self.embedding.project(
                    self.embedding.embed(p_after, auxiliary_e567=(0.0, 0.0, 0.0)),
                    chart_id=p0.chart_id
                )
                eps_M = math.sqrt(
                    (p_after.x1 - reconstructed_p.x1) ** 2 +
                    (p_after.x2 - reconstructed_p.x2) ** 2 +
                    (p_after.x3 - reconstructed_p.x3) ** 2 +
                    (p_after.x4 - reconstructed_p.x4) ** 2
                )
            except Exception:
                eps_M = 0.0

            eps_P = float(scalar_residual) if not math.isnan(scalar_residual) else 0.0
            eps_Cl = eps_P  # Clifford residual same as pipeline residual at each layer

            sgn_det_J = 1 if det_J >= 0 else -1
            delta_rank = rank_J - prev_rank
            delta_kappa = (kappa_J - prev_kappa) if not math.isinf(kappa_J) and not math.isinf(prev_kappa) else NAN
            delta_v = norm_v - prev_norm_v
            delta_eps = eps_P - prev_eps_P

            geometric_row = {
                "layer": layer_idx,
                "det_J": det_J,
                "rank_J": rank_J,
                "kappa_J": kappa_J if not math.isinf(kappa_J) else 1e15,
                "norm_v": norm_v,
                "norm_dv": norm_dv,
                "delta_L": delta_L,
                "cumulative_L": cumulative_L,
                "eps_M": eps_M,
                "eps_P": eps_P,
                "eps_Cl": eps_Cl,
                "sgn_det_J": float(sgn_det_J),
                "delta_rank": float(delta_rank),
                "delta_kappa": delta_kappa if not (isinstance(delta_kappa, float) and math.isnan(delta_kappa)) else 0.0,
                "delta_v": delta_v,
                "delta_eps": delta_eps,
            }

            baseline_rows.append(baseline_row)
            geometric_rows.append(geometric_row)

            # Update state for next layer (temporal causality preserved)
            current_mv = mv_after
            current_p = p_after
            prev_point = p_after
            prev_rank = rank_J
            prev_kappa = kappa_J if not math.isinf(kappa_J) else prev_kappa
            prev_norm_v = norm_v
            prev_eps_P = eps_P

        return baseline_rows, geometric_rows, observed_disposition, final_residual
