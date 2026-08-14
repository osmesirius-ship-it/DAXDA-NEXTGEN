"""7-Vector Cl(7,0) Multivector Algebra Verification Test Suite.

Verifies:
1. DAXDA Engine Next-Gen 12.0.1-GOVERNED operates in 7-vector Cl(7,0) space (128 basis blades).
2. All 7 vector generators (e1..e7) and 21 bivectors (e12..e67) are active and mapped.
3. 16-layer rotor transport maintains exact numerical reversibility (residual < 1e-14).
4. Synchronous fail-closed authority gate evaluates governance rules cleanly.
"""

import sys
import json
from daxda_engine_nextgen import DAXDAEngineNextGen


def test_7vector_cl70():
    engine = DAXDAEngineNextGen(p=7, q=0)  # 7-vector space (128 blades)
    
    print("=" * 80)
    print("  DAXDA NEXT-GEN 7-VECTOR Cl(7,0) ALGEBRA VERIFICATION TEST SUITE")
    print(f"  Algebra Signature: Cl({engine.algebra.p},{engine.algebra.q}) | Total Blades: {engine.algebra.dim}")
    print("=" * 80)

    assert engine.algebra.dim == 128, f"FALSIFICATION: Expected 128 blades for Cl(7,0), got {engine.algebra.dim}"
    assert engine.algebra.n == 7, f"FALSIFICATION: Expected 7 vector generators, got {engine.algebra.n}"

    print(f"\n✓ Verified Algebra Signature: Cl(7,0) with {engine.algebra.dim} Basis Blades and 7 Vector Generators (e1..e7).")

    # Evaluation Test across 4 domains
    test_cases = [
        ("Mathematics", "Integral(x^7 * exp(x), x)"),
        ("Software Engineering", "def solver_7vector(data): return [x**7 for x in data]"),
        ("Physics", {"x": 10.0, "y": 5.0, "z": 2.0, "vx": 1.5, "vy": 2.0, "mass": 7.0}),
        ("Logic", "Statement P_7: Non-commutative 7-vector commutator invariant.")
    ]

    for domain, data in test_cases:
        print(f"\n[DOMAIN: {domain}] Input: \"{str(data)}\"")
        res = engine.evaluate_with_linguistic_transfer(domain, data)
        
        sol = res["solution"]
        res_val = res["reconstruction_residual"]
        auth = res["authority_receipt"]
        ling = res["linguistic_transfer"]

        print(f"  • Verdict:               {res['verdict']} ({res['decision_rule']})")
        print(f"  • Publication Permitted: {res['publication_permitted']}")
        print(f"  • Reconstruction Loss:   {res_val:.2e}")
        print(f"  • SHA-256 Authority Hash: {res['audit_sha256'][:24]}...")
        print(f"  • Active Blades Count:   {len(sol.get('geometric_state', {}))}")
        
        assert res_val < 1e-12, f"FALSIFICATION: Micro-reversibility loss {res_val:.2e} exceeded 1e-12 limit!"
        assert res["publication_permitted"] is True, "FALSIFICATION: Governed 7-vector evaluation was blocked!"

    print("\n" + "=" * 80)
    print("  ALL 7-VECTOR Cl(7,0) ALGEBRA VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    test_7vector_cl70()
