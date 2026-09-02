"""Curvature Tensors on 4D Manifold: Riemann, Ricci, Ricci Scalar, and Kretschmann Invariant."""

from __future__ import annotations
import math
from typing import List, Dict, Any, Optional
try:
    from .chart import Point4D
    from .metric import MetricTensor4D
except (ImportError, ValueError):
    from chart import Point4D
    from metric import MetricTensor4D


class UndefinedCurvatureError(ArithmeticError):
    """Raised when curvature tensors cannot be mathematically evaluated."""
    pass


class CurvatureTensor4D:
    """Calculates exact curvature tensors from the metric and Levi-Civita connection on M^4."""

    def __init__(self, metric: MetricTensor4D):
        self.metric = metric

    def riemann_tensor_at(self, p: Point4D, eps: float = 1e-5) -> List[List[List[List[float]]]]:
        """Computes Riemann curvature tensor components R^rho_sigma_mu_nu at point p:
        
        R^rho_sigma_mu_nu = d_mu Gamma^rho_nu_sigma - d_nu Gamma^rho_mu_sigma
                           + Gamma^rho_mu_lambda Gamma^lambda_nu_sigma
                           - Gamma^rho_nu_lambda Gamma^lambda_mu_sigma
                           
        Returns:
            4D tensor R[rho][sigma][mu][nu]
        """
        try:
            gamma_0 = self.metric.christoffel_symbols_at(p, eps=eps)
        except Exception as e:
            raise UndefinedCurvatureError(f"Failed to evaluate Christoffel symbols at {p}: {e}")

        # Compute partial derivatives of Gamma with respect to x^mu and x^nu
        dgamma = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)] # [alpha_deriv][rho][mu][nu]
        coords = list(p.coords)

        for alpha in range(4):
            coords_plus = list(coords)
            coords_plus[alpha] += eps
            p_plus = Point4D.from_tuple(tuple(coords_plus), chart_id=p.chart_id)

            coords_minus = list(coords)
            coords_minus[alpha] -= eps
            p_minus = Point4D.from_tuple(tuple(coords_minus), chart_id=p.chart_id)

            try:
                g_p = self.metric.christoffel_symbols_at(p_plus, eps=eps)
                g_m = self.metric.christoffel_symbols_at(p_minus, eps=eps)
            except Exception as e:
                raise UndefinedCurvatureError(f"Derivative of Christoffel symbols undefined at {p}: {e}")

            for r in range(4):
                for m in range(4):
                    for n in range(4):
                        dgamma[alpha][r][m][n] = (g_p[r][m][n] - g_m[r][m][n]) / (2.0 * eps)

        riemann = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]

        for rho in range(4):
            for sigma in range(4):
                for mu in range(4):
                    for nu in range(4):
                        # Derivative terms: d_mu Gamma^rho_nu_sigma - d_nu Gamma^rho_mu_sigma
                        d_term = dgamma[mu][rho][nu][sigma] - dgamma[nu][rho][mu][sigma]

                        # Connection product terms
                        prod_term = 0.0
                        for lam in range(4):
                            prod_term += (
                                gamma_0[rho][mu][lam] * gamma_0[lam][nu][sigma]
                                - gamma_0[rho][nu][lam] * gamma_0[lam][mu][sigma]
                            )

                        val = d_term + prod_term
                        # Clean small numerical noise
                        if abs(val) < 1e-12:
                            val = 0.0
                        riemann[rho][sigma][mu][nu] = val

        return riemann

    def ricci_tensor_at(self, p: Point4D, eps: float = 1e-5) -> List[List[float]]:
        """Computes Ricci curvature tensor R_sigma_nu by contracting Riemann tensor:
        
        R_sigma_nu = R^lambda_sigma_lambda_nu
        
        Returns:
            4x4 matrix ricci[sigma][nu]
        """
        riemann = self.riemann_tensor_at(p, eps=eps)
        ricci = [[0.0] * 4 for _ in range(4)]

        for sigma in range(4):
            for nu in range(4):
                val = sum(riemann[lam][sigma][lam][nu] for lam in range(4))
                if abs(val) < 1e-12:
                    val = 0.0
                ricci[sigma][nu] = val

        return ricci

    def ricci_scalar_at(self, p: Point4D, eps: float = 1e-5) -> float:
        """Computes Ricci scalar curvature R = g^mu_nu R_mu_nu."""
        g_inv = self.metric.inverse_at(p)
        ricci = self.ricci_tensor_at(p, eps=eps)

        scalar = 0.0
        for mu in range(4):
            for nu in range(4):
                scalar += g_inv[mu][nu] * ricci[mu][nu]

        return 0.0 if abs(scalar) < 1e-12 else scalar

    def kretschmann_scalar_at(self, p: Point4D, eps: float = 1e-5) -> float:
        """Computes Kretschmann scalar invariant K = R_alpha_beta_gamma_delta R^alpha_beta_gamma_delta."""
        riemann = self.riemann_tensor_at(p, eps=eps)
        g = self.metric.evaluate_at(p)
        g_inv = self.metric.inverse_at(p)

        # Lower first index to get fully covariant Riemann R_alpha_beta_gamma_delta = g_alpha_rho R^rho_beta_gamma_delta
        r_cov = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for alpha in range(4):
            for beta in range(4):
                for gamma in range(4):
                    for delta in range(4):
                        r_cov[alpha][beta][gamma][delta] = sum(
                            g[alpha][rho] * riemann[rho][beta][gamma][delta] for rho in range(4)
                        )

        # Fully contravariant Riemann R^a_b_c_d = g^a_alpha g^b_beta g^c_gamma g^d_delta R_alpha_beta_gamma_delta
        r_contra = [[[[0.0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        val = 0.0
                        for al in range(4):
                            for be in range(4):
                                for ga in range(4):
                                    for de in range(4):
                                        val += (
                                            g_inv[a][al] * g_inv[b][be] * g_inv[c][ga] * g_inv[d][de]
                                            * r_cov[al][be][ga][de]
                                        )
                        r_contra[a][b][c][d] = val

        # Full contraction
        k_val = 0.0
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        k_val += r_cov[a][b][c][d] * r_contra[a][b][c][d]

        return 0.0 if abs(k_val) < 1e-12 else k_val
