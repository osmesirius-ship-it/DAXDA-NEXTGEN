"""Unified 4D Differentiable Manifold Object Manifold4D."""

from __future__ import annotations
import math
from typing import List, Tuple, Dict, Any, Optional, Callable
try:
    from .chart import Point4D, Chart4D, CoordinatePatch4D
    from .tangent_space import TangentVector4D, TangentSpace
    from .metric import MetricTensor4D
    from .curvature import CurvatureTensor4D
    from .transport import ParallelTransport4D, GeodesicStepper4D
    from .embedding import CliffordEmbedding4D
except (ImportError, ValueError):
    from chart import Point4D, Chart4D, CoordinatePatch4D
    from tangent_space import TangentVector4D, TangentSpace
    from metric import MetricTensor4D
    from curvature import CurvatureTensor4D
    from transport import ParallelTransport4D, GeodesicStepper4D
    from embedding import CliffordEmbedding4D


class Manifold4D:
    """Represents a smooth 4-dimensional Riemannian / pseudo-Riemannian manifold M^4."""

    def __init__(
        self,
        name: str = "M4_Euclidean",
        metric: Optional[MetricTensor4D] = None,
        default_chart_id: str = "U0"
    ):
        self.name = name
        self.default_chart_id = default_chart_id
        self.atlas = CoordinatePatch4D()
        
        # Add primary chart
        self.atlas.add_chart(Chart4D(chart_id=default_chart_id, description=f"Primary chart for {name}"))
        
        self.metric = metric or MetricTensor4D.flat_euclidean()
        self.curvature = CurvatureTensor4D(self.metric)
        self.transport = ParallelTransport4D(self.metric)
        self.geodesic = GeodesicStepper4D(self.metric)
        self.embedding = CliffordEmbedding4D()

    def point(self, x1: float, x2: float, x3: float, x4: float, chart_id: Optional[str] = None) -> Point4D:
        cid = chart_id or self.default_chart_id
        p = Point4D(x1, x2, x3, x4, chart_id=cid)
        self.atlas.charts[cid].validate_point(p)
        return p

    def tangent_space(self, point: Point4D) -> TangentSpace:
        return TangentSpace(point)

    def tangent_vector(self, point: Point4D, components: Tuple[float, float, float, float]) -> TangentVector4D:
        return TangentVector4D(point, components)

    def inner_product(self, u: TangentVector4D, v: TangentVector4D) -> float:
        return self.metric.inner_product(u, v)

    def norm(self, v: TangentVector4D) -> float:
        return self.metric.norm(v)

    def parallel_transport_step(
        self,
        v: TangentVector4D,
        dx: Tuple[float, float, float, float],
        next_point: Point4D
    ) -> TangentVector4D:
        return self.transport.step(v, dx, next_point)

    def geodesic_path(
        self,
        p0: Point4D,
        v0: Tuple[float, float, float, float],
        steps: int = 50,
        dt: float = 0.02
    ) -> Tuple[List[Point4D], float]:
        return self.geodesic.compute_geodesic(p0, v0, steps=steps, dt=dt)

    def embed_to_cl70(self, p: Point4D, aux: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        return self.embedding.embed(p, auxiliary_e567=aux)

    def project_from_cl70(self, mv, chart_id: Optional[str] = None) -> Point4D:
        cid = chart_id or self.default_chart_id
        return self.embedding.project(mv, chart_id=cid)
