# DAXDA V11.4 Reproducibility Guide

This archive (`daxda-v11.4-frozen`) contains the complete, frozen runtime environment for DAXDA V11.4, prepared for the 1,200-case critical evaluation benchmark.

## Archive Contents
- **Modules**: `semantic_encoder.py`, `geometric_transport.py`, `authority_gate.py`, `cl20.py`
- **Orchestrator**: `daxda_engine_v11_4.py`
- **Configuration**: `thresholds.json`, `patterns.json`
- **Evaluation**: `run_frozen_benchmark.py`, `evaluation_schema.json`
- **Manifest**: `runtime_manifest.json`

## Evaluation Protocol

1. **Verify Integrity**: Compare the SHA-256 hashes of all files in this directory against the `runtime_manifest.json`.
2. **Execute Benchmark**: Use the frozen runner to evaluate the hidden corpus:
   ```bash
   python3 run_frozen_benchmark.py --corpus /path/to/hidden_1200.jsonl --out results.jsonl
   ```
3. **Audit Receipts**: The runner will output a `results.jsonl` containing the `audit_sha256` and the full `layer_trace` for every case, demonstrating exact metadata-assisted reversibility.
4. **Scoring**: Compute the confusion matrix and check the pre-registered pass criteria against the `results.jsonl` output.

**Invariant Guarantee**: The `AuthorityGate` actively asserts $G(M_0) = G(\hat M_0)$. If the geometric transport fails to reconstruct an identical decision basis, the system will halt closed with a `TRANSPORT_DECISION_DIVERGENCE` rule.
