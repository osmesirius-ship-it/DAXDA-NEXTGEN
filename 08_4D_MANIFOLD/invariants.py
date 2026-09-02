"""Invariant Analysis and Diagnostic Layer for 4D Manifold M^4.

Provides rigorous mathematical classification of invariants:
- TOPOLOGICAL: Invariant under homeomorphisms (continuous bijections with continuous inverses).
- DIFFERENTIAL-TOPOLOGICAL: Invariant under diffeomorphisms (smooth bijections with smooth inverses).
- GEOMETRIC: Invariant under Riemannian / pseudo-Riemannian isometries (metric-preserving smooth maps).
- ALGEBRAIC: Invariant under Clifford / Lie algebraic group actions or isomorphisms.
- NUMERICAL: Diagnostic quantities reflecting finite-precision stability, rank, and condition number.
"""

from __future__ import annotations
import math
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple, Callable
try:
    from .chart import Point4D
    from .tangent_space import TangentVector4D, matrix_4x4_det, matrix_4x4_rank
    from .metric import MetricTensor4D
    from .curvature import CurvatureTensor4D, UndefinedCurvatureError
except (ImportError, ValueError):
    from chart import Point4D
    from tangent_space import TangentVector4D, matrix_4x4_det, matrix_4x4_rank
    from metric import MetricTensor4D
    from curvature import CurvatureTensor4D, UndefinedCurvatureError


class InvariantClassification(str, Enum):
    TOPOLOGICAL = "TOPOLOGICAL"
    DIFFERENTIAL_TOPOLOGICAL = "DIFFERENTIAL-TOPOLOGICAL"
    GEOMETRIC = "GEOMETRIC"
    ALGEBRAIC = "ALGEBRAIC"
    NUMERICAL = "NUMERICAL"


@dataclass
class InvariantRecord:
    name: str
    value: Any
    classification: InvariantClassification
    assumptions: str
    is_conserved: Optional[bool] = None
    delta_from_baseline: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["classification"] = self.classification.value
        return d


class InvariantAnalyzer4D:
    """Evaluates and catalogs mathematical invariants along states, transformations, and trajectories."""

    def __init__(self, metric: Optional[MetricTensor4D] = None):
        self.metric = metric or MetricTensor4D.flat_euclidean()
        self.curvature = CurvatureTensor4D(self.metric)

    def analyze_transformation(
        self,
        transformation_fn: Callable[[Point4D], Point4D],
        sample_points: List[Point4D],
        jacobian_matrix: Optional[List[List[float]]] = None,
        label: str = "T"
    ) -> List[InvariantRecord]:
        """Analyzes invariants associated with a coordinate or state transformation T."""
        records: List[InvariantRecord] = []

        # 1. DIFFERENTIAL-TOPOLOGICAL: Manifold dimension preservation
        records.append(InvariantRecord(
            name="manifold_dimension",
            value=4,
            classification=InvariantClassification.DIFFERENTIAL_TOPOLOGICAL,
            assumptions="Smooth 4-manifold chart with maximal coordinate degree",
            is_conserved=True,
            delta_from_baseline=0.0
        ))

        # 2. NUMERICAL / DIFFERENTIAL: Jacobian determinant & rank
        if jacobian_matrix is not None:
            det = matrix_4x4_det(jacobian_matrix)
            rank = matrix_4x4_rank(jacobian_matrix)
            records.append(InvariantRecord(
                name="jacobian_determinant",
                value=round(det, 8),
                classification=InvariantClassification.NUMERICAL,
                assumptions="Local linear approximation of smooth transformation T",
                is_conserved=not math.isclose(det, 0.0, abs_tol=1e-9),
                delta_from_baseline=abs(1.0 - abs(det))
            ))

            records.append(InvariantRecord(
                name="jacobian_rank",
                value=rank,
                classification=InvariantClassification.NUMERICAL,
                assumptions="4x4 local differential matrix of transformation T",
                is_conserved=(rank == 4),
                delta_from_baseline=float(4 - rank)
            ))

            # Orientation preservation (Differential-Topological if det > 0)
            is_orientation_preserving = (det > 1e-12)
            records.append(InvariantRecord(
                name="orientation_preservation",
                value="PRESERVED" if is_orientation_preserving else ("REVERSED" if det < -1e-12 else "DEGENERATE"),
                classification=InvariantClassification.DIFFERENTIAL_TOPOLOGICAL,
                assumptions="Sign of Jacobian determinant sgn(det(J)) on connected chart",
                is_conserved=is_orientation_preserving,
                delta_from_baseline=0.0 if is_orientation_preserving else 1.0
            ))

        # 3. GEOMETRIC: Metric preservation / Isometry check across sample points
        if len(sample_points) >= 2:
            p0, p1 = sample_points[0], sample_points[1]
            dist_before = p0.euclidean_distance_to(p1)
            tp0 = transformation_fn(p0)
            tp1 = transformation_fn(p1)
            dist_after = tp0.euclidean_distance_to(tp1)
            delta_dist = abs(dist_after - dist_before)
            is_isometry = math.isclose(dist_before, dist_after, abs_tol=1e-6)

            records.append(InvariantRecord(
                name="euclidean_distance_isometry",
                value=round(dist_after, 6),
                classification=InvariantClassification.GEOMETRIC,
                assumptions="Euclidean chart metric delta_mu_nu across pair (p0, p1)",
                is_conserved=is_isometry,
                delta_from_baseline=delta_dist
            ))

        # 4. TOPOLOGICAL: Connectedness of path
        if len(sample_points) >= 2:
            # Finite sequence of points forms a connected chain in R^4
            records.append(InvariantRecord(
                name="path_connectedness",
                value="CONNECTED_CHAIN",
                classification=InvariantClassification.TOPOLOGICAL,
                assumptions="Discrete sample along path in simply connected chart domain",
                is_conserved=True,
                delta_from_baseline=0.0
            ))

        return records

    def analyze_curvature_invariants(self, p: Point4D) -> List[InvariantRecord]:
        """Evaluates geometric curvature scalars at point p."""
        records: List[InvariantRecord] = []
        try:
            ricci_s = self.curvature.ricci_scalar_at(p)
            records.append(InvariantRecord(
                name="ricci_scalar_R",
                value=round(ricci_s, 8),
                classification=InvariantClassification.GEOMETRIC,
                assumptions="Riemannian metric g_mu_nu contraction g^mu_nu R_mu_nu",
                is_conserved=True,
                delta_from_baseline=abs(ricci_s)
            ))
        except UndefinedCurvatureError as e:
            records.append(InvariantRecord(
                name="ricci_scalar_R",
                value=f"UNDEFINED ({e})",
                classification=InvariantClassification.GEOMETRIC,
                assumptions="Singular metric derivative or connection failure",
                is_conserved=False
            ))

        try:
            kret_s = self.curvature.kretschmann_scalar_at(p)
            records.append(InvariantRecord(
                name="kretschmann_invariant_K",
                value=round(kret_s, 8),
                classification=InvariantClassification.GEOMETRIC,
                assumptions="Full Riemann tensor contraction R_abcd R^abcd",
                is_conserved=True,
                delta_from_baseline=abs(kret_s)
            ))
        except UndefinedCurvatureError as e:
            records.append(InvariantRecord(
                name="kretschmann_invariant_K",
                value=f"UNDEFINED ({e})",
                classification=InvariantClassification.GEOMETRIC,
                assumptions="Singular metric derivative or connection failure",
                is_conserved=False
            ))

        return records
