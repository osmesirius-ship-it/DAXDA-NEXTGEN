"""Tangent Space, Tangent Vectors, and Differential Pushforward on 4D Manifold M^4."""

from __future__ import annotations
import math
from typing import Tuple, List, Callable, Optional, Dict, Any
try:
    from .chart import Point4D
except (ImportError, ValueError):
    from chart import Point4D


def matrix_4x4_det(mat: List[List[float]]) -> float:
    """Computes exact determinant of a 4x4 matrix via Laplace expansion."""
    m = mat
    def det2(a: float, b: float, c: float, d: float) -> float:
        return a * d - b * c

    def det3(a1: float, a2: float, a3: float,
             b1: float, b2: float, b3: float,
             c1: float, c2: float, c3: float) -> float:
        return (
            a1 * det2(b2, b3, c2, c3)
            - a2 * det2(b1, b3, c1, c3)
            + a3 * det2(b1, b2, c1, c2)
        )

    return (
        m[0][0] * det3(m[1][1], m[1][2], m[1][3], m[2][1], m[2][2], m[2][3], m[3][1], m[3][2], m[3][3])
        - m[0][1] * det3(m[1][0], m[1][2], m[1][3], m[2][0], m[2][2], m[2][3], m[3][0], m[3][2], m[3][3])
        + m[0][2] * det3(m[1][0], m[1][1], m[1][3], m[2][0], m[2][1], m[2][3], m[3][0], m[3][1], m[3][3])
        - m[0][3] * det3(m[1][0], m[1][1], m[1][2], m[2][0], m[2][1], m[2][2], m[3][0], m[3][1], m[3][2])
    )


def matrix_4x4_inv(mat: List[List[float]]) -> List[List[float]]:
    """Computes inverse of a 4x4 matrix via adjugate matrix and determinant."""
    det = matrix_4x4_det(mat)
    if abs(det) < 1e-15:
        raise ValueError(f"Matrix is singular (det={det:.2e}), cannot compute inverse.")

    inv_det = 1.0 / det
    m = mat

    def minor3(r: int, c: int) -> float:
        rows = [i for i in range(4) if i != r]
        cols = [j for j in range(4) if j != c]
        sub = [[m[i][j] for j in cols] for i in rows]
        return (
            sub[0][0] * (sub[1][1] * sub[2][2] - sub[1][2] * sub[2][1])
            - sub[0][1] * (sub[1][0] * sub[2][2] - sub[1][2] * sub[2][0])
            + sub[0][2] * (sub[1][0] * sub[2][1] - sub[1][1] * sub[2][0])
        )

    inv = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            sign = 1.0 if (i + j) % 2 == 0 else -1.0
            # Adjugate is transpose of cofactor matrix
            inv[j][i] = sign * minor3(i, j) * inv_det

    return inv


def matrix_4x4_rank(mat: List[List[float]], tol: float = 1e-9) -> int:
    """Computes numerical rank of a 4x4 matrix via Gaussian elimination with partial pivoting."""
    a = [[float(val) for val in row] for row in mat]
    rank = 0
    num_rows, num_cols = 4, 4

    for col in range(num_cols):
        # Find pivot
        pivot_row = -1
        max_val = tol
        for r in range(rank, num_rows):
            if abs(a[r][col]) > max_val:
                max_val = abs(a[r][col])
                pivot_row = r

        if pivot_row == -1:
            continue

        # Swap rows
        a[rank], a[pivot_row] = a[pivot_row], a[rank]

        # Eliminate below
        pivot = a[rank][col]
        for r in range(rank + 1, num_rows):
            factor = a[r][col] / pivot
            for c in range(col, num_cols):
                a[r][c] -= factor * a[rank][c]

        rank += 1
        if rank == num_rows:
            break

    return rank


class TangentVector4D:
    """Represents a tangent vector v = v^mu d/dx^mu in T_p M."""

    __slots__ = ("_point", "_components")

    def __init__(self, point: Point4D, components: Tuple[float, float, float, float]):
        if len(components) != 4:
            raise ValueError(f"TangentVector4D requires 4 components, got {len(components)}")
        self._point = point
        self._components = (
            float(components[0]), float(components[1]), float(components[2]), float(components[3])
        )

    @classmethod
    def zero_at(cls, point: Point4D) -> TangentVector4D:
        return cls(point, (0.0, 0.0, 0.0, 0.0))

    @property
    def point(self) -> Point4D:
        return self._point

    @property
    def components(self) -> Tuple[float, float, float, float]:
        return self._components

    @property
    def v1(self) -> float:
        return self._components[0]

    @property
    def v2(self) -> float:
        return self._components[1]

    @property
    def v3(self) -> float:
        return self._components[2]

    @property
    def v4(self) -> float:
        return self._components[3]

    def __getitem__(self, index: int) -> float:
        return self._components[index]

    def __len__(self) -> int:
        return 4

    def __repr__(self) -> str:
        return f"TangentVector4D({self.v1:.6f}, {self.v2:.6f}, {self.v3:.6f}, {self.v4:.6f} @ {self._point})"

    def __add__(self, other: TangentVector4D) -> TangentVector4D:
        if self._point != other._point:
            raise ValueError("Cannot add tangent vectors at distinct base points.")
        return TangentVector4D(
            self._point,
            (self.v1 + other.v1, self.v2 + other.v2, self.v3 + other.v3, self.v4 + other.v4)
        )

    def __sub__(self, other: TangentVector4D) -> TangentVector4D:
        if self._point != other._point:
            raise ValueError("Cannot subtract tangent vectors at distinct base points.")
        return TangentVector4D(
            self._point,
            (self.v1 - other.v1, self.v2 - other.v2, self.v3 - other.v3, self.v4 - other.v4)
        )

    def __mul__(self, scalar: float) -> TangentVector4D:
        s = float(scalar)
        return TangentVector4D(
            self._point,
            (self.v1 * s, self.v2 * s, self.v3 * s, self.v4 * s)
        )

    __rmul__ = __mul__

    def directional_derivative(self, scalar_field: Callable[[Point4D], float], eps: float = 1e-6) -> float:
        """Evaluates v(f) = v^mu d_mu f via finite difference directional derivative."""
        base_val = scalar_field(self._point)
        coords = list(self._point.coords)
        deriv = 0.0
        for mu in range(4):
            if abs(self._components[mu]) > 1e-15:
                step_coords = list(coords)
                step_coords[mu] += eps
                step_p = Point4D.from_tuple(tuple(step_coords), chart_id=self._point.chart_id)
                df_dmu = (scalar_field(step_p) - base_val) / eps
                deriv += self._components[mu] * df_dmu
        return deriv

    def to_dict(self) -> Dict[str, Any]:
        return {
            "point": self._point.to_dict(),
            "components": [self.v1, self.v2, self.v3, self.v4]
        }


class TangentSpace:
    """Represents the tangent space T_p M at a given base point p."""

    def __init__(self, base_point: Point4D):
        self.base_point = base_point
        self.dim = 4

    def basis(self) -> List[TangentVector4D]:
        """Returns standard coordinate basis {d/dx1, d/dx2, d/dx3, d/dx4}."""
        basis_vectors = []
        for i in range(4):
            comp = [0.0, 0.0, 0.0, 0.0]
            comp[i] = 1.0
            basis_vectors.append(TangentVector4D(self.base_point, tuple(comp)))
        return basis_vectors

    def pushforward(
        self,
        v: TangentVector4D,
        jacobian_matrix: List[List[float]],
        target_point: Point4D
    ) -> TangentVector4D:
        """Applies pushforward d(phi)_p(v) = J^mu_nu v^nu to map tangent vector to target chart."""
        if v.point != self.base_point:
            raise ValueError(f"Vector base point {v.point} does not match tangent space base {self.base_point}")
        
        target_comp: List[float] = [0.0, 0.0, 0.0, 0.0]
        for mu in range(4):
            for nu in range(4):
                target_comp[mu] += jacobian_matrix[mu][nu] * v[nu]

        return TangentVector4D(target_point, tuple(target_comp))
