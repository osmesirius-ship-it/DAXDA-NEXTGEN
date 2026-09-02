"""Parallel Transport, Geodesic Integration, and Holonomy on 4D Manifold."""

from __future__ import annotations
import math
from typing import List, Tuple, Callable, Dict, Any, Optional
try:
    from .chart import Point4D
    from .tangent_space import TangentVector4D
    from .metric import MetricTensor4D
except (ImportError, ValueError):
    from chart import Point4D
    from tangent_space import TangentVector4D
    from metric import MetricTensor4D


class ParallelTransport4D:
    """Implements Levi-Civita parallel transport along parameterized curves on M^4."""

    def __init__(self, metric: MetricTensor4D):
        self.metric = metric

    def step(
        self,
        v: TangentVector4D,
        dx: Tuple[float, float, float, float],
        next_point: Point4D,
        eps: float = 1e-6
    ) -> TangentVector4D:
        """Transports vector v by coordinate displacement dx to next_point:
        
        v^lambda(t + dt) = v^lambda(t) - Gamma^lambda_mu_nu(p) * v^mu(t) * dx^nu
        """
        p = v.point
        gamma = self.metric.christoffel_symbols_at(p, eps=eps)

        v_new = [0.0, 0.0, 0.0, 0.0]
        for lam in range(4):
            correction = 0.0
            for mu in range(4):
                for nu in range(4):
                    correction += gamma[lam][mu][nu] * v[mu] * dx[nu]
            v_new[lam] = v[lam] - correction

        return TangentVector4D(next_point, (v_new[0], v_new[1], v_new[2], v_new[3]))

    def transport_along_curve(
        self,
        v0: TangentVector4D,
        curve_points: List[Point4D],
        eps: float = 1e-6
    ) -> List[TangentVector4D]:
        """Transports initial vector v0 along a discretized path of points."""
        if not curve_points:
            return [v0]
        if curve_points[0] != v0.point:
            raise ValueError(f"Curve starting point {curve_points[0]} does not match initial vector base {v0.point}")

        trajectory = [v0]
        current_v = v0

        for i in range(len(curve_points) - 1):
            p_curr = curve_points[i]
            p_next = curve_points[i + 1]
            dx = tuple(p_next[k] - p_curr[k] for k in range(4))
            current_v = self.step(current_v, dx, p_next, eps=eps)
            trajectory.append(current_v)

        return trajectory

    def compute_closed_loop_holonomy(
        self,
        v0: TangentVector4D,
        closed_curve: List[Point4D],
        eps: float = 1e-6
    ) -> Dict[str, Any]:
        """Computes parallel transport around a closed loop and measures holonomy error:
        
        epsilon_holonomy = ||v_final - v0||_g
        """
        if not closed_curve or closed_curve[0] != closed_curve[-1]:
            raise ValueError("Loop must begin and end at the same base point.")

        trace = self.transport_along_curve(v0, closed_curve, eps=eps)
        v_final = trace[-1]

        # Invert or re-evaluate at base point
        diff = TangentVector4D(
            v0.point,
            (v_final.v1 - v0.v1, v_final.v2 - v0.v2, v_final.v3 - v0.v3, v_final.v4 - v0.v4)
        )
        norm_error = self.metric.norm(diff)

        # Angle between v0 and v_final
        norm_v0 = self.metric.norm(v0)
        norm_vf = self.metric.norm(v_final)
        if norm_v0 > 1e-12 and norm_vf > 1e-12:
            cos_angle = self.metric.inner_product(v0, v_final) / (norm_v0 * norm_vf)
            cos_angle = max(-1.0, min(1.0, cos_angle))
            holonomy_angle_rad = math.acos(cos_angle)
        else:
            holonomy_angle_rad = 0.0

        return {
            "v0": v0.to_dict(),
            "v_final": v_final.to_dict(),
            "transport_residual": norm_error,
            "holonomy_angle_rad": holonomy_angle_rad,
            "holonomy_angle_deg": math.degrees(holonomy_angle_rad)
        }


class GeodesicStepper4D:
    """Integrates the 4D geodesic equation: d^2 x^lambda / dt^2 + Gamma^lambda_mu_nu dx^mu/dt dx^nu/dt = 0."""

    def __init__(self, metric: MetricTensor4D):
        self.metric = metric

    def step_rk4(
        self,
        p: Point4D,
        v: Tuple[float, float, float, float],
        dt: float,
        eps: float = 1e-6
    ) -> Tuple[Point4D, Tuple[float, float, float, float]]:
        """Performs a 4th-order Runge-Kutta integration step for geodesic trajectory."""
        def accel(pos: Point4D, vel: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
            gamma = self.metric.christoffel_symbols_at(pos, eps=eps)
            a = [0.0, 0.0, 0.0, 0.0]
            for lam in range(4):
                val = 0.0
                for mu in range(4):
                    for nu in range(4):
                        val -= gamma[lam][mu][nu] * vel[mu] * vel[nu]
                a[lam] = val
            return (a[0], a[1], a[2], a[3])

        # k1
        k1_x = v
        k1_v = accel(p, v)

        # k2
        p2_coords = tuple(p[i] + 0.5 * dt * k1_x[i] for i in range(4))
        p2 = Point4D.from_tuple(p2_coords, chart_id=p.chart_id)
        v2 = tuple(v[i] + 0.5 * dt * k1_v[i] for i in range(4))
        k2_x = v2
        k2_v = accel(p2, v2)

        # k3
        p3_coords = tuple(p[i] + 0.5 * dt * k2_x[i] for i in range(4))
        p3 = Point4D.from_tuple(p3_coords, chart_id=p.chart_id)
        v3 = tuple(v[i] + 0.5 * dt * k2_v[i] for i in range(4))
        k3_x = v3
        k3_v = accel(p3, v3)

        # k4
        p4_coords = tuple(p[i] + dt * k3_x[i] for i in range(4))
        p4 = Point4D.from_tuple(p4_coords, chart_id=p.chart_id)
        v4 = tuple(v[i] + dt * k3_v[i] for i in range(4))
        k4_x = v4
        k4_v = accel(p4, v4)

        # Update
        new_coords = tuple(
            p[i] + (dt / 6.0) * (k1_x[i] + 2.0 * k2_x[i] + 2.0 * k3_x[i] + k4_x[i])
            for i in range(4)
        )
        new_v = tuple(
            v[i] + (dt / 6.0) * (k1_v[i] + 2.0 * k2_v[i] + 2.0 * k3_v[i] + k4_v[i])
            for i in range(4)
        )

        return Point4D.from_tuple(new_coords, chart_id=p.chart_id), new_v

    def compute_geodesic(
        self,
        p0: Point4D,
        v0: Tuple[float, float, float, float],
        steps: int = 100,
        dt: float = 0.01,
        eps: float = 1e-6
    ) -> Tuple[List[Point4D], float]:
        """Integrates geodesic for n steps and computes total Riemannian path length."""
        points = [p0]
        curr_p = p0
        curr_v = v0
        total_length = 0.0

        for _ in range(steps):
            next_p, next_v = self.step_rk4(curr_p, curr_v, dt, eps=eps)
            # Compute arc-length element dl = sqrt(g_mu_nu v^mu v^nu) * dt
            tv = TangentVector4D(curr_p, curr_v)
            dl = self.metric.norm(tv) * dt
            total_length += dl

            points.append(next_p)
            curr_p = next_p
            curr_v = next_v

        return points, total_length
