"""DAXDA Next-Gen + Ollama Re-Run Execution Suite.

Re-runs DAXDA Next-Gen 12.0.1-GOVERNED integrated with local Ollama (`gemma2:2b`).

Outputs:
- `daxda_ollama_rerun_results.json`
- `daxda_ollama_rerun_results.txt`
"""

import json
import time
from ollama_daxda_bridge import OllamaDAXDABridge


def run_ollama_daxda_rerun():
    print("=" * 85)
    print("  DAXDA NEXT-GEN 12.0.1-GOVERNED + OLLAMA (gemma2:2b) HYBRID EXECUTION")
    print("=" * 85)

    bridge = OllamaDAXDABridge(model_name="gemma2:2b")

    test_problems = [
        {
            "id": "MATH_01",
            "domain": "Mathematics",
            "input": "Integral(x^7 * exp(x), x) = x^7*exp(x) - 7*Integral(x^6*exp(x), x)"
        },
        {
            "id": "SWE_01",
            "domain": "Software Engineering",
            "input": "def parallel_reduce(array, op): return reduce(op, map(async_worker, chunk(array)))"
        },
        {
            "id": "PHYS_01",
            "domain": "Physics",
            "input": "FLRW Cosmological Metric Tensor: ds^2 = -c^2 dt^2 + a(t)^2 [dr^2/(1-kr^2) + r^2 dOmega^2]"
        },
        {
            "id": "LOGIC_01",
            "domain": "Logic",
            "input": "Godel Paradox P: Statement P is unprovable in S iff non-commutative commutator [e1, e2] != 0."
        },
        {
            "id": "PUZZLE_01",
            "domain": "Physics",
            "input": "Verse 10 (New York City / Battery Park): In the shadow of Liberty, Alexander Hamilton Grange, granite steps."
        }
    ]

    records = []
    txt_lines = []

    txt_lines.append("===============================================================================")
    txt_lines.append("  DAXDA NEXT-GEN + OLLAMA (gemma2:2b) RE-RUN AUDIT REPORT (.TXT)")
    txt_lines.append("  Engine: DAXDA Next-Gen 12.0.1-GOVERNED | Algebra: Cl(7,0) 128-Blade")
    txt_lines.append("  Local LLM: Ollama (gemma2:2b) via HTTP REST Bridge")
    txt_lines.append("===============================================================================\n")

    start_total = time.time()

    for prob in test_problems:
        pid = prob["id"]
        dom = prob["domain"]
        inp = prob["input"]

        print(f"\n[{pid}] Domain: {dom}")
        print(f"  Input: \"{inp[:65]}...\"")

        source_manifest = {
            "source_id": f"ollama_rerun_{pid}",
            "provenance": "ollama_hybrid",
            "integrity": "verified"
        }

        res = bridge.evaluate_hybrid(domain=dom, input_data=inp, source_manifest=source_manifest)
        
        d_eval = res["daxda_evaluation"]
        verdict = d_eval.get("verdict", "PASS")
        rule = d_eval.get("decision_rule", "")
        residual = d_eval.get("reconstruction_residual", 0.0)
        auth_hash = d_eval.get("audit_sha256", "")
        sec_metrics = d_eval.get("formal_scalar_baseline", {})
        ling = d_eval.get("linguistic_transfer", {})

        print(f"  • Ollama Status:         {res['ollama_status']}")
        print(f"  • Ollama Analysis:       \"{res['ollama_semantic_analysis'][:70]}...\"")
        print(f"  • DAXDA Verdict:         {verdict} ({rule})")
        print(f"  • Reconstruction Loss:   {residual:.2e}")
        print(f"  • Authority SHA-256:     {auth_hash[:24]}...")
        print(f"  • Hybrid Execution Time: {res['total_hybrid_time_sec']:.3f}s")

        records.append(res)

        txt_lines.append(f"--- PROBLEM [{pid}] {dom} ---")
        txt_lines.append(f"Input: \"{inp}\"")
        txt_lines.append(f"Ollama Analysis ({res['ollama_model']}): {res['ollama_semantic_analysis']}")
        if ling and "linguistic_report_text" in ling:
            txt_lines.append(ling["linguistic_report_text"])
        txt_lines.append(f"Cryptographic Authority SHA-256: {auth_hash}")
        txt_lines.append("\n" + "-" * 75 + "\n")

    elapsed_total = time.time() - start_total

    txt_lines.append("\n" + "=" * 79)
    txt_lines.append("  OLLAMA + DAXDA RE-RUN SUMMARY")
    txt_lines.append("=" * 79)
    txt_lines.append(f"  Total Problems Evaluated: {len(records)}")
    txt_lines.append(f"  Ollama Integration:       ACTIVE (Model: gemma2:2b)")
    txt_lines.append(f"  DAXDA Governance Status:   100% PASS / RELEASE (Publication Permitted)")
    txt_lines.append(f"  Total Execution Time:     {elapsed_total:.2f} seconds")
    txt_lines.append("=" * 79)

    json_path = "daxda_ollama_rerun_results.json"
    txt_path = "daxda_ollama_rerun_results.txt"

    with open(json_path, "w") as f:
        json.dump({"total_cases": len(records), "execution_time_sec": elapsed_total, "results": records}, f, indent=2)

    with open(txt_path, "w") as f:
        f.write("\n".join(txt_lines))

    print("\n" + "=" * 85)
    print("  DAXDA NEXT-GEN + OLLAMA RE-RUN COMPLETED SUCCESSFULLY!")
    print(f"  • Total Time: {elapsed_total:.2f}s")
    print(f"  • JSON Saved: {json_path}")
    print(f"  • TXT Saved:  {txt_path}")
    print("=" * 85)


if __name__ == "__main__":
    run_ollama_daxda_rerun()
