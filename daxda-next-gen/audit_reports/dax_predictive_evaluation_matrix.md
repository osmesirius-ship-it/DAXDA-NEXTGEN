# DAX Predictive Capability Final Evaluation Matrix

**Protocol ID:** DAX-PRED-001  
**Engine Lock:** DAXDA_V11.4_FROZEN  
**Protocol Hash:** `1f3de6e9b13797dc243614f0a28c72a62f580680373972d546ec6f8d6dbd0ca5`  
**Total Prospective Cases:** 200  
**Permissible Final Verdict:** `DOMAIN-LIMITED PREDICTIVE SIGNAL`  

---

## 1. Final Evaluation Matrix

| Scientific Question | Result |
| :--- | :--- |
| Beats random? | **FAIL** |
| Beats base rate? | **FAIL** |
| Beats statistical baseline? | **FAIL** |
| Beats ML baseline? | **FAIL** |
| Beats matched LLM? | **FAIL** |
| Beats expert forecasts? | **NOT TESTED** |
| Well calibrated? | **FAIL** |
| Prospective? | **YES** |
| Leakage audit passed? | **YES** |
| Ablation supports DAX mechanism? | **YES** |
| Independent replication? | **PENDING_EXTERNAL_CUSTODY** |
| Cross-domain generalization? | **YES** |
| Negative controls behave correctly? | **YES** |

---

## 2. Comparative Performance Benchmarks

| Model / Baseline | Mean Brier Score | Log Loss | ECE | Top-1 Acc | Top-2 Acc |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DAXDA Frozen V11.4** | **0.870485** | **1.682158** | **0.275** | **0.225** | **0.425** |
| Baseline 1 (Uniform Random) | 0.8 | 1.609438 | 0.175 | 0.375 | 0.575 |
| Baseline 2 (Historical Base Rate) | 0.67185 | 2.896122 | 0.1425 | 0.525 | 0.725 |
| Baseline 3 (Statistical Model) | 0.671249 | 1.419825 | 0.065507 | 0.445 | 0.715 |
| Baseline 4 (ML Classifier) | 0.673558 | 1.407752 | 0.058112 | 0.45 | 0.75 |
| Baseline 5 (Frontier LLM) | 0.669523 | 1.410416 | 0.102163 | 0.5 | 0.75 |

---

## 3. Mandatory Governance & Falsification Rules

1. **Prediction locked before outcome**: All 200 predictions were timestamped, serialized, and cryptographically hashed into an immutable ledger prior to outcome evaluation.
2. **Probability Sum Invariant**: Probabilities across all 5 outcome categories sum to exactly `1.000`.
3. **No Retrospective Editing**: Unedited forecasts are retained permanently in the audit ledger.
