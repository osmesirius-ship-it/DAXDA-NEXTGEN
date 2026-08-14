#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, Any

import sys
sys.path.append("/Users/user/Downloads")
from daxda_engine_v7 import DAXDAEngineV7
from daxda_engine_v11 import DAXDAEngineV11
from daxda_engine_v11_3 import DAXDAEngineV11_3

def evaluate_ablation_direct_thresholding(prompt_text: str, sources=None) -> Dict[str, Any]:
    # We monkeypatch the LAYERS list to be empty for this specific evaluation,
    # effectively meaning M_0 is checked against the thresholds with no transformations.
    engine = DAXDAEngineV11_3()
    import daxda_engine_v11_3
    original_layers = daxda_engine_v11_3.LAYERS
    daxda_engine_v11_3.LAYERS = []
    try:
        result = engine.evaluate(prompt_text, sources=sources)
    finally:
        daxda_engine_v11_3.LAYERS = original_layers
    return result

def main():
    corpus_path = Path("internal_preflight.jsonl")
    if not corpus_path.exists():
        print(f"Error: {corpus_path} not found.")
        return

    cases = []
    with open(corpus_path, "r") as f:
        for line in f:
            if line.strip():
                cases.append(json.loads(line))

    v7_engine = DAXDAEngineV7()
    v11_2_engine = DAXDAEngineV11()
    v11_3_engine = DAXDAEngineV11_3()

    print(f"Loaded {len(cases)} test cases.")
    print(f"{'ID':<8} | {'Expected':<15} | {'V7 (Flags)':<15} | {'V11.2 (Partial)':<15} | {'V11.3 (Exact)':<15} | {'Ablation (No Layers)':<15}")
    print("-" * 95)
    
    matches_v11_2 = 0
    matches_v11_3 = 0
    matches_ablation = 0

    for i, case in enumerate(cases):
        prompt = case["prompt_text"]
        expected = case["expected_verdict"]

        v7_res = v7_engine.evaluate(prompt)
        v7_verdict = v7_res.get("verdict", "UNKNOWN")

        v11_2_res = v11_2_engine.evaluate(prompt, sources=case.get("sources"))
        v11_2_verdict = v11_2_res.get("verdict", "UNKNOWN")

        v11_3_res = v11_3_engine.evaluate(prompt, sources=case.get("sources"))
        v11_3_verdict = v11_3_res.get("verdict", "UNKNOWN")

        ablation_res = evaluate_ablation_direct_thresholding(prompt, case.get("sources"))
        ablation_verdict = ablation_res.get("verdict", "UNKNOWN")

        if v11_2_verdict == expected: matches_v11_2 += 1
        if v11_3_verdict == expected: matches_v11_3 += 1
        if ablation_verdict == expected: matches_ablation += 1
        
        print(f"P{i+1:<7} | {expected:<15} | {v7_verdict:<15} | {v11_2_verdict:<15} | {v11_3_verdict:<15} | {ablation_verdict:<15}")

    print("-" * 95)
    print(f"V11.2 Accuracy  : {matches_v11_2}/{len(cases)} ({matches_v11_2/len(cases):.2%})")
    print(f"V11.3 Accuracy  : {matches_v11_3}/{len(cases)} ({matches_v11_3/len(cases):.2%})")
    print(f"Ablation Acc.   : {matches_ablation}/{len(cases)} ({matches_ablation/len(cases):.2%})")
    print()
    print("ANALYSIS: If V11.3 Accuracy == Ablation Accuracy, then the geometric transformations")
    print("mathematically cancel out and act as an audit receipt rather than a reasoner.")

if __name__ == "__main__":
    main()
