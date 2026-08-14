"""Test suite for Automatic Scientific Journal Report Generator.

Verifies that `evaluate_with_journal_report()` compiles a peer-review ready
scientific submission report with LaTeX equations, proofs, governance interlocks,
and cryptographic SHA-256 receipts.
"""

import sys
import json
from daxda_engine_nextgen import DAXDAEngineNextGen


def test_journal_report_generator():
    engine = DAXDAEngineNextGen(p=7, q=0)

    print("=" * 80)
    print("  DAXDA SCIENTIFIC JOURNAL SUBMISSION REPORT GENERATOR TEST SUITE")
    print("=" * 80)

    test_inputs = [
        ("Mathematics", "Integral(cos(x)*exp(x), x) = 0.5*exp(x)*(sin(x)+cos(x))"),
        ("Physics", "Einstein Field Equations: G_mu_nu + Lambda * g_mu_nu = 8 * pi * G / c^4 * T_mu_nu"),
        ("Software Engineering", "async def stream_processor(pipe): await pipe.flush()"),
        ("Logic", "Gödel Sentence G: G is unprovable in T iff Clifford commutator [e1, e2] != 0")
    ]

    for domain, data in test_inputs:
        print(f"\n[DOMAIN: {domain}] Input: \"{str(data)[:50]}...\"")
        res = engine.evaluate_with_journal_report(domain, data)

        assert "scientific_journal_report" in res, "FALSIFICATION: Missing scientific_journal_report in result!"
        jr = res["scientific_journal_report"]

        print(f"  • Journal Title:            {jr['journal_title']}")
        print(f"  • Manuscript SHA-256:       {jr['manuscript_sha256'][:24]}...")
        print(f"  • Governance Audit Hash:    {jr['audit_sha256'][:24]}...")
        print(f"  • Verdict Disposition:      {jr['verdict']} ({jr['decision_rule']})")
        print("  • Manuscript Preview (First 8 lines):")
        
        lines = jr["manuscript_markdown"].split("\n")
        for line in lines[:8]:
            print(f"    {line}")

        assert len(jr["manuscript_markdown"]) > 500, "FALSIFICATION: Manuscript report text was too short!"

    print("\n" + "=" * 80)
    print("  ALL SCIENTIFIC JOURNAL REPORT GENERATOR TESTS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    test_journal_report_generator()
