"""Corpus schema for the failure prediction benchmark.

Each CorpusCase records all metadata required for reproducibility,
leakage auditing, and stratum-separated analysis.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


# ── Terminal Disposition Labels ─────────────────────────────────────────────
PASS = "PASS"
QUARANTINE = "QUARANTINE"
BLOCK = "BLOCK"

SAFE_LABELS = {PASS}
FAILURE_LABELS = {QUARANTINE, BLOCK}

# ── Stratum Labels ───────────────────────────────────────────────────────────
NATIVE_GOVERNANCE = "NATIVE_GOVERNANCE"
SYNTHETIC_MECHANISTIC = "SYNTHETIC_MECHANISTIC"

# ── Failure Family Tags (Synthetic) ─────────────────────────────────────────
FAMILY_BENIGN = "BENIGN"
FAMILY_CONTAINMENT = "CONTAINMENT_ADVERSARIAL"
FAMILY_CONTRADICTION = "SEMANTIC_CONTRADICTION"
FAMILY_NEAR_BOUNDARY = "NEAR_BOUNDARY"
FAMILY_PROGRESSIVE_DEGRADATION = "PROGRESSIVE_DEGRADATION"
FAMILY_RANK_LOSS = "RANK_DIMENSION_LOSS"
FAMILY_TRAJECTORY_ANOMALY = "TRAJECTORY_ANOMALY"
FAMILY_NUMERICAL_EXTREME = "NUMERICAL_EXTREME"

SYNTHETIC_FAMILIES = [
    FAMILY_BENIGN,
    FAMILY_CONTAINMENT,
    FAMILY_CONTRADICTION,
    FAMILY_NEAR_BOUNDARY,
    FAMILY_PROGRESSIVE_DEGRADATION,
    FAMILY_RANK_LOSS,
    FAMILY_TRAJECTORY_ANOMALY,
    FAMILY_NUMERICAL_EXTREME,
]

# ── Native Governance Families (derived from actual DAXDA behavior) ──────────
NATIVE_FAMILY_CLEAN = "NATIVE_CLEAN"
NATIVE_FAMILY_CONTAINMENT = "NATIVE_CONTAINMENT"
NATIVE_FAMILY_CONTRADICTION = "NATIVE_CONTRADICTION"
NATIVE_FAMILY_NEAR_BOUNDARY = "NATIVE_NEAR_BOUNDARY"
NATIVE_FAMILY_BLINDED_SEMANTIC = "NATIVE_BLINDED_SEMANTIC"
NATIVE_FAMILY_BENCHMARK = "NATIVE_BENCHMARK"

# Minimum N for a family to qualify for OOD generalization evaluation.
# Families below this threshold are reported as INSUFFICIENT_N.
OOD_MIN_FAMILY_N = 30
OOD_PREFERRED_FAMILY_N = 50


@dataclass
class CorpusCase:
    """Single benchmark case. All fields are immutable after construction."""

    # Identity
    case_id: str
    stratum: str                          # NATIVE_GOVERNANCE or SYNTHETIC_MECHANISTIC

    # Classification
    failure_family: str                   # e.g. RANK_DIMENSION_LOSS or NATIVE_NEAR_BOUNDARY
    ground_truth_terminal_disposition: str  # PASS / QUARANTINE / BLOCK

    # Binary label derived from ground_truth (SAFE=0, FAILURE=1)
    binary_label: int

    # Provenance
    source_type: str                      # e.g. NATIVE_DAXDA_PIPELINE or SYNTHETIC_CORPUS_GENERATOR
    synthetic_or_native: str              # "synthetic" or "native"
    seed: Optional[int]                   # RNG seed for synthetic; None for native
    expected_behavior: str                # Human-readable causal description

    # Input state (4D coordinates used as M^4 entry point)
    input_x1: float
    input_x2: float
    input_x3: float
    input_x4: float
    input_hash: str                       # SHA-256 of input coordinates

    # Split assignment (set during corpus finalization)
    split: str = "UNASSIGNED"            # "train" / "val" / "test"

    # Feature vectors (populated by feature_extractor; each entry = one layer)
    baseline_features: List[Dict[str, Any]] = field(default_factory=list)
    geometric_features: List[Dict[str, Any]] = field(default_factory=list)

    # Terminal outcome (populated after running through ManifoldPipelineAdapter)
    observed_terminal_disposition: Optional[str] = None
    trajectory_recorded: bool = False

    @classmethod
    def make_input_hash(cls, x1: float, x2: float, x3: float, x4: float) -> str:
        payload = f"{x1:.15f}|{x2:.15f}|{x3:.15f}|{x4:.15f}"
        return hashlib.sha256(payload.encode()).hexdigest()

    @property
    def is_failure(self) -> bool:
        return self.ground_truth_terminal_disposition in FAILURE_LABELS

    @property
    def is_native(self) -> bool:
        return self.stratum == NATIVE_GOVERNANCE

    @property
    def is_synthetic(self) -> bool:
        return self.stratum == SYNTHETIC_MECHANISTIC

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Omit feature vectors from metadata dict (stored separately)
        d.pop("baseline_features", None)
        d.pop("geometric_features", None)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
