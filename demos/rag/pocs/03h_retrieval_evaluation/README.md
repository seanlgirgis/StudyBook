# 03h_retrieval_evaluation

## What This POC Does
`03h_retrieval_evaluation` is a design-first evaluation layer for retrieval quality.

It evaluates existing outputs from:
- `03f_hybrid_retrieval` (retrieved chunk rankings)
- `03g_retrieval_decision` (decision label and recommended route)

This POC does not retrieve, decide, or answer customer questions by itself. It measures whether prior steps behaved as expected on labeled fixtures.

## Why Retrieval Evaluation Matters
Earlier POCs can produce outputs, but without a repeatable evaluation layer we cannot reliably answer:
- whether expected chunks are being surfaced
- whether ranking quality is improving or regressing
- whether decision/routing behavior matches expected policy

`03h` creates a measurable contract so future tuning decisions are evidence-based instead of intuition-based.

## Retrieval Ladder Position
- `03f_hybrid_retrieval`: produces ranked candidates
- `03g_retrieval_decision`: assigns retrieval quality label and route hint
- `03h_retrieval_evaluation`: scores both outputs against labeled expected cases

## Planned Inputs
- `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json`
- `pocs/03g_retrieval_decision/outputs/sample_retrieval_decisions.json`
- future fixture input (planned, not created yet):
  - `pocs/03h_retrieval_evaluation/fixtures/labeled_retrieval_cases.json`

Matching-key note for this POC:
- `case_id` is the primary fixture identity key.
- Because current `03f` and `03g` outputs may not include `case_id`, evaluation alignment may use a deterministic query key:
  - preferred key: `normalized_query`
  - fallback key: `query`
- `03h` should not require schema changes to `03f` or `03g` outputs in this step.

## Planned Metrics
- `hit_at_1`
- `hit_at_3`
- `hit_at_5`
- `expected_chunk_found`
- `expected_chunk_rank`
- `decision_label_match`
- `recommended_route_match`
- `failure_reason`

Per-case status semantics:
- `status="pass"` means the case met all required expectations.
- `status="fail"` means an actual expectation or required contract failed.
- `status="warning"` is reserved for non-contract, non-expectation data-quality conditions where evaluation still succeeds.
- expectation mismatches are failures, not warnings.
- warnings must not hide failures; if both occur, final status is `fail`.
- `failure_category` and `failure_reason` are fail-only fields:
  - if `status="pass"` or `status="warning"`, both must be `null`
  - if `status="fail"`, `failure_category` must have one primary category and `failure_reason` must have a short explanation

Rank-behavior scope note:
- `03h` records actual expected chunk rank and computes `hit_at_1`, `hit_at_3`, and `hit_at_5`.
- `03h` does not define custom expected-rank targets in this step.
- `03h` does not perform automatic threshold tuning.

## Planned Outputs (Not Created Yet)
- `pocs/03h_retrieval_evaluation/outputs/evaluation_report.json`
- `pocs/03h_retrieval_evaluation/outputs/evaluation_summary.md`

## What Success Means
- each labeled case can be evaluated deterministically
- retrieval ranking quality is measurable at top-1/top-3/top-5
- 03g decision behavior is measurable against expected labels/routes
- failures are categorized clearly for follow-up tuning discussion

## Non-Goals
`03h` must not:
- tune thresholds automatically
- call an LLM
- generate customer answers
- ask live clarification questions
- move anything into `integrated/servicecall-ai`
- rebuild `03d`, `03e`, `03f`, or `03g` artifacts

## Next Step After Design Approval
Implement evaluation schemas, fixture loader/validator, metric calculator, and report writer in `03h` using the contracts in `docs/CONTRACT.md` and checks in `docs/TEST_PLAN.md`.
