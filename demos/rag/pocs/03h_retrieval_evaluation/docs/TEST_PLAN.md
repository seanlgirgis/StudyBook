# 03h Retrieval Evaluation Test Plan

## Test Plan Goal
Define validation strategy for `03h_retrieval_evaluation` implementation before code is written.

This step is documentation-only. Tests are not implemented yet.

## Documentation-Only Acceptance Checks (Current Step)
- `README.md` exists and explains purpose, inputs, outputs, success criteria, and non-goals.
- `docs/DESIGN.md` exists and explains evaluation-layer architecture and boundaries.
- `docs/CONTRACT.md` exists and defines planned input/output schemas and validation rules.
- `docs/TEST_PLAN.md` exists and defines future implementation test coverage.
- no implementation files are added in this step.

## Future Implementation Test Coverage

## Happy Path Cases
- expected chunk appears at rank 1 and all matches pass.
- expected chunk appears in top 3 (not rank 1) and metrics reflect partial ranking success.
- expected chunk appears in top 5 and decision/route both match expected.

## Rank Miss Cases
- expected chunk found at rank 1 (`hit_at_1=true`, `hit_at_3=true`, `hit_at_5=true`).
- expected chunk found at rank 2 or 3 (`hit_at_1=false`, `hit_at_3=true`, `hit_at_5=true`).
- expected chunk found at rank 4 or 5 (`hit_at_1=false`, `hit_at_3=false`, `hit_at_5=true`).
- expected chunk found below top 5 (`hit_at_5=false`).
- expected chunk missing from ranked results (`expected_chunk_found=false`, `expected_chunk_rank=null`).

## Decision Mismatch Cases
- retrieved chunk metrics pass, but `decision_label_match=false`.
- decision mismatches for ambiguity-sensitive queries (for example heater vs water heater phrasing).
- verify `failure_category=DECISION_LABEL_MISMATCH` and actionable reason text.
- verify expectation mismatches are marked `status=fail`, not `status=warning`.

## Route Mismatch Cases
- `decision_label_match=true` but `recommended_route_match=false`.
- verify route mismatch is tracked independently from label mismatch.
- ensure mismatch reason explains expected vs actual route.

## Missing Expected Chunk Cases
- expected chunk absent from `03f` results.
- case missing in 03f query outputs.
- case missing in 03g decision outputs.
- ensure correct failure categories:
  - `EXPECTED_CHUNK_NOT_FOUND`
  - `MISSING_CASE_IN_03F_OUTPUT`
  - `MISSING_CASE_IN_03G_OUTPUT`
- verify each failing case has one primary failure category.

## Warning-Only Data-Quality Cases
- matched via fallback `query` because `normalized_query` is missing, but expectations still pass -> `status=warning`.
- optional traceability metadata missing while core evaluation still works -> `status=warning`.
- duplicate-looking query text exists but fixture `case_id` is unique and deterministic alignment still works -> `status=warning`.
- verify warning cases set `failure_category=null` and `failure_reason=null`.
- verify warning context is not written into `failure_reason`.
- verify no `warning_details` field is expected yet.

## Failure Over Warning Precedence Cases
- case has warning condition plus expected chunk missing -> final `status=fail`.
- case has warning condition plus decision label mismatch -> final `status=fail`.
- verify warnings never hide failures.
- verify failed cases always include one primary `failure_category` and a short `failure_reason`.

## Malformed Fixture Cases
- duplicate `case_id`.
- empty query.
- missing `expected_chunk_id`.
- invalid `expected_decision_label` enum value.
- invalid `expected_recommended_route` enum value.
- ensure validation fails with clear contract errors.

## Regression Checks
- repeated runs with identical inputs produce identical metric outputs.
- aggregate totals equal number of evaluated cases.
- monotonic rank metric consistency:
  - `hit_at_1 <= hit_at_3 <= hit_at_5` (as rates)
- per-case matching alignment consistency:
  - primary fixture identity remains `case_id`
  - alignment key uses `normalized_query` when available, else `query`
- no silent schema drift when upstream 03f/03g fields change.

## Guardrail Checks
- confirm no LLM/API call path is required.
- confirm no threshold auto-tuning is performed.
- confirm no custom expected-rank target tuning logic is added.
- confirm no customer answer generation fields exist in outputs.
- confirm no live clarification interaction logic is invoked.
- confirm warning semantics remain non-contract/non-expectation only.

## Exit Criteria For Future Implementation Step
Implementation may be considered PASS when:
- fixture-driven evaluation runs successfully
- contract validations pass
- metric computations are correct and deterministic
- failure categorization is complete and explainable
- report artifacts are generated in expected structure

## Explicit Status
No tests are implemented in this design step. This file defines the intended future test suite only.
