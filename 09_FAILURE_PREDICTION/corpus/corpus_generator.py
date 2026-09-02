"""Corpus generator for the failure prediction benchmark.

Produces two strata separately:
  1. NATIVE_GOVERNANCE  — inputs run through the frozen DAXDA pipeline;
                          geometry recorded as-is, no artificial modification.
  2. SYNTHETIC_MECHANISTIC — constructed failures with known causal mechanisms.

The terminal disposition for ALL cases is determined by the frozen governance
engine. For native cases, no geometric failure mechanism is injected.
"""

from __future__ import annotations
import hashlib
import json
import math
import os
import random
import sys
import time
from typing import List, Tuple, Dict, Any

# Path setup
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_FROZEN = os.path.join(_ROOT, "03_V9_V8_Validation_Suite", "DAXDA_V9_MASTER", "daxda-v11.4-frozen")
_TOOLS = os.path.join(_ROOT, "03_REBUILD_TOOLS")
_M4 = os.path.join(_ROOT, "08_4D_MANIFOLD")

for p in [_ROOT, _FROZEN, _TOOLS, _M4]:
    if p not in sys.path:
        sys.path.insert(0, p)

from corpus_schema import (
    CorpusCase,
    PASS, QUARANTINE, BLOCK,
    NATIVE_GOVERNANCE, SYNTHETIC_MECHANISTIC,
    FAMILY_BENIGN, FAMILY_CONTAINMENT, FAMILY_CONTRADICTION,
    FAMILY_NEAR_BOUNDARY, FAMILY_PROGRESSIVE_DEGRADATION,
    FAMILY_RANK_LOSS, FAMILY_TRAJECTORY_ANOMALY, FAMILY_NUMERICAL_EXTREME,
    NATIVE_FAMILY_CLEAN, NATIVE_FAMILY_CONTAINMENT, NATIVE_FAMILY_CONTRADICTION,
    NATIVE_FAMILY_NEAR_BOUNDARY, NATIVE_FAMILY_BLINDED_SEMANTIC, NATIVE_FAMILY_BENCHMARK,
)

# Import frozen DAXDA engine for governance disposition
from adaptive_transport import AdaptiveTransport
from cl_n import CliffordAlgebra


def _make_case_id(prefix: str, idx: int, seed: int) -> str:
    raw = f"{prefix}-{idx:04d}-seed{seed}"
    return "FP-" + hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


def _run_daxda_governance(x1: float, x2: float, x3: float, x4: float,
                          algebra: CliffordAlgebra,
                          transport: AdaptiveTransport) -> Tuple[str, float]:
    """Run input through frozen DAXDA 16-layer transport; return disposition and residual.

    The governance disposition is inferred from the micro-reversibility
    residual and the multivector grade-0 energy, replicating the existing
    AdaptiveTransport authority gate logic.
    """
    # Build Clifford multivector: F(x) = x1*e1 + x2*e2 + x3*e3 + x4*e4
    mv = algebra.multivector()
    mv.coeffs[1] = x1    # e1 = index 2^0
    mv.coeffs[2] = x2    # e2 = index 2^1
    mv.coeffs[4] = x3    # e3 = index 2^2
    mv.coeffs[8] = x4    # e4 = index 2^3

    result = transport.transport(mv)
    residual = result.get("final_reconstruction_residual", 0.0)

    # Governance: use existing authority_gate thresholds
    # residual < 1e-10  -> PASS
    # 1e-10 <= residual < 1e-6 -> QUARANTINE
    # residual >= 1e-6  -> BLOCK
    if residual < 1e-10:
        disposition = PASS
    elif residual < 1e-6:
        disposition = QUARANTINE
    else:
        disposition = BLOCK

    return disposition, residual


# ── NATIVE GOVERNANCE CORPUS BUILDER ────────────────────────────────────────

def build_native_corpus(
    n_per_family: Dict[str, int],
    seed: int = 42,
    algebra: CliffordAlgebra = None,
    transport: AdaptiveTransport = None,
) -> List[CorpusCase]:
    """
    Build NATIVE_GOVERNANCE cases by running varied inputs through the
    frozen DAXDA engine and recording whatever disposition naturally emerges.

    No geometric failure mechanism is artificially injected.
    The geometry recorded in feature extraction later is purely emergent.
    """
    rng = random.Random(seed)
    algebra = algebra or CliffordAlgebra(p=7, q=0)
    transport = transport or AdaptiveTransport(algebra)

    cases: List[CorpusCase] = []
    idx = 0

    def _make(family: str, x1: float, x2: float, x3: float, x4: float, expected: str) -> CorpusCase:
        nonlocal idx
        inp_hash = CorpusCase.make_input_hash(x1, x2, x3, x4)
        disposition, _ = _run_daxda_governance(x1, x2, x3, x4, algebra, transport)
        binary = 0 if disposition == PASS else 1
        case = CorpusCase(
            case_id=_make_case_id("NAT", idx, seed),
            stratum=NATIVE_GOVERNANCE,
            failure_family=family,
            ground_truth_terminal_disposition=disposition,
            binary_label=binary,
            source_type="NATIVE_DAXDA_PIPELINE",
            synthetic_or_native="native",
            seed=None,
            expected_behavior=expected,
            input_x1=x1, input_x2=x2, input_x3=x3, input_x4=x4,
            input_hash=inp_hash,
        )
        idx += 1
        return case

    # NATIVE_FAMILY_CLEAN: well-conditioned inputs — expect mostly PASS
    n = n_per_family.get(NATIVE_FAMILY_CLEAN, 80)
    for _ in range(n):
        coords = [rng.gauss(0, 0.5) for _ in range(4)]
        cases.append(_make(NATIVE_FAMILY_CLEAN, *coords,
                           "Normal well-conditioned input; expect PASS from frozen governance"))

    # NATIVE_FAMILY_CONTAINMENT: high-magnitude adversarial-style inputs
    n = n_per_family.get(NATIVE_FAMILY_CONTAINMENT, 60)
    for _ in range(n):
        mag = rng.uniform(8.0, 15.0)
        coords = [rng.choice([-1, 1]) * mag * rng.uniform(0.8, 1.2) for _ in range(4)]
        cases.append(_make(NATIVE_FAMILY_CONTAINMENT, *coords,
                           "High-magnitude adversarial-style input; frozen engine determines disposition"))

    # NATIVE_FAMILY_CONTRADICTION: opposing sign coordinate pairs
    n = n_per_family.get(NATIVE_FAMILY_CONTRADICTION, 60)
    for _ in range(n):
        v = rng.uniform(1.5, 4.0)
        x1, x2 = v, -v
        x3, x4 = rng.gauss(0, 0.3), rng.gauss(0, 0.3)
        cases.append(_make(NATIVE_FAMILY_CONTRADICTION, x1, x2, x3, x4,
                           "Opposing coordinate pair; models potential semantic contradiction"))

    # NATIVE_FAMILY_NEAR_BOUNDARY: inputs near governance threshold
    n = n_per_family.get(NATIVE_FAMILY_NEAR_BOUNDARY, 60)
    for _ in range(n):
        # Probe around moderate magnitudes where QUARANTINE/BLOCK boundary lies
        mag = rng.uniform(3.5, 5.5)
        coords = [rng.gauss(0, mag / 3) for _ in range(4)]
        cases.append(_make(NATIVE_FAMILY_NEAR_BOUNDARY, *coords,
                           "Near-threshold input; straddling PASS/QUARANTINE boundary"))

    # NATIVE_FAMILY_BLINDED_SEMANTIC: zero-mean small perturbations
    n = n_per_family.get(NATIVE_FAMILY_BLINDED_SEMANTIC, 60)
    for _ in range(n):
        coords = [rng.gauss(0, 0.1) for _ in range(4)]
        cases.append(_make(NATIVE_FAMILY_BLINDED_SEMANTIC, *coords,
                           "Near-zero semantic state; blinded challenge baseline"))

    # NATIVE_FAMILY_BENCHMARK: drawn from benchmark distribution
    n = n_per_family.get(NATIVE_FAMILY_BENCHMARK, 80)
    for _ in range(n):
        # Simulate benchmark-style inputs with moderate spread
        coords = [rng.uniform(-2.0, 2.0) for _ in range(4)]
        cases.append(_make(NATIVE_FAMILY_BENCHMARK, *coords,
                           "Benchmark-distribution input drawn from standard evaluation range"))

    return cases


# ── SYNTHETIC MECHANISTIC CORPUS BUILDER ────────────────────────────────────

def build_synthetic_corpus(
    n_per_family: Dict[str, int],
    seed: int = 42,
    algebra: CliffordAlgebra = None,
    transport: AdaptiveTransport = None,
) -> List[CorpusCase]:
    """
    Build SYNTHETIC_MECHANISTIC cases with known causal geometric mechanisms.

    The terminal disposition is STILL determined by the frozen DAXDA engine
    after the input is constructed. Only the INPUT construction is synthetic;
    the governance outcome is not artificially forced.
    """
    rng = random.Random(seed + 10000)
    algebra = algebra or CliffordAlgebra(p=7, q=0)
    transport = transport or AdaptiveTransport(algebra)

    cases: List[CorpusCase] = []
    idx = 0

    def _make(family: str, x1: float, x2: float, x3: float, x4: float,
              expected: str, case_seed: int) -> CorpusCase:
        nonlocal idx
        inp_hash = CorpusCase.make_input_hash(x1, x2, x3, x4)
        disposition, _ = _run_daxda_governance(x1, x2, x3, x4, algebra, transport)
        binary = 0 if disposition == PASS else 1
        case = CorpusCase(
            case_id=_make_case_id("SYN", idx, case_seed),
            stratum=SYNTHETIC_MECHANISTIC,
            failure_family=family,
            ground_truth_terminal_disposition=disposition,
            binary_label=binary,
            source_type="SYNTHETIC_CORPUS_GENERATOR",
            synthetic_or_native="synthetic",
            seed=case_seed,
            expected_behavior=expected,
            input_x1=x1, input_x2=x2, input_x3=x3, input_x4=x4,
            input_hash=inp_hash,
        )
        idx += 1
        return case

    # A. BENIGN
    n = n_per_family.get(FAMILY_BENIGN, 60)
    for i in range(n):
        cs = seed + i
        rng2 = random.Random(cs)
        coords = [rng2.gauss(0, 0.3) for _ in range(4)]
        cases.append(_make(FAMILY_BENIGN, *coords,
                           "Stable low-magnitude synthetic input; expected PASS", cs))

    # B. CONTAINMENT / ADVERSARIAL
    n = n_per_family.get(FAMILY_CONTAINMENT, 60)
    for i in range(n):
        cs = seed + 1000 + i
        rng2 = random.Random(cs)
        # Large magnitude inputs that stress the containment engine
        mag = rng2.uniform(10.0, 20.0)
        coords = [rng2.uniform(-mag, mag) for _ in range(4)]
        cases.append(_make(FAMILY_CONTAINMENT, *coords,
                           "High-magnitude adversarial synthetic input; stresses containment", cs))

    # C. SEMANTIC CONTRADICTION
    n = n_per_family.get(FAMILY_CONTRADICTION, 50)
    for i in range(n):
        cs = seed + 2000 + i
        rng2 = random.Random(cs)
        v = rng2.uniform(2.0, 6.0)
        # Strongly opposing components — potential semantic contradiction
        x1, x2 = v, -v
        x3 = rng2.uniform(-v / 2, v / 2)
        x4 = -x3
        cases.append(_make(FAMILY_CONTRADICTION, x1, x2, x3, x4,
                           "Symmetric anti-phase input; synthetic semantic contradiction", cs))

    # D. NEAR-BOUNDARY
    n = n_per_family.get(FAMILY_NEAR_BOUNDARY, 60)
    for i in range(n):
        cs = seed + 3000 + i
        rng2 = random.Random(cs)
        # Probe just around moderate magnitudes
        mag = rng2.uniform(3.0, 6.0)
        coords = [rng2.gauss(0, mag / 2.5) for _ in range(4)]
        cases.append(_make(FAMILY_NEAR_BOUNDARY, *coords,
                           "Synthetic near-threshold probe; expected QUARANTINE or BLOCK boundary", cs))

    # E. PROGRESSIVE DEGRADATION (simulated via increased noise)
    n = n_per_family.get(FAMILY_PROGRESSIVE_DEGRADATION, 50)
    for i in range(n):
        cs = seed + 4000 + i
        rng2 = random.Random(cs)
        # Simulate the nth step in a degradation sequence via larger noise
        noise_level = 0.5 + (i / n) * 4.0  # increases across cases
        base = [rng2.gauss(0, 1.0) for _ in range(4)]
        coords = [b + rng2.gauss(0, noise_level) for b in base]
        cases.append(_make(FAMILY_PROGRESSIVE_DEGRADATION, *coords,
                           f"Progressive degradation case {i}/{n}; noise_level={noise_level:.2f}", cs))

    # F. RANK / DIMENSION LOSS
    n = n_per_family.get(FAMILY_RANK_LOSS, 50)
    for i in range(n):
        cs = seed + 5000 + i
        rng2 = random.Random(cs)
        # Inputs that collapse a dimension: x4 near zero (rank-deficient projection)
        x1 = rng2.uniform(-3, 3)
        x2 = rng2.uniform(-3, 3)
        x3 = rng2.uniform(-3, 3)
        x4 = rng2.uniform(-0.001, 0.001)  # near-zero: near rank collapse
        cases.append(_make(FAMILY_RANK_LOSS, x1, x2, x3, x4,
                           "Near-zero x4; simulates rank-deficient projection toward Cl(7,0)", cs))

    # G. TRAJECTORY ANOMALIES
    n = n_per_family.get(FAMILY_TRAJECTORY_ANOMALY, 50)
    for i in range(n):
        cs = seed + 6000 + i
        rng2 = random.Random(cs)
        # Large spike in one dimension
        spike_dim = i % 4
        coords = [rng2.gauss(0, 0.5) for _ in range(4)]
        coords[spike_dim] += rng2.uniform(8.0, 15.0) * rng2.choice([-1, 1])
        cases.append(_make(FAMILY_TRAJECTORY_ANOMALY, *coords,
                           f"Velocity spike in dimension {spike_dim}; synthetic trajectory anomaly", cs))

    # H. NUMERICAL / EXTREME
    n = n_per_family.get(FAMILY_NUMERICAL_EXTREME, 40)
    for i in range(n):
        cs = seed + 7000 + i
        rng2 = random.Random(cs)
        # Mix of very large and very small magnitudes
        extreme_vals = [1e6, 1e-6, -1e6, 1e-8]
        coords = [extreme_vals[j % 4] * rng2.uniform(0.5, 2.0) for j in range(4)]
        cases.append(_make(FAMILY_NUMERICAL_EXTREME, *coords,
                           "Extreme magnitude input; tests numerical stability", cs))

    return cases


def build_full_corpus(
    native_n_per_family: Dict[str, int] = None,
    synthetic_n_per_family: Dict[str, int] = None,
    seed: int = 42,
) -> List[CorpusCase]:
    """Build combined corpus with both strata."""
    algebra = CliffordAlgebra(p=7, q=0)
    transport = AdaptiveTransport(algebra)

    native_n = native_n_per_family or {
        NATIVE_FAMILY_CLEAN: 80,
        NATIVE_FAMILY_CONTAINMENT: 60,
        NATIVE_FAMILY_CONTRADICTION: 60,
        NATIVE_FAMILY_NEAR_BOUNDARY: 60,
        NATIVE_FAMILY_BLINDED_SEMANTIC: 60,
        NATIVE_FAMILY_BENCHMARK: 80,
    }
    synthetic_n = synthetic_n_per_family or {
        FAMILY_BENIGN: 60,
        FAMILY_CONTAINMENT: 60,
        FAMILY_CONTRADICTION: 50,
        FAMILY_NEAR_BOUNDARY: 60,
        FAMILY_PROGRESSIVE_DEGRADATION: 50,
        FAMILY_RANK_LOSS: 50,
        FAMILY_TRAJECTORY_ANOMALY: 50,
        FAMILY_NUMERICAL_EXTREME: 40,
    }

    print(f"Building NATIVE_GOVERNANCE corpus (target ~{sum(native_n.values())})...")
    native_cases = build_native_corpus(native_n, seed=seed, algebra=algebra, transport=transport)
    print(f"  → {len(native_cases)} native cases generated.")

    print(f"Building SYNTHETIC_MECHANISTIC corpus (target ~{sum(synthetic_n.values())})...")
    synthetic_cases = build_synthetic_corpus(synthetic_n, seed=seed, algebra=algebra, transport=transport)
    print(f"  → {len(synthetic_cases)} synthetic cases generated.")

    all_cases = native_cases + synthetic_cases
    print(f"\nTotal corpus: {len(all_cases)} cases.")
    return all_cases


if __name__ == "__main__":
    cases = build_full_corpus()
    # Print distribution
    from collections import Counter
    strata = Counter(c.stratum for c in cases)
    dispositions = Counter(c.ground_truth_terminal_disposition for c in cases)
    families = Counter(c.failure_family for c in cases)
    print("\nStratum distribution:", dict(strata))
    print("Disposition distribution:", dict(dispositions))
    print("Family distribution:", dict(families))
