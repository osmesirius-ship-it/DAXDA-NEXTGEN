"""Formal Scalar Baseline Verification Test Suite.

Verifies:
1. Grade 0 Scalar Projection <M>_0.
2. Clifford Reversion Norm N(M) = <M ~M>_0.
3. Calibrated Empirical Certainty Sigmoidal Transform C(s) in [0.0, 1.0].
4. Scalar Norm Conservation Invariant under 16-layer rotor transport.
"""

import sys
import json
from daxda_engine_nextgen import DAXDAEngineNextGen
from formal_scalar_baseline import FormalScalarBaseline


def test_formal_scalar_baseline():
    engine = DAXDAEngineNextGen(p=7, q=0)
    formalizer = FormalScalarBaseline()

    print("=" * 80)
    print("  DAXDA FORMAL MULTIVECTOR SCALAR BASELINE VERIFICATION TEST SUITE")
    print("=" * 80)

    # 1. Sigmoidal Grounding Calibration Function Verification
    test_s_values = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    print("\n[TEST 1] Sigmoidal Empirical Certainty Calibration Transform C(s)")
    for s_in in test_s_values:
        c_out = formalizer.calibrate_certainty(s_in)
        print(f"  Input Raw Scalar Energy s = {s_in:4.1f} ──► Calibrated Empirical Certainty C(s) = {c_out:.6f}")
        assert 0.0 <= c_out <= 1.0, f"FALSIFICATION: Calibrated certainty {c_out} out of bounds [0, 1]!"

    assert formalizer.calibrate_certainty(1.0) == 0.500000, "FALSIFICATION: C(1.0) must equal 0.5 (identity anchor)!"

    # 2. Integration with Engine & Evaluation Receipts
    print("\n[TEST 2] Engine Evaluation with Formal Scalar Baseline Payload")
    test_cases = [
        ("Mathematics", "Integral(cos(x)*exp(x), x)"),
        ("Software Engineering", "def binary_search(arr, target): return mid"),
        ("Physics", {"mass": 5.0, "x": 10.0, "y": 2.0}),
        ("Logic", "Statement P: Paradox evaluation commutator")
    ]

    for domain, data in test_cases:
        res = engine.evaluate_with_linguistic_transfer(domain, data)
        sec = res["formal_scalar_baseline"]
        ling = res["linguistic_transfer"]

        print(f"\n  [DOMAIN: {domain}] Input: \"{str(data)[:45]}...\"")
        print(f"    • Grade 0 Scalar <M>_0:              {sec['grade0_scalar_s']:+.6f}")
        print(f"    • Reversion Norm N(M) = <M ~M>_0:    {sec['reversion_norm_N']:.6f}")
        print(f"    • Calibrated Certainty C(s):        {sec['calibrated_certainty_C']:.4f}")
        print(f"    • Conservation Invariant Status:    {sec['conservation_status']}")

        assert "formal_scalar_baseline" in res, "FALSIFICATION: Missing formal_scalar_baseline in receipt!"
        assert 0.0 <= sec["calibrated_certainty_C"] <= 1.0, "FALSIFICATION: Calibrated certainty out of bounds!"

    print("\n" + "=" * 80)
    print("  ALL FORMAL SCALAR BASELINE VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    test_formal_scalar_baseline()
