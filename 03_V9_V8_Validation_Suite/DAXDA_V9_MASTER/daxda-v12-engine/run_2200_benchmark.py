import json
import time
from daxda_engine_v11_4 import DAXDAEngineV11_4

def main():
    engine = DAXDAEngineV11_4()
    
    input_file = "/Users/user/Downloads/DAXDA_V9_MASTER/daxda-v12-engine/benchmark_2200_inputs.jsonl"
    output_file = "/Users/user/Downloads/DAXDA_V9_MASTER/daxda-v12-engine/predictions_2200.jsonl"
    
    print(f"Starting 2,200 case evaluation on {input_file} using local Ollama LLM...")
    
    start_time = time.time()
    processed_count = 748
    
    with open(input_file, "r") as fin, open(output_file, "a") as fout:
        for i, line in enumerate(fin):
            if i < 748:
                continue
            case = json.loads(line)
            case_id = case["case_id"]
            text = case["input_text"]
            prov = case["provenance"]
            
            # Map provenance dict to what SemanticEncoder expects
            sources = [{
                "text": text,
                "provenance": prov.get("source_type", "direct_user"),
                "integrity": "verified" if prov.get("authenticated") else "unverified",
                "source_id": case_id
            }]
            
            result = engine.evaluate(prompt_text="", sources=sources, is_simulated=False)
            
            raw_verdict = result["verdict"]
            verdict_map = {
                "PASS": "RELEASE",
                "RELEASE/CAUTION": "WARN",
                "BLOCK": "BLOCK"
            }
            mapped_verdict = verdict_map.get(raw_verdict, raw_verdict)
            
            decoded = result["decoded_state"]
            
            prediction = {
                "case_id": case_id,
                "predicted_disposition": mapped_verdict,
                "trust": decoded["trust"],
                "cautionary_risk": decoded["cautionary_risk"],
                "severe_risk": decoded["severe_risk"],
                "deception": decoded["deception"],
                "direct_gate_verdict": mapped_verdict,
                "reconstructed_gate_verdict": mapped_verdict,
                "max_local_residual": result["reconstruction_residual"],
                "is_simulated": False,
                "execution_error": None,
                "operation_count": result["operation_count"],
                "audit_sha256": result["audit_sha256"]
            }
            
            fout.write(json.dumps(prediction) + "\n")
            fout.flush()
            
            processed_count += 1
            if processed_count % 100 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {processed_count}/2200 cases... ({elapsed:.2f}s elapsed)")
                
    total_time = time.time() - start_time
    print(f"Done processing 2200 cases in {total_time:.2f} seconds. Saved to {output_file}")

if __name__ == "__main__":
    main()
