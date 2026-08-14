import json
import random

def main():
    target_categories = [
        'non_operational_medical_education', 'direct_prompt_injection', 'sensitive_data_transformation', 
        'model_asset_exfiltration', 'destructive_file_operation', 'tool_output_injection', 
        'supply_chain_confusion', 'defensive_security_analysis', 'authorized_system_administration', 
        'unsafe_medical_autonomy', 'logging_suppression', 'benign_general_knowledge', 'credential_redaction'
    ]
    
    # 13 categories. To get 2200 total, we do 13 * 169 = 2197. Add 3 to the first one.
    counts = {c: 169 for c in target_categories}
    counts[target_categories[0]] += 3
    
    print(f"Target distribution: {counts}")
    
    # First, group all case_ids by category
    labels_file = "/Users/user/Downloads/daxda-v11.4-benchmark-12000/benchmark_labels_private.jsonl"
    category_to_ids = {c: [] for c in target_categories}
    
    with open(labels_file, "r") as f:
        for line in f:
            obj = json.loads(line)
            cat = obj["subgroup"]
            if cat in category_to_ids:
                category_to_ids[cat].append(obj["case_id"])
                
    # Sample the specific counts
    selected_ids = set()
    for cat, count in counts.items():
        sampled = random.sample(category_to_ids[cat], count)
        selected_ids.update(sampled)
        
    print(f"Total selected IDs: {len(selected_ids)}")
    
    # Now extract those from the inputs file and labels file
    inputs_in = "/Users/user/Downloads/daxda-v11-2.4-benchmark-12000/benchmark_inputs_blind.jsonl"
    inputs_out = "/Users/user/Downloads/DAXDA_V9_MASTER/daxda-v12-engine/benchmark_2200_inputs.jsonl"
    
    labels_out = "/Users/user/Downloads/DAXDA_V9_MASTER/daxda-v12-engine/benchmark_2200_labels.jsonl"
    
    extracted_inputs = 0
    with open(inputs_in, "r") as fin, open(inputs_out, "w") as fout:
        for line in fin:
            obj = json.loads(line)
            if obj["case_id"] in selected_ids:
                fout.write(line)
                extracted_inputs += 1
                
    extracted_labels = 0
    with open(labels_file, "r") as fin, open(labels_out, "w") as fout:
        for line in fin:
            obj = json.loads(line)
            if obj["case_id"] in selected_ids:
                fout.write(line)
                extracted_labels += 1
                
    print(f"Wrote {extracted_inputs} inputs and {extracted_labels} labels to daxda-v12-engine/")

if __name__ == "__main__":
    main()
