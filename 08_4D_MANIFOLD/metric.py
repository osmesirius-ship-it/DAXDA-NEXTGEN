"""Metric Tensor, Connection Coefficients (Christoffel Symbols), and Index Operations on 4D Manifold."""

from __future__ import annotations
import math
from typing import List, Callable, Optional, Dict, Any, Tuple
try:
    from .chart import Point4D
    from .tangent_space import TangentVector4D, matrix_4x4_det, matrix_4x4_inv
except (ImportError, ValueError):
    from chart import Point4D
    from tangent_space import TangentVector4D, matrix_4x4_det, matrix_4x4_inv


class MetricTensor4D:
    """Represents a smooth symmetric (0,2) metric tensor field g_mu_nu(x) on 4D Manifold M^4."""

    def __init__(
        self,
        metric_fn: Optional[Callable[[Point4D], List[List[float]]]] = None,
        name: str = "Flat Euclidean Metric g=diag(1,1,1,1)",
        is_riemannian: bool = True
    ):
        self.name = name
        self.is_riemannian = is_riemannian
        self.dim = 4
        # Default metric: Flat Euclidean diag(1, 1, 1, 1)
        self._metric_fn = metric_fn or self._default_flat_metric

    @staticmethod
    def _default_flat_metric(p: Point4D) -> List[List[float]]:
        return [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]

    @classmethod
    def flat_euclidean(cls) -> MetricTensor4D:
        """Returns flat Riemannian Euclidean metric g = diag(1, 1, 1, 1)."""
        return cls(name="Flat Euclidean Metric g=diag(1,1,1,1)", is_riemannian=True)

    @classmethod
    def minkowski_fixture(cls) -> MetricTensor4D:
        """Returns mathematical pseudo-Riemannian fixture eta = diag(-1, 1, 1, 1).
        
        NOTE: This is provided strictly as a mathematical comparison test fixture.
        It does NOT imply or model physical spacetime in DAXDA's state manifold.
        """
        def minkowski_fn(p: Point4D) -> List[List[float]]:
            return [
                [-1.0, 0.0, 0.0, 0.0],
                [0.0,  1.0, 0.0, 0.0],
                [0.0,  0.0, 1.0, 0.0],
                [0.0,  0.0, 0.0, 1.0],
            ]
        return cls(metric_fn=minkowski_fn, name="Minkowski Fixture eta=diag(-1,1,1,1)", is_riemannian=False)

    @classmethod
    def conformally_flat(cls, conformal_factor_fn: Callable[[Point4D], float]) -> MetricTensor4D:
        """Returns conformally flat curved metric g_mu_nu(x) = Omega(x)^2 * delta_mu_nu."""
        def metric_fn(p: Point4D) -> List[List[float]]:
            omega = conformal_factor_fn(p)
            omega2 = omega * omega
            return [
                [omega2, 0.0, 0.0, 0.0],
                [0.0, omega2, 0.0, 0.0],
                [0.0, 0.0, omega2, 0.0],
                [0.0, 0.0, 0.0, omega2],
            ]
        return cls(metric_fn=metric_fn, name="Conformally Flat Curved Metric", is_riemannian=True)

    def evaluate_at(self, p: Point4D) -> List[List[float]]:
        """Evaluates g_mu_nu at point p."""
        g = self._metric_fn(p)
        # Validate 4x4 symmetric matrix
        if len(g) != 4 or any(len(row) != 4 for row in g):
            raise ValueError(f"Metric at {p} must be a 4x4 matrix, got {len(g)}x{len(g[0]) if g else 0}")
        # Check symmetry
        for i in range(4):
            for j in range(i + 1, 4):
                if not math.isclose(g[i][j], g[j][i], abs_tol=1e-9):
                    raise ValueError(f"Metric at {p} is non-symmetric: g[{i}][{j}]={g[i][j]} != g[{j}][{i}]={g[j][i]}")
        return g

    def inverse_at(self, p: Point4D) -> List[List[float]]:
        """Evaluates inverse metric g^mu_nu at point p."""
        g = self.evaluate_at(p)
        return matrix_4x4_inv(g)

    def determinant_at(self, p: Point4D) -> float:
        """Evaluates metric determinant det(g) at point p."""
        g = self.evaluate_at(p)
        return matrix_4x4_det(g)

    def inner_product(self, u: TangentVector4D, v: TangentVector4D) -> float:
        """Computes metric inner product <u, v>_g = g_mu_nu u^mu v^nu at shared base point."""
        if u.point != v.point:
            raise ValueError(f"Vectors u (at {u.point}) and v (at {v.point}) have different base points.")
        g = self.evaluate_at(u.point)
        prod = 0.0
        for mu in range(4):
            for nu in range(4):
                prod += g[mu][nu] * u[mu] * v[nu]
        return prod

    def norm(self, v: TangentVector4D) -> float:
        """Computes metric norm ||v||_g = sqrt(|<v, v>_g|)."""
        val = self.inner_product(v, v)
        return math.sqrt(abs(val))

    def lower_index(self, v: TangentVector4D) -> Tuple[float, float, float, float]:
        """Lowers vector index: v_mu = g_mu_nu v^nu."""
        g = self.evaluate_at(v.point)
        co_comp = [0.0, 0.0, 0.0, 0.0]
        for mu in range(4):
            for nu in range(4):
                co_comp[mu] += g[mu][nu] * v[nu]
        return (co_comp[0], co_comp[1], co_comp[2], co_comp[3])

    def raise_index(self, point: Point4D, covector: Tuple[float, float, float, float]) -> TangentVector4D:
        """Raises covector index: v^mu = g^mu_nu v_nu."""
        g_inv = self.inverse_at(point)
        vec_comp = [0.0, 0.0, 0.0, 0.0]
        for mu in range(4):
            for nu in range(4):
                vec_comp[mu] += g_inv[mu][nu] * covector[nu]
        return TangentVector4D(point, (vec_comp[0], vec_comp[1], vec_comp[2], vec_comp[3]))

    def metric_derivatives_at(self, p: Point4D, eps: float = 1e-6) -> List[List[List[float]]]:
        """Computes partial derivatives d_sigma g_mu_nu at point p.
        
        Returns:
            3D tensor dg[sigma][mu][nu] = d(g_mu_nu)/dx^sigma
        """
        dg = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
        coords = list(p.coords)

        for sigma in range(4):
            coords_plus = list(coords)
            coords_plus[sigma] += eps
            p_plus = Point4D.from_tuple(tuple(coords_plus), chart_id=p.chart_id)

            coords_minus = list(coords)
            coords_minus[sigma] -= eps
            p_minus = Point4D.from_tuple(tuple(coords_minus), chart_id=p.chart_id)

            g_plus = self.evaluate_at(p_plus)
            g_minus = self.evaluate_at(p_minus)

            for mu in range(4):
                for nu in range(4):
                    dg[sigma][mu][nu] = (g_plus[mu][nu] - g_minus[mu][nu]) / (2.0 * eps)

        return dg

    def christoffel_symbols_at(self, p: Point4D, eps: float = 1e-6) -> List[List[List[float]]]:
        """Computes Christoffel symbols of the second kind:
        
        Gamma^lambda_mu_nu = 1/2 * g^lambda_sigma * (d_mu g_nu_sigma + d_nu g_mu_sigma - d_sigma g_mu_nu)
        
        Returns:
            3D tensor gamma[lambda_idx][mu][nu]
        """
        g_inv = self.inverse_at(p)
        dg = self.metric_derivatives_at(p, eps=eps)

        gamma = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]

        for lam in range(4):
            for mu in range(4):
                for nu in range(4):
                    sum_sigma = 0.0
                    for sigma in range(4):
                        # d_mu g_nu_sigma + d_nu g_mu_sigma - d_sigma g_mu_nu
                        term = (
                            dg[mu][nu][sigma]
                            + dg[nu][mu][sigma]
                            - dg[sigma][mu][nu]
                        )
                        sum_sigma += g_inv[lam][sigma] * term
                    gamma[lam][mu][nu] = 0.5 * sum_sigma

        return gamma
