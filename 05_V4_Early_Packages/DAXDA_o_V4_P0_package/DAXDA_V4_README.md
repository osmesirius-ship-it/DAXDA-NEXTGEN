# DAXDA-o V4 P0 Canonical Development Reference

## Scope

This package is a deterministic development regression harness for the five-stage DAXDA-o prototype:

1. Semantic and relationship parsing
2. Structured relationship graph construction
3. Graph-to-state projection
4. `Cl(2,0) × R_>=0` state evolution
5. Deterministic governance gating

The evaluation file is external to the implementation and protected by a hard-coded SHA-256 digest. It is a **development benchmark**, not an independently authored or blinded scientific evaluation.

## Files

- `daxda_empirical_research_suite_v4.py` — executable benchmark and engine prototype
- `daxda_v4_frozen_eval.json` — 120-case balanced frozen development dataset
- `daxda_v4_benchmark_report.json` — full per-case output, metrics, state diagnostics, and timing
- `daxda_v4_misclassifications.json` — errors-only report; empty in the current run

## Run

From the directory containing all files:

    python3 daxda_empirical_research_suite_v4.py

The process exits with an assertion failure when any P0 target is missed.

## Current verified development-set result

- Accuracy: 100.00% (120/120)
- PASS recall: 100.00%
- RELEASE/CAUTION recall: 100.00%
- BLOCK recall: 100.00%
- False release rate: 0.00% (0/40)
- Macro F1: 1.0000
- Multiclass MCC: 1.0000
- Cross-label near-collisions under 0.05: 0/4,800
- Unique evolved states: 49/120

These values are valid only for the included development distribution. They do not establish out-of-distribution performance, independent validation, general language understanding, or deployment safety.
