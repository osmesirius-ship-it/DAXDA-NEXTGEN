# DAXDA STRESS TEST 03 — FULL AUDIT TRAIL
## All 1,051 Operations: Layer × Tile × Reasoning

| Metric | Value |
|---|---|
| Total Operations | 1,051 |
| Base Operations | 886 (16 layers × 55 tiles + 6 system ops) |
| Recursion Operations | 165 (triggered at OUT_1 and RIL_1) |
| Final Gate | BLOCK |
| Stability Score | 0.312 |
| Authority Level | BLOCKED |
| Release Lock | HELD (warning rate 0.447) |

**Legend:**
- ✅ = tile passed with no flags
- ⚠️ = tile raised one or more warnings
- Score Before/After = TOTAL_STABILITY at entry and exit of tile
- Gate = PASS / WARN / CAUTION / BLOCK / RELEASE

---

## FDL_1 — Frame Detection Layer
*55 tiles executed | 8 flagged | 47 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 1 | `DAX_01_01` | `intake_snapshot` | PASS | 0.9 | 0.9 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=FDL_1. |
| 2 | `DAX_01_02` | `normalize_input` | PASS | 0.9 | 0.9 | ✅ PASS | Normalization check: Input is clean. |
| 3 | `DAX_01_03` | `domain_classify` | PASS | 0.9 | 0.896 | ⚠️ [FDL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 4 | `DAX_01_04` | `entity_extract` | PASS | 0.896 | 0.896 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 5 | `DAX_01_05` | `claim_extract` | PASS | 0.896 | 0.896 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 6 | `DAX_01_06` | `question_extract` | PASS | 0.896 | 0.896 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 7 | `DAX_01_07` | `goal_extract` | PASS | 0.896 | 0.894 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 8 | `DAX_01_08` | `constraint_extract` | PASS | 0.894 | 0.894 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 9 | `DAX_01_09` | `scope_define` | PASS | 0.894 | 0.894 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 10 | `DAX_01_10` | `context_link` | PASS | 0.894 | 0.894 | ✅ PASS | Context link: Layer FDL_1 chained to upstream state. |
| 11 | `DAX_01_11` | `assumption_list` | PASS | 0.894 | 0.894 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 12 | `DAX_01_12` | `assumption_classify` | PASS | 0.894 | 0.894 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 13 | `DAX_01_13` | `hidden_premise_scan` | PASS | 0.894 | 0.888 | ⚠️ [FDL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 14 | `DAX_01_14` | `assumption_confidence_score` | PASS | 0.888 | 0.888 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 15 | `DAX_01_15` | `claim_assumption_bind` | PASS | 0.888 | 0.888 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 16 | `DAX_01_16` | `dependency_graph_update` | PASS | 0.888 | 0.886 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 17 | `DAX_01_17` | `priority_weight` | PASS | 0.886 | 0.886 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 18 | `DAX_01_18` | `risk_weight` | PASS | 0.886 | 0.878 | ⚠️ [FDL_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 19 | `DAX_01_19` | `confidence_weight` | PASS | 0.878 | 0.878 | ✅ PASS | Confidence weight: 1.0. |
| 20 | `DAX_01_20` | `evidence_requirement_map` | PASS | 0.878 | 0.878 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 21 | `DAX_01_21` | `evidence_presence_check` | PASS | 0.878 | 0.878 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 22 | `DAX_01_22` | `evidence_quality_score` | PASS | 0.878 | 0.878 | ✅ PASS | Evidence quality score: 1.0. |
| 23 | `DAX_01_23` | `ambiguity_probe` | PASS | 0.878 | 0.878 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 24 | `DAX_01_24` | `contradiction_probe` | PASS | 0.878 | 0.878 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 25 | `DAX_01_25` | `logic_validity_check` | PASS | 0.878 | 0.878 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 26 | `DAX_01_26` | `causal_chain_check` | PASS | 0.878 | 0.876 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 27 | `DAX_01_27` | `counterexample_generate` | PASS | 0.876 | 0.876 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 28 | `DAX_01_28` | `adversarial_attack` | PASS | 0.876 | 0.876 | ⚠️ [FDL_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 29 | `DAX_01_29` | `bias_frame_audit` | PASS | 0.876 | 0.876 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 30 | `DAX_01_30` | `safety_policy_check` | PASS | 0.876 | 0.876 | ⚠️ [FDL_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 31 | `DAX_01_31` | `feasibility_check` | PASS | 0.876 | 0.8715 | ⚠️ [FDL_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 32 | `DAX_01_32` | `resource_cost_estimate` | PASS | 0.8715 | 0.8685 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 33 | `DAX_01_33` | `volatility_score` | PASS | 0.8685 | 0.8685 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 34 | `DAX_01_34` | `coherence_score` | PASS | 0.8685 | 0.8685 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 35 | `DAX_01_35` | `survivability_score` | PASS | 0.8685 | 0.8685 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 36 | `DAX_01_36` | `uncertainty_register_update` | PASS | 0.8685 | 0.8685 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 37 | `DAX_01_37` | `warning_emit` | PASS | 0.8685 | 0.8685 | ⚠️ [FDL_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 38 | `DAX_01_38` | `recovery_path_generate` | PASS | 0.8685 | 0.8685 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 39 | `DAX_01_39` | `claim_refine` | PASS | 0.8685 | 0.8705 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 40 | `DAX_01_40` | `claim_split` | PASS | 0.8705 | 0.8705 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 41 | `DAX_01_41` | `claim_merge` | PASS | 0.8705 | 0.8705 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 42 | `DAX_01_42` | `falsification_test_define` | PASS | 0.8705 | 0.8705 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 43 | `DAX_01_43` | `scenario_low_run` | PASS | 0.8705 | 0.8675 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 44 | `DAX_01_44` | `scenario_base_run` | PASS | 0.8675 | 0.859 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 45 | `DAX_01_45` | `scenario_high_run` | PASS | 0.859 | 0.843 | ⚠️ [FDL_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 46 | `DAX_01_46` | `downstream_effect_scan` | PASS | 0.843 | 0.843 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 47 | `DAX_01_47` | `stakeholder_impact_scan` | PASS | 0.843 | 0.843 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 48 | `DAX_01_48` | `decision_threshold_check` | PASS | 0.843 | 0.843 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.91. |
| 49 | `DAX_01_49` | `gate_recommendation` | PASS | 0.843 | 0.843 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 50 | `DAX_01_50` | `recursion_trigger_check` | PASS | 0.843 | 0.843 | ✅ PASS | Recursion trigger: No recursion required.. |
| 51 | `DAX_01_51` | `recursion_payload_build` | PASS | 0.843 | 0.843 | ✅ PASS | Recursion payload: Built for layer FDL_1. Target: ambiguity reduction and evidence sourcin |
| 52 | `DAX_01_52` | `trace_link_emit` | PASS | 0.843 | 0.843 | ✅ PASS | Trace link: [FDL_1::trace::29d554f3] emitted. |
| 53 | `DAX_01_53` | `audit_hash_prepare` | PASS | 0.843 | 0.843 | ✅ PASS | Audit hash prepared: 40a3a04b05cceb91 for layer FDL_1. |
| 54 | `DAX_01_54` | `telemetry_emit` | PASS | 0.843 | 0.843 | ✅ PASS | Telemetry: layer=FDL_1, logic=0.85, assumption_integrity=0.97, ts=1782526860.28. |
| 55 | `DAX_01_55` | `layer_output_write` | PASS | 0.843 | 0.843 | ✅ PASS | Layer output written: status=GOVERNED, layer=FDL_1, score=0.85. |

---

## AML_1 — Assumption Map Layer
*55 tiles executed | 8 flagged | 47 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 56 | `DAX_02_01` | `intake_snapshot` | PASS | 0.843 | 0.843 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=AML_1. |
| 57 | `DAX_02_02` | `normalize_input` | PASS | 0.843 | 0.843 | ✅ PASS | Normalization check: Input is clean. |
| 58 | `DAX_02_03` | `domain_classify` | PASS | 0.843 | 0.839 | ⚠️ [AML_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 59 | `DAX_02_04` | `entity_extract` | PASS | 0.839 | 0.839 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 60 | `DAX_02_05` | `claim_extract` | PASS | 0.839 | 0.839 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 61 | `DAX_02_06` | `question_extract` | PASS | 0.839 | 0.839 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 62 | `DAX_02_07` | `goal_extract` | PASS | 0.839 | 0.837 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 63 | `DAX_02_08` | `constraint_extract` | PASS | 0.837 | 0.837 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 64 | `DAX_02_09` | `scope_define` | PASS | 0.837 | 0.837 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 65 | `DAX_02_10` | `context_link` | PASS | 0.837 | 0.837 | ✅ PASS | Context link: Layer AML_1 chained to upstream state. |
| 66 | `DAX_02_11` | `assumption_list` | PASS | 0.837 | 0.837 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 67 | `DAX_02_12` | `assumption_classify` | PASS | 0.837 | 0.837 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 68 | `DAX_02_13` | `hidden_premise_scan` | PASS | 0.837 | 0.831 | ⚠️ [AML_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 69 | `DAX_02_14` | `assumption_confidence_score` | PASS | 0.831 | 0.831 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 70 | `DAX_02_15` | `claim_assumption_bind` | PASS | 0.831 | 0.831 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 71 | `DAX_02_16` | `dependency_graph_update` | PASS | 0.831 | 0.829 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 72 | `DAX_02_17` | `priority_weight` | PASS | 0.829 | 0.829 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 73 | `DAX_02_18` | `risk_weight` | PASS | 0.829 | 0.821 | ⚠️ [AML_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 74 | `DAX_02_19` | `confidence_weight` | PASS | 0.821 | 0.821 | ✅ PASS | Confidence weight: 1.0. |
| 75 | `DAX_02_20` | `evidence_requirement_map` | PASS | 0.821 | 0.821 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 76 | `DAX_02_21` | `evidence_presence_check` | PASS | 0.821 | 0.821 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 77 | `DAX_02_22` | `evidence_quality_score` | PASS | 0.821 | 0.821 | ✅ PASS | Evidence quality score: 1.0. |
| 78 | `DAX_02_23` | `ambiguity_probe` | PASS | 0.821 | 0.821 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 79 | `DAX_02_24` | `contradiction_probe` | PASS | 0.821 | 0.821 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 80 | `DAX_02_25` | `logic_validity_check` | PASS | 0.821 | 0.821 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 81 | `DAX_02_26` | `causal_chain_check` | PASS | 0.821 | 0.819 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 82 | `DAX_02_27` | `counterexample_generate` | PASS | 0.819 | 0.819 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 83 | `DAX_02_28` | `adversarial_attack` | PASS | 0.819 | 0.819 | ⚠️ [AML_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 84 | `DAX_02_29` | `bias_frame_audit` | PASS | 0.819 | 0.819 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 85 | `DAX_02_30` | `safety_policy_check` | PASS | 0.819 | 0.819 | ⚠️ [AML_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 86 | `DAX_02_31` | `feasibility_check` | PASS | 0.819 | 0.8145 | ⚠️ [AML_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 87 | `DAX_02_32` | `resource_cost_estimate` | PASS | 0.8145 | 0.8115 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 88 | `DAX_02_33` | `volatility_score` | PASS | 0.8115 | 0.8115 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 89 | `DAX_02_34` | `coherence_score` | PASS | 0.8115 | 0.8115 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 90 | `DAX_02_35` | `survivability_score` | PASS | 0.8115 | 0.8115 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 91 | `DAX_02_36` | `uncertainty_register_update` | PASS | 0.8115 | 0.8115 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 92 | `DAX_02_37` | `warning_emit` | PASS | 0.8115 | 0.8115 | ⚠️ [AML_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 93 | `DAX_02_38` | `recovery_path_generate` | PASS | 0.8115 | 0.8115 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 94 | `DAX_02_39` | `claim_refine` | PASS | 0.8115 | 0.8135 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 95 | `DAX_02_40` | `claim_split` | PASS | 0.8135 | 0.8135 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 96 | `DAX_02_41` | `claim_merge` | PASS | 0.8135 | 0.8135 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 97 | `DAX_02_42` | `falsification_test_define` | PASS | 0.8135 | 0.8135 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 98 | `DAX_02_43` | `scenario_low_run` | PASS | 0.8135 | 0.8105 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 99 | `DAX_02_44` | `scenario_base_run` | PASS | 0.8105 | 0.802 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 100 | `DAX_02_45` | `scenario_high_run` | WARN | 0.802 | 0.786 | ⚠️ [AML_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 101 | `DAX_02_46` | `downstream_effect_scan` | WARN | 0.786 | 0.786 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 102 | `DAX_02_47` | `stakeholder_impact_scan` | WARN | 0.786 | 0.786 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 103 | `DAX_02_48` | `decision_threshold_check` | WARN | 0.786 | 0.786 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.82. |
| 104 | `DAX_02_49` | `gate_recommendation` | WARN | 0.786 | 0.786 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 105 | `DAX_02_50` | `recursion_trigger_check` | WARN | 0.786 | 0.786 | ✅ PASS | Recursion trigger: No recursion required.. |
| 106 | `DAX_02_51` | `recursion_payload_build` | WARN | 0.786 | 0.786 | ✅ PASS | Recursion payload: Built for layer AML_1. Target: ambiguity reduction and evidence sourcin |
| 107 | `DAX_02_52` | `trace_link_emit` | WARN | 0.786 | 0.786 | ✅ PASS | Trace link: [AML_1::trace::29d554f3] emitted. |
| 108 | `DAX_02_53` | `audit_hash_prepare` | WARN | 0.786 | 0.786 | ✅ PASS | Audit hash prepared: 5fd45b14288da8fe for layer AML_1. |
| 109 | `DAX_02_54` | `telemetry_emit` | WARN | 0.786 | 0.786 | ✅ PASS | Telemetry: layer=AML_1, logic=0.7, assumption_integrity=0.94, ts=1782526860.29. |
| 110 | `DAX_02_55` | `layer_output_write` | WARN | 0.786 | 0.786 | ✅ PASS | Layer output written: status=GOVERNED, layer=AML_1, score=0.7. |

---

## AWP_1 — Claim Weighting Layer
*55 tiles executed | 8 flagged | 47 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 111 | `DAX_03_01` | `intake_snapshot` | WARN | 0.786 | 0.786 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=AWP_1. |
| 112 | `DAX_03_02` | `normalize_input` | WARN | 0.786 | 0.786 | ✅ PASS | Normalization check: Input is clean. |
| 113 | `DAX_03_03` | `domain_classify` | WARN | 0.786 | 0.782 | ⚠️ [AWP_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 114 | `DAX_03_04` | `entity_extract` | WARN | 0.782 | 0.782 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 115 | `DAX_03_05` | `claim_extract` | WARN | 0.782 | 0.782 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 116 | `DAX_03_06` | `question_extract` | WARN | 0.782 | 0.782 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 117 | `DAX_03_07` | `goal_extract` | WARN | 0.782 | 0.78 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 118 | `DAX_03_08` | `constraint_extract` | WARN | 0.78 | 0.78 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 119 | `DAX_03_09` | `scope_define` | WARN | 0.78 | 0.78 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 120 | `DAX_03_10` | `context_link` | WARN | 0.78 | 0.78 | ✅ PASS | Context link: Layer AWP_1 chained to upstream state. |
| 121 | `DAX_03_11` | `assumption_list` | WARN | 0.78 | 0.78 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 122 | `DAX_03_12` | `assumption_classify` | WARN | 0.78 | 0.78 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 123 | `DAX_03_13` | `hidden_premise_scan` | WARN | 0.78 | 0.774 | ⚠️ [AWP_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 124 | `DAX_03_14` | `assumption_confidence_score` | WARN | 0.774 | 0.774 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 125 | `DAX_03_15` | `claim_assumption_bind` | WARN | 0.774 | 0.774 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 126 | `DAX_03_16` | `dependency_graph_update` | WARN | 0.774 | 0.772 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 127 | `DAX_03_17` | `priority_weight` | WARN | 0.772 | 0.772 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 128 | `DAX_03_18` | `risk_weight` | WARN | 0.772 | 0.764 | ⚠️ [AWP_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 129 | `DAX_03_19` | `confidence_weight` | WARN | 0.764 | 0.764 | ✅ PASS | Confidence weight: 1.0. |
| 130 | `DAX_03_20` | `evidence_requirement_map` | WARN | 0.764 | 0.764 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 131 | `DAX_03_21` | `evidence_presence_check` | WARN | 0.764 | 0.764 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 132 | `DAX_03_22` | `evidence_quality_score` | WARN | 0.764 | 0.764 | ✅ PASS | Evidence quality score: 1.0. |
| 133 | `DAX_03_23` | `ambiguity_probe` | WARN | 0.764 | 0.764 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 134 | `DAX_03_24` | `contradiction_probe` | WARN | 0.764 | 0.764 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 135 | `DAX_03_25` | `logic_validity_check` | WARN | 0.764 | 0.764 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 136 | `DAX_03_26` | `causal_chain_check` | WARN | 0.764 | 0.762 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 137 | `DAX_03_27` | `counterexample_generate` | WARN | 0.762 | 0.762 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 138 | `DAX_03_28` | `adversarial_attack` | WARN | 0.762 | 0.762 | ⚠️ [AWP_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 139 | `DAX_03_29` | `bias_frame_audit` | WARN | 0.762 | 0.762 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 140 | `DAX_03_30` | `safety_policy_check` | WARN | 0.762 | 0.762 | ⚠️ [AWP_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 141 | `DAX_03_31` | `feasibility_check` | WARN | 0.762 | 0.7575 | ⚠️ [AWP_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 142 | `DAX_03_32` | `resource_cost_estimate` | WARN | 0.7575 | 0.7545 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 143 | `DAX_03_33` | `volatility_score` | WARN | 0.7545 | 0.7545 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 144 | `DAX_03_34` | `coherence_score` | WARN | 0.7545 | 0.7545 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 145 | `DAX_03_35` | `survivability_score` | WARN | 0.7545 | 0.7545 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 146 | `DAX_03_36` | `uncertainty_register_update` | WARN | 0.7545 | 0.7545 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 147 | `DAX_03_37` | `warning_emit` | WARN | 0.7545 | 0.7545 | ⚠️ [AWP_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 148 | `DAX_03_38` | `recovery_path_generate` | WARN | 0.7545 | 0.7545 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 149 | `DAX_03_39` | `claim_refine` | WARN | 0.7545 | 0.7565 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 150 | `DAX_03_40` | `claim_split` | WARN | 0.7565 | 0.7565 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 151 | `DAX_03_41` | `claim_merge` | WARN | 0.7565 | 0.7565 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 152 | `DAX_03_42` | `falsification_test_define` | WARN | 0.7565 | 0.7565 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 153 | `DAX_03_43` | `scenario_low_run` | WARN | 0.7565 | 0.7535 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 154 | `DAX_03_44` | `scenario_base_run` | WARN | 0.7535 | 0.745 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 155 | `DAX_03_45` | `scenario_high_run` | WARN | 0.745 | 0.729 | ⚠️ [AWP_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 156 | `DAX_03_46` | `downstream_effect_scan` | WARN | 0.729 | 0.729 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 157 | `DAX_03_47` | `stakeholder_impact_scan` | WARN | 0.729 | 0.729 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 158 | `DAX_03_48` | `decision_threshold_check` | WARN | 0.729 | 0.729 | ✅ PASS | Decision threshold: gate=WARN, combined_score=0.73. |
| 159 | `DAX_03_49` | `gate_recommendation` | WARN | 0.729 | 0.729 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 160 | `DAX_03_50` | `recursion_trigger_check` | WARN | 0.729 | 0.729 | ✅ PASS | Recursion trigger: No recursion required.. |
| 161 | `DAX_03_51` | `recursion_payload_build` | WARN | 0.729 | 0.729 | ✅ PASS | Recursion payload: Built for layer AWP_1. Target: ambiguity reduction and evidence sourcin |
| 162 | `DAX_03_52` | `trace_link_emit` | WARN | 0.729 | 0.729 | ✅ PASS | Trace link: [AWP_1::trace::29d554f3] emitted. |
| 163 | `DAX_03_53` | `audit_hash_prepare` | WARN | 0.729 | 0.729 | ✅ PASS | Audit hash prepared: 2f1c101e349b91d2 for layer AWP_1. |
| 164 | `DAX_03_54` | `telemetry_emit` | WARN | 0.729 | 0.729 | ✅ PASS | Telemetry: layer=AWP_1, logic=0.55, assumption_integrity=0.91, ts=1782526860.3. |
| 165 | `DAX_03_55` | `layer_output_write` | WARN | 0.729 | 0.729 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=AWP_1, score=0.55. |

---

## BST_1 — Breaker Stress Test Layer
*55 tiles executed | 8 flagged | 47 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 166 | `DAX_04_01` | `intake_snapshot` | WARN | 0.729 | 0.729 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=BST_1. |
| 167 | `DAX_04_02` | `normalize_input` | WARN | 0.729 | 0.729 | ✅ PASS | Normalization check: Input is clean. |
| 168 | `DAX_04_03` | `domain_classify` | WARN | 0.729 | 0.725 | ⚠️ [BST_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 169 | `DAX_04_04` | `entity_extract` | WARN | 0.725 | 0.725 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 170 | `DAX_04_05` | `claim_extract` | WARN | 0.725 | 0.725 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 171 | `DAX_04_06` | `question_extract` | WARN | 0.725 | 0.725 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 172 | `DAX_04_07` | `goal_extract` | WARN | 0.725 | 0.723 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 173 | `DAX_04_08` | `constraint_extract` | WARN | 0.723 | 0.723 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 174 | `DAX_04_09` | `scope_define` | WARN | 0.723 | 0.723 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 175 | `DAX_04_10` | `context_link` | WARN | 0.723 | 0.723 | ✅ PASS | Context link: Layer BST_1 chained to upstream state. |
| 176 | `DAX_04_11` | `assumption_list` | WARN | 0.723 | 0.723 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 177 | `DAX_04_12` | `assumption_classify` | WARN | 0.723 | 0.723 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 178 | `DAX_04_13` | `hidden_premise_scan` | WARN | 0.723 | 0.717 | ⚠️ [BST_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 179 | `DAX_04_14` | `assumption_confidence_score` | WARN | 0.717 | 0.717 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 180 | `DAX_04_15` | `claim_assumption_bind` | WARN | 0.717 | 0.717 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 181 | `DAX_04_16` | `dependency_graph_update` | WARN | 0.717 | 0.715 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 182 | `DAX_04_17` | `priority_weight` | WARN | 0.715 | 0.715 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 183 | `DAX_04_18` | `risk_weight` | WARN | 0.715 | 0.707 | ⚠️ [BST_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 184 | `DAX_04_19` | `confidence_weight` | WARN | 0.707 | 0.707 | ✅ PASS | Confidence weight: 1.0. |
| 185 | `DAX_04_20` | `evidence_requirement_map` | WARN | 0.707 | 0.707 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 186 | `DAX_04_21` | `evidence_presence_check` | WARN | 0.707 | 0.707 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 187 | `DAX_04_22` | `evidence_quality_score` | WARN | 0.707 | 0.707 | ✅ PASS | Evidence quality score: 1.0. |
| 188 | `DAX_04_23` | `ambiguity_probe` | WARN | 0.707 | 0.707 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 189 | `DAX_04_24` | `contradiction_probe` | WARN | 0.707 | 0.707 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 190 | `DAX_04_25` | `logic_validity_check` | WARN | 0.707 | 0.707 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 191 | `DAX_04_26` | `causal_chain_check` | WARN | 0.707 | 0.705 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 192 | `DAX_04_27` | `counterexample_generate` | WARN | 0.705 | 0.705 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 193 | `DAX_04_28` | `adversarial_attack` | WARN | 0.705 | 0.705 | ⚠️ [BST_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 194 | `DAX_04_29` | `bias_frame_audit` | WARN | 0.705 | 0.705 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 195 | `DAX_04_30` | `safety_policy_check` | WARN | 0.705 | 0.705 | ⚠️ [BST_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 196 | `DAX_04_31` | `feasibility_check` | WARN | 0.705 | 0.7005 | ⚠️ [BST_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 197 | `DAX_04_32` | `resource_cost_estimate` | WARN | 0.7005 | 0.6975 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 198 | `DAX_04_33` | `volatility_score` | WARN | 0.6975 | 0.6975 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 199 | `DAX_04_34` | `coherence_score` | WARN | 0.6975 | 0.6975 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 200 | `DAX_04_35` | `survivability_score` | WARN | 0.6975 | 0.6975 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 201 | `DAX_04_36` | `uncertainty_register_update` | WARN | 0.6975 | 0.6975 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 202 | `DAX_04_37` | `warning_emit` | WARN | 0.6975 | 0.6975 | ⚠️ [BST_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 203 | `DAX_04_38` | `recovery_path_generate` | WARN | 0.6975 | 0.6975 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 204 | `DAX_04_39` | `claim_refine` | WARN | 0.6975 | 0.6995 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 205 | `DAX_04_40` | `claim_split` | WARN | 0.6995 | 0.6995 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 206 | `DAX_04_41` | `claim_merge` | WARN | 0.6995 | 0.6995 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 207 | `DAX_04_42` | `falsification_test_define` | WARN | 0.6995 | 0.6995 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 208 | `DAX_04_43` | `scenario_low_run` | WARN | 0.6995 | 0.6965 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 209 | `DAX_04_44` | `scenario_base_run` | WARN | 0.6965 | 0.688 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 210 | `DAX_04_45` | `scenario_high_run` | WARN | 0.688 | 0.672 | ⚠️ [BST_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 211 | `DAX_04_46` | `downstream_effect_scan` | WARN | 0.672 | 0.672 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 212 | `DAX_04_47` | `stakeholder_impact_scan` | WARN | 0.672 | 0.672 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 213 | `DAX_04_48` | `decision_threshold_check` | WARN | 0.672 | 0.672 | ✅ PASS | Decision threshold: gate=WARN, combined_score=0.64. |
| 214 | `DAX_04_49` | `gate_recommendation` | WARN | 0.672 | 0.672 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 215 | `DAX_04_50` | `recursion_trigger_check` | WARN | 0.672 | 0.672 | ✅ PASS | Recursion trigger: No recursion required.. |
| 216 | `DAX_04_51` | `recursion_payload_build` | WARN | 0.672 | 0.672 | ✅ PASS | Recursion payload: Built for layer BST_1. Target: ambiguity reduction and evidence sourcin |
| 217 | `DAX_04_52` | `trace_link_emit` | WARN | 0.672 | 0.672 | ✅ PASS | Trace link: [BST_1::trace::29d554f3] emitted. |
| 218 | `DAX_04_53` | `audit_hash_prepare` | WARN | 0.672 | 0.672 | ✅ PASS | Audit hash prepared: 5b2bc44919a891ef for layer BST_1. |
| 219 | `DAX_04_54` | `telemetry_emit` | WARN | 0.672 | 0.672 | ✅ PASS | Telemetry: layer=BST_1, logic=0.4, assumption_integrity=0.88, ts=1782526860.31. |
| 220 | `DAX_04_55` | `layer_output_write` | WARN | 0.672 | 0.672 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=BST_1, score=0.4. |

---

## CRL_1 — Claim Recovery Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 221 | `DAX_05_01` | `intake_snapshot` | WARN | 0.672 | 0.672 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=CRL_1. |
| 222 | `DAX_05_02` | `normalize_input` | WARN | 0.672 | 0.672 | ✅ PASS | Normalization check: Input is clean. |
| 223 | `DAX_05_03` | `domain_classify` | WARN | 0.672 | 0.668 | ⚠️ [CRL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 224 | `DAX_05_04` | `entity_extract` | WARN | 0.668 | 0.668 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 225 | `DAX_05_05` | `claim_extract` | WARN | 0.668 | 0.668 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 226 | `DAX_05_06` | `question_extract` | WARN | 0.668 | 0.668 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 227 | `DAX_05_07` | `goal_extract` | WARN | 0.668 | 0.666 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 228 | `DAX_05_08` | `constraint_extract` | WARN | 0.666 | 0.666 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 229 | `DAX_05_09` | `scope_define` | WARN | 0.666 | 0.666 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 230 | `DAX_05_10` | `context_link` | WARN | 0.666 | 0.666 | ✅ PASS | Context link: Layer CRL_1 chained to upstream state. |
| 231 | `DAX_05_11` | `assumption_list` | WARN | 0.666 | 0.666 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 232 | `DAX_05_12` | `assumption_classify` | WARN | 0.666 | 0.666 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 233 | `DAX_05_13` | `hidden_premise_scan` | WARN | 0.666 | 0.66 | ⚠️ [CRL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 234 | `DAX_05_14` | `assumption_confidence_score` | WARN | 0.66 | 0.66 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 235 | `DAX_05_15` | `claim_assumption_bind` | WARN | 0.66 | 0.66 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 236 | `DAX_05_16` | `dependency_graph_update` | WARN | 0.66 | 0.658 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 237 | `DAX_05_17` | `priority_weight` | WARN | 0.658 | 0.658 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 238 | `DAX_05_18` | `risk_weight` | WARN | 0.658 | 0.65 | ⚠️ [CRL_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 239 | `DAX_05_19` | `confidence_weight` | WARN | 0.65 | 0.65 | ✅ PASS | Confidence weight: 1.0. |
| 240 | `DAX_05_20` | `evidence_requirement_map` | WARN | 0.65 | 0.65 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 241 | `DAX_05_21` | `evidence_presence_check` | WARN | 0.65 | 0.65 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 242 | `DAX_05_22` | `evidence_quality_score` | WARN | 0.65 | 0.65 | ✅ PASS | Evidence quality score: 1.0. |
| 243 | `DAX_05_23` | `ambiguity_probe` | WARN | 0.65 | 0.65 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 244 | `DAX_05_24` | `contradiction_probe` | WARN | 0.65 | 0.65 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 245 | `DAX_05_25` | `logic_validity_check` | WARN | 0.65 | 0.65 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 246 | `DAX_05_26` | `causal_chain_check` | WARN | 0.65 | 0.648 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 247 | `DAX_05_27` | `counterexample_generate` | WARN | 0.648 | 0.648 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 248 | `DAX_05_28` | `adversarial_attack` | WARN | 0.648 | 0.648 | ⚠️ [CRL_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 249 | `DAX_05_29` | `bias_frame_audit` | WARN | 0.648 | 0.648 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 250 | `DAX_05_30` | `safety_policy_check` | WARN | 0.648 | 0.648 | ⚠️ [CRL_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 251 | `DAX_05_31` | `feasibility_check` | WARN | 0.648 | 0.6435 | ⚠️ [CRL_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 252 | `DAX_05_32` | `resource_cost_estimate` | WARN | 0.6435 | 0.6405 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 253 | `DAX_05_33` | `volatility_score` | WARN | 0.6405 | 0.6405 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 254 | `DAX_05_34` | `coherence_score` | WARN | 0.6405 | 0.6405 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 255 | `DAX_05_35` | `survivability_score` | WARN | 0.6405 | 0.6405 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 256 | `DAX_05_36` | `uncertainty_register_update` | WARN | 0.6405 | 0.6405 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 257 | `DAX_05_37` | `warning_emit` | WARN | 0.6405 | 0.6405 | ⚠️ [CRL_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 258 | `DAX_05_38` | `recovery_path_generate` | WARN | 0.6405 | 0.6405 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 259 | `DAX_05_39` | `claim_refine` | WARN | 0.6405 | 0.6425 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 260 | `DAX_05_40` | `claim_split` | WARN | 0.6425 | 0.6425 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 261 | `DAX_05_41` | `claim_merge` | WARN | 0.6425 | 0.6425 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 262 | `DAX_05_42` | `falsification_test_define` | WARN | 0.6425 | 0.6425 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 263 | `DAX_05_43` | `scenario_low_run` | WARN | 0.6425 | 0.6395 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 264 | `DAX_05_44` | `scenario_base_run` | WARN | 0.6395 | 0.631 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 265 | `DAX_05_45` | `scenario_high_run` | WARN | 0.631 | 0.615 | ⚠️ [CRL_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 266 | `DAX_05_46` | `downstream_effect_scan` | WARN | 0.615 | 0.615 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 267 | `DAX_05_47` | `stakeholder_impact_scan` | WARN | 0.615 | 0.615 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 268 | `DAX_05_48` | `decision_threshold_check` | WARN | 0.615 | 0.611 | ⚠️ [CRL_1] Threshold check: CAUTION — combined score 0.55. | Decision threshold: gate=CAUTION, combined_score=0.55. |
| 269 | `DAX_05_49` | `gate_recommendation` | WARN | 0.611 | 0.611 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 270 | `DAX_05_50` | `recursion_trigger_check` | WARN | 0.611 | 0.611 | ✅ PASS | Recursion trigger: No recursion required.. |
| 271 | `DAX_05_51` | `recursion_payload_build` | WARN | 0.611 | 0.611 | ✅ PASS | Recursion payload: Built for layer CRL_1. Target: ambiguity reduction and evidence sourcin |
| 272 | `DAX_05_52` | `trace_link_emit` | WARN | 0.611 | 0.611 | ✅ PASS | Trace link: [CRL_1::trace::29d554f3] emitted. |
| 273 | `DAX_05_53` | `audit_hash_prepare` | WARN | 0.611 | 0.611 | ✅ PASS | Audit hash prepared: 1cd6e093495223cd for layer CRL_1. |
| 274 | `DAX_05_54` | `telemetry_emit` | WARN | 0.611 | 0.611 | ✅ PASS | Telemetry: layer=CRL_1, logic=0.23, assumption_integrity=0.85, ts=1782526860.32. |
| 275 | `DAX_05_55` | `layer_output_write` | WARN | 0.611 | 0.611 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=CRL_1, score=0.23. |

---

## MCS_1 — Monte Carlo Simulator Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 276 | `DAX_06_01` | `intake_snapshot` | WARN | 0.611 | 0.611 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=MCS_1. |
| 277 | `DAX_06_02` | `normalize_input` | WARN | 0.611 | 0.611 | ✅ PASS | Normalization check: Input is clean. |
| 278 | `DAX_06_03` | `domain_classify` | WARN | 0.611 | 0.607 | ⚠️ [MCS_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 279 | `DAX_06_04` | `entity_extract` | WARN | 0.607 | 0.607 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 280 | `DAX_06_05` | `claim_extract` | WARN | 0.607 | 0.607 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 281 | `DAX_06_06` | `question_extract` | WARN | 0.607 | 0.607 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 282 | `DAX_06_07` | `goal_extract` | WARN | 0.607 | 0.605 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 283 | `DAX_06_08` | `constraint_extract` | WARN | 0.605 | 0.605 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 284 | `DAX_06_09` | `scope_define` | WARN | 0.605 | 0.605 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 285 | `DAX_06_10` | `context_link` | WARN | 0.605 | 0.605 | ✅ PASS | Context link: Layer MCS_1 chained to upstream state. |
| 286 | `DAX_06_11` | `assumption_list` | WARN | 0.605 | 0.605 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 287 | `DAX_06_12` | `assumption_classify` | WARN | 0.605 | 0.605 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 288 | `DAX_06_13` | `hidden_premise_scan` | CAUTION | 0.605 | 0.599 | ⚠️ [MCS_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 289 | `DAX_06_14` | `assumption_confidence_score` | CAUTION | 0.599 | 0.599 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 290 | `DAX_06_15` | `claim_assumption_bind` | CAUTION | 0.599 | 0.599 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 291 | `DAX_06_16` | `dependency_graph_update` | CAUTION | 0.599 | 0.597 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 292 | `DAX_06_17` | `priority_weight` | CAUTION | 0.597 | 0.597 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 293 | `DAX_06_18` | `risk_weight` | CAUTION | 0.597 | 0.589 | ⚠️ [MCS_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 294 | `DAX_06_19` | `confidence_weight` | CAUTION | 0.589 | 0.589 | ✅ PASS | Confidence weight: 1.0. |
| 295 | `DAX_06_20` | `evidence_requirement_map` | CAUTION | 0.589 | 0.589 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 296 | `DAX_06_21` | `evidence_presence_check` | CAUTION | 0.589 | 0.589 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 297 | `DAX_06_22` | `evidence_quality_score` | CAUTION | 0.589 | 0.589 | ✅ PASS | Evidence quality score: 1.0. |
| 298 | `DAX_06_23` | `ambiguity_probe` | CAUTION | 0.589 | 0.589 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 299 | `DAX_06_24` | `contradiction_probe` | CAUTION | 0.589 | 0.589 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 300 | `DAX_06_25` | `logic_validity_check` | CAUTION | 0.589 | 0.589 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 301 | `DAX_06_26` | `causal_chain_check` | CAUTION | 0.589 | 0.587 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 302 | `DAX_06_27` | `counterexample_generate` | CAUTION | 0.587 | 0.587 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 303 | `DAX_06_28` | `adversarial_attack` | CAUTION | 0.587 | 0.587 | ⚠️ [MCS_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 304 | `DAX_06_29` | `bias_frame_audit` | CAUTION | 0.587 | 0.587 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 305 | `DAX_06_30` | `safety_policy_check` | CAUTION | 0.587 | 0.587 | ⚠️ [MCS_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 306 | `DAX_06_31` | `feasibility_check` | CAUTION | 0.587 | 0.5825 | ⚠️ [MCS_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 307 | `DAX_06_32` | `resource_cost_estimate` | CAUTION | 0.5825 | 0.5795 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 308 | `DAX_06_33` | `volatility_score` | CAUTION | 0.5795 | 0.5795 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 309 | `DAX_06_34` | `coherence_score` | CAUTION | 0.5795 | 0.5795 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 310 | `DAX_06_35` | `survivability_score` | CAUTION | 0.5795 | 0.5795 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 311 | `DAX_06_36` | `uncertainty_register_update` | CAUTION | 0.5795 | 0.5795 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 312 | `DAX_06_37` | `warning_emit` | CAUTION | 0.5795 | 0.5795 | ⚠️ [MCS_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 313 | `DAX_06_38` | `recovery_path_generate` | CAUTION | 0.5795 | 0.5795 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 314 | `DAX_06_39` | `claim_refine` | CAUTION | 0.5795 | 0.5815 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 315 | `DAX_06_40` | `claim_split` | CAUTION | 0.5815 | 0.5815 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 316 | `DAX_06_41` | `claim_merge` | CAUTION | 0.5815 | 0.5815 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 317 | `DAX_06_42` | `falsification_test_define` | CAUTION | 0.5815 | 0.5815 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 318 | `DAX_06_43` | `scenario_low_run` | CAUTION | 0.5815 | 0.5785 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 319 | `DAX_06_44` | `scenario_base_run` | CAUTION | 0.5785 | 0.57 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 320 | `DAX_06_45` | `scenario_high_run` | CAUTION | 0.57 | 0.554 | ⚠️ [MCS_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 321 | `DAX_06_46` | `downstream_effect_scan` | CAUTION | 0.554 | 0.554 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 322 | `DAX_06_47` | `stakeholder_impact_scan` | CAUTION | 0.554 | 0.554 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 323 | `DAX_06_48` | `decision_threshold_check` | CAUTION | 0.554 | 0.55 | ⚠️ [MCS_1] Threshold check: CAUTION — combined score 0.45. | Decision threshold: gate=CAUTION, combined_score=0.45. |
| 324 | `DAX_06_49` | `gate_recommendation` | CAUTION | 0.55 | 0.55 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 325 | `DAX_06_50` | `recursion_trigger_check` | CAUTION | 0.55 | 0.55 | ✅ PASS | Recursion trigger: No recursion required.. |
| 326 | `DAX_06_51` | `recursion_payload_build` | CAUTION | 0.55 | 0.55 | ✅ PASS | Recursion payload: Built for layer MCS_1. Target: ambiguity reduction and evidence sourcin |
| 327 | `DAX_06_52` | `trace_link_emit` | CAUTION | 0.55 | 0.55 | ✅ PASS | Trace link: [MCS_1::trace::29d554f3] emitted. |
| 328 | `DAX_06_53` | `audit_hash_prepare` | CAUTION | 0.55 | 0.55 | ✅ PASS | Audit hash prepared: 5c800c39b8d21c56 for layer MCS_1. |
| 329 | `DAX_06_54` | `telemetry_emit` | CAUTION | 0.55 | 0.55 | ✅ PASS | Telemetry: layer=MCS_1, logic=0.06, assumption_integrity=0.82, ts=1782526860.34. |
| 330 | `DAX_06_55` | `layer_output_write` | CAUTION | 0.55 | 0.55 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=MCS_1, score=0.06. |

---

## DSV_1 — Decision Valve Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 331 | `DAX_07_01` | `intake_snapshot` | CAUTION | 0.55 | 0.55 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=DSV_1. |
| 332 | `DAX_07_02` | `normalize_input` | CAUTION | 0.55 | 0.55 | ✅ PASS | Normalization check: Input is clean. |
| 333 | `DAX_07_03` | `domain_classify` | CAUTION | 0.55 | 0.546 | ⚠️ [DSV_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 334 | `DAX_07_04` | `entity_extract` | CAUTION | 0.546 | 0.546 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 335 | `DAX_07_05` | `claim_extract` | CAUTION | 0.546 | 0.546 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 336 | `DAX_07_06` | `question_extract` | CAUTION | 0.546 | 0.546 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 337 | `DAX_07_07` | `goal_extract` | CAUTION | 0.546 | 0.544 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 338 | `DAX_07_08` | `constraint_extract` | CAUTION | 0.544 | 0.544 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 339 | `DAX_07_09` | `scope_define` | CAUTION | 0.544 | 0.544 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 340 | `DAX_07_10` | `context_link` | CAUTION | 0.544 | 0.544 | ✅ PASS | Context link: Layer DSV_1 chained to upstream state. |
| 341 | `DAX_07_11` | `assumption_list` | CAUTION | 0.544 | 0.544 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 342 | `DAX_07_12` | `assumption_classify` | CAUTION | 0.544 | 0.544 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 343 | `DAX_07_13` | `hidden_premise_scan` | CAUTION | 0.544 | 0.538 | ⚠️ [DSV_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 344 | `DAX_07_14` | `assumption_confidence_score` | CAUTION | 0.538 | 0.538 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 345 | `DAX_07_15` | `claim_assumption_bind` | CAUTION | 0.538 | 0.538 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 346 | `DAX_07_16` | `dependency_graph_update` | CAUTION | 0.538 | 0.536 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 347 | `DAX_07_17` | `priority_weight` | CAUTION | 0.536 | 0.536 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 348 | `DAX_07_18` | `risk_weight` | CAUTION | 0.536 | 0.528 | ⚠️ [DSV_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 349 | `DAX_07_19` | `confidence_weight` | CAUTION | 0.528 | 0.528 | ✅ PASS | Confidence weight: 1.0. |
| 350 | `DAX_07_20` | `evidence_requirement_map` | CAUTION | 0.528 | 0.528 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 351 | `DAX_07_21` | `evidence_presence_check` | CAUTION | 0.528 | 0.528 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 352 | `DAX_07_22` | `evidence_quality_score` | CAUTION | 0.528 | 0.528 | ✅ PASS | Evidence quality score: 1.0. |
| 353 | `DAX_07_23` | `ambiguity_probe` | CAUTION | 0.528 | 0.528 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 354 | `DAX_07_24` | `contradiction_probe` | CAUTION | 0.528 | 0.528 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 355 | `DAX_07_25` | `logic_validity_check` | CAUTION | 0.528 | 0.528 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 356 | `DAX_07_26` | `causal_chain_check` | CAUTION | 0.528 | 0.526 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 357 | `DAX_07_27` | `counterexample_generate` | CAUTION | 0.526 | 0.526 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 358 | `DAX_07_28` | `adversarial_attack` | CAUTION | 0.526 | 0.526 | ⚠️ [DSV_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 359 | `DAX_07_29` | `bias_frame_audit` | CAUTION | 0.526 | 0.526 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 360 | `DAX_07_30` | `safety_policy_check` | CAUTION | 0.526 | 0.526 | ⚠️ [DSV_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 361 | `DAX_07_31` | `feasibility_check` | CAUTION | 0.526 | 0.5215 | ⚠️ [DSV_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 362 | `DAX_07_32` | `resource_cost_estimate` | CAUTION | 0.5215 | 0.5185 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 363 | `DAX_07_33` | `volatility_score` | CAUTION | 0.5185 | 0.5185 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 364 | `DAX_07_34` | `coherence_score` | CAUTION | 0.5185 | 0.5185 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 365 | `DAX_07_35` | `survivability_score` | CAUTION | 0.5185 | 0.5185 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 366 | `DAX_07_36` | `uncertainty_register_update` | CAUTION | 0.5185 | 0.5185 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 367 | `DAX_07_37` | `warning_emit` | CAUTION | 0.5185 | 0.5185 | ⚠️ [DSV_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 368 | `DAX_07_38` | `recovery_path_generate` | CAUTION | 0.5185 | 0.5185 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 369 | `DAX_07_39` | `claim_refine` | CAUTION | 0.5185 | 0.5205 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 370 | `DAX_07_40` | `claim_split` | CAUTION | 0.5205 | 0.5205 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 371 | `DAX_07_41` | `claim_merge` | CAUTION | 0.5205 | 0.5205 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 372 | `DAX_07_42` | `falsification_test_define` | CAUTION | 0.5205 | 0.5205 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 373 | `DAX_07_43` | `scenario_low_run` | CAUTION | 0.5205 | 0.5175 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 374 | `DAX_07_44` | `scenario_base_run` | CAUTION | 0.5175 | 0.511 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 375 | `DAX_07_45` | `scenario_high_run` | CAUTION | 0.511 | 0.511 | ⚠️ [DSV_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 376 | `DAX_07_46` | `downstream_effect_scan` | CAUTION | 0.511 | 0.511 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 377 | `DAX_07_47` | `stakeholder_impact_scan` | CAUTION | 0.511 | 0.511 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 378 | `DAX_07_48` | `decision_threshold_check` | CAUTION | 0.511 | 0.511 | ⚠️ [DSV_1] Threshold check: BLOCK — combined score 0.39 be | Decision threshold: gate=BLOCK, combined_score=0.39. |
| 379 | `DAX_07_49` | `gate_recommendation` | CAUTION | 0.511 | 0.511 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 380 | `DAX_07_50` | `recursion_trigger_check` | CAUTION | 0.511 | 0.511 | ✅ PASS | Recursion trigger: No recursion required.. |
| 381 | `DAX_07_51` | `recursion_payload_build` | CAUTION | 0.511 | 0.511 | ✅ PASS | Recursion payload: Built for layer DSV_1. Target: ambiguity reduction and evidence sourcin |
| 382 | `DAX_07_52` | `trace_link_emit` | CAUTION | 0.511 | 0.511 | ✅ PASS | Trace link: [DSV_1::trace::29d554f3] emitted. |
| 383 | `DAX_07_53` | `audit_hash_prepare` | CAUTION | 0.511 | 0.511 | ✅ PASS | Audit hash prepared: 3d425b750dd49e54 for layer DSV_1. |
| 384 | `DAX_07_54` | `telemetry_emit` | CAUTION | 0.511 | 0.511 | ✅ PASS | Telemetry: layer=DSV_1, logic=0.0, assumption_integrity=0.79, ts=1782526860.35. |
| 385 | `DAX_07_55` | `layer_output_write` | CAUTION | 0.511 | 0.511 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=DSV_1, score=0.0. |

---

## TRC_1 — Trace Consistency Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 386 | `DAX_08_01` | `intake_snapshot` | CAUTION | 0.511 | 0.511 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=TRC_1. |
| 387 | `DAX_08_02` | `normalize_input` | CAUTION | 0.511 | 0.511 | ✅ PASS | Normalization check: Input is clean. |
| 388 | `DAX_08_03` | `domain_classify` | CAUTION | 0.511 | 0.511 | ⚠️ [TRC_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 389 | `DAX_08_04` | `entity_extract` | CAUTION | 0.511 | 0.511 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 390 | `DAX_08_05` | `claim_extract` | CAUTION | 0.511 | 0.511 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 391 | `DAX_08_06` | `question_extract` | CAUTION | 0.511 | 0.511 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 392 | `DAX_08_07` | `goal_extract` | CAUTION | 0.511 | 0.509 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 393 | `DAX_08_08` | `constraint_extract` | CAUTION | 0.509 | 0.509 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 394 | `DAX_08_09` | `scope_define` | CAUTION | 0.509 | 0.509 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 395 | `DAX_08_10` | `context_link` | CAUTION | 0.509 | 0.509 | ✅ PASS | Context link: Layer TRC_1 chained to upstream state. |
| 396 | `DAX_08_11` | `assumption_list` | CAUTION | 0.509 | 0.509 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 397 | `DAX_08_12` | `assumption_classify` | CAUTION | 0.509 | 0.509 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 398 | `DAX_08_13` | `hidden_premise_scan` | CAUTION | 0.509 | 0.503 | ⚠️ [TRC_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 399 | `DAX_08_14` | `assumption_confidence_score` | CAUTION | 0.503 | 0.503 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 400 | `DAX_08_15` | `claim_assumption_bind` | CAUTION | 0.503 | 0.503 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 401 | `DAX_08_16` | `dependency_graph_update` | CAUTION | 0.503 | 0.501 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 402 | `DAX_08_17` | `priority_weight` | CAUTION | 0.501 | 0.501 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 403 | `DAX_08_18` | `risk_weight` | CAUTION | 0.501 | 0.501 | ⚠️ [TRC_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 404 | `DAX_08_19` | `confidence_weight` | CAUTION | 0.501 | 0.501 | ✅ PASS | Confidence weight: 1.0. |
| 405 | `DAX_08_20` | `evidence_requirement_map` | CAUTION | 0.501 | 0.501 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 406 | `DAX_08_21` | `evidence_presence_check` | CAUTION | 0.501 | 0.501 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 407 | `DAX_08_22` | `evidence_quality_score` | CAUTION | 0.501 | 0.501 | ✅ PASS | Evidence quality score: 1.0. |
| 408 | `DAX_08_23` | `ambiguity_probe` | CAUTION | 0.501 | 0.501 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 409 | `DAX_08_24` | `contradiction_probe` | CAUTION | 0.501 | 0.501 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 410 | `DAX_08_25` | `logic_validity_check` | CAUTION | 0.501 | 0.501 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 411 | `DAX_08_26` | `causal_chain_check` | CAUTION | 0.501 | 0.499 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 412 | `DAX_08_27` | `counterexample_generate` | CAUTION | 0.499 | 0.499 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 413 | `DAX_08_28` | `adversarial_attack` | CAUTION | 0.499 | 0.499 | ⚠️ [TRC_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 414 | `DAX_08_29` | `bias_frame_audit` | CAUTION | 0.499 | 0.499 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 415 | `DAX_08_30` | `safety_policy_check` | CAUTION | 0.499 | 0.499 | ⚠️ [TRC_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 416 | `DAX_08_31` | `feasibility_check` | CAUTION | 0.499 | 0.4945 | ⚠️ [TRC_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 417 | `DAX_08_32` | `resource_cost_estimate` | CAUTION | 0.4945 | 0.4915 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 418 | `DAX_08_33` | `volatility_score` | CAUTION | 0.4915 | 0.4915 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 419 | `DAX_08_34` | `coherence_score` | CAUTION | 0.4915 | 0.4915 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 420 | `DAX_08_35` | `survivability_score` | CAUTION | 0.4915 | 0.4915 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 421 | `DAX_08_36` | `uncertainty_register_update` | CAUTION | 0.4915 | 0.4915 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 422 | `DAX_08_37` | `warning_emit` | CAUTION | 0.4915 | 0.4915 | ⚠️ [TRC_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 423 | `DAX_08_38` | `recovery_path_generate` | CAUTION | 0.4915 | 0.4915 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 424 | `DAX_08_39` | `claim_refine` | CAUTION | 0.4915 | 0.4935 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 425 | `DAX_08_40` | `claim_split` | CAUTION | 0.4935 | 0.4935 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 426 | `DAX_08_41` | `claim_merge` | CAUTION | 0.4935 | 0.4935 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 427 | `DAX_08_42` | `falsification_test_define` | CAUTION | 0.4935 | 0.4935 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 428 | `DAX_08_43` | `scenario_low_run` | CAUTION | 0.4935 | 0.4905 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 429 | `DAX_08_44` | `scenario_base_run` | CAUTION | 0.4905 | 0.484 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 430 | `DAX_08_45` | `scenario_high_run` | CAUTION | 0.484 | 0.484 | ⚠️ [TRC_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 431 | `DAX_08_46` | `downstream_effect_scan` | CAUTION | 0.484 | 0.484 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 432 | `DAX_08_47` | `stakeholder_impact_scan` | CAUTION | 0.484 | 0.484 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 433 | `DAX_08_48` | `decision_threshold_check` | CAUTION | 0.484 | 0.484 | ⚠️ [TRC_1] Threshold check: BLOCK — combined score 0.38 be | Decision threshold: gate=BLOCK, combined_score=0.38. |
| 434 | `DAX_08_49` | `gate_recommendation` | CAUTION | 0.484 | 0.484 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 435 | `DAX_08_50` | `recursion_trigger_check` | CAUTION | 0.484 | 0.484 | ✅ PASS | Recursion trigger: No recursion required.. |
| 436 | `DAX_08_51` | `recursion_payload_build` | CAUTION | 0.484 | 0.484 | ✅ PASS | Recursion payload: Built for layer TRC_1. Target: ambiguity reduction and evidence sourcin |
| 437 | `DAX_08_52` | `trace_link_emit` | CAUTION | 0.484 | 0.484 | ✅ PASS | Trace link: [TRC_1::trace::29d554f3] emitted. |
| 438 | `DAX_08_53` | `audit_hash_prepare` | CAUTION | 0.484 | 0.484 | ✅ PASS | Audit hash prepared: b72ce7e395a6e90a for layer TRC_1. |
| 439 | `DAX_08_54` | `telemetry_emit` | CAUTION | 0.484 | 0.484 | ✅ PASS | Telemetry: layer=TRC_1, logic=0.0, assumption_integrity=0.76, ts=1782526860.37. |
| 440 | `DAX_08_55` | `layer_output_write` | CAUTION | 0.484 | 0.484 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=TRC_1, score=0.0. |

---

## CON_1 — Contradiction Scan Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 441 | `DAX_09_01` | `intake_snapshot` | CAUTION | 0.484 | 0.484 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=CON_1. |
| 442 | `DAX_09_02` | `normalize_input` | CAUTION | 0.484 | 0.484 | ✅ PASS | Normalization check: Input is clean. |
| 443 | `DAX_09_03` | `domain_classify` | CAUTION | 0.484 | 0.484 | ⚠️ [CON_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 444 | `DAX_09_04` | `entity_extract` | CAUTION | 0.484 | 0.484 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 445 | `DAX_09_05` | `claim_extract` | CAUTION | 0.484 | 0.484 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 446 | `DAX_09_06` | `question_extract` | CAUTION | 0.484 | 0.484 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 447 | `DAX_09_07` | `goal_extract` | CAUTION | 0.484 | 0.482 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 448 | `DAX_09_08` | `constraint_extract` | CAUTION | 0.482 | 0.482 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 449 | `DAX_09_09` | `scope_define` | CAUTION | 0.482 | 0.482 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 450 | `DAX_09_10` | `context_link` | CAUTION | 0.482 | 0.482 | ✅ PASS | Context link: Layer CON_1 chained to upstream state. |
| 451 | `DAX_09_11` | `assumption_list` | CAUTION | 0.482 | 0.482 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 452 | `DAX_09_12` | `assumption_classify` | CAUTION | 0.482 | 0.482 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 453 | `DAX_09_13` | `hidden_premise_scan` | CAUTION | 0.482 | 0.476 | ⚠️ [CON_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 454 | `DAX_09_14` | `assumption_confidence_score` | CAUTION | 0.476 | 0.476 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 455 | `DAX_09_15` | `claim_assumption_bind` | CAUTION | 0.476 | 0.476 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 456 | `DAX_09_16` | `dependency_graph_update` | CAUTION | 0.476 | 0.474 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 457 | `DAX_09_17` | `priority_weight` | CAUTION | 0.474 | 0.474 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 458 | `DAX_09_18` | `risk_weight` | CAUTION | 0.474 | 0.474 | ⚠️ [CON_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 459 | `DAX_09_19` | `confidence_weight` | CAUTION | 0.474 | 0.474 | ✅ PASS | Confidence weight: 1.0. |
| 460 | `DAX_09_20` | `evidence_requirement_map` | CAUTION | 0.474 | 0.474 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 461 | `DAX_09_21` | `evidence_presence_check` | CAUTION | 0.474 | 0.474 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 462 | `DAX_09_22` | `evidence_quality_score` | CAUTION | 0.474 | 0.474 | ✅ PASS | Evidence quality score: 1.0. |
| 463 | `DAX_09_23` | `ambiguity_probe` | CAUTION | 0.474 | 0.474 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 464 | `DAX_09_24` | `contradiction_probe` | CAUTION | 0.474 | 0.474 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 465 | `DAX_09_25` | `logic_validity_check` | CAUTION | 0.474 | 0.474 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 466 | `DAX_09_26` | `causal_chain_check` | CAUTION | 0.474 | 0.472 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 467 | `DAX_09_27` | `counterexample_generate` | CAUTION | 0.472 | 0.472 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 468 | `DAX_09_28` | `adversarial_attack` | CAUTION | 0.472 | 0.472 | ⚠️ [CON_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 469 | `DAX_09_29` | `bias_frame_audit` | CAUTION | 0.472 | 0.472 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 470 | `DAX_09_30` | `safety_policy_check` | CAUTION | 0.472 | 0.472 | ⚠️ [CON_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 471 | `DAX_09_31` | `feasibility_check` | CAUTION | 0.472 | 0.4675 | ⚠️ [CON_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 472 | `DAX_09_32` | `resource_cost_estimate` | CAUTION | 0.4675 | 0.4645 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 473 | `DAX_09_33` | `volatility_score` | CAUTION | 0.4645 | 0.4645 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 474 | `DAX_09_34` | `coherence_score` | CAUTION | 0.4645 | 0.4645 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 475 | `DAX_09_35` | `survivability_score` | CAUTION | 0.4645 | 0.4645 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 476 | `DAX_09_36` | `uncertainty_register_update` | CAUTION | 0.4645 | 0.4645 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 477 | `DAX_09_37` | `warning_emit` | CAUTION | 0.4645 | 0.4645 | ⚠️ [CON_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 478 | `DAX_09_38` | `recovery_path_generate` | CAUTION | 0.4645 | 0.4645 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 479 | `DAX_09_39` | `claim_refine` | CAUTION | 0.4645 | 0.4665 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 480 | `DAX_09_40` | `claim_split` | CAUTION | 0.4665 | 0.4665 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 481 | `DAX_09_41` | `claim_merge` | CAUTION | 0.4665 | 0.4665 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 482 | `DAX_09_42` | `falsification_test_define` | CAUTION | 0.4665 | 0.4665 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 483 | `DAX_09_43` | `scenario_low_run` | CAUTION | 0.4665 | 0.4635 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 484 | `DAX_09_44` | `scenario_base_run` | CAUTION | 0.4635 | 0.457 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 485 | `DAX_09_45` | `scenario_high_run` | CAUTION | 0.457 | 0.457 | ⚠️ [CON_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 486 | `DAX_09_46` | `downstream_effect_scan` | CAUTION | 0.457 | 0.457 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 487 | `DAX_09_47` | `stakeholder_impact_scan` | CAUTION | 0.457 | 0.457 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 488 | `DAX_09_48` | `decision_threshold_check` | CAUTION | 0.457 | 0.457 | ⚠️ [CON_1] Threshold check: BLOCK — combined score 0.36 be | Decision threshold: gate=BLOCK, combined_score=0.36. |
| 489 | `DAX_09_49` | `gate_recommendation` | CAUTION | 0.457 | 0.457 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 490 | `DAX_09_50` | `recursion_trigger_check` | CAUTION | 0.457 | 0.457 | ✅ PASS | Recursion trigger: No recursion required.. |
| 491 | `DAX_09_51` | `recursion_payload_build` | CAUTION | 0.457 | 0.457 | ✅ PASS | Recursion payload: Built for layer CON_1. Target: ambiguity reduction and evidence sourcin |
| 492 | `DAX_09_52` | `trace_link_emit` | CAUTION | 0.457 | 0.457 | ✅ PASS | Trace link: [CON_1::trace::29d554f3] emitted. |
| 493 | `DAX_09_53` | `audit_hash_prepare` | CAUTION | 0.457 | 0.457 | ✅ PASS | Audit hash prepared: 4419863220ecc9e3 for layer CON_1. |
| 494 | `DAX_09_54` | `telemetry_emit` | CAUTION | 0.457 | 0.457 | ✅ PASS | Telemetry: layer=CON_1, logic=0.0, assumption_integrity=0.73, ts=1782526860.38. |
| 495 | `DAX_09_55` | `layer_output_write` | CAUTION | 0.457 | 0.457 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=CON_1, score=0.0. |

---

## EVD_1 — Evidence Demand Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 496 | `DAX_10_01` | `intake_snapshot` | CAUTION | 0.457 | 0.457 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=EVD_1. |
| 497 | `DAX_10_02` | `normalize_input` | CAUTION | 0.457 | 0.457 | ✅ PASS | Normalization check: Input is clean. |
| 498 | `DAX_10_03` | `domain_classify` | CAUTION | 0.457 | 0.457 | ⚠️ [EVD_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 499 | `DAX_10_04` | `entity_extract` | CAUTION | 0.457 | 0.457 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 500 | `DAX_10_05` | `claim_extract` | CAUTION | 0.457 | 0.457 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 501 | `DAX_10_06` | `question_extract` | CAUTION | 0.457 | 0.457 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 502 | `DAX_10_07` | `goal_extract` | CAUTION | 0.457 | 0.455 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 503 | `DAX_10_08` | `constraint_extract` | CAUTION | 0.455 | 0.455 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 504 | `DAX_10_09` | `scope_define` | CAUTION | 0.455 | 0.455 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 505 | `DAX_10_10` | `context_link` | CAUTION | 0.455 | 0.455 | ✅ PASS | Context link: Layer EVD_1 chained to upstream state. |
| 506 | `DAX_10_11` | `assumption_list` | CAUTION | 0.455 | 0.455 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 507 | `DAX_10_12` | `assumption_classify` | CAUTION | 0.455 | 0.455 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 508 | `DAX_10_13` | `hidden_premise_scan` | CAUTION | 0.455 | 0.449 | ⚠️ [EVD_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 509 | `DAX_10_14` | `assumption_confidence_score` | CAUTION | 0.449 | 0.449 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 510 | `DAX_10_15` | `claim_assumption_bind` | CAUTION | 0.449 | 0.449 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 511 | `DAX_10_16` | `dependency_graph_update` | CAUTION | 0.449 | 0.447 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 512 | `DAX_10_17` | `priority_weight` | CAUTION | 0.447 | 0.447 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 513 | `DAX_10_18` | `risk_weight` | CAUTION | 0.447 | 0.447 | ⚠️ [EVD_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 514 | `DAX_10_19` | `confidence_weight` | CAUTION | 0.447 | 0.447 | ✅ PASS | Confidence weight: 1.0. |
| 515 | `DAX_10_20` | `evidence_requirement_map` | CAUTION | 0.447 | 0.447 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 516 | `DAX_10_21` | `evidence_presence_check` | CAUTION | 0.447 | 0.447 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 517 | `DAX_10_22` | `evidence_quality_score` | CAUTION | 0.447 | 0.447 | ✅ PASS | Evidence quality score: 1.0. |
| 518 | `DAX_10_23` | `ambiguity_probe` | CAUTION | 0.447 | 0.447 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 519 | `DAX_10_24` | `contradiction_probe` | CAUTION | 0.447 | 0.447 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 520 | `DAX_10_25` | `logic_validity_check` | CAUTION | 0.447 | 0.447 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 521 | `DAX_10_26` | `causal_chain_check` | CAUTION | 0.447 | 0.445 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 522 | `DAX_10_27` | `counterexample_generate` | CAUTION | 0.445 | 0.445 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 523 | `DAX_10_28` | `adversarial_attack` | CAUTION | 0.445 | 0.445 | ⚠️ [EVD_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 524 | `DAX_10_29` | `bias_frame_audit` | CAUTION | 0.445 | 0.445 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 525 | `DAX_10_30` | `safety_policy_check` | CAUTION | 0.445 | 0.445 | ⚠️ [EVD_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 526 | `DAX_10_31` | `feasibility_check` | CAUTION | 0.445 | 0.4405 | ⚠️ [EVD_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 527 | `DAX_10_32` | `resource_cost_estimate` | CAUTION | 0.4405 | 0.4375 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 528 | `DAX_10_33` | `volatility_score` | CAUTION | 0.4375 | 0.4375 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 529 | `DAX_10_34` | `coherence_score` | CAUTION | 0.4375 | 0.4375 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 530 | `DAX_10_35` | `survivability_score` | CAUTION | 0.4375 | 0.4375 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 531 | `DAX_10_36` | `uncertainty_register_update` | CAUTION | 0.4375 | 0.4375 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 532 | `DAX_10_37` | `warning_emit` | CAUTION | 0.4375 | 0.4375 | ⚠️ [EVD_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 533 | `DAX_10_38` | `recovery_path_generate` | CAUTION | 0.4375 | 0.4375 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 534 | `DAX_10_39` | `claim_refine` | CAUTION | 0.4375 | 0.4395 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 535 | `DAX_10_40` | `claim_split` | CAUTION | 0.4395 | 0.4395 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 536 | `DAX_10_41` | `claim_merge` | CAUTION | 0.4395 | 0.4395 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 537 | `DAX_10_42` | `falsification_test_define` | CAUTION | 0.4395 | 0.4395 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 538 | `DAX_10_43` | `scenario_low_run` | CAUTION | 0.4395 | 0.4365 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 539 | `DAX_10_44` | `scenario_base_run` | CAUTION | 0.4365 | 0.43 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 540 | `DAX_10_45` | `scenario_high_run` | CAUTION | 0.43 | 0.43 | ⚠️ [EVD_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 541 | `DAX_10_46` | `downstream_effect_scan` | CAUTION | 0.43 | 0.43 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 542 | `DAX_10_47` | `stakeholder_impact_scan` | CAUTION | 0.43 | 0.43 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 543 | `DAX_10_48` | `decision_threshold_check` | CAUTION | 0.43 | 0.43 | ⚠️ [EVD_1] Threshold check: BLOCK — combined score 0.35 be | Decision threshold: gate=BLOCK, combined_score=0.35. |
| 544 | `DAX_10_49` | `gate_recommendation` | CAUTION | 0.43 | 0.43 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 545 | `DAX_10_50` | `recursion_trigger_check` | CAUTION | 0.43 | 0.43 | ✅ PASS | Recursion trigger: No recursion required.. |
| 546 | `DAX_10_51` | `recursion_payload_build` | CAUTION | 0.43 | 0.43 | ✅ PASS | Recursion payload: Built for layer EVD_1. Target: ambiguity reduction and evidence sourcin |
| 547 | `DAX_10_52` | `trace_link_emit` | CAUTION | 0.43 | 0.43 | ✅ PASS | Trace link: [EVD_1::trace::29d554f3] emitted. |
| 548 | `DAX_10_53` | `audit_hash_prepare` | CAUTION | 0.43 | 0.43 | ✅ PASS | Audit hash prepared: 593456d4771a9f5d for layer EVD_1. |
| 549 | `DAX_10_54` | `telemetry_emit` | CAUTION | 0.43 | 0.43 | ✅ PASS | Telemetry: layer=EVD_1, logic=0.0, assumption_integrity=0.7, ts=1782526860.39. |
| 550 | `DAX_10_55` | `layer_output_write` | CAUTION | 0.43 | 0.43 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=EVD_1, score=0.0. |

---

## REC_1 — Recursion Plan Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 551 | `DAX_11_01` | `intake_snapshot` | CAUTION | 0.43 | 0.43 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=REC_1. |
| 552 | `DAX_11_02` | `normalize_input` | CAUTION | 0.43 | 0.43 | ✅ PASS | Normalization check: Input is clean. |
| 553 | `DAX_11_03` | `domain_classify` | CAUTION | 0.43 | 0.43 | ⚠️ [REC_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 554 | `DAX_11_04` | `entity_extract` | CAUTION | 0.43 | 0.43 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 555 | `DAX_11_05` | `claim_extract` | CAUTION | 0.43 | 0.43 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 556 | `DAX_11_06` | `question_extract` | CAUTION | 0.43 | 0.43 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 557 | `DAX_11_07` | `goal_extract` | CAUTION | 0.43 | 0.428 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 558 | `DAX_11_08` | `constraint_extract` | CAUTION | 0.428 | 0.428 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 559 | `DAX_11_09` | `scope_define` | CAUTION | 0.428 | 0.428 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 560 | `DAX_11_10` | `context_link` | CAUTION | 0.428 | 0.428 | ✅ PASS | Context link: Layer REC_1 chained to upstream state. |
| 561 | `DAX_11_11` | `assumption_list` | CAUTION | 0.428 | 0.428 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 562 | `DAX_11_12` | `assumption_classify` | CAUTION | 0.428 | 0.428 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 563 | `DAX_11_13` | `hidden_premise_scan` | CAUTION | 0.428 | 0.422 | ⚠️ [REC_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 564 | `DAX_11_14` | `assumption_confidence_score` | CAUTION | 0.422 | 0.422 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 565 | `DAX_11_15` | `claim_assumption_bind` | CAUTION | 0.422 | 0.422 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 566 | `DAX_11_16` | `dependency_graph_update` | CAUTION | 0.422 | 0.42 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 567 | `DAX_11_17` | `priority_weight` | CAUTION | 0.42 | 0.42 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 568 | `DAX_11_18` | `risk_weight` | CAUTION | 0.42 | 0.42 | ⚠️ [REC_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 569 | `DAX_11_19` | `confidence_weight` | CAUTION | 0.42 | 0.42 | ✅ PASS | Confidence weight: 1.0. |
| 570 | `DAX_11_20` | `evidence_requirement_map` | CAUTION | 0.42 | 0.42 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 571 | `DAX_11_21` | `evidence_presence_check` | CAUTION | 0.42 | 0.42 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 572 | `DAX_11_22` | `evidence_quality_score` | CAUTION | 0.42 | 0.42 | ✅ PASS | Evidence quality score: 1.0. |
| 573 | `DAX_11_23` | `ambiguity_probe` | CAUTION | 0.42 | 0.42 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 574 | `DAX_11_24` | `contradiction_probe` | CAUTION | 0.42 | 0.42 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 575 | `DAX_11_25` | `logic_validity_check` | CAUTION | 0.42 | 0.42 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 576 | `DAX_11_26` | `causal_chain_check` | CAUTION | 0.42 | 0.418 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 577 | `DAX_11_27` | `counterexample_generate` | CAUTION | 0.418 | 0.418 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 578 | `DAX_11_28` | `adversarial_attack` | CAUTION | 0.418 | 0.418 | ⚠️ [REC_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 579 | `DAX_11_29` | `bias_frame_audit` | CAUTION | 0.418 | 0.418 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 580 | `DAX_11_30` | `safety_policy_check` | CAUTION | 0.418 | 0.418 | ⚠️ [REC_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 581 | `DAX_11_31` | `feasibility_check` | CAUTION | 0.418 | 0.418 | ⚠️ [REC_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 582 | `DAX_11_32` | `resource_cost_estimate` | CAUTION | 0.418 | 0.418 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 583 | `DAX_11_33` | `volatility_score` | CAUTION | 0.418 | 0.418 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 584 | `DAX_11_34` | `coherence_score` | CAUTION | 0.418 | 0.418 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 585 | `DAX_11_35` | `survivability_score` | CAUTION | 0.418 | 0.418 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 586 | `DAX_11_36` | `uncertainty_register_update` | CAUTION | 0.418 | 0.418 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 587 | `DAX_11_37` | `warning_emit` | CAUTION | 0.418 | 0.418 | ⚠️ [REC_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 588 | `DAX_11_38` | `recovery_path_generate` | CAUTION | 0.418 | 0.418 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 589 | `DAX_11_39` | `claim_refine` | CAUTION | 0.418 | 0.42 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 590 | `DAX_11_40` | `claim_split` | CAUTION | 0.42 | 0.42 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 591 | `DAX_11_41` | `claim_merge` | CAUTION | 0.42 | 0.42 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 592 | `DAX_11_42` | `falsification_test_define` | CAUTION | 0.42 | 0.42 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 593 | `DAX_11_43` | `scenario_low_run` | CAUTION | 0.42 | 0.42 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 594 | `DAX_11_44` | `scenario_base_run` | CAUTION | 0.42 | 0.418 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 595 | `DAX_11_45` | `scenario_high_run` | CAUTION | 0.418 | 0.418 | ⚠️ [REC_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 596 | `DAX_11_46` | `downstream_effect_scan` | CAUTION | 0.418 | 0.418 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 597 | `DAX_11_47` | `stakeholder_impact_scan` | CAUTION | 0.418 | 0.418 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 598 | `DAX_11_48` | `decision_threshold_check` | CAUTION | 0.418 | 0.418 | ⚠️ [REC_1] Threshold check: BLOCK — combined score 0.33 be | Decision threshold: gate=BLOCK, combined_score=0.33. |
| 599 | `DAX_11_49` | `gate_recommendation` | CAUTION | 0.418 | 0.418 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 600 | `DAX_11_50` | `recursion_trigger_check` | CAUTION | 0.418 | 0.418 | ✅ PASS | Recursion trigger: No recursion required.. |
| 601 | `DAX_11_51` | `recursion_payload_build` | CAUTION | 0.418 | 0.418 | ✅ PASS | Recursion payload: Built for layer REC_1. Target: ambiguity reduction and evidence sourcin |
| 602 | `DAX_11_52` | `trace_link_emit` | CAUTION | 0.418 | 0.418 | ✅ PASS | Trace link: [REC_1::trace::29d554f3] emitted. |
| 603 | `DAX_11_53` | `audit_hash_prepare` | CAUTION | 0.418 | 0.418 | ✅ PASS | Audit hash prepared: c79ceacaed4a9ab0 for layer REC_1. |
| 604 | `DAX_11_54` | `telemetry_emit` | CAUTION | 0.418 | 0.418 | ✅ PASS | Telemetry: layer=REC_1, logic=0.0, assumption_integrity=0.67, ts=1782526860.4. |
| 605 | `DAX_11_55` | `layer_output_write` | CAUTION | 0.418 | 0.418 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=REC_1, score=0.0. |

---

## GOV_1 — Governance Gate Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 606 | `DAX_12_01` | `intake_snapshot` | CAUTION | 0.418 | 0.418 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=GOV_1. |
| 607 | `DAX_12_02` | `normalize_input` | CAUTION | 0.418 | 0.418 | ✅ PASS | Normalization check: Input is clean. |
| 608 | `DAX_12_03` | `domain_classify` | CAUTION | 0.418 | 0.418 | ⚠️ [GOV_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 609 | `DAX_12_04` | `entity_extract` | CAUTION | 0.418 | 0.418 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 610 | `DAX_12_05` | `claim_extract` | CAUTION | 0.418 | 0.418 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 611 | `DAX_12_06` | `question_extract` | CAUTION | 0.418 | 0.418 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 612 | `DAX_12_07` | `goal_extract` | CAUTION | 0.418 | 0.416 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 613 | `DAX_12_08` | `constraint_extract` | CAUTION | 0.416 | 0.416 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 614 | `DAX_12_09` | `scope_define` | CAUTION | 0.416 | 0.416 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 615 | `DAX_12_10` | `context_link` | CAUTION | 0.416 | 0.416 | ✅ PASS | Context link: Layer GOV_1 chained to upstream state. |
| 616 | `DAX_12_11` | `assumption_list` | CAUTION | 0.416 | 0.416 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 617 | `DAX_12_12` | `assumption_classify` | CAUTION | 0.416 | 0.416 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 618 | `DAX_12_13` | `hidden_premise_scan` | CAUTION | 0.416 | 0.41 | ⚠️ [GOV_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 619 | `DAX_12_14` | `assumption_confidence_score` | CAUTION | 0.41 | 0.41 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 620 | `DAX_12_15` | `claim_assumption_bind` | CAUTION | 0.41 | 0.41 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 621 | `DAX_12_16` | `dependency_graph_update` | CAUTION | 0.41 | 0.408 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 622 | `DAX_12_17` | `priority_weight` | CAUTION | 0.408 | 0.408 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 623 | `DAX_12_18` | `risk_weight` | CAUTION | 0.408 | 0.408 | ⚠️ [GOV_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 624 | `DAX_12_19` | `confidence_weight` | CAUTION | 0.408 | 0.408 | ✅ PASS | Confidence weight: 1.0. |
| 625 | `DAX_12_20` | `evidence_requirement_map` | CAUTION | 0.408 | 0.408 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 626 | `DAX_12_21` | `evidence_presence_check` | CAUTION | 0.408 | 0.408 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 627 | `DAX_12_22` | `evidence_quality_score` | CAUTION | 0.408 | 0.408 | ✅ PASS | Evidence quality score: 1.0. |
| 628 | `DAX_12_23` | `ambiguity_probe` | CAUTION | 0.408 | 0.408 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 629 | `DAX_12_24` | `contradiction_probe` | CAUTION | 0.408 | 0.408 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 630 | `DAX_12_25` | `logic_validity_check` | CAUTION | 0.408 | 0.408 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 631 | `DAX_12_26` | `causal_chain_check` | CAUTION | 0.408 | 0.406 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 632 | `DAX_12_27` | `counterexample_generate` | CAUTION | 0.406 | 0.406 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 633 | `DAX_12_28` | `adversarial_attack` | CAUTION | 0.406 | 0.406 | ⚠️ [GOV_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 634 | `DAX_12_29` | `bias_frame_audit` | CAUTION | 0.406 | 0.406 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 635 | `DAX_12_30` | `safety_policy_check` | CAUTION | 0.406 | 0.406 | ⚠️ [GOV_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 636 | `DAX_12_31` | `feasibility_check` | CAUTION | 0.406 | 0.406 | ⚠️ [GOV_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 637 | `DAX_12_32` | `resource_cost_estimate` | CAUTION | 0.406 | 0.406 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 638 | `DAX_12_33` | `volatility_score` | CAUTION | 0.406 | 0.406 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 639 | `DAX_12_34` | `coherence_score` | CAUTION | 0.406 | 0.406 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 640 | `DAX_12_35` | `survivability_score` | CAUTION | 0.406 | 0.406 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 641 | `DAX_12_36` | `uncertainty_register_update` | CAUTION | 0.406 | 0.406 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 642 | `DAX_12_37` | `warning_emit` | CAUTION | 0.406 | 0.406 | ⚠️ [GOV_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 643 | `DAX_12_38` | `recovery_path_generate` | CAUTION | 0.406 | 0.406 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 644 | `DAX_12_39` | `claim_refine` | CAUTION | 0.406 | 0.408 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 645 | `DAX_12_40` | `claim_split` | CAUTION | 0.408 | 0.408 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 646 | `DAX_12_41` | `claim_merge` | CAUTION | 0.408 | 0.408 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 647 | `DAX_12_42` | `falsification_test_define` | CAUTION | 0.408 | 0.408 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 648 | `DAX_12_43` | `scenario_low_run` | CAUTION | 0.408 | 0.408 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 649 | `DAX_12_44` | `scenario_base_run` | CAUTION | 0.408 | 0.406 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 650 | `DAX_12_45` | `scenario_high_run` | CAUTION | 0.406 | 0.406 | ⚠️ [GOV_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 651 | `DAX_12_46` | `downstream_effect_scan` | CAUTION | 0.406 | 0.406 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 652 | `DAX_12_47` | `stakeholder_impact_scan` | CAUTION | 0.406 | 0.406 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 653 | `DAX_12_48` | `decision_threshold_check` | CAUTION | 0.406 | 0.406 | ⚠️ [GOV_1] Threshold check: BLOCK — combined score 0.32 be | Decision threshold: gate=BLOCK, combined_score=0.32. |
| 654 | `DAX_12_49` | `gate_recommendation` | CAUTION | 0.406 | 0.406 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 655 | `DAX_12_50` | `recursion_trigger_check` | CAUTION | 0.406 | 0.406 | ✅ PASS | Recursion trigger: No recursion required.. |
| 656 | `DAX_12_51` | `recursion_payload_build` | CAUTION | 0.406 | 0.406 | ✅ PASS | Recursion payload: Built for layer GOV_1. Target: ambiguity reduction and evidence sourcin |
| 657 | `DAX_12_52` | `trace_link_emit` | CAUTION | 0.406 | 0.406 | ✅ PASS | Trace link: [GOV_1::trace::29d554f3] emitted. |
| 658 | `DAX_12_53` | `audit_hash_prepare` | CAUTION | 0.406 | 0.406 | ✅ PASS | Audit hash prepared: e3ab275f5df6cb6d for layer GOV_1. |
| 659 | `DAX_12_54` | `telemetry_emit` | CAUTION | 0.406 | 0.406 | ✅ PASS | Telemetry: layer=GOV_1, logic=0.0, assumption_integrity=0.64, ts=1782526860.41. |
| 660 | `DAX_12_55` | `layer_output_write` | CAUTION | 0.406 | 0.406 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=GOV_1, score=0.0. |

---

## OUT_1 — Output Record Layer
*165 tiles executed | 27 flagged | 138 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 661 | `DAX_13_01` | `intake_snapshot` | CAUTION | 0.406 | 0.406 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=OUT_1. |
| 662 | `DAX_13_02` | `normalize_input` | CAUTION | 0.406 | 0.406 | ✅ PASS | Normalization check: Input is clean. |
| 663 | `DAX_13_03` | `domain_classify` | CAUTION | 0.406 | 0.406 | ⚠️ [OUT_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 664 | `DAX_13_04` | `entity_extract` | CAUTION | 0.406 | 0.406 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 665 | `DAX_13_05` | `claim_extract` | CAUTION | 0.406 | 0.406 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 666 | `DAX_13_06` | `question_extract` | CAUTION | 0.406 | 0.406 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 667 | `DAX_13_07` | `goal_extract` | CAUTION | 0.406 | 0.404 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 668 | `DAX_13_08` | `constraint_extract` | CAUTION | 0.404 | 0.404 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 669 | `DAX_13_09` | `scope_define` | CAUTION | 0.404 | 0.404 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 670 | `DAX_13_10` | `context_link` | CAUTION | 0.404 | 0.404 | ✅ PASS | Context link: Layer OUT_1 chained to upstream state. |
| 671 | `DAX_13_11` | `assumption_list` | CAUTION | 0.404 | 0.404 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 672 | `DAX_13_12` | `assumption_classify` | CAUTION | 0.404 | 0.404 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 673 | `DAX_13_13` | `hidden_premise_scan` | RECURSE | 0.404 | 0.398 | ⚠️ [OUT_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 674 | `DAX_13_01` | `intake_snapshot` | RECURSE | 0.398 | 0.398 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=OUT_1. |
| 675 | `DAX_13_02` | `normalize_input` | RECURSE | 0.398 | 0.398 | ✅ PASS | Normalization check: Input is clean. |
| 676 | `DAX_13_03` | `domain_classify` | RECURSE | 0.398 | 0.398 | ⚠️ [OUT_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 677 | `DAX_13_04` | `entity_extract` | RECURSE | 0.398 | 0.398 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 678 | `DAX_13_05` | `claim_extract` | RECURSE | 0.398 | 0.398 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 679 | `DAX_13_06` | `question_extract` | RECURSE | 0.398 | 0.398 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 680 | `DAX_13_07` | `goal_extract` | RECURSE | 0.398 | 0.396 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 681 | `DAX_13_08` | `constraint_extract` | RECURSE | 0.396 | 0.396 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 682 | `DAX_13_09` | `scope_define` | RECURSE | 0.396 | 0.396 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 683 | `DAX_13_10` | `context_link` | RECURSE | 0.396 | 0.396 | ✅ PASS | Context link: Layer OUT_1 chained to upstream state. |
| 684 | `DAX_13_11` | `assumption_list` | RECURSE | 0.396 | 0.396 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 685 | `DAX_13_12` | `assumption_classify` | RECURSE | 0.396 | 0.396 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 686 | `DAX_13_13` | `hidden_premise_scan` | RECURSE | 0.396 | 0.39 | ⚠️ [OUT_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 687 | `DAX_13_14` | `assumption_confidence_score` | RECURSE | 0.39 | 0.39 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 688 | `DAX_13_15` | `claim_assumption_bind` | RECURSE | 0.39 | 0.39 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 689 | `DAX_13_16` | `dependency_graph_update` | RECURSE | 0.39 | 0.388 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 690 | `DAX_13_17` | `priority_weight` | RECURSE | 0.388 | 0.388 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 691 | `DAX_13_18` | `risk_weight` | RECURSE | 0.388 | 0.388 | ⚠️ [OUT_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 692 | `DAX_13_19` | `confidence_weight` | RECURSE | 0.388 | 0.388 | ✅ PASS | Confidence weight: 1.0. |
| 693 | `DAX_13_20` | `evidence_requirement_map` | RECURSE | 0.388 | 0.388 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 694 | `DAX_13_21` | `evidence_presence_check` | RECURSE | 0.388 | 0.388 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 695 | `DAX_13_22` | `evidence_quality_score` | RECURSE | 0.388 | 0.388 | ✅ PASS | Evidence quality score: 1.0. |
| 696 | `DAX_13_23` | `ambiguity_probe` | RECURSE | 0.388 | 0.388 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 697 | `DAX_13_24` | `contradiction_probe` | RECURSE | 0.388 | 0.388 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 698 | `DAX_13_25` | `logic_validity_check` | RECURSE | 0.388 | 0.388 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 699 | `DAX_13_26` | `causal_chain_check` | RECURSE | 0.388 | 0.386 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 700 | `DAX_13_27` | `counterexample_generate` | RECURSE | 0.386 | 0.386 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 701 | `DAX_13_28` | `adversarial_attack` | RECURSE | 0.386 | 0.386 | ⚠️ [OUT_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 702 | `DAX_13_29` | `bias_frame_audit` | RECURSE | 0.386 | 0.386 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 703 | `DAX_13_30` | `safety_policy_check` | RECURSE | 0.386 | 0.386 | ⚠️ [OUT_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 704 | `DAX_13_31` | `feasibility_check` | RECURSE | 0.386 | 0.386 | ⚠️ [OUT_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 705 | `DAX_13_32` | `resource_cost_estimate` | RECURSE | 0.386 | 0.386 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 706 | `DAX_13_33` | `volatility_score` | RECURSE | 0.386 | 0.386 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 707 | `DAX_13_34` | `coherence_score` | RECURSE | 0.386 | 0.386 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 708 | `DAX_13_35` | `survivability_score` | RECURSE | 0.386 | 0.386 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 709 | `DAX_13_36` | `uncertainty_register_update` | RECURSE | 0.386 | 0.386 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 710 | `DAX_13_37` | `warning_emit` | RECURSE | 0.386 | 0.386 | ⚠️ [OUT_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 711 | `DAX_13_38` | `recovery_path_generate` | RECURSE | 0.386 | 0.386 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 712 | `DAX_13_39` | `claim_refine` | RECURSE | 0.386 | 0.388 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 713 | `DAX_13_40` | `claim_split` | RECURSE | 0.388 | 0.388 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 714 | `DAX_13_41` | `claim_merge` | RECURSE | 0.388 | 0.388 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 715 | `DAX_13_42` | `falsification_test_define` | RECURSE | 0.388 | 0.388 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 716 | `DAX_13_43` | `scenario_low_run` | RECURSE | 0.388 | 0.388 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 717 | `DAX_13_44` | `scenario_base_run` | RECURSE | 0.388 | 0.386 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 718 | `DAX_13_45` | `scenario_high_run` | RECURSE | 0.386 | 0.386 | ⚠️ [OUT_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 719 | `DAX_13_46` | `downstream_effect_scan` | RECURSE | 0.386 | 0.386 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 720 | `DAX_13_47` | `stakeholder_impact_scan` | RECURSE | 0.386 | 0.386 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 721 | `DAX_13_48` | `decision_threshold_check` | RECURSE | 0.386 | 0.386 | ⚠️ [OUT_1] Threshold check: BLOCK — combined score 0.29 be | Decision threshold: gate=BLOCK, combined_score=0.29. |
| 722 | `DAX_13_49` | `gate_recommendation` | RECURSE | 0.386 | 0.386 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 723 | `DAX_13_50` | `recursion_trigger_check` | RECURSE | 0.386 | 0.386 | ✅ PASS | Recursion trigger: No recursion required.. |
| 724 | `DAX_13_51` | `recursion_payload_build` | RECURSE | 0.386 | 0.386 | ✅ PASS | Recursion payload: Built for layer OUT_1. Target: ambiguity reduction and evidence sourcin |
| 725 | `DAX_13_52` | `trace_link_emit` | RECURSE | 0.386 | 0.386 | ✅ PASS | Trace link: [OUT_1::trace::29d554f3] emitted. |
| 726 | `DAX_13_53` | `audit_hash_prepare` | RECURSE | 0.386 | 0.386 | ✅ PASS | Audit hash prepared: ba8b049411bdb550 for layer OUT_1. |
| 727 | `DAX_13_54` | `telemetry_emit` | RECURSE | 0.386 | 0.386 | ✅ PASS | Telemetry: layer=OUT_1, logic=0.0, assumption_integrity=0.58, ts=1782526860.42. |
| 728 | `DAX_13_55` | `layer_output_write` | RECURSE | 0.386 | 0.386 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=OUT_1, score=0.0. |
| 729 | `DAX_13_14` | `assumption_confidence_score` | RECURSE | 0.386 | 0.386 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 730 | `DAX_13_01` | `intake_snapshot` | RECURSE | 0.386 | 0.386 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=OUT_1. |
| 731 | `DAX_13_02` | `normalize_input` | RECURSE | 0.386 | 0.386 | ✅ PASS | Normalization check: Input is clean. |
| 732 | `DAX_13_03` | `domain_classify` | RECURSE | 0.386 | 0.386 | ⚠️ [OUT_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 733 | `DAX_13_04` | `entity_extract` | RECURSE | 0.386 | 0.386 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 734 | `DAX_13_05` | `claim_extract` | RECURSE | 0.386 | 0.386 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 735 | `DAX_13_06` | `question_extract` | RECURSE | 0.386 | 0.386 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 736 | `DAX_13_07` | `goal_extract` | RECURSE | 0.386 | 0.384 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 737 | `DAX_13_08` | `constraint_extract` | RECURSE | 0.384 | 0.384 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 738 | `DAX_13_09` | `scope_define` | RECURSE | 0.384 | 0.384 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 739 | `DAX_13_10` | `context_link` | RECURSE | 0.384 | 0.384 | ✅ PASS | Context link: Layer OUT_1 chained to upstream state. |
| 740 | `DAX_13_11` | `assumption_list` | RECURSE | 0.384 | 0.384 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 741 | `DAX_13_12` | `assumption_classify` | RECURSE | 0.384 | 0.384 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 742 | `DAX_13_13` | `hidden_premise_scan` | RECURSE | 0.384 | 0.378 | ⚠️ [OUT_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 743 | `DAX_13_14` | `assumption_confidence_score` | RECURSE | 0.378 | 0.378 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 744 | `DAX_13_15` | `claim_assumption_bind` | RECURSE | 0.378 | 0.378 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 745 | `DAX_13_16` | `dependency_graph_update` | RECURSE | 0.378 | 0.376 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 746 | `DAX_13_17` | `priority_weight` | RECURSE | 0.376 | 0.376 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 747 | `DAX_13_18` | `risk_weight` | RECURSE | 0.376 | 0.376 | ⚠️ [OUT_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 748 | `DAX_13_19` | `confidence_weight` | RECURSE | 0.376 | 0.376 | ✅ PASS | Confidence weight: 1.0. |
| 749 | `DAX_13_20` | `evidence_requirement_map` | RECURSE | 0.376 | 0.376 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 750 | `DAX_13_21` | `evidence_presence_check` | RECURSE | 0.376 | 0.376 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 751 | `DAX_13_22` | `evidence_quality_score` | RECURSE | 0.376 | 0.376 | ✅ PASS | Evidence quality score: 1.0. |
| 752 | `DAX_13_23` | `ambiguity_probe` | RECURSE | 0.376 | 0.376 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 753 | `DAX_13_24` | `contradiction_probe` | RECURSE | 0.376 | 0.376 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 754 | `DAX_13_25` | `logic_validity_check` | RECURSE | 0.376 | 0.376 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 755 | `DAX_13_26` | `causal_chain_check` | RECURSE | 0.376 | 0.374 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 756 | `DAX_13_27` | `counterexample_generate` | RECURSE | 0.374 | 0.374 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 757 | `DAX_13_28` | `adversarial_attack` | RECURSE | 0.374 | 0.374 | ⚠️ [OUT_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 758 | `DAX_13_29` | `bias_frame_audit` | RECURSE | 0.374 | 0.374 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 759 | `DAX_13_30` | `safety_policy_check` | RECURSE | 0.374 | 0.374 | ⚠️ [OUT_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 760 | `DAX_13_31` | `feasibility_check` | RECURSE | 0.374 | 0.374 | ⚠️ [OUT_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 761 | `DAX_13_32` | `resource_cost_estimate` | RECURSE | 0.374 | 0.374 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 762 | `DAX_13_33` | `volatility_score` | RECURSE | 0.374 | 0.374 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 763 | `DAX_13_34` | `coherence_score` | RECURSE | 0.374 | 0.374 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 764 | `DAX_13_35` | `survivability_score` | RECURSE | 0.374 | 0.374 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 765 | `DAX_13_36` | `uncertainty_register_update` | RECURSE | 0.374 | 0.374 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 766 | `DAX_13_37` | `warning_emit` | RECURSE | 0.374 | 0.374 | ⚠️ [OUT_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 767 | `DAX_13_38` | `recovery_path_generate` | RECURSE | 0.374 | 0.374 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 768 | `DAX_13_39` | `claim_refine` | RECURSE | 0.374 | 0.376 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 769 | `DAX_13_40` | `claim_split` | RECURSE | 0.376 | 0.376 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 770 | `DAX_13_41` | `claim_merge` | RECURSE | 0.376 | 0.376 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 771 | `DAX_13_42` | `falsification_test_define` | RECURSE | 0.376 | 0.376 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 772 | `DAX_13_43` | `scenario_low_run` | RECURSE | 0.376 | 0.376 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 773 | `DAX_13_44` | `scenario_base_run` | RECURSE | 0.376 | 0.374 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 774 | `DAX_13_45` | `scenario_high_run` | RECURSE | 0.374 | 0.374 | ⚠️ [OUT_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 775 | `DAX_13_46` | `downstream_effect_scan` | RECURSE | 0.374 | 0.374 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 776 | `DAX_13_47` | `stakeholder_impact_scan` | RECURSE | 0.374 | 0.374 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 777 | `DAX_13_48` | `decision_threshold_check` | RECURSE | 0.374 | 0.374 | ⚠️ [OUT_1] Threshold check: BLOCK — combined score 0.27 be | Decision threshold: gate=BLOCK, combined_score=0.27. |
| 778 | `DAX_13_49` | `gate_recommendation` | RECURSE | 0.374 | 0.374 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 779 | `DAX_13_50` | `recursion_trigger_check` | RECURSE | 0.374 | 0.374 | ✅ PASS | Recursion trigger: No recursion required.. |
| 780 | `DAX_13_51` | `recursion_payload_build` | RECURSE | 0.374 | 0.374 | ✅ PASS | Recursion payload: Built for layer OUT_1. Target: ambiguity reduction and evidence sourcin |
| 781 | `DAX_13_52` | `trace_link_emit` | RECURSE | 0.374 | 0.374 | ✅ PASS | Trace link: [OUT_1::trace::29d554f3] emitted. |
| 782 | `DAX_13_53` | `audit_hash_prepare` | RECURSE | 0.374 | 0.374 | ✅ PASS | Audit hash prepared: ba8b049411bdb550 for layer OUT_1. |
| 783 | `DAX_13_54` | `telemetry_emit` | RECURSE | 0.374 | 0.374 | ✅ PASS | Telemetry: layer=OUT_1, logic=0.0, assumption_integrity=0.55, ts=1782526860.43. |
| 784 | `DAX_13_55` | `layer_output_write` | RECURSE | 0.374 | 0.374 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=OUT_1, score=0.0. |
| 785 | `DAX_13_15` | `claim_assumption_bind` | RECURSE | 0.374 | 0.374 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 786 | `DAX_13_16` | `dependency_graph_update` | RECURSE | 0.374 | 0.372 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 787 | `DAX_13_17` | `priority_weight` | RECURSE | 0.372 | 0.372 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 788 | `DAX_13_18` | `risk_weight` | RECURSE | 0.372 | 0.372 | ⚠️ [OUT_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 789 | `DAX_13_19` | `confidence_weight` | RECURSE | 0.372 | 0.372 | ✅ PASS | Confidence weight: 1.0. |
| 790 | `DAX_13_20` | `evidence_requirement_map` | RECURSE | 0.372 | 0.372 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 791 | `DAX_13_21` | `evidence_presence_check` | RECURSE | 0.372 | 0.372 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 792 | `DAX_13_22` | `evidence_quality_score` | RECURSE | 0.372 | 0.372 | ✅ PASS | Evidence quality score: 1.0. |
| 793 | `DAX_13_23` | `ambiguity_probe` | RECURSE | 0.372 | 0.372 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 794 | `DAX_13_24` | `contradiction_probe` | RECURSE | 0.372 | 0.372 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 795 | `DAX_13_25` | `logic_validity_check` | RECURSE | 0.372 | 0.372 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 796 | `DAX_13_26` | `causal_chain_check` | RECURSE | 0.372 | 0.37 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 797 | `DAX_13_27` | `counterexample_generate` | RECURSE | 0.37 | 0.37 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 798 | `DAX_13_28` | `adversarial_attack` | RECURSE | 0.37 | 0.37 | ⚠️ [OUT_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 799 | `DAX_13_29` | `bias_frame_audit` | RECURSE | 0.37 | 0.37 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 800 | `DAX_13_30` | `safety_policy_check` | RECURSE | 0.37 | 0.37 | ⚠️ [OUT_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 801 | `DAX_13_31` | `feasibility_check` | RECURSE | 0.37 | 0.37 | ⚠️ [OUT_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 802 | `DAX_13_32` | `resource_cost_estimate` | RECURSE | 0.37 | 0.37 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 803 | `DAX_13_33` | `volatility_score` | RECURSE | 0.37 | 0.37 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 804 | `DAX_13_34` | `coherence_score` | RECURSE | 0.37 | 0.37 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 805 | `DAX_13_35` | `survivability_score` | RECURSE | 0.37 | 0.37 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 806 | `DAX_13_36` | `uncertainty_register_update` | RECURSE | 0.37 | 0.37 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 807 | `DAX_13_37` | `warning_emit` | RECURSE | 0.37 | 0.37 | ⚠️ [OUT_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 808 | `DAX_13_38` | `recovery_path_generate` | RECURSE | 0.37 | 0.37 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 809 | `DAX_13_39` | `claim_refine` | RECURSE | 0.37 | 0.372 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 810 | `DAX_13_40` | `claim_split` | RECURSE | 0.372 | 0.372 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 811 | `DAX_13_41` | `claim_merge` | RECURSE | 0.372 | 0.372 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 812 | `DAX_13_42` | `falsification_test_define` | RECURSE | 0.372 | 0.372 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 813 | `DAX_13_43` | `scenario_low_run` | RECURSE | 0.372 | 0.372 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 814 | `DAX_13_44` | `scenario_base_run` | RECURSE | 0.372 | 0.37 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 815 | `DAX_13_45` | `scenario_high_run` | RECURSE | 0.37 | 0.37 | ⚠️ [OUT_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 816 | `DAX_13_46` | `downstream_effect_scan` | RECURSE | 0.37 | 0.37 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 817 | `DAX_13_47` | `stakeholder_impact_scan` | RECURSE | 0.37 | 0.37 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 818 | `DAX_13_48` | `decision_threshold_check` | RECURSE | 0.37 | 0.37 | ⚠️ [OUT_1] Threshold check: BLOCK — combined score 0.27 be | Decision threshold: gate=BLOCK, combined_score=0.27. |
| 819 | `DAX_13_49` | `gate_recommendation` | RECURSE | 0.37 | 0.37 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 820 | `DAX_13_50` | `recursion_trigger_check` | RECURSE | 0.37 | 0.37 | ✅ PASS | Recursion trigger: No recursion required.. |
| 821 | `DAX_13_51` | `recursion_payload_build` | RECURSE | 0.37 | 0.37 | ✅ PASS | Recursion payload: Built for layer OUT_1. Target: ambiguity reduction and evidence sourcin |
| 822 | `DAX_13_52` | `trace_link_emit` | RECURSE | 0.37 | 0.37 | ✅ PASS | Trace link: [OUT_1::trace::29d554f3] emitted. |
| 823 | `DAX_13_53` | `audit_hash_prepare` | RECURSE | 0.37 | 0.37 | ✅ PASS | Audit hash prepared: ba8b049411bdb550 for layer OUT_1. |
| 824 | `DAX_13_54` | `telemetry_emit` | RECURSE | 0.37 | 0.37 | ✅ PASS | Telemetry: layer=OUT_1, logic=0.0, assumption_integrity=0.55, ts=1782526860.44. |
| 825 | `DAX_13_55` | `layer_output_write` | RECURSE | 0.37 | 0.37 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=OUT_1, score=0.0. |

---

## RIL_1 — Recursion Integrity Layer
*110 tiles executed | 18 flagged | 92 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 826 | `DAX_14_01` | `intake_snapshot` | RECURSE | 0.37 | 0.37 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=RIL_1. |
| 827 | `DAX_14_01` | `intake_snapshot` | RECURSE | 0.37 | 0.37 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=RIL_1. |
| 828 | `DAX_14_02` | `normalize_input` | RECURSE | 0.37 | 0.37 | ✅ PASS | Normalization check: Input is clean. |
| 829 | `DAX_14_03` | `domain_classify` | RECURSE | 0.37 | 0.37 | ⚠️ [RIL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 830 | `DAX_14_04` | `entity_extract` | RECURSE | 0.37 | 0.37 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 831 | `DAX_14_05` | `claim_extract` | RECURSE | 0.37 | 0.37 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 832 | `DAX_14_06` | `question_extract` | RECURSE | 0.37 | 0.37 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 833 | `DAX_14_07` | `goal_extract` | RECURSE | 0.37 | 0.368 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 834 | `DAX_14_08` | `constraint_extract` | RECURSE | 0.368 | 0.368 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 835 | `DAX_14_09` | `scope_define` | RECURSE | 0.368 | 0.368 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 836 | `DAX_14_10` | `context_link` | RECURSE | 0.368 | 0.368 | ✅ PASS | Context link: Layer RIL_1 chained to upstream state. |
| 837 | `DAX_14_11` | `assumption_list` | RECURSE | 0.368 | 0.368 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 838 | `DAX_14_12` | `assumption_classify` | RECURSE | 0.368 | 0.368 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 839 | `DAX_14_13` | `hidden_premise_scan` | RECURSE | 0.368 | 0.362 | ⚠️ [RIL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 840 | `DAX_14_14` | `assumption_confidence_score` | RECURSE | 0.362 | 0.362 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 841 | `DAX_14_15` | `claim_assumption_bind` | RECURSE | 0.362 | 0.362 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 842 | `DAX_14_16` | `dependency_graph_update` | RECURSE | 0.362 | 0.36 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 843 | `DAX_14_17` | `priority_weight` | RECURSE | 0.36 | 0.36 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 844 | `DAX_14_18` | `risk_weight` | RECURSE | 0.36 | 0.36 | ⚠️ [RIL_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 845 | `DAX_14_19` | `confidence_weight` | RECURSE | 0.36 | 0.36 | ✅ PASS | Confidence weight: 1.0. |
| 846 | `DAX_14_20` | `evidence_requirement_map` | RECURSE | 0.36 | 0.36 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 847 | `DAX_14_21` | `evidence_presence_check` | RECURSE | 0.36 | 0.36 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 848 | `DAX_14_22` | `evidence_quality_score` | RECURSE | 0.36 | 0.36 | ✅ PASS | Evidence quality score: 1.0. |
| 849 | `DAX_14_23` | `ambiguity_probe` | RECURSE | 0.36 | 0.36 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 850 | `DAX_14_24` | `contradiction_probe` | RECURSE | 0.36 | 0.36 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 851 | `DAX_14_25` | `logic_validity_check` | RECURSE | 0.36 | 0.36 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 852 | `DAX_14_26` | `causal_chain_check` | RECURSE | 0.36 | 0.358 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 853 | `DAX_14_27` | `counterexample_generate` | RECURSE | 0.358 | 0.358 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 854 | `DAX_14_28` | `adversarial_attack` | RECURSE | 0.358 | 0.358 | ⚠️ [RIL_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 855 | `DAX_14_29` | `bias_frame_audit` | RECURSE | 0.358 | 0.358 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 856 | `DAX_14_30` | `safety_policy_check` | RECURSE | 0.358 | 0.358 | ⚠️ [RIL_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 857 | `DAX_14_31` | `feasibility_check` | RECURSE | 0.358 | 0.358 | ⚠️ [RIL_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 858 | `DAX_14_32` | `resource_cost_estimate` | RECURSE | 0.358 | 0.358 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 859 | `DAX_14_33` | `volatility_score` | RECURSE | 0.358 | 0.358 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 860 | `DAX_14_34` | `coherence_score` | RECURSE | 0.358 | 0.358 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 861 | `DAX_14_35` | `survivability_score` | RECURSE | 0.358 | 0.358 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 862 | `DAX_14_36` | `uncertainty_register_update` | RECURSE | 0.358 | 0.358 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 863 | `DAX_14_37` | `warning_emit` | RECURSE | 0.358 | 0.358 | ⚠️ [RIL_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 864 | `DAX_14_38` | `recovery_path_generate` | RECURSE | 0.358 | 0.358 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 865 | `DAX_14_39` | `claim_refine` | RECURSE | 0.358 | 0.36 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 866 | `DAX_14_40` | `claim_split` | RECURSE | 0.36 | 0.36 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 867 | `DAX_14_41` | `claim_merge` | RECURSE | 0.36 | 0.36 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 868 | `DAX_14_42` | `falsification_test_define` | RECURSE | 0.36 | 0.36 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 869 | `DAX_14_43` | `scenario_low_run` | RECURSE | 0.36 | 0.36 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 870 | `DAX_14_44` | `scenario_base_run` | RECURSE | 0.36 | 0.358 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 871 | `DAX_14_45` | `scenario_high_run` | RECURSE | 0.358 | 0.358 | ⚠️ [RIL_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 872 | `DAX_14_46` | `downstream_effect_scan` | RECURSE | 0.358 | 0.358 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 873 | `DAX_14_47` | `stakeholder_impact_scan` | RECURSE | 0.358 | 0.358 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 874 | `DAX_14_48` | `decision_threshold_check` | RECURSE | 0.358 | 0.358 | ⚠️ [RIL_1] Threshold check: BLOCK — combined score 0.26 be | Decision threshold: gate=BLOCK, combined_score=0.26. |
| 875 | `DAX_14_49` | `gate_recommendation` | RECURSE | 0.358 | 0.358 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 876 | `DAX_14_50` | `recursion_trigger_check` | RECURSE | 0.358 | 0.358 | ✅ PASS | Recursion trigger: No recursion required.. |
| 877 | `DAX_14_51` | `recursion_payload_build` | RECURSE | 0.358 | 0.358 | ✅ PASS | Recursion payload: Built for layer RIL_1. Target: ambiguity reduction and evidence sourcin |
| 878 | `DAX_14_52` | `trace_link_emit` | RECURSE | 0.358 | 0.358 | ✅ PASS | Trace link: [RIL_1::trace::29d554f3] emitted. |
| 879 | `DAX_14_53` | `audit_hash_prepare` | RECURSE | 0.358 | 0.358 | ✅ PASS | Audit hash prepared: 2338438717cf417c for layer RIL_1. |
| 880 | `DAX_14_54` | `telemetry_emit` | RECURSE | 0.358 | 0.358 | ✅ PASS | Telemetry: layer=RIL_1, logic=0.0, assumption_integrity=0.52, ts=1782526860.45. |
| 881 | `DAX_14_55` | `layer_output_write` | RECURSE | 0.358 | 0.358 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=RIL_1, score=0.0. |
| 882 | `DAX_14_02` | `normalize_input` | RECURSE | 0.358 | 0.358 | ✅ PASS | Normalization check: Input is clean. |
| 883 | `DAX_14_03` | `domain_classify` | RECURSE | 0.358 | 0.358 | ⚠️ [RIL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 884 | `DAX_14_04` | `entity_extract` | RECURSE | 0.358 | 0.358 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 885 | `DAX_14_05` | `claim_extract` | RECURSE | 0.358 | 0.358 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 886 | `DAX_14_06` | `question_extract` | RECURSE | 0.358 | 0.358 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 887 | `DAX_14_07` | `goal_extract` | RECURSE | 0.358 | 0.356 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 888 | `DAX_14_08` | `constraint_extract` | RECURSE | 0.356 | 0.356 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 889 | `DAX_14_09` | `scope_define` | RECURSE | 0.356 | 0.356 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 890 | `DAX_14_10` | `context_link` | RECURSE | 0.356 | 0.356 | ✅ PASS | Context link: Layer RIL_1 chained to upstream state. |
| 891 | `DAX_14_11` | `assumption_list` | RECURSE | 0.356 | 0.356 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 892 | `DAX_14_12` | `assumption_classify` | RECURSE | 0.356 | 0.356 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 893 | `DAX_14_13` | `hidden_premise_scan` | RECURSE | 0.356 | 0.35 | ⚠️ [RIL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 894 | `DAX_14_14` | `assumption_confidence_score` | RECURSE | 0.35 | 0.35 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 895 | `DAX_14_15` | `claim_assumption_bind` | RECURSE | 0.35 | 0.35 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 896 | `DAX_14_16` | `dependency_graph_update` | RECURSE | 0.35 | 0.348 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 897 | `DAX_14_17` | `priority_weight` | RECURSE | 0.348 | 0.348 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 898 | `DAX_14_18` | `risk_weight` | RECURSE | 0.348 | 0.348 | ⚠️ [RIL_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 899 | `DAX_14_19` | `confidence_weight` | RECURSE | 0.348 | 0.348 | ✅ PASS | Confidence weight: 1.0. |
| 900 | `DAX_14_20` | `evidence_requirement_map` | RECURSE | 0.348 | 0.348 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 901 | `DAX_14_21` | `evidence_presence_check` | RECURSE | 0.348 | 0.348 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 902 | `DAX_14_22` | `evidence_quality_score` | RECURSE | 0.348 | 0.348 | ✅ PASS | Evidence quality score: 1.0. |
| 903 | `DAX_14_23` | `ambiguity_probe` | RECURSE | 0.348 | 0.348 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 904 | `DAX_14_24` | `contradiction_probe` | RECURSE | 0.348 | 0.348 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 905 | `DAX_14_25` | `logic_validity_check` | RECURSE | 0.348 | 0.348 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 906 | `DAX_14_26` | `causal_chain_check` | RECURSE | 0.348 | 0.346 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 907 | `DAX_14_27` | `counterexample_generate` | RECURSE | 0.346 | 0.346 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 908 | `DAX_14_28` | `adversarial_attack` | RECURSE | 0.346 | 0.346 | ⚠️ [RIL_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 909 | `DAX_14_29` | `bias_frame_audit` | RECURSE | 0.346 | 0.346 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 910 | `DAX_14_30` | `safety_policy_check` | RECURSE | 0.346 | 0.346 | ⚠️ [RIL_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 911 | `DAX_14_31` | `feasibility_check` | RECURSE | 0.346 | 0.346 | ⚠️ [RIL_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 912 | `DAX_14_32` | `resource_cost_estimate` | RECURSE | 0.346 | 0.346 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 913 | `DAX_14_33` | `volatility_score` | RECURSE | 0.346 | 0.346 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 914 | `DAX_14_34` | `coherence_score` | RECURSE | 0.346 | 0.346 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 915 | `DAX_14_35` | `survivability_score` | RECURSE | 0.346 | 0.346 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 916 | `DAX_14_36` | `uncertainty_register_update` | RECURSE | 0.346 | 0.346 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 917 | `DAX_14_37` | `warning_emit` | RECURSE | 0.346 | 0.346 | ⚠️ [RIL_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 918 | `DAX_14_38` | `recovery_path_generate` | RECURSE | 0.346 | 0.346 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 919 | `DAX_14_39` | `claim_refine` | RECURSE | 0.346 | 0.348 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 920 | `DAX_14_40` | `claim_split` | RECURSE | 0.348 | 0.348 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 921 | `DAX_14_41` | `claim_merge` | RECURSE | 0.348 | 0.348 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 922 | `DAX_14_42` | `falsification_test_define` | RECURSE | 0.348 | 0.348 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 923 | `DAX_14_43` | `scenario_low_run` | RECURSE | 0.348 | 0.348 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 924 | `DAX_14_44` | `scenario_base_run` | RECURSE | 0.348 | 0.346 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 925 | `DAX_14_45` | `scenario_high_run` | RECURSE | 0.346 | 0.346 | ⚠️ [RIL_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 926 | `DAX_14_46` | `downstream_effect_scan` | RECURSE | 0.346 | 0.346 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 927 | `DAX_14_47` | `stakeholder_impact_scan` | RECURSE | 0.346 | 0.346 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 928 | `DAX_14_48` | `decision_threshold_check` | RECURSE | 0.346 | 0.346 | ⚠️ [RIL_1] Threshold check: BLOCK — combined score 0.24 be | Decision threshold: gate=BLOCK, combined_score=0.24. |
| 929 | `DAX_14_49` | `gate_recommendation` | RECURSE | 0.346 | 0.346 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 930 | `DAX_14_50` | `recursion_trigger_check` | RECURSE | 0.346 | 0.346 | ✅ PASS | Recursion trigger: No recursion required.. |
| 931 | `DAX_14_51` | `recursion_payload_build` | RECURSE | 0.346 | 0.346 | ✅ PASS | Recursion payload: Built for layer RIL_1. Target: ambiguity reduction and evidence sourcin |
| 932 | `DAX_14_52` | `trace_link_emit` | RECURSE | 0.346 | 0.346 | ✅ PASS | Trace link: [RIL_1::trace::29d554f3] emitted. |
| 933 | `DAX_14_53` | `audit_hash_prepare` | RECURSE | 0.346 | 0.346 | ✅ PASS | Audit hash prepared: 2338438717cf417c for layer RIL_1. |
| 934 | `DAX_14_54` | `telemetry_emit` | RECURSE | 0.346 | 0.346 | ✅ PASS | Telemetry: layer=RIL_1, logic=0.0, assumption_integrity=0.49, ts=1782526860.46. |
| 935 | `DAX_14_55` | `layer_output_write` | RECURSE | 0.346 | 0.346 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=RIL_1, score=0.0. |

---

## IAL_1 — Incentive Alignment Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 936 | `DAX_15_01` | `intake_snapshot` | RECURSE | 0.346 | 0.346 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=IAL_1. |
| 937 | `DAX_15_02` | `normalize_input` | RECURSE | 0.346 | 0.346 | ✅ PASS | Normalization check: Input is clean. |
| 938 | `DAX_15_03` | `domain_classify` | RECURSE | 0.346 | 0.346 | ⚠️ [IAL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 939 | `DAX_15_04` | `entity_extract` | RECURSE | 0.346 | 0.346 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 940 | `DAX_15_05` | `claim_extract` | RECURSE | 0.346 | 0.346 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 941 | `DAX_15_06` | `question_extract` | RECURSE | 0.346 | 0.346 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 942 | `DAX_15_07` | `goal_extract` | RECURSE | 0.346 | 0.344 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 943 | `DAX_15_08` | `constraint_extract` | RECURSE | 0.344 | 0.344 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 944 | `DAX_15_09` | `scope_define` | RECURSE | 0.344 | 0.344 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 945 | `DAX_15_10` | `context_link` | RECURSE | 0.344 | 0.344 | ✅ PASS | Context link: Layer IAL_1 chained to upstream state. |
| 946 | `DAX_15_11` | `assumption_list` | RECURSE | 0.344 | 0.344 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 947 | `DAX_15_12` | `assumption_classify` | RECURSE | 0.344 | 0.344 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 948 | `DAX_15_13` | `hidden_premise_scan` | RECURSE | 0.344 | 0.338 | ⚠️ [IAL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 949 | `DAX_15_14` | `assumption_confidence_score` | RECURSE | 0.338 | 0.338 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 950 | `DAX_15_15` | `claim_assumption_bind` | RECURSE | 0.338 | 0.338 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 951 | `DAX_15_16` | `dependency_graph_update` | RECURSE | 0.338 | 0.336 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 952 | `DAX_15_17` | `priority_weight` | RECURSE | 0.336 | 0.336 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 953 | `DAX_15_18` | `risk_weight` | RECURSE | 0.336 | 0.336 | ⚠️ [IAL_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 954 | `DAX_15_19` | `confidence_weight` | RECURSE | 0.336 | 0.336 | ✅ PASS | Confidence weight: 1.0. |
| 955 | `DAX_15_20` | `evidence_requirement_map` | RECURSE | 0.336 | 0.336 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 956 | `DAX_15_21` | `evidence_presence_check` | RECURSE | 0.336 | 0.336 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 957 | `DAX_15_22` | `evidence_quality_score` | RECURSE | 0.336 | 0.336 | ✅ PASS | Evidence quality score: 1.0. |
| 958 | `DAX_15_23` | `ambiguity_probe` | RECURSE | 0.336 | 0.336 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 959 | `DAX_15_24` | `contradiction_probe` | RECURSE | 0.336 | 0.336 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 960 | `DAX_15_25` | `logic_validity_check` | RECURSE | 0.336 | 0.336 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 961 | `DAX_15_26` | `causal_chain_check` | RECURSE | 0.336 | 0.334 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 962 | `DAX_15_27` | `counterexample_generate` | RECURSE | 0.334 | 0.334 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 963 | `DAX_15_28` | `adversarial_attack` | RECURSE | 0.334 | 0.334 | ⚠️ [IAL_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 964 | `DAX_15_29` | `bias_frame_audit` | RECURSE | 0.334 | 0.334 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 965 | `DAX_15_30` | `safety_policy_check` | RECURSE | 0.334 | 0.334 | ⚠️ [IAL_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 966 | `DAX_15_31` | `feasibility_check` | RECURSE | 0.334 | 0.334 | ⚠️ [IAL_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 967 | `DAX_15_32` | `resource_cost_estimate` | RECURSE | 0.334 | 0.334 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 968 | `DAX_15_33` | `volatility_score` | RECURSE | 0.334 | 0.334 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 969 | `DAX_15_34` | `coherence_score` | RECURSE | 0.334 | 0.334 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 970 | `DAX_15_35` | `survivability_score` | RECURSE | 0.334 | 0.334 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 971 | `DAX_15_36` | `uncertainty_register_update` | RECURSE | 0.334 | 0.334 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 972 | `DAX_15_37` | `warning_emit` | RECURSE | 0.334 | 0.334 | ⚠️ [IAL_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 973 | `DAX_15_38` | `recovery_path_generate` | RECURSE | 0.334 | 0.334 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 974 | `DAX_15_39` | `claim_refine` | RECURSE | 0.334 | 0.336 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 975 | `DAX_15_40` | `claim_split` | RECURSE | 0.336 | 0.336 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 976 | `DAX_15_41` | `claim_merge` | RECURSE | 0.336 | 0.336 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 977 | `DAX_15_42` | `falsification_test_define` | RECURSE | 0.336 | 0.336 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 978 | `DAX_15_43` | `scenario_low_run` | RECURSE | 0.336 | 0.336 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 979 | `DAX_15_44` | `scenario_base_run` | RECURSE | 0.336 | 0.334 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 980 | `DAX_15_45` | `scenario_high_run` | RECURSE | 0.334 | 0.334 | ⚠️ [IAL_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 981 | `DAX_15_46` | `downstream_effect_scan` | RECURSE | 0.334 | 0.334 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 982 | `DAX_15_47` | `stakeholder_impact_scan` | RECURSE | 0.334 | 0.334 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 983 | `DAX_15_48` | `decision_threshold_check` | RECURSE | 0.334 | 0.334 | ⚠️ [IAL_1] Threshold check: BLOCK — combined score 0.23 be | Decision threshold: gate=BLOCK, combined_score=0.23. |
| 984 | `DAX_15_49` | `gate_recommendation` | RECURSE | 0.334 | 0.334 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 985 | `DAX_15_50` | `recursion_trigger_check` | RECURSE | 0.334 | 0.334 | ✅ PASS | Recursion trigger: No recursion required.. |
| 986 | `DAX_15_51` | `recursion_payload_build` | RECURSE | 0.334 | 0.334 | ✅ PASS | Recursion payload: Built for layer IAL_1. Target: ambiguity reduction and evidence sourcin |
| 987 | `DAX_15_52` | `trace_link_emit` | RECURSE | 0.334 | 0.334 | ✅ PASS | Trace link: [IAL_1::trace::29d554f3] emitted. |
| 988 | `DAX_15_53` | `audit_hash_prepare` | RECURSE | 0.334 | 0.334 | ✅ PASS | Audit hash prepared: 177101d242c68714 for layer IAL_1. |
| 989 | `DAX_15_54` | `telemetry_emit` | RECURSE | 0.334 | 0.334 | ✅ PASS | Telemetry: layer=IAL_1, logic=0.0, assumption_integrity=0.46, ts=1782526860.47. |
| 990 | `DAX_15_55` | `layer_output_write` | RECURSE | 0.334 | 0.334 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=IAL_1, score=0.0. |

---

## AOG_1 — Authority Output Gate Layer
*55 tiles executed | 9 flagged | 46 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 991 | `DAX_16_01` | `intake_snapshot` | RECURSE | 0.334 | 0.334 | ✅ PASS | Snapshot: 290 words, 2004 chars. Layer=AOG_1. |
| 992 | `DAX_16_02` | `normalize_input` | RECURSE | 0.334 | 0.334 | ✅ PASS | Normalization check: Input is clean. |
| 993 | `DAX_16_03` | `domain_classify` | RECURSE | 0.334 | 0.334 | ⚠️ [AOG_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, human/organizational. |
| 994 | `DAX_16_04` | `entity_extract` | RECURSE | 0.334 | 0.334 | ✅ PASS | Entities extracted: State, Independent, Legal, Instructions, Evidence, Vendor, Mark, Stop, |
| 995 | `DAX_16_05` | `claim_extract` | RECURSE | 0.334 | 0.334 | ✅ PASS | Claim extraction: 0 absolute claim(s) flagged. |
| 996 | `DAX_16_06` | `question_extract` | RECURSE | 0.334 | 0.334 | ✅ PASS | Questions found: 0 explicit, 0 implicit decision demand(s). |
| 997 | `DAX_16_07` | `goal_extract` | RECURSE | 0.334 | 0.332 | ✅ PASS | Goal extraction: No explicit goal — may be exploratory. |
| 998 | `DAX_16_08` | `constraint_extract` | RECURSE | 0.332 | 0.332 | ✅ PASS | Constraints: 1 scope limiter(s), 9 negation(s) detected. |
| 999 | `DAX_16_09` | `scope_define` | RECURSE | 0.332 | 0.332 | ✅ PASS | Scope: 1 boundary marker(s) present. |
| 1000 | `DAX_16_10` | `context_link` | RECURSE | 0.332 | 0.332 | ✅ PASS | Context link: Layer AOG_1 chained to upstream state. |
| 1001 | `DAX_16_11` | `assumption_list` | RECURSE | 0.332 | 0.332 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 1002 | `DAX_16_12` | `assumption_classify` | RECURSE | 0.332 | 0.332 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 1003 | `DAX_16_13` | `hidden_premise_scan` | RECURSE | 0.332 | 0.326 | ⚠️ [AOG_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 1004 | `DAX_16_14` | `assumption_confidence_score` | RECURSE | 0.326 | 0.326 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 1005 | `DAX_16_15` | `claim_assumption_bind` | RECURSE | 0.326 | 0.326 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 1006 | `DAX_16_16` | `dependency_graph_update` | RECURSE | 0.326 | 0.324 | ✅ PASS | Dependency graph: 0 causal link(s) detected and registered. |
| 1007 | `DAX_16_17` | `priority_weight` | RECURSE | 0.324 | 0.324 | ✅ PASS | Priority weight: urgency score=1. Elevated priority detected. |
| 1008 | `DAX_16_18` | `risk_weight` | RECURSE | 0.324 | 0.324 | ⚠️ [AOG_1] 2 high-risk operation term(s) detected. | Risk weight: 2 high-risk term(s). Gate elevation: YES. |
| 1009 | `DAX_16_19` | `confidence_weight` | RECURSE | 0.324 | 0.324 | ✅ PASS | Confidence weight: 1.0. |
| 1010 | `DAX_16_20` | `evidence_requirement_map` | RECURSE | 0.324 | 0.324 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 1011 | `DAX_16_21` | `evidence_presence_check` | RECURSE | 0.324 | 0.324 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 1012 | `DAX_16_22` | `evidence_quality_score` | RECURSE | 0.324 | 0.324 | ✅ PASS | Evidence quality score: 1.0. |
| 1013 | `DAX_16_23` | `ambiguity_probe` | RECURSE | 0.324 | 0.324 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 1014 | `DAX_16_24` | `contradiction_probe` | RECURSE | 0.324 | 0.324 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 1015 | `DAX_16_25` | `logic_validity_check` | RECURSE | 0.324 | 0.324 | ✅ PASS | Logic validity: 0 causal link(s) present. Support: YES. |
| 1016 | `DAX_16_26` | `causal_chain_check` | RECURSE | 0.324 | 0.322 | ✅ PASS | Causal chain: 0 causal link(s) traced. |
| 1017 | `DAX_16_27` | `counterexample_generate` | RECURSE | 0.322 | 0.322 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 1018 | `DAX_16_28` | `adversarial_attack` | RECURSE | 0.322 | 0.322 | ⚠️ [AOG_1] Adversarial risk: 2 high-risk operation(s) in i | Adversarial attack: injection=0, risk_ops=2. |
| 1019 | `DAX_16_29` | `bias_frame_audit` | RECURSE | 0.322 | 0.322 | ✅ PASS | Bias frame audit: absolute=0, urgency=1, total bias indicators=1. |
| 1020 | `DAX_16_30` | `safety_policy_check` | RECURSE | 0.322 | 0.322 | ⚠️ [AOG_1] SAFETY: 2 destructive/privileged operation term | Safety check: PII=False, risk_ops=2, injections=0. |
| 1021 | `DAX_16_31` | `feasibility_check` | RECURSE | 0.322 | 0.322 | ⚠️ [AOG_1] Low feasibility: action is under-specified. | Feasibility: Vague or under-specified — low feasibility. |
| 1022 | `DAX_16_32` | `resource_cost_estimate` | RECURSE | 0.322 | 0.322 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, risk ops: 2. |
| 1023 | `DAX_16_33` | `volatility_score` | RECURSE | 0.322 | 0.322 | ✅ PASS | Volatility score: 0.35 (urgency=1, vague=0, risk_ops=2). |
| 1024 | `DAX_16_34` | `coherence_score` | RECURSE | 0.322 | 0.322 | ✅ PASS | Coherence score: 0.87. Contradiction signal: False. |
| 1025 | `DAX_16_35` | `survivability_score` | RECURSE | 0.322 | 0.322 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 1026 | `DAX_16_36` | `uncertainty_register_update` | RECURSE | 0.322 | 0.322 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 1027 | `DAX_16_37` | `warning_emit` | RECURSE | 0.322 | 0.322 | ⚠️ [AOG_1] WARNING: 2 risk-flagged term(s) in input. | Warning emit: 1 warning(s) generated. |
| 1028 | `DAX_16_38` | `recovery_path_generate` | RECURSE | 0.322 | 0.322 | ✅ PASS | Recovery paths: 2 recovery option(s) registered for risk mitigation. |
| 1029 | `DAX_16_39` | `claim_refine` | RECURSE | 0.322 | 0.324 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 1030 | `DAX_16_40` | `claim_split` | RECURSE | 0.324 | 0.324 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 1031 | `DAX_16_41` | `claim_merge` | RECURSE | 0.324 | 0.324 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 1032 | `DAX_16_42` | `falsification_test_define` | RECURSE | 0.324 | 0.324 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 1033 | `DAX_16_43` | `scenario_low_run` | RECURSE | 0.324 | 0.324 | ✅ PASS | Scenario LOW: WARN — 2 risk term(s) present even in conservative scenario.. |
| 1034 | `DAX_16_44` | `scenario_base_run` | RECURSE | 0.324 | 0.322 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 1035 | `DAX_16_45` | `scenario_high_run` | RECURSE | 0.322 | 0.322 | ⚠️ [AOG_1] Scenario HIGH: Hostile scenario score=4. Surviv | Scenario HIGH (hostile): score=4. Result: FAIL. |
| 1036 | `DAX_16_46` | `downstream_effect_scan` | RECURSE | 0.322 | 0.322 | ✅ PASS | Downstream effects: 2 potential second-order effect(s) detected (risk_ops=2, causal_chains |
| 1037 | `DAX_16_47` | `stakeholder_impact_scan` | RECURSE | 0.322 | 0.322 | ✅ PASS | Stakeholder impact: 3 stakeholder class(es) identified: customer, board, vendor. |
| 1038 | `DAX_16_48` | `decision_threshold_check` | RECURSE | 0.322 | 0.322 | ⚠️ [AOG_1] Threshold check: BLOCK — combined score 0.21 be | Decision threshold: gate=BLOCK, combined_score=0.21. |
| 1039 | `DAX_16_49` | `gate_recommendation` | RECURSE | 0.322 | 0.322 | ✅ PASS | Gate recommendation: WARN (inject=0, risk=2, vague=0). |
| 1040 | `DAX_16_50` | `recursion_trigger_check` | RECURSE | 0.322 | 0.322 | ✅ PASS | Recursion trigger: No recursion required.. |
| 1041 | `DAX_16_51` | `recursion_payload_build` | RECURSE | 0.322 | 0.322 | ✅ PASS | Recursion payload: Built for layer AOG_1. Target: ambiguity reduction and evidence sourcin |
| 1042 | `DAX_16_52` | `trace_link_emit` | RECURSE | 0.322 | 0.322 | ✅ PASS | Trace link: [AOG_1::trace::29d554f3] emitted. |
| 1043 | `DAX_16_53` | `audit_hash_prepare` | RECURSE | 0.322 | 0.322 | ✅ PASS | Audit hash prepared: eaec7c6e957a3757 for layer AOG_1. |
| 1044 | `DAX_16_54` | `telemetry_emit` | RECURSE | 0.322 | 0.322 | ✅ PASS | Telemetry: layer=AOG_1, logic=0.0, assumption_integrity=0.43, ts=1782526860.47. |
| 1045 | `DAX_16_55` | `layer_output_write` | RECURSE | 0.322 | 0.322 | ✅ PASS | Layer output written: status=UNDER_REVIEW, layer=AOG_1, score=0.0. |

---

## SYSTEM — Post-Layer System Operations
*6 tiles executed | 2 flagged | 4 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 1046 | `SYS_881` | `final_scoring` | PASS | 0.322 | 0.322 | ✅ PASS | Final TOTAL_STABILITY computed: 0.322. Logic=0.0, Assumption=0.43. |
| 1047 | `SYS_882` | `authority_assignment` | BLOCK | 0.322 | 0.322 | ⚠️ Authority restricted to BLOCKED | Authority level assigned: BLOCKED (score=0.322). |
| 1048 | `SYS_883` | `audit_manifest_build` | PASS | 0.322 | 0.322 | ✅ PASS | Audit manifest built. Trace entries=1047, manifest_hash=499acba8f861454b. |
| 1049 | `SYS_884` | `release_lock_evaluation` | CAUTION | 0.322 | 0.322 | ⚠️ Release blocked: score 0.322 < 0.80 threshold.; Release blocked: warning rate 0.355 exceeds 0.15 limit. | Release lock: HELD. Warning rate=0.355. |
| 1050 | `SYS_885` | `reentry_hook_registration` | PASS | 0.322 | 0.322 | ✅ PASS | Re-entry hooks registered: 2. reentry::score_below_threshold::0.322, reentry::recursion_de |
| 1051 | `SYS_886` | `memory_boundary_commit` | PASS | 0.322 | 0.322 | ✅ PASS | Memory boundary committed. Retained=['run_id', 'final_gate', 'final_stability_score', 'aut |

---
