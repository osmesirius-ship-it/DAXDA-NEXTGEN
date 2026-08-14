"""Test script for DAXDA Reproducible Linguistic Blade Transfer Function.

Executes evaluations across Mathematics, Software Engineering, Physics, and Logic,
verifying that natural language reports are 100% reproducible with matching 
SHA-256 integrity hashes across multiple runs.
"""

import sys
import json
import hashlib
from daxda_engine_nextgen import DAXDAEngineNextGen


def test_reproducibility():
    engine = DAXDAEngineNextGen(p=4, q=1)
    
    print("=" * 80)
    print("  DAXDA REPRODUCIBLE LINGUISTIC BLADE TRANSFER VERIFICATION")
    print("=" * 80)

    test_inputs = [
        ("Mathematics", "Integral(sin(x)*exp(x), x) = 0.5*exp(x)*(sin(x)-cos(x))"),
        ("Software Engineering", "def quicksort(arr): return arr if len(arr) <= 1 else quicksort(...)"),
        ("Physics", {"mass": 5.0, "x": 10.0, "y": 5.0, "vx": 1.5, "vy": 2.0}),
        ("Logic", "Statement P: P is unprovable in system S iff [e1, e2] = 2*e12 vanishes.")
    ]

    for domain, data in test_inputs:
        print(f"\n[DOMAIN: {domain.upper()}] Input: \"{str(data)[:60]}...\"")
        
        # Run 1
        res1 = engine.evaluate_with_linguistic_transfer(domain, data)
        ling1 = res1["linguistic_transfer"]
        hash1 = ling1["linguistic_sha256"]
        
        # Run 2 (Verify Reproducibility)
        res2 = engine.evaluate_with_linguistic_transfer(domain, data)
        ling2 = res2["linguistic_transfer"]
        hash2 = ling2["linguistic_sha256"]
        
        print("  Natural Language Report Snippet:")
        report_lines = ling1["linguistic_report_text"].split("\n")
        for line in report_lines[:12]:
            print(f"    {line}")
            
        print(f"  Run 1 SHA-256 Hash: {hash1}")
        print(f"  Run 2 SHA-256 Hash: {hash2}")
        
        assert hash1 == hash2, "FALSIFICATION: Linguistic reports were not identical!"
        print(f"  >>> Reproducibility Status: PASSED (100% Identical SHA-256 Hash)")

    print("\n" + "=" * 80)
    print("  ALL LINGUISTIC BLADE TRANSFER REPRODUCIBILITY TESTS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    test_reproducibility()
