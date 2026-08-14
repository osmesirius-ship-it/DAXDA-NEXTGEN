"""DAXDA Next-Gen Python Package Initialization.

Exposes core Clifford geometric algebra components, cognitive loop solvers,
linguistic blade transfer engines, and governed authority gates.
"""

from cl_n import CliffordAlgebra, Multivector
from universal_encoder import UniversalEncoder
from adaptive_transport import AdaptiveRotorTransport
from cognitive_loop import CognitiveLoop
from linguistic_transfer import LinguisticBladeTransfer
from governed_authority_gate import GovernedAuthorityGate
from formal_scalar_baseline import FormalScalarBaseline
from daxda_engine_nextgen import DAXDAEngineNextGen

__version__ = "12.0.1-GOVERNED"

__all__ = [
    "CliffordAlgebra",
    "Multivector",
    "UniversalEncoder",
    "AdaptiveRotorTransport",
    "CognitiveLoop",
    "LinguisticBladeTransfer",
    "GovernedAuthorityGate",
    "FormalScalarBaseline",
    "DAXDAEngineNextGen",
    "__version__"
]
