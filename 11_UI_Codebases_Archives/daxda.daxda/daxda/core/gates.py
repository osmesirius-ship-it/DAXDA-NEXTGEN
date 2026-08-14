"""
DAXDA.IA — Gate State Definitions
Nicole Protocol / 886-Ops Architecture
"""
from enum import Enum


class GateState(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    CAUTION = "CAUTION"
    RECURSE = "RECURSE"
    BLOCK = "BLOCK"
    RELEASE = "RELEASE"


# Thresholds that determine gate state from a composite stability score (0.0–1.0)
GATE_THRESHOLDS = {
    GateState.PASS:    (0.80, 1.00),
    GateState.WARN:    (0.60, 0.80),
    GateState.CAUTION: (0.40, 0.60),
    GateState.RECURSE: (0.20, 0.40),
    GateState.BLOCK:   (0.00, 0.20),
}


def score_to_gate(score: float) -> GateState:
    """Map a stability score to a gate state."""
    for state, (low, high) in GATE_THRESHOLDS.items():
        if low <= score <= high:
            return state
    return GateState.BLOCK


GATE_DESCRIPTIONS = {
    GateState.PASS:    "Strong enough to proceed. Release layer output with trace.",
    GateState.WARN:    "Usable but weakened. Release with warning and uncertainty note.",
    GateState.CAUTION: "Material ambiguity or volatility. Release only with caveats.",
    GateState.RECURSE: "Current state is insufficient. Build recursion payload and re-enter.",
    GateState.BLOCK:   "Unsafe, unsupported, or invalid. Do not release final claim/action.",
    GateState.RELEASE: "Final authority gate cleared. Emit governed output and audit manifest.",
}
