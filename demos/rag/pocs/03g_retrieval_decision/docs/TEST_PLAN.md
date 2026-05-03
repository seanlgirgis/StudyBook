# 03g Retrieval Decision Test Plan

## Test Plan Goal
Validate that `03g` produces deterministic, explainable retrieval-quality decisions from `03f` hybrid retrieval evidence.

This test plan is design-only and defines future implementation checks.

## Acceptance Checks
- decision layer consumes `03f`-compatible input structure
- one decision label is produced per query
- decisions are deterministic for identical input/config
- evidence and reason codes are present and auditable
- non-goal boundaries are preserved (no answer generation, no LLM usage)

## Unit Test Scenarios

## Decision Label Assignment
- strong case: high top score, clear gap, low tie count -> `strong_match`
- ambiguous case: top scores close, several near ties -> `ambiguous_match`
- weak case: moderate evidence below confidence policy -> `weak_match`
- no match case: zero/near-zero evidence -> `no_match`
- clarification case: policy trigger on ambiguity/weakness -> `needs_clarification`

## Threshold Boundary Tests
- exact equality at each threshold boundary
- just below and just above each threshold
- ordering precedence when multiple rule conditions apply

## Score-Gap and Close-Candidate Tests
- large top gap with medium score should not be treated like tie plateau
- tiny top gap with many close candidates should map to ambiguity
- single candidate result set should handle missing rank-2 gap safely

## Source Diversity Tests
- concentrated top-k from one source family
- highly diverse top-k from many sources
- verify configured diversity threshold impact on ambiguity/clarification

## Contract Validation Tests
- missing required input fields fail with clear validation error
- malformed numeric types fail validation
- unknown decision label is rejected
- `selected_chunk_ids` contract behavior for `no_match` is enforced

## Determinism Tests
- repeated runs with same input/config produce identical output
- sorted input variants (already ranked vs explicitly re-ranked) produce same decision

## Non-Goal Guardrail Tests
- output has no answer text field
- output has no business-intent-finalization field
- no external model/API invocation path is required

## Edge Case Tests
- empty query string (if allowed upstream) with empty/noisy results
- empty `results` list
- all equal scores across top-k
- contradictory modality signal (high char, very low word)
- extremely large top-k input trimmed to decision window

## Integration-Style Scenarios (Fixture Driven)
Use fixed fixtures based on 03f-style outputs:
- clean query fixtures
- typo-heavy query fixtures
- ambiguous service-term fixtures (for example heater vs water heater)
- unrelated query fixtures

Expected:
- stable label
- clear reason codes
- evidence snapshot aligned to computed signals

## Traceability and Reporting
Each test failure should identify:
- query fixture id
- config version id
- expected label vs actual label
- evidence values that drove mismatch

This makes threshold tuning transparent during ladder progression.
