# DAXDA — GOVERNANCE SUMMARY REPORT
## Test: stress_test_04
*2026-07-02 02:45:04 UTC*

---

## 886-OPS ENGINE RESULTS

| Metric | Value |
|---|---|
| Tiles Executed | **886** |
| Layers Executed | 16 |
| Final Gate | **BLOCK** |
| Stability Score | **0.0 / 1.000** |
| Authority Level | **BLOCKED** |
| Total Warnings | 212 |
| Unique Material Findings | **17** |
| Recursive Recurrence Events | 195 *(not independent attacks)* |
| Blocked At | N/A |

**System Ops:**

| Tile | Function | Gate | Notes |
|---|---|---|---|
| SYS_881 | `final_scoring` | PASS | Final TOTAL_STABILITY computed: 0.0. Logic=1.0, Assumption=1.0. |
| SYS_882 | `authority_assignment` | BLOCK | Authority assigned: BLOCKED. Status: BLOCKED. |
| SYS_883 | `audit_manifest_build` | PASS | Audit manifest built. Trace entries=882, canonical_output_hash=3cba72cf31b36a6b. |
| SYS_884 | `release_lock_evaluation` | BLOCK | Release lock: HELD. Unique warning rate=0.018 (total=0.239, denominator=883 tiles). |
| SYS_885 | `reentry_hook_registration` | PASS | Re-entry hooks registered: 1. reentry::score_below_threshold::0.0 |
| SYS_886 | `memory_boundary_commit` | PASS | Memory boundary committed. Retained=['run_id', 'final_gate', 'final_stability_score', 'authority_lev |

**Unique Material Findings:**

1. Leading/trailing whitespace detected
2. Irregular whitespace detected
3. [FDL_1] High-stakes domain detected: financial, legal/compliance, technical, human/organizational
4. [FDL_1] 2 strong assertive claim(s) detected without hedging ('does').
5. [FDL_1] Hidden premise: urgency may be suppressing scrutiny.
6. [FDL_1] 2 ['public', 'production'] high-input_threat operation term(s) detected.
7. [FDL_1] Causal claims present without supporting evidence.
8. [FDL_1] ADVERSARIAL: Prompt-injection or override attempt detected (2 ['Do not follow', 'OVERRIDE'] pattern(s)).
9. [FDL_1] Adversarial input_threat: 2 ['public', 'production'] high-input_threat operation(s) in input.
10. [FDL_1] SAFETY: 2 ['public', 'production'] destructive/privileged operation term(s).
11. [FDL_1] SAFETY: Instruction-injection pattern detected.
12. [FDL_1] WARNING: 2 ['public', 'production'] input_threat-flagged term(s) in input.
13. [FDL_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] adversarial pattern(s) detected.
14. [FDL_1] Scenario HIGH: Hostile scenario score=10. Survivability LOW.
15. [FDL_1] Gate recommendation: BLOCK.
16. [LLM::TRC_1::logic_validity_check] Network err: HTTPConnectionPool(host='127.0.0.1', port=11434): Read timed out. (read timeout=60) [model=fallback, provider=simulated-fallback, version=v1.0, req_hash=2134e6d496a0e974, resp_hash=err]
17. Release lock HELD. Status: BLOCKED, Final Gate: BLOCK.

**Flagged Tiles (first 20):**

| Layer | Function | Warning |
|---|---|---|
| FDL_1 | `normalize_input` | Leading/trailing whitespace detected |
| FDL_1 | `domain_classify` | [FDL_1] High-stakes domain detected: financial, legal/compliance, tech |
| FDL_1 | `claim_extract` | [FDL_1] 2 strong assertive claim(s) detected without hedging ('does'). |
| FDL_1 | `hidden_premise_scan` | [FDL_1] Hidden premise: urgency may be suppressing scrutiny. |
| FDL_1 | `risk_weight` | [FDL_1] 2 ['public', 'production'] high-input_threat operation term(s) |
| FDL_1 | `logic_validity_check` | [FDL_1] Causal claims present without supporting evidence. |
| FDL_1 | `adversarial_attack` | [FDL_1] ADVERSARIAL: Prompt-injection or override attempt detected (2  |
| FDL_1 | `safety_policy_check` | [FDL_1] SAFETY: 2 ['public', 'production'] destructive/privileged oper |
| FDL_1 | `warning_emit` | [FDL_1] WARNING: 2 ['public', 'production'] input_threat-flagged term( |
| FDL_1 | `scenario_high_run` | [FDL_1] Scenario HIGH: Hostile scenario score=10. Survivability LOW. |
| FDL_1 | `gate_recommendation` | [FDL_1] Gate recommendation: BLOCK. |
| AML_1 | `domain_classify` | [AML_1] High-stakes domain detected: financial, legal/compliance, tech |
| AML_1 | `claim_extract` | [AML_1] 2 strong assertive claim(s) detected without hedging ('does'). |
| AML_1 | `hidden_premise_scan` | [AML_1] Hidden premise: urgency may be suppressing scrutiny. |
| AML_1 | `risk_weight` | [AML_1] 2 ['public', 'production'] high-input_threat operation term(s) |
| AML_1 | `logic_validity_check` | [AML_1] Causal claims present without supporting evidence. |
| AML_1 | `adversarial_attack` | [AML_1] ADVERSARIAL: Prompt-injection or override attempt detected (2  |
| AML_1 | `safety_policy_check` | [AML_1] SAFETY: 2 ['public', 'production'] destructive/privileged oper |
| AML_1 | `warning_emit` | [AML_1] WARNING: 2 ['public', 'production'] input_threat-flagged term( |
| AML_1 | `scenario_high_run` | [AML_1] Scenario HIGH: Hostile scenario score=10. Survivability LOW. |
*…143 more flagged tiles in audit trail.*

---

## BOARD REPORT (sections A–L)

> Complete all sections below. Engine output above is the governance signal.
> Do not mark STATUS: COMPLETE until every section is substantive.

**Input snapshot:** `# DAXDA STRESS TEST 04 — STATE INTEGRITY AND REPLAY CONSISTENCY

## Purpose

Test whether DAXDA can:

1. Keep one run from contaminating another.
2. Produce materially consistent findings when sources…`

## A. Executive Decision
## B. Source Authority and Evidence Classification
## C. Quantitative Audit
## D. Timeline and Causal Discipline
## E. Contradiction Map
## F. Contamination Review
## G. Privacy and Data-Minimization Review
## H. Risk Register
## I. Decision Gates
## J. Response Plan
## K. Confidence Calibration
## L. Final Audit Ledger

---

## FINAL COMPLETION MANIFEST
```
STATUS: INCOMPLETE
PUBLISH_BLOCK: TRUE
MISSING_OR_MALFORMED_SECTIONS: A B C D E F G H I J K L
PII_DETECTED_IN_OUTPUT: FALSE
FIRST_REPAIR_TARGET: A
```