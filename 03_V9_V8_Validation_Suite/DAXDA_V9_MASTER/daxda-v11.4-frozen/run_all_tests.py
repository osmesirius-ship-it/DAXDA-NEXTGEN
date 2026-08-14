"""DAXDA Next-Gen Unified Master Test Suite Runner.

Discovers and executes all registered component unit tests:
1. `test_governed_authority_gate.py`
2. `test_7vector_cl70.py`
3. `test_formal_scalar_baseline.py`
4. `test_linguistic_transfer.py`

Outputs a clean summary report of test results, timing, and pass/fail status.
"""

import sys
import time
import unittest


def run_master_test_suite():
    print("=" * 80)
    print("  DAXDA NEXT-GEN 12.0.1-GOVERNED: MASTER TEST SUITE RUNNER")
    print("=" * 80)

    test_modules = [
        "test_governed_authority_gate",
        "test_7vector_cl70",
        "test_formal_scalar_baseline",
        "test_linguistic_transfer",
        "test_journal_report_generator"
    ]

    start_total = time.time()
    results = []

    for mod_name in test_modules:
        print(f"\n>>> Running Module: {mod_name}...")
        start_mod = time.time()
        try:
            mod = __import__(mod_name)
            # Find test function in module
            test_fn_name = [f for f in dir(mod) if f.startswith("test_") and callable(getattr(mod, f))][0]
            test_fn = getattr(mod, test_fn_name)
            test_fn()
            elapsed_mod = time.time() - start_mod
            results.append((mod_name, "PASSED", elapsed_mod))
            print(f"  ✓ {mod_name} PASSED in {elapsed_mod:.3f}s")
        except Exception as e:
            elapsed_mod = time.time() - start_mod
            results.append((mod_name, f"FAILED: {e}", elapsed_mod))
            print(f"  ✗ {mod_name} FAILED in {elapsed_mod:.3f}s: {e}")

    total_elapsed = time.time() - start_total

    print("\n" + "=" * 80)
    print("  DAXDA MASTER TEST SUITE SUMMARY")
    print("=" * 80)
    passed_count = sum(1 for _, status, _ in results if status == "PASSED")
    total_count = len(results)

    for mod_name, status, el in results:
        print(f"  • {mod_name:<32}: {status:<10} ({el:.3f}s)")

    print("-" * 80)
    print(f"  Total Passed: {passed_count} / {total_count} ({passed_count/total_count*100:.1f}%)")
    print(f"  Total Time:   {total_elapsed:.3f} seconds")
    print("=" * 80)

    if passed_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    run_master_test_suite()
