"""Coordinate Charts, Points, and Transition Maps for 4D Manifold M^4."""

from __future__ import annotations
import math
from typing import Tuple, Callable, Optional, Dict, Any, List


class Point4D:
    """Represents a point on a 4-dimensional manifold in local chart coordinates."""
    
    __slots__ = ("_coords", "_chart_id")

    def __init__(self, x1: float, x2: float, x3: float, x4: float, chart_id: str = "U0"):
        self._coords: Tuple[float, float, float, float] = (
            float(x1), float(x2), float(x3), float(x4)
        )
        self._chart_id = str(chart_id)

    @classmethod
    def from_tuple(cls, coords: Tuple[float, float, float, float], chart_id: str = "U0") -> Point4D:
        if len(coords) != 4:
            raise ValueError(f"Point4D requires exactly 4 coordinates, got {len(coords)}")
        return cls(coords[0], coords[1], coords[2], coords[3], chart_id=chart_id)

    @classmethod
    def zero(cls, chart_id: str = "U0") -> Point4D:
        return cls(0.0, 0.0, 0.0, 0.0, chart_id=chart_id)

    @property
    def x1(self) -> float:
        return self._coords[0]

    @property
    def x2(self) -> float:
        return self._coords[1]

    @property
    def x3(self) -> float:
        return self._coords[2]

    @property
    def x4(self) -> float:
        return self._coords[3]

    @property
    def coords(self) -> Tuple[float, float, float, float]:
        return self._coords

    @property
    def chart_id(self) -> str:
        return self._chart_id

    def __getitem__(self, index: int) -> float:
        return self._coords[index]

    def __len__(self) -> int:
        return 4

    def __repr__(self) -> str:
        return f"Point4D({self.x1:.6f}, {self.x2:.6f}, {self.x3:.6f}, {self.x4:.6f}, chart='{self._chart_id}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point4D):
            return False
        return self._chart_id == other._chart_id and all(
            math.isclose(a, b, abs_tol=1e-12) for a, b in zip(self._coords, other._coords)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chart_id": self._chart_id,
            "coords": [self.x1, self.x2, self.x3, self.x4]
        }

    def euclidean_distance_to(self, other: Point4D) -> float:
        """Euclidean distance in local chart coordinates."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self._coords, other._coords)))


class Chart4D:
    """Local coordinate chart phi_i : U_i -> R^4."""

    def __init__(
        self,
        chart_id: str = "U0",
        domain_predicate: Optional[Callable[[Point4D], bool]] = None,
        description: str = "Canonical 4D Cartesian Chart"
    ):
        self.chart_id = chart_id
        self.domain_predicate = domain_predicate or (lambda p: True)
        self.description = description
        self.dim = 4

    def contains(self, point: Point4D) -> bool:
        """Checks whether a point lies within the open domain U_i of the chart."""
        return bool(self.domain_predicate(point))

    def validate_point(self, point: Point4D) -> None:
        if not self.contains(point):
            raise ValueError(f"Point {point} is outside the valid domain of chart '{self.chart_id}'")


class CoordinatePatch4D:
    """Manages an atlas of 4D charts and transition maps phi_ij : U_i cap U_j -> R^4."""

    def __init__(self):
        self.charts: Dict[str, Chart4D] = {}
        # Transitions keyed by (source_chart_id, target_chart_id)
        self.transitions: Dict[
            Tuple[str, str],
            Callable[[Point4D], Point4D]
        ] = {}
        self.transition_jacobians: Dict[
            Tuple[str, str],
            Callable[[Point4D], List[List[float]]]
        ] = {}

    def add_chart(self, chart: Chart4D) -> None:
        self.charts[chart.chart_id] = chart

    def register_transition(
        self,
        from_chart: str,
        to_chart: str,
        map_fn: Callable[[Point4D], Point4D],
        jacobian_fn: Optional[Callable[[Point4D], List[List[float]]]] = None
    ) -> None:
        if from_chart not in self.charts or to_chart not in self.charts:
            raise KeyError(f"Both charts '{from_chart}' and '{to_chart}' must be registered before transition.")
        self.transitions[(from_chart, to_chart)] = map_fn
        if jacobian_fn is not None:
            self.transition_jacobians[(from_chart, to_chart)] = jacobian_fn

    def transition(self, point: Point4D, target_chart: str) -> Point4D:
        """Transforms a point from its current chart into the target chart."""
        source_chart = point.chart_id
        if source_chart == target_chart:
            return point

        if (source_chart, target_chart) not in self.transitions:
            raise KeyError(
                f"No transition map registered from chart '{source_chart}' to chart '{target_chart}'"
            )

        self.charts[source_chart].validate_point(point)
        target_point = self.transitions[(source_chart, target_chart)](point)
        self.charts[target_chart].validate_point(target_point)
        return target_point

    def get_jacobian(self, point: Point4D, target_chart: str, eps: float = 1e-6) -> List[List[float]]:
        """Returns the 4x4 Jacobian matrix d(phi_j^mu) / d(phi_i^nu) at point."""
        source_chart = point.chart_id
        if source_chart == target_chart:
            # Identity Jacobian
            return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]

        if (source_chart, target_chart) in self.transition_jacobians:
            return self.transition_jacobians[(source_chart, target_chart)](point)

        # Fallback to numerical finite differences
        map_fn = self.transitions[(source_chart, target_chart)]
        base_target = map_fn(point)
        jac: List[List[float]] = [[0.0] * 4 for _ in range(4)]

        coords = list(point.coords)
        for nu in range(4):
            coords_plus = list(coords)
            coords_plus[nu] += eps
            p_plus = Point4D.from_tuple(tuple(coords_plus), chart_id=source_chart)
            target_plus = map_fn(p_plus)
            for mu in range(4):
                jac[mu][nu] = (target_plus[mu] - base_target[mu]) / eps

        return jac
