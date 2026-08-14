#!/usr/bin/env python3
import argparse
import json
import sys
import time
from daxda_engine_v11_4 import DAXDAEngineV11_4

def main():
    parser = argparse.ArgumentParser(description="DAXDA V11.4 Frozen Benchmark Runner")
    parser.add_argument("--corpus", required=True, help="Path to JSONL corpus file")
    parser.add_argument("--out", default="benchmark_results.jsonl", help="Output path for receipts")
    args = parser.parse_args()

    engine = DAXDAEngineV11_4()
    
    total = 0
    start = time.time()
    
    with open(args.corpus, 'r') as f_in, open(args.out, 'w') as f_out:
        for line in f_in:
            if not line.strip(): continue
            case = json.loads(line)
            prompt = case.get("prompt_text", "")
            sources = case.get("sources")
            is_simulated = case.get("is_simulated", False)
            
            res = engine.evaluate(prompt, sources, is_simulated)
            
            out_payload = {
                "case_id": case.get("case_id", f"idx_{total}"),
                "engine_version": res["engine_version"],
                "verdict": res["verdict"],
                "decision_rule": res["decision_rule"],
                "audit_sha256": res["audit_sha256"],
                "layer_trace": res["layer_trace"]
            }
            f_out.write(json.dumps(out_payload) + "\n")
            total += 1
            
    elapsed = time.time() - start
    print(f"Benchmark complete. Evaluated {total} cases in {elapsed:.2f} seconds.")
    print(f"Results written to {args.out}")

if __name__ == "__main__":
    main()
