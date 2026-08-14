"""Governed Authority Gate Test Suite.

Verifies that DAXDA Engine Next-Gen 12.0.1-GOVERNED correctly enforces:
1. Fail-closed BLOCK when evidence integrity fails.
2. Fail-closed CONTAIN when domain scope is unauthorized.
3. Fail-closed BLOCK when evaluation is simulated.
4. Publication PERMITTED with formal authority receipt when evidence is verified.
"""

import sys
import json
from daxda_engine_nextgen import DAXDAEngineNextGen


def test_governed_authority_gate():
    engine = DAXDAEngineNextGen(p=4, q=1)
    
    print("=" * 80)
    print("  DAXDA NEXT-GEN 12.0.1-GOVERNED AUTHORITY GATE TEST SUITE")
    print("=" * 80)

    # Test 1: Verified Input -> Publication Permitted
    print("\n[TEST 1] Verified Source Input -> Governed PASS / RELEASE")
    v_manifest = {"source_id": "input_01", "provenance": "direct_user", "integrity": "verified"}
    res1 = engine.evaluate("Mathematics", "Integral(cos(x), x)", source_manifest=v_manifest)
    print(f"  Verdict: {res1['verdict']} | Rule: {res1['decision_rule']}")
    print(f"  Publication Permitted: {res1['publication_permitted']}")
    print(f"  Authority Receipt SHA256: {res1['audit_sha256'][:24]}...")
    assert res1["publication_permitted"] is True, "FALSIFICATION: Governed verified evaluation was blocked!"

    # Test 2: Evidence Integrity Failed -> Fail-Closed BLOCK
    print("\n[TEST 2] Failed Evidence Integrity -> Fail-Closed BLOCK")
    f_manifest = {"source_id": "untrusted_input", "provenance": "external_data", "integrity": "failed"}
    res2 = engine.evaluate("Mathematics", "Integral(cos(x), x)", source_manifest=f_manifest)
    print(f"  Verdict: {res2['verdict']} | Rule: {res2['decision_rule']}")
    print(f"  Publication Permitted: {res2['publication_permitted']}")
    print(f"  Reason: {res2['reason']}")
    assert res2["publication_permitted"] is False, "FALSIFICATION: Unverified evidence integrity was not blocked!"

    # Test 3: Unauthorized Domain -> Fail-Closed CONTAIN
    print("\n[TEST 3] Unauthorized Domain Scope -> Fail-Closed CONTAIN")
    res3 = engine.evaluate("Unauthorized_Domain", "test", source_manifest=v_manifest)
    print(f"  Verdict: {res3['verdict']} | Rule: {res3['decision_rule']}")
    print(f"  Publication Permitted: {res3['publication_permitted']}")
    assert res3["publication_permitted"] is False, "FALSIFICATION: Unauthorized domain scope was not contained!"

    # Test 4: Simulated Evaluation -> Fail-Closed BLOCK
    print("\n[TEST 4] Simulated Evaluation -> Fail-Closed BLOCK")
    res4 = engine.evaluate("Physics", {"x": 1.0}, source_manifest=v_manifest, is_simulated=True)
    print(f"  Verdict: {res4['verdict']} | Rule: {res4['decision_rule']}")
    print(f"  Publication Permitted: {res4['publication_permitted']}")
    assert res4["publication_permitted"] is False, "FALSIFICATION: Simulated evaluation was not blocked!"

    print("\n" + "=" * 80)
    print("  ALL GOVERNED AUTHORITY GATE FAIL-CLOSED TESTS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    test_governed_authority_gate()
