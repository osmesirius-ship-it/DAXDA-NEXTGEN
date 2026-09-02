"""Clifford Cl(7,0) Embedding and Projection for 4D Manifold States."""

from __future__ import annotations
import math
import sys
import os
from typing import Tuple, Dict, Any, List, Optional, Callable

# Add frozen core path to access cl_n without modifying frozen files
_FROZEN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_V9_V8_Validation_Suite", "DAXDA_V9_MASTER", "daxda-v11.4-frozen"))
if _FROZEN_DIR not in sys.path:
    sys.path.insert(0, _FROZEN_DIR)

try:
    from cl_n import CliffordAlgebra, Multivector
except ImportError:
    raise ImportError(f"Could not import cl_n from frozen directory: {_FROZEN_DIR}")

try:
    from .chart import Point4D
except (ImportError, ValueError):
    from chart import Point4D


class CliffordEmbedding4D:
    """Explicit mapping F : M^4 -> Cl(7,0) and projection Pi : Cl(7,0) -> M^4."""

    def __init__(self, algebra: Optional[CliffordAlgebra] = None):
        # DAXDA's standard Cl(7,0) algebra (128 basis blades)
        self.algebra = algebra or CliffordAlgebra(p=7, q=0)
        # Basis vector index lookup in Cl(7,0):
        # 1-vectors are stored at 2^i: e1 -> 1, e2 -> 2, e3 -> 4, e4 -> 8, e5 -> 16, e6 -> 32, e7 -> 64
        self.e1_idx = 1
        self.e2_idx = 2
        self.e3_idx = 4
        self.e4_idx = 8
        self.e5_idx = 16
        self.e6_idx = 32
        self.e7_idx = 64

    def embed(
        self,
        point: Point4D,
        auxiliary_e567: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    ) -> Multivector:
        """Injective baseline linear embedding F(x1,x2,x3,x4) = x1 e1 + x2 e2 + x3 e3 + x4 e4 (+ aux).
        
        Args:
            point: Point4D in local coordinates (x1, x2, x3, x4)
            auxiliary_e567: Optional coefficients for remaining auxiliary generators (e5, e6, e7).
                           Treated purely as auxiliary algebraic coordinates.
        """
        mv = Multivector(self.algebra)
        mv.coeffs[self.e1_idx] = float(point.x1)
        mv.coeffs[self.e2_idx] = float(point.x2)
        mv.coeffs[self.e3_idx] = float(point.x3)
        mv.coeffs[self.e4_idx] = float(point.x4)

        if auxiliary_e567[0] != 0.0:
            mv.coeffs[self.e5_idx] = float(auxiliary_e567[0])
        if auxiliary_e567[1] != 0.0:
            mv.coeffs[self.e6_idx] = float(auxiliary_e567[1])
        if auxiliary_e567[2] != 0.0:
            mv.coeffs[self.e7_idx] = float(auxiliary_e567[2])

        return mv

    def project(self, mv: Multivector, chart_id: str = "U0") -> Point4D:
        """Canonical projection Pi : Cl(7,0) -> M^4 extracting (e1, e2, e3, e4) components."""
        x1 = mv.coeffs[self.e1_idx]
        x2 = mv.coeffs[self.e2_idx]
        x3 = mv.coeffs[self.e3_idx]
        x4 = mv.coeffs[self.e4_idx]
        return Point4D(x1, x2, x3, x4, chart_id=chart_id)

    def extract_auxiliary(self, mv: Multivector) -> Tuple[float, float, float]:
        """Extracts auxiliary degrees of freedom (e5, e6, e7) from multivector."""
        return (
            mv.coeffs[self.e5_idx],
            mv.coeffs[self.e6_idx],
            mv.coeffs[self.e7_idx]
        )

    def test_projection_roundtrip(self, point: Point4D) -> Tuple[Point4D, float]:
        """Tests Pi(F(x)) = x and measures projection residual epsilon = ||x - Pi(F(x))||."""
        embedded = self.embed(point)
        projected = self.project(embedded, chart_id=point.chart_id)
        residual = point.euclidean_distance_to(projected)
        return projected, residual

    def test_information_loss(
        self,
        points: List[Point4D],
        collision_tolerance: float = 1e-12
    ) -> Dict[str, Any]:
        """Tests whether distinct points in M^4 produce identical/colliding Clifford representations."""
        n = len(points)
        collisions = []
        max_residual = 0.0

        for i in range(n):
            p_i = points[i]
            proj, res = self.test_projection_roundtrip(p_i)
            if res > max_residual:
                max_residual = res

            for j in range(i + 1, n):
                p_j = points[j]
                spatial_dist = p_i.euclidean_distance_to(p_j)
                if spatial_dist > collision_tolerance:
                    # They are distinct in M^4; check their Clifford representations
                    mv_i = self.embed(p_i)
                    mv_j = self.embed(p_j)
                    diff_mag = (mv_i - mv_j).magnitude()

                    if diff_mag <= collision_tolerance:
                        collisions.append({
                            "index_a": i,
                            "index_b": j,
                            "point_a": p_i.to_dict(),
                            "point_b": p_j.to_dict(),
                            "spatial_dist": spatial_dist,
                            "clifford_diff": diff_mag
                        })

        return {
            "total_points_tested": n,
            "distinct_pairs_tested": n * (n - 1) // 2,
            "collisions_detected": len(collisions),
            "collision_details": collisions,
            "max_projection_residual": max_residual,
            "is_strictly_injective": len(collisions) == 0 and max_residual < collision_tolerance
        }
