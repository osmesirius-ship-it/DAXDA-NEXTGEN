"""4D Manifold Research Layer for DAXDA.

A mathematically explicit, differentiable 4-manifold M^4 layer operating beneath
and alongside DAXDA's Cl(7,0) Clifford representation.
"""

from .chart import Point4D, Chart4D, CoordinatePatch4D
from .tangent_space import TangentVector4D, TangentSpace
from .metric import MetricTensor4D
from .curvature import CurvatureTensor4D, UndefinedCurvatureError
from .transport import ParallelTransport4D, GeodesicStepper4D
from .embedding import CliffordEmbedding4D
from .manifold import Manifold4D
from .invariants import InvariantClassification, InvariantRecord, InvariantAnalyzer4D
from .manifold_adapter import ManifoldPipelineAdapter, Trajectory4D, TrajectoryState4D

__version__ = "0.1.0-exp-4d"

__all__ = [
    "Point4D",
    "Chart4D",
    "CoordinatePatch4D",
    "TangentVector4D",
    "TangentSpace",
    "MetricTensor4D",
    "CurvatureTensor4D",
    "UndefinedCurvatureError",
    "ParallelTransport4D",
    "GeodesicStepper4D",
    "CliffordEmbedding4D",
    "Manifold4D",
    "InvariantClassification",
    "InvariantRecord",
    "InvariantAnalyzer4D",
    "ManifoldPipelineAdapter",
    "Trajectory4D",
    "TrajectoryState4D",
]
