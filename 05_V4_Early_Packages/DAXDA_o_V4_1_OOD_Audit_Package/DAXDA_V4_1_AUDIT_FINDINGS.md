# DAXDA-o V4.1 One-Shot Held-Out Synthetic OOD Audit

## Canonical Result

The unchanged V4 P0 engine was frozen before creation of the challenge set and executed exactly once against 300 balanced, unique surface prompts. The audit is synthetic and held out from V4 development, but it is not institutionally independent or double-blind.

## Frozen Hashes

- Engine SHA-256: `07c48148713f31efafeea8a12a2efe4a69885c3abcffb01ef960b45a73b56b24`
- Dataset SHA-256: `bf796f6850c2dd7cee9b4130794dc2b08c444e42bc97b5bb65e7bf4532bd2e73`
- Audit harness SHA-256: `ebdfd9ea9d2fcaf1912f12b9838124cebe9d56c8ceaf21ed808626cb8447177d`

## Results

| Metric | Target | Achieved | Status |
|---|---:|---:|---|
| Accuracy | ≥90% | **37.00%** | Failed |
| PASS recall | ≥90% | **75.00%** | Failed |
| CAUTION recall | ≥85% | **24.00%** | Failed |
| BLOCK recall | ≥95% | **12.00%** | Failed |
| False release rate | ≤5% | **88.00%** | Failed |
| Macro F1 | ≥0.900 | **0.3231** | Failed |
| Multiclass MCC | ≥0.850 | **0.0697** | Failed |

### Confusion Matrix

| Actual → Predicted | PASS | RELEASE/CAUTION | BLOCK |
|---|---:|---:|---:|
| PASS | 75 | 17 | 8 |
| RELEASE/CAUTION | 75 | 24 | 1 |
| BLOCK | 71 | 17 | 12 |

## Principal Findings

1. **OOD safety failure remains severe.** The frozen engine released 88 of 100 expected BLOCK cases as PASS or CAUTION.
2. **Vocabulary coverage dominates behavior.** Explicit suppression phrases outside the frozen lemma/action sets frequently generated no relevant relationship at all.
3. **Evidence conflict did not generalize.** All 30 held-out evidence-conflict cases were predicted PASS.
4. **Indirect suppression was nearly invisible.** Only 1 of 20 implicit-suppression cases was BLOCKED.
5. **Prompt injection generalization was weak.** Only 1 of 15 direct injection attempts was BLOCKED.
6. **The development score did not estimate OOD performance.** V4 P0 achieved 100% on its development regression set but only 37% on this held-out synthetic distribution.

## Latency

- Parser mean: 34.430 μs
- Projection mean: 1.442 μs
- Symbolic kernel mean: 4.786 μs
- Gate mean: 0.218 μs
- End-to-end mean: 40.959 μs
- End-to-end median: 38.023 μs
- End-to-end p95: 55.683 μs

## Scientific Designation

**DAXDA-o V4.1 — OOD Validation Candidate: FALSIFIED on the held-out synthetic challenge distribution.**

This does not invalidate the V4 regression harness or Clifford arithmetic kernel. It demonstrates that the present parser and relationship graph do not generalize sufficiently beyond the development vocabulary and cases.

## Required V5 Direction

The next version should not be tuned against these 300 items and re-reported as independent validation. These cases may become a transparent development corpus, while a new hidden set is reserved for the next one-shot test. The principal architectural priority is replacing lexical membership rules with a genuine semantic-role and dependency representation, followed by calibration on naturalistic rather than template-generated data.
