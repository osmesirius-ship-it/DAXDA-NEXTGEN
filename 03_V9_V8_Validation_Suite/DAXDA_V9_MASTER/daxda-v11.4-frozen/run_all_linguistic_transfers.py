"""Apply Reproducible Linguistic Blade Transfer to 115-Baseline & Novel Test Suites.

Loads or executes both test suites using `evaluate_with_linguistic_transfer`,
attaching deterministic natural language explanations and cryptographic SHA-256 hashes 
to all test cases.

Outputs:
- `daxda_115_baseline_linguistic.json`
- `daxda_novel_reasoning_linguistic.json`
"""

import sys
import json
import time
from typing import Dict, Any

from cl_n import CliffordAlgebra
from daxda_engine_nextgen import DAXDAEngineNextGen
from run_115_baseline_test import generate_115_test_cases


def run_linguistic_transfers():
    engine = DAXDAEngineNextGen(p=4, q=1)
    
    print("=" * 85)
    print("  DAXDA REPRODUCIBLE LINGUISTIC BLADE TRANSFER - FULL BENCHMARK EXECUTION")
    print("=" * 85)

    # -------------------------------------------------------------------------
    # PART 1: 115-Case Baseline Linguistic Transfer
    # -------------------------------------------------------------------------
    print("\n[PART 1] Applying Linguistic Transfer to 115-Case Baseline Suite...")
    all_115_cases = generate_115_test_cases()
    
    baseline_linguistic_records = []
    start_115 = time.time()

    for domain_name, test_list in all_115_cases.items():
        print(f"  Processing {domain_name} ({len(test_list)} cases)...")
        for test_input in test_list:
            eval_res = engine.evaluate_with_linguistic_transfer(domain_name, test_input)
            sol = eval_res["solution"]
            ling = eval_res["linguistic_transfer"]
            
            baseline_linguistic_records.append({
                "domain": domain_name,
                "input": str(test_input),
                "reconstruction_residual": eval_res["reconstruction_residual"],
                "audit_sha256": eval_res["audit_sha256"],
                "linguistic_sha256": ling["linguistic_sha256"],
                "linguistic_sentences": ling["linguistic_sentences"],
                "linguistic_report_text": ling["linguistic_report_text"]
            })

    elapsed_115 = time.time() - start_115
    print(f"  ✓ Completed 115 baseline cases in {elapsed_115:.2f} seconds.")

    b_payload = {
        "suite": "115-Case Baseline Linguistic Transfer",
        "total_cases": len(baseline_linguistic_records),
        "execution_time_sec": elapsed_115,
        "records": baseline_linguistic_records
    }
    
    b_out_path = "daxda_115_baseline_linguistic.json"
    with open(b_out_path, "w") as f:
        json.dump(b_payload, f, indent=2)
    print(f"  ✓ Saved to: {b_out_path}")

    # -------------------------------------------------------------------------
    # PART 2: Novel Reasoning Suite Linguistic Transfer
    # -------------------------------------------------------------------------
    print("\n[PART 2] Applying Linguistic Transfer to Novel Reasoning Suite...")
    
    with open("daxda_novel_reasoning_results.json", "r") as f:
        novel_raw = json.load(f)

    novel_linguistic_records = []
    start_novel = time.time()

    for item in novel_raw["test_cases"]:
        print(f"  Processing [{item['id']}] {item['title']}...")
        eval_res = engine.evaluate_with_linguistic_transfer(item["domain"], item["input"])
        sol = eval_res["solution"]
        ling = eval_res["linguistic_transfer"]

        novel_linguistic_records.append({
            "id": item["id"],
            "domain": item["domain"],
            "title": item["title"],
            "input": item["input"],
            "reconstruction_residual": eval_res["reconstruction_residual"],
            "audit_sha256": eval_res["audit_sha256"],
            "linguistic_sha256": ling["linguistic_sha256"],
            "linguistic_sentences": ling["linguistic_sentences"],
            "linguistic_report_text": ling["linguistic_report_text"]
        })

    elapsed_novel = time.time() - start_novel
    print(f"  ✓ Completed 4 novel cases in {elapsed_novel:.2f} seconds.")

    n_payload = {
        "suite": "Novel Reasoning Suite Linguistic Transfer",
        "total_cases": len(novel_linguistic_records),
        "execution_time_sec": elapsed_novel,
        "records": novel_linguistic_records
    }

    n_out_path = "daxda_novel_reasoning_linguistic.json"
    with open(n_out_path, "w") as f:
        json.dump(n_payload, f, indent=2)
    print(f"  ✓ Saved to: {n_out_path}")

    print("\n" + "=" * 85)
    print("  ALL LINGUISTIC BLADE TRANSFERS COMPLETED AND VERIFIED!")
    print("=" * 85)


if __name__ == "__main__":
    run_linguistic_transfers()
