# DAXDA — FULL AUDIT TRAIL
## Test: stress_test_04
*2026-07-02 02:45:04 UTC*

| Metric | Value |
|---|---|
| Total Operations | 886 |
| Recursion Operations | 0 |
| Final Gate | **BLOCK** |
| Stability Score | **0.0** |
| Authority Level | **BLOCKED** |
| Unique Material Findings | **17** |
| Recursive Recurrence Events | 195 |

**Legend:** ✅ clean &nbsp;|&nbsp; ⚠️ flagged &nbsp;|&nbsp; Score = TOTAL_STABILITY at tile entry/exit

---

## FDL_1 — Frame Detection Layer
*55 tiles | 11 flagged | 44 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 1 | `DAX_01_01` | `intake_snapshot` | PASS | DR:1.00 | DR:1.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=FDL_1. |
| 2 | `DAX_01_02` | `normalize_input` | WARN | DR:1.00 | DR:0.98 | ⚠️ Leading/trailing whitespace detected; Irregular whitespace detected | Normalization check: Leading/trailing whitespace detected, Irregular whitespace detected. |
| 3 | `DAX_01_03` | `domain_classify` | WARN | DR:0.98 | DR:0.96 | ⚠️ [FDL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 4 | `DAX_01_04` | `entity_extract` | PASS | DR:0.96 | DR:0.96 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 5 | `DAX_01_05` | `claim_extract` | WARN | DR:0.96 | DR:0.92 | ⚠️ [FDL_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 6 | `DAX_01_06` | `question_extract` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 7 | `DAX_01_07` | `goal_extract` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 8 | `DAX_01_08` | `constraint_extract` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 9 | `DAX_01_09` | `scope_define` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 10 | `DAX_01_10` | `context_link` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Context link: Layer FDL_1 chained to upstream state. |
| 11 | `DAX_01_11` | `assumption_list` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 12 | `DAX_01_12` | `assumption_classify` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 13 | `DAX_01_13` | `hidden_premise_scan` | WARN | DR:0.92 | DR:0.92 | ⚠️ [FDL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 14 | `DAX_01_14` | `assumption_confidence_score` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 15 | `DAX_01_15` | `claim_assumption_bind` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 16 | `DAX_01_16` | `dependency_graph_update` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 17 | `DAX_01_17` | `priority_weight` | PASS | DR:0.92 | DR:0.92 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 18 | `DAX_01_18` | `risk_weight` | WARN | DR:0.92 | DR:0.88 | ⚠️ [FDL_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 19 | `DAX_01_19` | `confidence_weight` | PASS | DR:0.88 | DR:0.88 | ✅ PASS | Confidence weight: 1.0. |
| 20 | `DAX_01_20` | `evidence_requirement_map` | PASS | DR:0.88 | DR:0.88 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 21 | `DAX_01_21` | `evidence_presence_check` | PASS | DR:0.88 | DR:0.88 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 22 | `DAX_01_22` | `evidence_quality_score` | PASS | DR:0.88 | DR:0.88 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 23 | `DAX_01_23` | `ambiguity_probe` | PASS | DR:0.88 | DR:0.88 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 24 | `DAX_01_24` | `contradiction_probe` | PASS | DR:0.88 | DR:0.88 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 25 | `DAX_01_25` | `logic_validity_check` | WARN | DR:0.88 | DR:0.85 | ⚠️ [FDL_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 26 | `DAX_01_26` | `causal_chain_check` | PASS | DR:0.85 | DR:0.85 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 27 | `DAX_01_27` | `counterexample_generate` | PASS | DR:0.85 | DR:0.85 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 28 | `DAX_01_28` | `adversarial_attack` | WARN | DR:0.85 | DR:0.70 | ⚠️ [FDL_1] ADVERSARIAL: Prompt-injection or override attem; [FDL_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 29 | `DAX_01_29` | `bias_frame_audit` | PASS | DR:0.70 | DR:0.70 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 30 | `DAX_01_30` | `safety_policy_check` | WARN | DR:0.70 | DR:0.70 | ⚠️ [FDL_1] SAFETY: 2 ['public', 'production'] destructive/; [FDL_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 31 | `DAX_01_31` | `feasibility_check` | PASS | DR:0.70 | DR:0.70 | ✅ PASS | Feasibility: Actionable. |
| 32 | `DAX_01_32` | `resource_cost_estimate` | PASS | DR:0.70 | DR:0.68 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 33 | `DAX_01_33` | `volatility_score` | PASS | DR:0.68 | DR:0.68 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 34 | `DAX_01_34` | `coherence_score` | PASS | DR:0.68 | DR:0.68 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 35 | `DAX_01_35` | `survivability_score` | PASS | DR:0.68 | DR:0.68 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 36 | `DAX_01_36` | `uncertainty_register_update` | PASS | DR:0.68 | DR:0.68 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 37 | `DAX_01_37` | `warning_emit` | WARN | DR:0.68 | DR:0.68 | ⚠️ [FDL_1] WARNING: 2 ['public', 'production'] input_threa; [FDL_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 38 | `DAX_01_38` | `recovery_path_generate` | PASS | DR:0.68 | DR:0.68 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 39 | `DAX_01_39` | `claim_refine` | PASS | DR:0.68 | DR:0.69 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 40 | `DAX_01_40` | `claim_split` | PASS | DR:0.69 | DR:0.69 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 41 | `DAX_01_41` | `claim_merge` | PASS | DR:0.69 | DR:0.69 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 42 | `DAX_01_42` | `falsification_test_define` | PASS | DR:0.69 | DR:0.69 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 43 | `DAX_01_43` | `scenario_low_run` | PASS | DR:0.69 | DR:0.67 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 44 | `DAX_01_44` | `scenario_base_run` | PASS | DR:0.67 | DR:0.65 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 45 | `DAX_01_45` | `scenario_high_run` | WARN | DR:0.65 | DR:0.45 | ⚠️ [FDL_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 46 | `DAX_01_46` | `downstream_effect_scan` | PASS | DR:0.45 | DR:0.43 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 47 | `DAX_01_47` | `stakeholder_impact_scan` | PASS | DR:0.43 | DR:0.43 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 48 | `DAX_01_48` | `decision_threshold_check` | PASS | DR:0.43 | DR:0.43 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 49 | `DAX_01_49` | `gate_recommendation` | WARN | DR:0.43 | DR:0.40 | ⚠️ [FDL_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 50 | `DAX_01_50` | `recursion_trigger_check` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Recursion trigger: No recursion required.. |
| 51 | `DAX_01_51` | `recursion_payload_build` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Recursion payload: Built for layer FDL_1. Target: ambiguity reduction and evidence sourcin |
| 52 | `DAX_01_52` | `trace_link_emit` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Trace link: [FDL_1::trace::7b59ae10] emitted. |
| 53 | `DAX_01_53` | `audit_hash_prepare` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Audit hash prepared: f4f138895c42d5c8 for layer FDL_1. |
| 54 | `DAX_01_54` | `telemetry_emit` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Telemetry: layer=FDL_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959342.23 |
| 55 | `DAX_01_55` | `layer_output_write` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Layer output written: status=GOVERNED, layer=FDL_1, score=0.9. |

---

## AML_1 — Assumption Map Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 56 | `DAX_02_01` | `intake_snapshot` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=AML_1. |
| 57 | `DAX_02_02` | `normalize_input` | PASS | DR:0.40 | DR:0.40 | ✅ PASS | Normalization check: Input is clean. |
| 58 | `DAX_02_03` | `domain_classify` | WARN | DR:0.40 | DR:0.38 | ⚠️ [AML_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 59 | `DAX_02_04` | `entity_extract` | PASS | DR:0.38 | DR:0.38 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 60 | `DAX_02_05` | `claim_extract` | WARN | DR:0.38 | DR:0.34 | ⚠️ [AML_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 61 | `DAX_02_06` | `question_extract` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 62 | `DAX_02_07` | `goal_extract` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 63 | `DAX_02_08` | `constraint_extract` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 64 | `DAX_02_09` | `scope_define` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 65 | `DAX_02_10` | `context_link` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Context link: Layer AML_1 chained to upstream state. |
| 66 | `DAX_02_11` | `assumption_list` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 67 | `DAX_02_12` | `assumption_classify` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 68 | `DAX_02_13` | `hidden_premise_scan` | WARN | DR:0.34 | DR:0.34 | ⚠️ [AML_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 69 | `DAX_02_14` | `assumption_confidence_score` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 70 | `DAX_02_15` | `claim_assumption_bind` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 71 | `DAX_02_16` | `dependency_graph_update` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 72 | `DAX_02_17` | `priority_weight` | PASS | DR:0.34 | DR:0.34 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 73 | `DAX_02_18` | `risk_weight` | WARN | DR:0.34 | DR:0.30 | ⚠️ [AML_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 74 | `DAX_02_19` | `confidence_weight` | PASS | DR:0.30 | DR:0.30 | ✅ PASS | Confidence weight: 1.0. |
| 75 | `DAX_02_20` | `evidence_requirement_map` | PASS | DR:0.30 | DR:0.30 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 76 | `DAX_02_21` | `evidence_presence_check` | PASS | DR:0.30 | DR:0.30 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 77 | `DAX_02_22` | `evidence_quality_score` | PASS | DR:0.30 | DR:0.30 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 78 | `DAX_02_23` | `ambiguity_probe` | PASS | DR:0.30 | DR:0.30 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 79 | `DAX_02_24` | `contradiction_probe` | PASS | DR:0.30 | DR:0.30 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 80 | `DAX_02_25` | `logic_validity_check` | WARN | DR:0.30 | DR:0.27 | ⚠️ [AML_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 81 | `DAX_02_26` | `causal_chain_check` | PASS | DR:0.27 | DR:0.27 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 82 | `DAX_02_27` | `counterexample_generate` | PASS | DR:0.27 | DR:0.27 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 83 | `DAX_02_28` | `adversarial_attack` | WARN | DR:0.27 | DR:0.12 | ⚠️ [AML_1] ADVERSARIAL: Prompt-injection or override attem; [AML_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 84 | `DAX_02_29` | `bias_frame_audit` | PASS | DR:0.12 | DR:0.12 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 85 | `DAX_02_30` | `safety_policy_check` | WARN | DR:0.12 | DR:0.12 | ⚠️ [AML_1] SAFETY: 2 ['public', 'production'] destructive/; [AML_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 86 | `DAX_02_31` | `feasibility_check` | PASS | DR:0.12 | DR:0.12 | ✅ PASS | Feasibility: Actionable. |
| 87 | `DAX_02_32` | `resource_cost_estimate` | PASS | DR:0.12 | DR:0.10 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 88 | `DAX_02_33` | `volatility_score` | PASS | DR:0.10 | DR:0.10 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 89 | `DAX_02_34` | `coherence_score` | PASS | DR:0.10 | DR:0.10 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 90 | `DAX_02_35` | `survivability_score` | PASS | DR:0.10 | DR:0.10 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 91 | `DAX_02_36` | `uncertainty_register_update` | PASS | DR:0.10 | DR:0.10 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 92 | `DAX_02_37` | `warning_emit` | WARN | DR:0.10 | DR:0.10 | ⚠️ [AML_1] WARNING: 2 ['public', 'production'] input_threa; [AML_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 93 | `DAX_02_38` | `recovery_path_generate` | PASS | DR:0.10 | DR:0.10 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 94 | `DAX_02_39` | `claim_refine` | PASS | DR:0.10 | DR:0.11 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 95 | `DAX_02_40` | `claim_split` | PASS | DR:0.11 | DR:0.11 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 96 | `DAX_02_41` | `claim_merge` | PASS | DR:0.11 | DR:0.11 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 97 | `DAX_02_42` | `falsification_test_define` | PASS | DR:0.11 | DR:0.11 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 98 | `DAX_02_43` | `scenario_low_run` | PASS | DR:0.11 | DR:0.09 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 99 | `DAX_02_44` | `scenario_base_run` | PASS | DR:0.09 | DR:0.07 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 100 | `DAX_02_45` | `scenario_high_run` | WARN | DR:0.07 | DR:0.00 | ⚠️ [AML_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 101 | `DAX_02_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 102 | `DAX_02_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 103 | `DAX_02_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 104 | `DAX_02_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AML_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 105 | `DAX_02_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 106 | `DAX_02_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer AML_1. Target: ambiguity reduction and evidence sourcin |
| 107 | `DAX_02_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [AML_1::trace::7b59ae10] emitted. |
| 108 | `DAX_02_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: a2279f3a937e6041 for layer AML_1. |
| 109 | `DAX_02_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=AML_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959402.29 |
| 110 | `DAX_02_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=AML_1, score=0.9. |

---

## AWP_1 — Claim Weighting Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 111 | `DAX_03_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=AWP_1. |
| 112 | `DAX_03_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 113 | `DAX_03_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 114 | `DAX_03_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 115 | `DAX_03_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 116 | `DAX_03_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 117 | `DAX_03_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 118 | `DAX_03_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 119 | `DAX_03_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 120 | `DAX_03_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer AWP_1 chained to upstream state. |
| 121 | `DAX_03_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 122 | `DAX_03_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 123 | `DAX_03_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 124 | `DAX_03_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 125 | `DAX_03_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 126 | `DAX_03_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 127 | `DAX_03_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 128 | `DAX_03_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 129 | `DAX_03_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 130 | `DAX_03_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 131 | `DAX_03_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 132 | `DAX_03_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 133 | `DAX_03_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 134 | `DAX_03_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 135 | `DAX_03_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 136 | `DAX_03_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 137 | `DAX_03_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 138 | `DAX_03_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] ADVERSARIAL: Prompt-injection or override attem; [AWP_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 139 | `DAX_03_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 140 | `DAX_03_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] SAFETY: 2 ['public', 'production'] destructive/; [AWP_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 141 | `DAX_03_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 142 | `DAX_03_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 143 | `DAX_03_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 144 | `DAX_03_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 145 | `DAX_03_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 146 | `DAX_03_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 147 | `DAX_03_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] WARNING: 2 ['public', 'production'] input_threa; [AWP_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 148 | `DAX_03_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 149 | `DAX_03_39` | `claim_refine` | PASS | DR:0.00 | DR:0.01 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 150 | `DAX_03_40` | `claim_split` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 151 | `DAX_03_41` | `claim_merge` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 152 | `DAX_03_42` | `falsification_test_define` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 153 | `DAX_03_43` | `scenario_low_run` | PASS | DR:0.01 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 154 | `DAX_03_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 155 | `DAX_03_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 156 | `DAX_03_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 157 | `DAX_03_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 158 | `DAX_03_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 159 | `DAX_03_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AWP_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 160 | `DAX_03_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 161 | `DAX_03_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer AWP_1. Target: ambiguity reduction and evidence sourcin |
| 162 | `DAX_03_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [AWP_1::trace::7b59ae10] emitted. |
| 163 | `DAX_03_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 6b1a09e0cc968256 for layer AWP_1. |
| 164 | `DAX_03_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=AWP_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959462.37 |
| 165 | `DAX_03_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=AWP_1, score=0.9. |

---

## BST_1 — Breaker Stress Test Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 166 | `DAX_04_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=BST_1. |
| 167 | `DAX_04_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 168 | `DAX_04_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 169 | `DAX_04_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 170 | `DAX_04_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 171 | `DAX_04_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 172 | `DAX_04_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 173 | `DAX_04_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 174 | `DAX_04_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 175 | `DAX_04_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer BST_1 chained to upstream state. |
| 176 | `DAX_04_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 177 | `DAX_04_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 178 | `DAX_04_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 179 | `DAX_04_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 180 | `DAX_04_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 181 | `DAX_04_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 182 | `DAX_04_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 183 | `DAX_04_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 184 | `DAX_04_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 185 | `DAX_04_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 186 | `DAX_04_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 187 | `DAX_04_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 188 | `DAX_04_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 189 | `DAX_04_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 190 | `DAX_04_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 191 | `DAX_04_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 192 | `DAX_04_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 193 | `DAX_04_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] ADVERSARIAL: Prompt-injection or override attem; [BST_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 194 | `DAX_04_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 195 | `DAX_04_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] SAFETY: 2 ['public', 'production'] destructive/; [BST_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 196 | `DAX_04_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 197 | `DAX_04_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 198 | `DAX_04_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 199 | `DAX_04_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 200 | `DAX_04_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 201 | `DAX_04_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 202 | `DAX_04_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] WARNING: 2 ['public', 'production'] input_threa; [BST_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 203 | `DAX_04_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 204 | `DAX_04_39` | `claim_refine` | PASS | DR:0.00 | DR:0.01 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 205 | `DAX_04_40` | `claim_split` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 206 | `DAX_04_41` | `claim_merge` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 207 | `DAX_04_42` | `falsification_test_define` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 208 | `DAX_04_43` | `scenario_low_run` | PASS | DR:0.01 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 209 | `DAX_04_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 210 | `DAX_04_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 211 | `DAX_04_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 212 | `DAX_04_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 213 | `DAX_04_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 214 | `DAX_04_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [BST_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 215 | `DAX_04_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 216 | `DAX_04_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer BST_1. Target: ambiguity reduction and evidence sourcin |
| 217 | `DAX_04_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [BST_1::trace::7b59ae10] emitted. |
| 218 | `DAX_04_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 87766c974461ac92 for layer BST_1. |
| 219 | `DAX_04_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=BST_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959522.45 |
| 220 | `DAX_04_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=BST_1, score=0.9. |

---

## CRL_1 — Claim Recovery Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 221 | `DAX_05_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=CRL_1. |
| 222 | `DAX_05_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 223 | `DAX_05_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 224 | `DAX_05_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 225 | `DAX_05_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 226 | `DAX_05_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 227 | `DAX_05_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 228 | `DAX_05_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 229 | `DAX_05_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 230 | `DAX_05_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer CRL_1 chained to upstream state. |
| 231 | `DAX_05_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 232 | `DAX_05_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 233 | `DAX_05_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 234 | `DAX_05_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 235 | `DAX_05_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 236 | `DAX_05_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 237 | `DAX_05_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 238 | `DAX_05_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 239 | `DAX_05_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 240 | `DAX_05_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 241 | `DAX_05_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 242 | `DAX_05_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 243 | `DAX_05_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 244 | `DAX_05_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 245 | `DAX_05_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 246 | `DAX_05_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 247 | `DAX_05_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 248 | `DAX_05_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] ADVERSARIAL: Prompt-injection or override attem; [CRL_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 249 | `DAX_05_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 250 | `DAX_05_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] SAFETY: 2 ['public', 'production'] destructive/; [CRL_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 251 | `DAX_05_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 252 | `DAX_05_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 253 | `DAX_05_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 254 | `DAX_05_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 255 | `DAX_05_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 256 | `DAX_05_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 257 | `DAX_05_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] WARNING: 2 ['public', 'production'] input_threa; [CRL_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 258 | `DAX_05_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 259 | `DAX_05_39` | `claim_refine` | PASS | DR:0.00 | DR:0.01 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 260 | `DAX_05_40` | `claim_split` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 261 | `DAX_05_41` | `claim_merge` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 262 | `DAX_05_42` | `falsification_test_define` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 263 | `DAX_05_43` | `scenario_low_run` | PASS | DR:0.01 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 264 | `DAX_05_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 265 | `DAX_05_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 266 | `DAX_05_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 267 | `DAX_05_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 268 | `DAX_05_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 269 | `DAX_05_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CRL_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 270 | `DAX_05_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 271 | `DAX_05_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer CRL_1. Target: ambiguity reduction and evidence sourcin |
| 272 | `DAX_05_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [CRL_1::trace::7b59ae10] emitted. |
| 273 | `DAX_05_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: d611686d4c58d83f for layer CRL_1. |
| 274 | `DAX_05_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=CRL_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959582.53 |
| 275 | `DAX_05_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=CRL_1, score=0.9. |

---

## MCS_1 — Monte Carlo Simulator Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 276 | `DAX_06_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=MCS_1. |
| 277 | `DAX_06_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 278 | `DAX_06_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 279 | `DAX_06_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 280 | `DAX_06_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 281 | `DAX_06_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 282 | `DAX_06_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 283 | `DAX_06_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 284 | `DAX_06_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 285 | `DAX_06_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer MCS_1 chained to upstream state. |
| 286 | `DAX_06_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 287 | `DAX_06_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 288 | `DAX_06_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 289 | `DAX_06_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 290 | `DAX_06_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 291 | `DAX_06_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 292 | `DAX_06_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 293 | `DAX_06_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 294 | `DAX_06_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 295 | `DAX_06_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 296 | `DAX_06_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 297 | `DAX_06_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 298 | `DAX_06_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 299 | `DAX_06_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 300 | `DAX_06_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 301 | `DAX_06_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 302 | `DAX_06_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 303 | `DAX_06_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] ADVERSARIAL: Prompt-injection or override attem; [MCS_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 304 | `DAX_06_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 305 | `DAX_06_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] SAFETY: 2 ['public', 'production'] destructive/; [MCS_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 306 | `DAX_06_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 307 | `DAX_06_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 308 | `DAX_06_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 309 | `DAX_06_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 310 | `DAX_06_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 311 | `DAX_06_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 312 | `DAX_06_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] WARNING: 2 ['public', 'production'] input_threa; [MCS_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 313 | `DAX_06_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 314 | `DAX_06_39` | `claim_refine` | PASS | DR:0.00 | DR:0.01 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 315 | `DAX_06_40` | `claim_split` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 316 | `DAX_06_41` | `claim_merge` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 317 | `DAX_06_42` | `falsification_test_define` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 318 | `DAX_06_43` | `scenario_low_run` | PASS | DR:0.01 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 319 | `DAX_06_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 320 | `DAX_06_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 321 | `DAX_06_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 322 | `DAX_06_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 323 | `DAX_06_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 324 | `DAX_06_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [MCS_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 325 | `DAX_06_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 326 | `DAX_06_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer MCS_1. Target: ambiguity reduction and evidence sourcin |
| 327 | `DAX_06_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [MCS_1::trace::7b59ae10] emitted. |
| 328 | `DAX_06_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: b1b1564e4256883c for layer MCS_1. |
| 329 | `DAX_06_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=MCS_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959642.61 |
| 330 | `DAX_06_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=MCS_1, score=0.9. |

---

## DSV_1 — Decision Valve Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 331 | `DAX_07_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=DSV_1. |
| 332 | `DAX_07_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 333 | `DAX_07_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 334 | `DAX_07_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 335 | `DAX_07_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 336 | `DAX_07_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 337 | `DAX_07_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 338 | `DAX_07_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 339 | `DAX_07_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 340 | `DAX_07_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer DSV_1 chained to upstream state. |
| 341 | `DAX_07_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 342 | `DAX_07_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 343 | `DAX_07_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 344 | `DAX_07_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 345 | `DAX_07_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 346 | `DAX_07_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 347 | `DAX_07_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 348 | `DAX_07_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 349 | `DAX_07_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 350 | `DAX_07_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 351 | `DAX_07_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 352 | `DAX_07_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 353 | `DAX_07_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 354 | `DAX_07_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 355 | `DAX_07_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 356 | `DAX_07_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 357 | `DAX_07_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 358 | `DAX_07_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] ADVERSARIAL: Prompt-injection or override attem; [DSV_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 359 | `DAX_07_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 360 | `DAX_07_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] SAFETY: 2 ['public', 'production'] destructive/; [DSV_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 361 | `DAX_07_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 362 | `DAX_07_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 363 | `DAX_07_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 364 | `DAX_07_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 365 | `DAX_07_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 366 | `DAX_07_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 367 | `DAX_07_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] WARNING: 2 ['public', 'production'] input_threa; [DSV_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 368 | `DAX_07_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 369 | `DAX_07_39` | `claim_refine` | PASS | DR:0.00 | DR:0.01 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 370 | `DAX_07_40` | `claim_split` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 371 | `DAX_07_41` | `claim_merge` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 372 | `DAX_07_42` | `falsification_test_define` | PASS | DR:0.01 | DR:0.01 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 373 | `DAX_07_43` | `scenario_low_run` | PASS | DR:0.01 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 374 | `DAX_07_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 375 | `DAX_07_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 376 | `DAX_07_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 377 | `DAX_07_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 378 | `DAX_07_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 379 | `DAX_07_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [DSV_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 380 | `DAX_07_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 381 | `DAX_07_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer DSV_1. Target: ambiguity reduction and evidence sourcin |
| 382 | `DAX_07_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [DSV_1::trace::7b59ae10] emitted. |
| 383 | `DAX_07_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: db56dedd413285c4 for layer DSV_1. |
| 384 | `DAX_07_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=DSV_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959702.77 |
| 385 | `DAX_07_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=DSV_1, score=0.9. |

---

## TRC_1 — Trace Consistency Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 386 | `DAX_08_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=TRC_1. |
| 387 | `DAX_08_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 388 | `DAX_08_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 389 | `DAX_08_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 390 | `DAX_08_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 391 | `DAX_08_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 392 | `DAX_08_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 393 | `DAX_08_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 394 | `DAX_08_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 395 | `DAX_08_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer TRC_1 chained to upstream state. |
| 396 | `DAX_08_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 397 | `DAX_08_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 398 | `DAX_08_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 399 | `DAX_08_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 400 | `DAX_08_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 401 | `DAX_08_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 402 | `DAX_08_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 403 | `DAX_08_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 404 | `DAX_08_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 405 | `DAX_08_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 406 | `DAX_08_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 407 | `DAX_08_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 408 | `DAX_08_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 409 | `DAX_08_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 410 | `DAX_08_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] Causal claims present without supporting eviden; [LLM::TRC_1::logic_validity_check] Network err: HTTPCon | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. / LLM override: |
| 411 | `DAX_08_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 412 | `DAX_08_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 413 | `DAX_08_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] ADVERSARIAL: Prompt-injection or override attem; [TRC_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 414 | `DAX_08_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 415 | `DAX_08_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] SAFETY: 2 ['public', 'production'] destructive/; [TRC_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 416 | `DAX_08_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 417 | `DAX_08_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 418 | `DAX_08_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 419 | `DAX_08_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 420 | `DAX_08_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 421 | `DAX_08_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 422 | `DAX_08_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] WARNING: 2 ['public', 'production'] input_threa; [TRC_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 423 | `DAX_08_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 424 | `DAX_08_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 425 | `DAX_08_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 426 | `DAX_08_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 427 | `DAX_08_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 428 | `DAX_08_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 429 | `DAX_08_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 430 | `DAX_08_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 431 | `DAX_08_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 432 | `DAX_08_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 433 | `DAX_08_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 434 | `DAX_08_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [TRC_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 435 | `DAX_08_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 436 | `DAX_08_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer TRC_1. Target: ambiguity reduction and evidence sourcin |
| 437 | `DAX_08_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [TRC_1::trace::7b59ae10] emitted. |
| 438 | `DAX_08_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 6dff522a2723c72d for layer TRC_1. |
| 439 | `DAX_08_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=TRC_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959762.91 |
| 440 | `DAX_08_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=TRC_1, score=0.9. |

---

## CON_1 — Contradiction Scan Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 441 | `DAX_09_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=CON_1. |
| 442 | `DAX_09_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 443 | `DAX_09_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 444 | `DAX_09_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 445 | `DAX_09_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 446 | `DAX_09_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 447 | `DAX_09_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 448 | `DAX_09_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 449 | `DAX_09_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 450 | `DAX_09_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer CON_1 chained to upstream state. |
| 451 | `DAX_09_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 452 | `DAX_09_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 453 | `DAX_09_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 454 | `DAX_09_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 455 | `DAX_09_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 456 | `DAX_09_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 457 | `DAX_09_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 458 | `DAX_09_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 459 | `DAX_09_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 460 | `DAX_09_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 461 | `DAX_09_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 462 | `DAX_09_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 463 | `DAX_09_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 464 | `DAX_09_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 465 | `DAX_09_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 466 | `DAX_09_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 467 | `DAX_09_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 468 | `DAX_09_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] ADVERSARIAL: Prompt-injection or override attem; [CON_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 469 | `DAX_09_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 470 | `DAX_09_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] SAFETY: 2 ['public', 'production'] destructive/; [CON_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 471 | `DAX_09_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 472 | `DAX_09_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 473 | `DAX_09_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 474 | `DAX_09_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 475 | `DAX_09_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 476 | `DAX_09_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 477 | `DAX_09_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] WARNING: 2 ['public', 'production'] input_threa; [CON_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 478 | `DAX_09_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 479 | `DAX_09_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 480 | `DAX_09_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 481 | `DAX_09_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 482 | `DAX_09_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 483 | `DAX_09_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 484 | `DAX_09_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 485 | `DAX_09_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 486 | `DAX_09_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 487 | `DAX_09_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 488 | `DAX_09_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 489 | `DAX_09_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [CON_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 490 | `DAX_09_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 491 | `DAX_09_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer CON_1. Target: ambiguity reduction and evidence sourcin |
| 492 | `DAX_09_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [CON_1::trace::7b59ae10] emitted. |
| 493 | `DAX_09_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 65b51d921430729c for layer CON_1. |
| 494 | `DAX_09_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=CON_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959823.05 |
| 495 | `DAX_09_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=CON_1, score=0.9. |

---

## EVD_1 — Evidence Demand Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 496 | `DAX_10_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=EVD_1. |
| 497 | `DAX_10_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 498 | `DAX_10_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 499 | `DAX_10_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 500 | `DAX_10_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 501 | `DAX_10_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 502 | `DAX_10_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 503 | `DAX_10_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 504 | `DAX_10_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 505 | `DAX_10_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer EVD_1 chained to upstream state. |
| 506 | `DAX_10_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 507 | `DAX_10_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 508 | `DAX_10_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 509 | `DAX_10_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 510 | `DAX_10_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 511 | `DAX_10_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 512 | `DAX_10_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 513 | `DAX_10_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 514 | `DAX_10_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 515 | `DAX_10_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 516 | `DAX_10_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 517 | `DAX_10_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 518 | `DAX_10_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 519 | `DAX_10_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 520 | `DAX_10_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 521 | `DAX_10_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 522 | `DAX_10_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 523 | `DAX_10_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] ADVERSARIAL: Prompt-injection or override attem; [EVD_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 524 | `DAX_10_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 525 | `DAX_10_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] SAFETY: 2 ['public', 'production'] destructive/; [EVD_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 526 | `DAX_10_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 527 | `DAX_10_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 528 | `DAX_10_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 529 | `DAX_10_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 530 | `DAX_10_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 531 | `DAX_10_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 532 | `DAX_10_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] WARNING: 2 ['public', 'production'] input_threa; [EVD_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 533 | `DAX_10_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 534 | `DAX_10_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 535 | `DAX_10_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 536 | `DAX_10_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 537 | `DAX_10_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 538 | `DAX_10_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 539 | `DAX_10_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 540 | `DAX_10_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 541 | `DAX_10_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 542 | `DAX_10_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 543 | `DAX_10_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 544 | `DAX_10_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [EVD_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 545 | `DAX_10_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 546 | `DAX_10_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer EVD_1. Target: ambiguity reduction and evidence sourcin |
| 547 | `DAX_10_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [EVD_1::trace::7b59ae10] emitted. |
| 548 | `DAX_10_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 2137970453dba9f8 for layer EVD_1. |
| 549 | `DAX_10_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=EVD_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959883.13 |
| 550 | `DAX_10_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=EVD_1, score=0.9. |

---

## REC_1 — Recursion Plan Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 551 | `DAX_11_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=REC_1. |
| 552 | `DAX_11_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 553 | `DAX_11_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 554 | `DAX_11_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 555 | `DAX_11_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 556 | `DAX_11_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 557 | `DAX_11_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 558 | `DAX_11_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 559 | `DAX_11_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 560 | `DAX_11_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer REC_1 chained to upstream state. |
| 561 | `DAX_11_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 562 | `DAX_11_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 563 | `DAX_11_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 564 | `DAX_11_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 565 | `DAX_11_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 566 | `DAX_11_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 567 | `DAX_11_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 568 | `DAX_11_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 569 | `DAX_11_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 570 | `DAX_11_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 571 | `DAX_11_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 572 | `DAX_11_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 573 | `DAX_11_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 574 | `DAX_11_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 575 | `DAX_11_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 576 | `DAX_11_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 577 | `DAX_11_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 578 | `DAX_11_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] ADVERSARIAL: Prompt-injection or override attem; [REC_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 579 | `DAX_11_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 580 | `DAX_11_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] SAFETY: 2 ['public', 'production'] destructive/; [REC_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 581 | `DAX_11_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 582 | `DAX_11_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 583 | `DAX_11_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 584 | `DAX_11_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 585 | `DAX_11_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 586 | `DAX_11_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 587 | `DAX_11_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] WARNING: 2 ['public', 'production'] input_threa; [REC_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 588 | `DAX_11_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 589 | `DAX_11_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 590 | `DAX_11_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 591 | `DAX_11_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 592 | `DAX_11_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 593 | `DAX_11_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 594 | `DAX_11_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 595 | `DAX_11_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 596 | `DAX_11_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 597 | `DAX_11_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 598 | `DAX_11_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 599 | `DAX_11_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [REC_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 600 | `DAX_11_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 601 | `DAX_11_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer REC_1. Target: ambiguity reduction and evidence sourcin |
| 602 | `DAX_11_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [REC_1::trace::7b59ae10] emitted. |
| 603 | `DAX_11_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 6de5c07bf65cdd51 for layer REC_1. |
| 604 | `DAX_11_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=REC_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782959943.26 |
| 605 | `DAX_11_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=REC_1, score=0.9. |

---

## GOV_1 — Governance Gate Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 606 | `DAX_12_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=GOV_1. |
| 607 | `DAX_12_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 608 | `DAX_12_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 609 | `DAX_12_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 610 | `DAX_12_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 611 | `DAX_12_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 612 | `DAX_12_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 613 | `DAX_12_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 614 | `DAX_12_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 615 | `DAX_12_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer GOV_1 chained to upstream state. |
| 616 | `DAX_12_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 617 | `DAX_12_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 618 | `DAX_12_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 619 | `DAX_12_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 620 | `DAX_12_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 621 | `DAX_12_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 622 | `DAX_12_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 623 | `DAX_12_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 624 | `DAX_12_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 625 | `DAX_12_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 626 | `DAX_12_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 627 | `DAX_12_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 628 | `DAX_12_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 629 | `DAX_12_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 630 | `DAX_12_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 631 | `DAX_12_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 632 | `DAX_12_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 633 | `DAX_12_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] ADVERSARIAL: Prompt-injection or override attem; [GOV_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 634 | `DAX_12_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 635 | `DAX_12_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] SAFETY: 2 ['public', 'production'] destructive/; [GOV_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 636 | `DAX_12_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 637 | `DAX_12_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 638 | `DAX_12_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 639 | `DAX_12_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 640 | `DAX_12_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 641 | `DAX_12_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 642 | `DAX_12_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] WARNING: 2 ['public', 'production'] input_threa; [GOV_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 643 | `DAX_12_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 644 | `DAX_12_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 645 | `DAX_12_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 646 | `DAX_12_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 647 | `DAX_12_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 648 | `DAX_12_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 649 | `DAX_12_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 650 | `DAX_12_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 651 | `DAX_12_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 652 | `DAX_12_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 653 | `DAX_12_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 654 | `DAX_12_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [GOV_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 655 | `DAX_12_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 656 | `DAX_12_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer GOV_1. Target: ambiguity reduction and evidence sourcin |
| 657 | `DAX_12_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [GOV_1::trace::7b59ae10] emitted. |
| 658 | `DAX_12_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 789f704f94a3a1a8 for layer GOV_1. |
| 659 | `DAX_12_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=GOV_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782960003.39 |
| 660 | `DAX_12_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=GOV_1, score=0.9. |

---

## OUT_1 — Output Record Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 661 | `DAX_13_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=OUT_1. |
| 662 | `DAX_13_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 663 | `DAX_13_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 664 | `DAX_13_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 665 | `DAX_13_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 666 | `DAX_13_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 667 | `DAX_13_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 668 | `DAX_13_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 669 | `DAX_13_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 670 | `DAX_13_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer OUT_1 chained to upstream state. |
| 671 | `DAX_13_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 672 | `DAX_13_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 673 | `DAX_13_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 674 | `DAX_13_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 675 | `DAX_13_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 676 | `DAX_13_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 677 | `DAX_13_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 678 | `DAX_13_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 679 | `DAX_13_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 680 | `DAX_13_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 681 | `DAX_13_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 682 | `DAX_13_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 683 | `DAX_13_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 684 | `DAX_13_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 685 | `DAX_13_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 686 | `DAX_13_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 687 | `DAX_13_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 688 | `DAX_13_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] ADVERSARIAL: Prompt-injection or override attem; [OUT_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 689 | `DAX_13_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 690 | `DAX_13_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] SAFETY: 2 ['public', 'production'] destructive/; [OUT_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 691 | `DAX_13_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 692 | `DAX_13_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 693 | `DAX_13_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 694 | `DAX_13_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 695 | `DAX_13_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 696 | `DAX_13_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 697 | `DAX_13_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] WARNING: 2 ['public', 'production'] input_threa; [OUT_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 698 | `DAX_13_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 699 | `DAX_13_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 700 | `DAX_13_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 701 | `DAX_13_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 702 | `DAX_13_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 703 | `DAX_13_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 704 | `DAX_13_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 705 | `DAX_13_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 706 | `DAX_13_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 707 | `DAX_13_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 708 | `DAX_13_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 709 | `DAX_13_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [OUT_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 710 | `DAX_13_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 711 | `DAX_13_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer OUT_1. Target: ambiguity reduction and evidence sourcin |
| 712 | `DAX_13_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [OUT_1::trace::7b59ae10] emitted. |
| 713 | `DAX_13_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: 716d08267e0f8624 for layer OUT_1. |
| 714 | `DAX_13_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=OUT_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782960063.48 |
| 715 | `DAX_13_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=OUT_1, score=0.9. |

---

## RIL_1 — Recursion Integrity Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 716 | `DAX_14_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=RIL_1. |
| 717 | `DAX_14_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 718 | `DAX_14_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 719 | `DAX_14_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 720 | `DAX_14_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 721 | `DAX_14_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 722 | `DAX_14_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 723 | `DAX_14_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 724 | `DAX_14_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 725 | `DAX_14_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer RIL_1 chained to upstream state. |
| 726 | `DAX_14_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 727 | `DAX_14_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 728 | `DAX_14_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 729 | `DAX_14_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 730 | `DAX_14_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 731 | `DAX_14_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 732 | `DAX_14_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 733 | `DAX_14_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 734 | `DAX_14_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 735 | `DAX_14_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 736 | `DAX_14_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 737 | `DAX_14_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 738 | `DAX_14_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 739 | `DAX_14_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 740 | `DAX_14_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 741 | `DAX_14_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 742 | `DAX_14_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 743 | `DAX_14_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] ADVERSARIAL: Prompt-injection or override attem; [RIL_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 744 | `DAX_14_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 745 | `DAX_14_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] SAFETY: 2 ['public', 'production'] destructive/; [RIL_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 746 | `DAX_14_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 747 | `DAX_14_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 748 | `DAX_14_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 749 | `DAX_14_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 750 | `DAX_14_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 751 | `DAX_14_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 752 | `DAX_14_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] WARNING: 2 ['public', 'production'] input_threa; [RIL_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 753 | `DAX_14_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 754 | `DAX_14_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 755 | `DAX_14_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 756 | `DAX_14_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 757 | `DAX_14_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 758 | `DAX_14_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 759 | `DAX_14_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 760 | `DAX_14_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 761 | `DAX_14_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 762 | `DAX_14_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 763 | `DAX_14_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 764 | `DAX_14_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [RIL_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 765 | `DAX_14_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 766 | `DAX_14_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer RIL_1. Target: ambiguity reduction and evidence sourcin |
| 767 | `DAX_14_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [RIL_1::trace::7b59ae10] emitted. |
| 768 | `DAX_14_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: ea73716b0f451e73 for layer RIL_1. |
| 769 | `DAX_14_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=RIL_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782960123.62 |
| 770 | `DAX_14_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=RIL_1, score=0.9. |

---

## IAL_1 — Incentive Alignment Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 771 | `DAX_15_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=IAL_1. |
| 772 | `DAX_15_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 773 | `DAX_15_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 774 | `DAX_15_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 775 | `DAX_15_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 776 | `DAX_15_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 777 | `DAX_15_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 778 | `DAX_15_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 779 | `DAX_15_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 780 | `DAX_15_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer IAL_1 chained to upstream state. |
| 781 | `DAX_15_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 782 | `DAX_15_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 783 | `DAX_15_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 784 | `DAX_15_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 785 | `DAX_15_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 786 | `DAX_15_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 787 | `DAX_15_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 788 | `DAX_15_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 789 | `DAX_15_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 790 | `DAX_15_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 791 | `DAX_15_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 792 | `DAX_15_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 793 | `DAX_15_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 794 | `DAX_15_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 795 | `DAX_15_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 796 | `DAX_15_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 797 | `DAX_15_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 798 | `DAX_15_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] ADVERSARIAL: Prompt-injection or override attem; [IAL_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 799 | `DAX_15_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 800 | `DAX_15_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] SAFETY: 2 ['public', 'production'] destructive/; [IAL_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 801 | `DAX_15_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 802 | `DAX_15_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 803 | `DAX_15_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 804 | `DAX_15_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 805 | `DAX_15_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 806 | `DAX_15_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 807 | `DAX_15_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] WARNING: 2 ['public', 'production'] input_threa; [IAL_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 808 | `DAX_15_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 809 | `DAX_15_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 810 | `DAX_15_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 811 | `DAX_15_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 812 | `DAX_15_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 813 | `DAX_15_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 814 | `DAX_15_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 815 | `DAX_15_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 816 | `DAX_15_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 817 | `DAX_15_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 818 | `DAX_15_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 819 | `DAX_15_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [IAL_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 820 | `DAX_15_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 821 | `DAX_15_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer IAL_1. Target: ambiguity reduction and evidence sourcin |
| 822 | `DAX_15_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [IAL_1::trace::7b59ae10] emitted. |
| 823 | `DAX_15_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: f25eecdc893a59c9 for layer IAL_1. |
| 824 | `DAX_15_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=IAL_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782960183.79 |
| 825 | `DAX_15_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=IAL_1, score=0.9. |

---

## AOG_1 — Authority Output Gate Layer
*55 tiles | 10 flagged | 45 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 826 | `DAX_16_01` | `intake_snapshot` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Snapshot: 1396 words, 10156 chars. Layer=AOG_1. |
| 827 | `DAX_16_02` | `normalize_input` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Normalization check: Input is clean. |
| 828 | `DAX_16_03` | `domain_classify` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] High-stakes domain detected: financial, legal/c | Domains classified: financial, legal/compliance, technical, human/organizational. |
| 829 | `DAX_16_04` | `entity_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Entities extracted: Why, Verifiable, Independent Run Decisions, No, Legal, Sections, Verif |
| 830 | `DAX_16_05` | `claim_extract` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] 2 strong assertive claim(s) detected without he | Claim extraction: 0 absolute + 2 assertive = 2 total claim(s) flagged. |
| 831 | `DAX_16_06` | `question_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Questions found: 0 explicit, 33 ['review', 'evaluate', 'approve', 'Audit', 'choose', 'Appr |
| 832 | `DAX_16_07` | `goal_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Goal extraction: Decision-oriented goal detected. |
| 833 | `DAX_16_08` | `constraint_extract` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Constraints: 1 ['merely'] scope limiter(s), 25 ['without', 'not', 'NONE', 'Not', 'No'] neg |
| 834 | `DAX_16_09` | `scope_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scope: 1 ['merely'] boundary marker(s) present. |
| 835 | `DAX_16_10` | `context_link` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Context link: Layer AOG_1 chained to upstream state. |
| 836 | `DAX_16_11` | `assumption_list` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption inventory: 0 absolute term(s) imply foundational assumptions. |
| 837 | `DAX_16_12` | `assumption_classify` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption types: financial, operational, ethical/legal. |
| 838 | `DAX_16_13` | `hidden_premise_scan` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] Hidden premise: urgency may be suppressing scru | Hidden premise scan: 1 hidden premise(s) exposed. |
| 839 | `DAX_16_14` | `assumption_confidence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Assumption confidence: 1.0 (0 vague qualifier(s) reduce confidence). |
| 840 | `DAX_16_15` | `claim_assumption_bind` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim-assumption binding: 0 claim(s) bound to foundational assumptions. |
| 841 | `DAX_16_16` | `dependency_graph_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Dependency graph: 3 ['so', 'because'] causal link(s) detected and registered. |
| 842 | `DAX_16_17` | `priority_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Priority weight: urgency score=1 ['must']. Elevated priority detected. |
| 843 | `DAX_16_18` | `risk_weight` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] 2 ['public', 'production'] high-input_threat op | Risk weight: 2 ['public', 'production'] high-input_threat term(s). Gate elevation: YES. |
| 844 | `DAX_16_19` | `confidence_weight` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Confidence weight: 1.0. |
| 845 | `DAX_16_20` | `evidence_requirement_map` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence required for 0 claim(s). Evidence burden is manageable. |
| 846 | `DAX_16_21` | `evidence_presence_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence presence: Evidence or data reference found. |
| 847 | `DAX_16_22` | `evidence_quality_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Evidence quality score: 1.0 (10 quality marker(s) for 2 ['does'] claim(s)). |
| 848 | `DAX_16_23` | `ambiguity_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Ambiguity probe: 0 vague qualifier(s). Ambiguity level: LOW. |
| 849 | `DAX_16_24` | `contradiction_probe` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Contradiction probe: No direct contradictions found. |
| 850 | `DAX_16_25` | `logic_validity_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] Causal claims present without supporting eviden | Logic validity: 3 ['so', 'because'] causal claim(s) lack explicit support. |
| 851 | `DAX_16_26` | `causal_chain_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Causal chain: 3 ['so', 'because'] causal link(s) traced. |
| 852 | `DAX_16_27` | `counterexample_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Counterexample generation: 0 absolute claim(s) are vulnerable to counterexample attack. |
| 853 | `DAX_16_28` | `adversarial_attack` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] ADVERSARIAL: Prompt-injection or override attem; [AOG_1] Adversarial input_threat: 2 ['public', 'product | Adversarial attack: injection=2 ['Do not follow', 'OVERRIDE'], input_threat_ops=2 ['public |
| 854 | `DAX_16_29` | `bias_frame_audit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Bias frame audit: absolute=0, urgency=1 ['must'], total bias indicators=1 ['must']. |
| 855 | `DAX_16_30` | `safety_policy_check` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] SAFETY: 2 ['public', 'production'] destructive/; [AOG_1] SAFETY: Instruction-injection pattern detected. | Safety check: PII=False, input_threat_ops=2 ['public', 'production'], injections=2 ['Do no |
| 856 | `DAX_16_31` | `feasibility_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Feasibility: Actionable. |
| 857 | `DAX_16_32` | `resource_cost_estimate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Resource cost estimate: HIGH. Financial ref: True, input_threat ops: 2 ['public', 'product |
| 858 | `DAX_16_33` | `volatility_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Volatility score: 0.35 (urgency=1 ['must'], vague=0, input_threat_ops=2 ['public', 'produc |
| 859 | `DAX_16_34` | `coherence_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Coherence score: 0.9. Contradiction signal: False. |
| 860 | `DAX_16_35` | `survivability_score` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Survivability: 0.9. Evidence support: True. |
| 861 | `DAX_16_36` | `uncertainty_register_update` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Uncertainty register: 0 unknown/uncertain element(s) recorded. |
| 862 | `DAX_16_37` | `warning_emit` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] WARNING: 2 ['public', 'production'] input_threa; [AOG_1] WARNING: 2 ['Do not follow', 'OVERRIDE'] advers | Warning emit: 2 warning(s) generated. |
| 863 | `DAX_16_38` | `recovery_path_generate` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recovery paths: 2 ['public', 'production'] recovery option(s) registered for input_threat  |
| 864 | `DAX_16_39` | `claim_refine` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim refinement: 0 absolute claim(s) flagged for downgrading to qualified form. |
| 865 | `DAX_16_40` | `claim_split` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim split: Complex input — splitting into sub-claims recommended.. |
| 866 | `DAX_16_41` | `claim_merge` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Claim merge: Compatible claims consolidated. No contradicting merges detected. |
| 867 | `DAX_16_42` | `falsification_test_define` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Falsification tests: 0 absolute claim(s) require falsification conditions before authority |
| 868 | `DAX_16_43` | `scenario_low_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario LOW: WARN — 2 ['public', 'production'] input_threat term(s) present even in conse |
| 869 | `DAX_16_44` | `scenario_base_run` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Scenario BASE: CAUTION — base scenario reveals actionability concerns.. |
| 870 | `DAX_16_45` | `scenario_high_run` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] Scenario HIGH: Hostile scenario score=10. Survi | Scenario HIGH (hostile): score=10. Result: FAIL. |
| 871 | `DAX_16_46` | `downstream_effect_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Downstream effects: 5 ['public', 'so', 'production', 'because'] potential second-order eff |
| 872 | `DAX_16_47` | `stakeholder_impact_scan` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Stakeholder impact: 2 stakeholder class(es) identified: public, vendor. |
| 873 | `DAX_16_48` | `decision_threshold_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Decision threshold: gate=PASS, combined_score=0.9. |
| 874 | `DAX_16_49` | `gate_recommendation` | WARN | DR:0.00 | DR:0.00 | ⚠️ [AOG_1] Gate recommendation: BLOCK. | Gate recommendation: BLOCK (inject=2 ['Do not follow', 'OVERRIDE'], input_threat=2 ['publi |
| 875 | `DAX_16_50` | `recursion_trigger_check` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion trigger: No recursion required.. |
| 876 | `DAX_16_51` | `recursion_payload_build` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Recursion payload: Built for layer AOG_1. Target: ambiguity reduction and evidence sourcin |
| 877 | `DAX_16_52` | `trace_link_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Trace link: [AOG_1::trace::7b59ae10] emitted. |
| 878 | `DAX_16_53` | `audit_hash_prepare` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Audit hash prepared: a38d29f48af7de4a for layer AOG_1. |
| 879 | `DAX_16_54` | `telemetry_emit` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Telemetry: layer=AOG_1, decision_readiness=0.9, evidence_sufficiency=0.9, ts=1782960244.08 |
| 880 | `DAX_16_55` | `layer_output_write` | PASS | DR:0.00 | DR:0.00 | ✅ PASS | Layer output written: status=GOVERNED, layer=AOG_1, score=0.9. |

---

## SYSTEM — Post-Layer System Operations
*6 tiles | 2 flagged | 4 clean*

| Op | Tile ID | Function | Gate | Score Before | Score After | Status | Reasoning |
|---|---|---|---|---|---|---|---|
| 881 | `SYS_881` | `final_scoring` | PASS | 0.0 | 0.0 | ✅ PASS | Final TOTAL_STABILITY computed: 0.0. Logic=1.0, Assumption=1.0. |
| 882 | `SYS_882` | `authority_assignment` | BLOCK | 0.0 | 0.0 | ⚠️ Authority restricted to BLOCKED | Authority assigned: BLOCKED. Status: BLOCKED. |
| 883 | `SYS_883` | `audit_manifest_build` | PASS | 0.0 | 0.0 | ✅ PASS | Audit manifest built. Trace entries=882, canonical_output_hash=3cba72cf31b36a6b. |
| 884 | `SYS_884` | `release_lock_evaluation` | BLOCK | 0.0 | 0.0 | ⚠️ Release lock HELD. Status: BLOCKED, Final Gate: BLOCK. | Release lock: HELD. Unique warning rate=0.018 (total=0.239, denominator=883 tiles). |
| 885 | `SYS_885` | `reentry_hook_registration` | PASS | 0.0 | 0.0 | ✅ PASS | Re-entry hooks registered: 1. reentry::score_below_threshold::0.0 |
| 886 | `SYS_886` | `memory_boundary_commit` | PASS | 0.0 | 0.0 | ✅ PASS | Memory boundary committed. Retained=['run_id', 'final_gate', 'final_stability_score', 'aut |

---
