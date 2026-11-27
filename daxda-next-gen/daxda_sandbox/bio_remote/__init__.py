"""
DAXDA BIO-REMOTE Simulation & Operational Mapping Package
=========================================================
Solicitation: DoD SBIR DPA27BZ02-DV003 — Human Universal Remote (Amended)

Provides biophysical forearm modeling (16-ch dry sEMG + 32-element 7.5 MHz PMUT),
Clifford Geometric Algebra Cl(8,2) invariant phase-orbit decoding, AOG_1 fail-closed
biomechanical safety firewalling, and 100,000+ trial Monte Carlo operational mapping.
"""

from .forearm_physics import (
    ActionClass,
    ACTION_NAMES,
    SYSTEM_ROUTING_MAP,
    ForearmSimulationConfig,
    generate_forearm_batch,
)
from .clifford_cl8_2 import (
    Cl82InvariantFeatures,
    extract_cl82_invariants,
)
from .aog1_firewall import (
    AOG1SafetyThresholds,
    BioRemoteSystemModel,
    FirewallEvaluationResult,
)

__all__ = [
    "ActionClass",
    "ACTION_NAMES",
    "SYSTEM_ROUTING_MAP",
    "ForearmSimulationConfig",
    "generate_forearm_batch",
    "Cl82InvariantFeatures",
    "extract_cl82_invariants",
    "AOG1SafetyThresholds",
    "BioRemoteSystemModel",
    "FirewallEvaluationResult",
]
