"""
DAXDA Guard: Air-Gapped Synchronous AI Security & Autonomous Fail-Closed Interceptor.
"""

from .core import DAXDAGuardCore, Multivector, GovernanceReceipt
from .decorator import enforce_governance
from .actuator_boundary import (
    AuthoritativePolicyEngine,
    ActuatorBoundary,
    ActuatorAuthorizationReceipt,
    AdapterExecutionMode,
    GovernedPropulsionActuator,
    GovernanceDisposition,
    FailClosedReason,
)
from .nasa_analog_client import (
    NASAAnalogClientSession,
    AnalogMissionType,
    CrewStationRole,
    DataSensitivity,
    ClinicalMedicalFirewall,
    DeepSpaceCommsBuffer,
    AnalogPEPActionGate,
    GateDisposition,
)

__version__ = "1.0.0"
__all__ = [
    "DAXDAGuardCore",
    "Multivector",
    "GovernanceReceipt",
    "enforce_governance",
    "AuthoritativePolicyEngine",
    "ActuatorBoundary",
    "ActuatorAuthorizationReceipt",
    "AdapterExecutionMode",
    "GovernedPropulsionActuator",
    "GovernanceDisposition",
    "FailClosedReason",
    "NASAAnalogClientSession",
    "AnalogMissionType",
    "CrewStationRole",
    "DataSensitivity",
    "ClinicalMedicalFirewall",
    "DeepSpaceCommsBuffer",
    "AnalogPEPActionGate",
    "GateDisposition",
]
