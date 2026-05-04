# 03h Retrieval Evaluation Design

## Problem
`03f` and `03g` currently produce useful outputs, but there is no standardized way to verify whether those outputs are correct for known expected cases.

Without an evaluation layer:
- retrieval quality can drift without detection
- decision logic regressions can go unnoticed
- threshold tuning discussions become subjective

## Conceptual Model
`03h` is an observer layer, not a generation layer.

It consumes:
1. labeled expected-case fixtures (ground truth contract)
2. retrieval results from `03f`
3. decision results from `03g`

It emits:
- per-case pass/fail signals
- aggregate metric summaries
- failure categories for triage

Per-case status is planned as:
- `pass`
- `fail`
- `warning`

Status policy:
- `pass`: all required expectations are met.
- `fail`: any expectation mismatch or required contract failure occurs.
- `warning`: only non-contract, non-expectation data-quality issues where evaluation still completes.
- warnings never override failures; if a case has both, final status is `fail`.
- `failure_category` and `failure_reason` are used only when status is `fail`.
- warning context is not stored in `failure_reason`; warning detail capture is deferred.

## Evaluation Flow
1. Load labeled fixture cases.
2. Load existing `03f` retrieval output (do not rebuild retrieval).
3. Load existing `03g` decision output (do not rerun decision logic).
4. Match each fixture case to retrieval/decision records with this identity strategy:
   - fixture primary identity: `case_id`
   - upstream alignment key (until upstream includes `case_id`): deterministic query key
   - preferred query key: `normalized_query`
   - fallback query key: `query`
   - no required output schema changes to `03f` or `03g` in this POC
5. Evaluate retrieval ranking expectations.
6. Evaluate decision label and recommended route expectations.
7. Assign failure categories/reasons for mismatches.
8. Produce structured report and human-readable summary.

## How 03f Retrieval Is Evaluated
For each labeled case, compare expected chunk identity to ranked retrieval results.

Primary checks:
- `expected_chunk_found`
- `expected_chunk_rank`
- `hit_at_1`
- `hit_at_3`
- `hit_at_5`

Rank behavior for this step:
- record actual expected chunk rank when present
- compute `hit_at_1`, `hit_at_3`, and `hit_at_5`
- do not introduce custom expected-rank target thresholds yet

Interpretation guidance:
- `hit_at_1=true` indicates strongest retrieval precision for that case.
- `hit_at_3`/`hit_at_5` capture near-miss quality and practical recoverability.
- rank misses identify where tuning may improve ordering without changing candidate generation.

## How 03g Retrieval Decision Is Evaluated
For each labeled case, compare expected policy outputs to actual `03g` outputs.

Primary checks:
- `decision_label_match`
- `recommended_route_match`

This separates two concerns:
- retrieval correctness (what was retrieved)
- decision correctness (how retrieval evidence was classified/routed)

## Failure Categories
Planned categories for triage:
- `EXPECTED_CHUNK_NOT_FOUND`
- `EXPECTED_CHUNK_RANK_TOO_LOW`
- `DECISION_LABEL_MISMATCH`
- `RECOMMENDED_ROUTE_MISMATCH`
- `MISSING_CASE_IN_03F_OUTPUT`
- `MISSING_CASE_IN_03G_OUTPUT`
- `MALFORMED_FIXTURE_CASE`

`failure_reason` should be short and actionable, tied to one primary category per case.
Each failed case should have one primary failure category.
Supporting details may be included in `failure_reason`.
Do not implement multi-category failure logic yet.

Failure vs warning rule:
- expectation mismatches and required-contract misses are always failures.
- examples of failures:
  - expected chunk not found
  - decision label mismatch
  - recommended route mismatch
  - missing required `03f` case
  - missing required `03g` case
  - malformed fixture case
- examples of warnings (non-failure data quality):
  - matched by fallback `query` because `normalized_query` was missing
  - optional traceability metadata missing while core evaluation still works
  - ambiguous duplicate-looking query text exists, but fixture `case_id` remains unique
- warning context is deferred until a future optional `warning_details` field is approved.
- do not add `warning_details` in this step.

## Threshold Tuning Notes (Later, Not in 03h Design Step)
`03h` should identify where thresholds may need tuning, but it should not tune automatically.

How `03h` supports later tuning:
- quantify mismatch patterns by category
- show where expected chunk is present but poorly ranked
- show where route/label mismatches cluster by query type

Out of scope for this step:
- automatic threshold optimization
- parameter search
- model-based judge

## Design Boundaries
`03h` is evaluation-only and deterministic.

Must not:
- call LLMs
- generate answers
- ask clarifying questions
- alter prior artifacts from `03d`-`03g`
- move work into `integrated/servicecall-ai`

## Teaching Explanation
Think of the retrieval ladder as a student and `03h` as the exam grader:
- `03f` answers: "which chunks seem relevant"
- `03g` answers: "how confident should we be"
- `03h` answers: "were those outputs correct for known expected cases"

This grading layer is what turns retrieval behavior into measurable engineering quality.
