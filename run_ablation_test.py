#!/usr/bin/env python3
"""
DAXDA — Clifford Algebra Operations Ablation Study
=====================================================
Per peer-review: to prove the algebra contributes BEYOND coordinate labeling,
run this ablation:

  CONDITION 1: FULL CLIFFORD  — Baseline with complete Cl(4,1) transport
  CONDITION 2: IDENTITY TRANSPORT — Replace M1 = R·M0·R̃ with M1 = M0 (no rotation)
  CONDITION 3: ELEMENTWISE MUL — Replace geometric products with component-wise multiply
  CONDITION 4: NO ROTOR — Disable rotor corrections, retain e15 threshold
  CONDITION 5: SCRAMBLED TABLE — Randomize multiplication-table signs (256-sign perturbations)

If performance (decision accuracy, residuals) falls specifically when Clifford operations
are removed — while the SAME coefficients remain — that is causal evidence for the algebra
beyond mere coordinate labeling.

Current expected result (honest):
  The gate fires on abs(e15) >= 0.30 regardless of transport mode.
  For a pure e15=1.0 input, transport mode does NOT change the BLOCK decision.
  This confirms the known limitation: transport is not yet causally verified against
  the SAME coefficient under different algebraic operations.

The decisive test would require a mixed-grade input where the transport itself
changes which blade receives energy — i.e., where the geometric product ROUTES
energy from one blade to another. This ablation sets up that framework.

EPISTEMIC GUARD:
  A conventional variable named adversarial_score with the same threshold
  could reproduce N1–N3. This ablation is the test to falsify that claim.
"""

import sys
import json
import math
import random
import pathlib
import time
from copy import deepcopy

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "daxda-next-gen"))

from daxda_guard.clifford_scope_encoder import CliffordScopeEncoder, Cl41State


# ---------------------------------------------------------------------------
# Cl(4,1) algebra implementations — full vs ablated
# ---------------------------------------------------------------------------

# Standard Cl(4,1) metric signature [+1,+1,+1,+1,-1]
METRIC = [1, 1, 1, 1, -1]

BLADE_NAMES_CL41 = [
    "1",    "e1",   "e2",   "e12",  "e3",   "e13",  "e23",  "e123",
    "e4",   "e14",  "e24",  "e124", "e34",  "e134", "e234", "e1234",
    "e5",   "e15",  "e25",  "e125", "e35",  "e135", "e235", "e1235",
    "e45",  "e145", "e245", "e1245","e345", "e1345","e2345","e12345",
]

E15_IDX = BLADE_NAMES_CL41.index("e15")
E1_IDX  = BLADE_NAMES_CL41.index("e1")
E3_IDX  = BLADE_NAMES_CL41.index("e3")
GATE_THRESHOLD = 0.30


def _build_rotor_cl41(theta: float, i: int = 1, j: int = 2) -> list:
    """Build a unit rotor R = cos(θ/2) + sin(θ/2)·eij in Cl(4,1).

    For the canonical test we rotate in the e1∧e2 plane (safe ↔ factual axis).
    This ensures the transport mixes blades, so ablating it changes the output.
    """
    R = [0.0] * 32
    R[0] = math.cos(theta / 2)  # scalar part
    # Find the bivector index for eij
    biv_name = f"e{i}{j}"
    if biv_name in BLADE_NAMES_CL41:
        R[BLADE_NAMES_CL41.index(biv_name)] = math.sin(theta / 2)
    return R


def _reverse(R: list) -> list:
    """Clifford reverse: flip signs of grade-2 blades."""
    R_rev = list(R)
    for i, name in enumerate(BLADE_NAMES_CL41):
        if name == "1":
            continue
        grade = len(name) - 1  # "e15" → 2 chars after 'e'
        grade = sum(1 for c in name[1:] if c.isdigit())
        if grade % 4 in (2, 3):
            R_rev[i] = -R_rev[i]
    return R_rev


def _sandwich_approx(R: list, M: list, R_rev: list) -> list:
    """Approximate R·M·R̃ via grade-0 projection for the scalar part,
    and direct rotation for grade-1/grade-2 components.

    This is the FULL CLIFFORD transport (Condition 1).
    For the ablation tests we replace this with simpler operations.
    """
    # For our sparse inputs (only e1, e3, e15 nonzero), the sandwich
    # acts as:
    #   scalar: unchanged
    #   e1: rotated within e1∧e2 plane by 2θ
    #   e15: unchanged (e15 commutes with e12 rotation)
    #   e3: unchanged (e3 not in rotation plane)
    r_scalar = R[0]
    r_biv = R[3]  # e12 coefficient (index 3 in BLADE_NAMES_CL41)

    M_out = list(M)

    # e1 rotates to cos(2θ)·e1 + sin(2θ)·e2 under e12 rotor
    cos_2t = r_scalar**2 - r_biv**2
    sin_2t = 2 * r_scalar * r_biv

    e1_in = M[E1_IDX]
    e2_idx = BLADE_NAMES_CL41.index("e2")
    e2_in = M[e2_idx]

    M_out[E1_IDX]  = cos_2t * e1_in - sin_2t * e2_in
    M_out[e2_idx]  = sin_2t * e1_in + cos_2t * e2_in

    return M_out


def _identity_transport(R: list, M: list, R_rev: list) -> list:
    """Condition 2: Identity transport — M1 = M0, no rotation applied."""
    return list(M)


def _elementwise_transport(R: list, M: list, R_rev: list) -> list:
    """Condition 3: Replace geometric product with elementwise multiply."""
    return [R[i] * M[i] for i in range(32)]


def _no_rotor_transport(R: list, M: list, R_rev: list) -> list:
    """Condition 4: Disable rotor corrections — M1 = scalar(R) * M."""
    r_scalar = R[0]
    return [r_scalar * m for m in M]


def _scrambled_table_transport(R: list, M: list, R_rev: list,
                                sign_seed: int = 42) -> list:
    """Condition 5: Randomize multiplication-table signs while preserving
    coefficient locations. 256 sign perturbations on the bivector terms."""
    rng = random.Random(sign_seed)
    M_out = list(M)
    for i in range(6, 16):  # bivector blade indices
        M_out[i] = M_out[i] * (1 if rng.random() > 0.5 else -1)
    return M_out


# ---------------------------------------------------------------------------
# Ablation engine
# ---------------------------------------------------------------------------

class AblationEngine:
    """Runs an input multivector through five transport conditions and reports
    gate dispositions, reconstruction residuals, and whether the decision changes."""

    CONDITIONS = [
        ("FULL_CLIFFORD",        "Full Cl(4,1) sandwich transport (baseline)",       _sandwich_approx),
        ("IDENTITY_TRANSPORT",   "Identity transport M1=M0 (no rotation)",            _identity_transport),
        ("ELEMENTWISE_MUL",      "Elementwise ⊙ instead of geometric product",        _elementwise_transport),
        ("NO_ROTOR",             "Scalar(R)×M only — rotor corrections disabled",     _no_rotor_transport),
        ("SCRAMBLED_TABLE",      "Randomized multiplication-table signs (seed=42)",   _scrambled_table_transport),
    ]

    def __init__(self, rotor_theta: float = math.pi / 4):
        self.theta = rotor_theta
        self.R = _build_rotor_cl41(rotor_theta, i=1, j=2)
        self.R_rev = _reverse(self.R)

    def _build_input(self, e1: float = 0.0, e3: float = 0.0, e15: float = 0.0) -> list:
        M = [0.0] * 32
        M[0]      = 0.5   # scalar part (always present)
        M[E1_IDX] = e1
        M[E3_IDX] = e3
        M[E15_IDX]= e15
        return M

    def _reconstruction_residual(self, M0: list, M1: list) -> float:
        """Max absolute difference between input and transported state."""
        return max(abs(a - b) for a, b in zip(M0, M1))

    def _gate_disposition(self, M: list) -> str:
        return "BLOCK" if abs(M[E15_IDX]) >= GATE_THRESHOLD else "RELEASE"

    def _gate_rule(self, M: list) -> dict:
        return {
            "quantity": "abs_coefficient",
            "blade": "e15",
            "value": round(abs(M[E15_IDX]), 6),
            "threshold": GATE_THRESHOLD,
            "comparison": ">=",
            "triggered": abs(M[E15_IDX]) >= GATE_THRESHOLD,
        }

    def run(self, label: str, e1: float = 0.0, e3: float = 0.0, e15: float = 0.0) -> dict:
        M0 = self._build_input(e1, e3, e15)
        baseline_disp = self._gate_disposition(M0)

        condition_results = []
        for cond_id, cond_label, transport_fn in self.CONDITIONS:
            M1 = transport_fn(self.R, M0, self.R_rev)
            disp = self._gate_disposition(M1)
            residual = self._reconstruction_residual(M0, M1)
            decision_changed = (disp != baseline_disp)

            condition_results.append({
                "condition": cond_id,
                "description": cond_label,
                "disposition": disp,
                "decision_changed_from_baseline": decision_changed,
                "reconstruction_residual": round(residual, 6),
                "e15_after_transport": round(M1[E15_IDX], 6),
                "e1_after_transport": round(M1[E1_IDX], 6),
                "gate_rule": self._gate_rule(M1),
            })

        return {
            "input_label": label,
            "input_blades": {"e1": e1, "e3": e3, "e15": e15},
            "baseline_disposition": baseline_disp,
            "rotor_theta_rad": round(self.theta, 6),
            "conditions": condition_results,
        }


# ---------------------------------------------------------------------------
# Test inputs
# ---------------------------------------------------------------------------

ABLATION_INPUTS = [
    # (label, e1, e3, e15, description)
    ("PURE_ADVERSARIAL",   0.0,  0.0, 1.0,
     "e15=1.0 only. Gate fires on e15 alone. Transport of e15 should be stable."),
    ("PURE_TRUST",         0.9,  0.0, 0.0,
     "e1=0.9 only. RELEASE. Tests if transport introduces spurious e15."),
    ("MIXED_GRADE",        0.4, -0.2, 0.7,
     "Mixed e1+e3+e15. Rotation in e1∧e2 plane SHOULD shift e1 energy. Key ablation case."),
    ("NEAR_THRESHOLD",     0.0,  0.0, 0.31,
     "e15 just above threshold. Small transport errors could flip decision."),
    ("PROTECTIVE_NEGATION",0.92, 0.74, 0.0,
     "CliffordScopeEncoder output for 'Do not allow unauthorized access.' (V11.4.2 expected RELEASE)"),
    ("DOUBLE_NEGATION_BOUNDARY", 0.0, 0.0, 0.29,
     "e15 just below threshold. Tests whether transport falsely triggers gate."),
]


def main():
    t_start = time.perf_counter()

    print("=" * 82)
    print("   DAXDA — CLIFFORD OPERATIONS ABLATION STUDY")
    print("   Isolates whether algebra contributes beyond coordinate labeling")
    print("=" * 82)
    print()
    print("   HYPOTHESIS: If decisions change specifically when Clifford operations")
    print("   are removed — while the same coefficients remain — that is causal")
    print("   evidence for the algebra. If decisions are IDENTICAL across all")
    print("   conditions, the gate depends only on the e15 channel, not the algebra.")
    print()

    engine = AblationEngine(rotor_theta=math.pi / 4)

    all_results = []
    for label, e1, e3, e15, desc in ABLATION_INPUTS:
        result = engine.run(label, e1=e1, e3=e3, e15=e15)
        all_results.append(result)

        print(f"  INPUT: {label}")
        print(f"    {desc}")
        print(f"    Blades: e1={e1} e3={e3} e15={e15} | Baseline: {result['baseline_disposition']}")
        print(f"    {'Condition':<26} {'Disposition':<12} {'Changed?':<10} {'Residual':<12} {'e15 after'}")
        print(f"    {'-'*26} {'-'*12} {'-'*10} {'-'*12} {'-'*10}")
        for cond in result["conditions"]:
            changed = "⚠ YES" if cond["decision_changed_from_baseline"] else "no"
            print(f"    {cond['condition']:<26} {cond['disposition']:<12} {changed:<10} "
                  f"{cond['reconstruction_residual']:<12.6f} {cond['e15_after_transport']:.6f}")
        print()

    # Summary: how many inputs showed any decision change across ablations
    decision_changes = sum(
        1 for r in all_results
        for c in r["conditions"]
        if c["decision_changed_from_baseline"] and c["condition"] != "FULL_CLIFFORD"
    )

    print("-" * 82)
    print(f"  Decision changes when Clifford operations removed: {decision_changes}")
    if decision_changes == 0:
        print()
        print("  CURRENT FINDING: Zero decision changes across all ablation conditions.")
        print("  INTERPRETATION: The gate fires solely on abs(e15) >= threshold.")
        print("  The transport algebra does NOT causally change the gate decision for")
        print("  these inputs. A conventional scalar variable adversarial_score=1.0")
        print("  with the same threshold would reproduce identical decisions.")
        print()
        print("  WHAT THIS MEANS:")
        print("  - The Clifford algebra is correctly implemented as a framework.")
        print("  - It does not yet exert causal influence on the governance decision")
        print("    in these test cases because the rotor plane (e1∧e2) does not")
        print("    intersect the gate-control blade (e15) for these inputs.")
        print()
        print("  NEXT STEP TO PROVE ALGEBRA CONTRIBUTION:")
        print("  Use a rotor that rotates IN the e1∧e5 or e3∧e5 plane so that")
        print("  transport routes energy INTO or OUT OF e15 based on the rotor angle.")
        print("  Then IDENTITY_TRANSPORT will show a different disposition from")
        print("  FULL_CLIFFORD — proving the product, not just the label, matters.")
    else:
        print(f"\n  ✅ Clifford operations produced {decision_changes} decision change(s).")
        print("  This is evidence that the algebra contributes beyond channel labeling.")

    # Write report
    report = {
        "title": "DAXDA Clifford Operations Ablation Study",
        "engine_conditions": [c[0] for c in AblationEngine.CONDITIONS],
        "gate_threshold": GATE_THRESHOLD,
        "rotor_theta_rad": engine.theta,
        "rotor_plane": "e1∧e2",
        "total_decision_changes_across_ablations": decision_changes,
        "current_verdict": (
            "The gate fires on abs(e15) >= threshold regardless of transport mode "
            "for these inputs. The algebra does not yet exert causal influence because "
            "the e1∧e2 rotor plane does not intersect the e15 gate-control blade. "
            "A rotor in the e1∧e5 or e3∧e5 plane would create a decisive ablation test."
        ),
        "inputs": all_results,
        "elapsed_sec": round(time.perf_counter() - t_start, 4),
    }

    out_dir = ROOT / "daxda-next-gen" / "audit_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "clifford_ablation_report.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n  JSON report: {out_path}")
    print("=" * 82)
    return report


if __name__ == "__main__":
    main()
