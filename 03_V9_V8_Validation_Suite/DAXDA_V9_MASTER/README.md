# DAXDA-o V9 Master — External Evaluation Candidate

This is a stabilized reference candidate, not an external-validation result.

An explicitly developer-authored 16-case preflight scored V9 16/16 and frozen
V7 6/16 after V9 repairs. This is only a smoke/regression result and must not be
presented as external evidence.

## Architecture

- 16 named governance layers × 55 documented tile slots + 6 post-layer operations = 886 operations.
- Genuine Cl(2,0) multivectors with geometric product, reversion, grade projection, norm, normalization, and rotor action.
- Provenance is evaluated separately from semantic content.
- Untrusted metadata/tool/external data cannot become controlling instructions.
- Detection, context qualification, geometric transformation, and policy gating are separate stages.
- Every layer emits a SHA-256 receipt.

## Evaluation

The evaluator supplies a hidden JSONL corpus using `evaluator_corpus_template.jsonl`, freezes labels before execution, and runs:

`python3 compare_v7_v9.py hidden.jsonl --v7 ../DAXDA_V7_MASTER/daxda_engine_v7.py --out sealed_results.json`

The harness compares the exact frozen V7 artifact with V9. It does not generate labels, delete failures, or claim independence.

## Claim boundary

Results produced on a developer-authored corpus are internal preflight results. Only an evaluator-controlled corpus, independent adjudication, frozen hashes, and auditable custody can support an independent-validation claim.
