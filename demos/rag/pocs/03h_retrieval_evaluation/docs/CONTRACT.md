# 03h Retrieval Evaluation Contract

## Contract Purpose
Define planned input/output contracts for evaluating retrieval (`03f`) and retrieval decision (`03g`) against labeled fixtures.

This is a documentation-only contract for design approval.

## Planned Input Contracts

### 1) Labeled Fixture Cases (Planned)
Planned path (not created yet):
- `pocs/03h_retrieval_evaluation/fixtures/labeled_retrieval_cases.json`

Planned model name:
- `LabeledRetrievalCase`

Planned shape:
```json
{
  "case_id": "case_001",
  "query": "heater repaid",
  "normalized_query": "heater repaid",
  "expected_chunk_id": "heating_repair_overview__chunk_000",
  "expected_decision_label": "needs_clarification",
  "expected_recommended_route": "clarification_path",
  "notes": "Ambiguous phrase may map to heating or water heater intent"
}
```

Planned batch wrapper:
```json
{
  "poc": "03h_retrieval_evaluation",
  "fixture_version": "v1",
  "cases": []
}
```

Identity and alignment behavior:
- `case_id` is the primary identity key for each labeled fixture case.
- For this POC, upstream `03f` and `03g` outputs may not include `case_id`.
- Therefore, case alignment may use deterministic query keys:
  - preferred: `normalized_query`
  - fallback: `query`
- `03h` should not require changes to current `03f` or `03g` output contracts.

### 2) 03f Retrieval Output Input
Expected source artifact:
- `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json`

Expected per-query minimum fields:
- `query`
- `normalized_query`
- `results` (ranked)

Expected per-result minimum fields:
- `rank`
- `chunk_id`
- `hybrid_score`
- `word_score`
- `char_score`
- source metadata fields used for traceability

### 3) 03g Decision Output Input
Expected source artifact:
- `pocs/03g_retrieval_decision/outputs/sample_retrieval_decisions.json`

Expected per-query decision minimum fields:
- `query`
- `normalized_query`
- `decision_label`
- `recommended_route`
- `reason_codes`
- `evidence`

## Planned Evaluation Result Contract
Planned model name:
- `EvaluationCaseResult`

Planned shape:
```json
{
  "case_id": "case_001",
  "query": "heater repaid",
  "status": "fail",
  "expected_chunk_id": "heating_repair_overview__chunk_000",
  "expected_chunk_found": true,
  "expected_chunk_rank": 2,
  "hit_at_1": false,
  "hit_at_3": true,
  "hit_at_5": true,
  "expected_decision_label": "needs_clarification",
  "actual_decision_label": "ambiguous_match",
  "decision_label_match": false,
  "expected_recommended_route": "clarification_path",
  "actual_recommended_route": "clarification_path",
  "recommended_route_match": true,
  "failure_category": "DECISION_LABEL_MISMATCH",
  "failure_reason": "Expected needs_clarification but got ambiguous_match"
}
```

Planned `status` enum:
- `pass`
- `fail`
- `warning`

Pass-state rule:
- if `status="pass"`, then `failure_category=null` and `failure_reason=null`.

Failure-state rule:
- each failed case should include one primary `failure_category`.
- supporting details may be provided in `failure_reason`.
- multi-category failure logic is out of scope for this step.

Warning-state rule:
- `status="warning"` is reserved for non-contract, non-expectation data-quality conditions.
- expectation mismatches must not be represented as warnings.
- warnings must not hide failures; if both warning and failure conditions exist, final `status` must be `fail`.
- if `status="warning"`, then `failure_category=null` and `failure_reason=null`.
- warning context must not be stored in `failure_reason`.
- this contract does not add a dedicated `warning_details` field yet; warning details may be captured in a future optional field.

Normative status assignment order (pseudocode):
```text
if any required expectation check fails OR any required contract check fails:
    status = "fail"
    failure_category = <one primary failure category>
    failure_reason = <short human-readable explanation>
else if any warning-level data-quality condition exists:
    status = "warning"
    failure_category = null
    failure_reason = null
else:
    status = "pass"
    failure_category = null
    failure_reason = null
```

Additional status guarantees:
- failure checks happen first and take precedence over warning checks.
- warning context must not be written into `failure_reason`.
- `warning_details` is intentionally not part of the current schema.

## Planned Aggregate Report Contract
Planned output artifact (not created yet):
- `pocs/03h_retrieval_evaluation/outputs/evaluation_report.json`

Planned shape:
```json
{
  "poc": "03h_retrieval_evaluation",
  "input_sources": {
    "retrieval_results": "pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json",
    "decision_results": "pocs/03g_retrieval_decision/outputs/sample_retrieval_decisions.json",
    "labeled_fixtures": "pocs/03h_retrieval_evaluation/fixtures/labeled_retrieval_cases.json"
  },
  "metrics": {
    "total_cases": 0,
    "hit_at_1": 0.0,
    "hit_at_3": 0.0,
    "hit_at_5": 0.0,
    "decision_label_match_rate": 0.0,
    "recommended_route_match_rate": 0.0
  },
  "failure_breakdown": {
    "EXPECTED_CHUNK_NOT_FOUND": 0,
    "EXPECTED_CHUNK_RANK_TOO_LOW": 0,
    "DECISION_LABEL_MISMATCH": 0,
    "RECOMMENDED_ROUTE_MISMATCH": 0,
    "MISSING_CASE_IN_03F_OUTPUT": 0,
    "MISSING_CASE_IN_03G_OUTPUT": 0,
    "MALFORMED_FIXTURE_CASE": 0
  },
  "case_results": []
}
```

Planned human-readable companion artifact (not created yet):
- `pocs/03h_retrieval_evaluation/outputs/evaluation_summary.md`

## Validation Rules (Planned)
- every fixture case must have a unique `case_id`
- `query` must be non-empty
- `expected_chunk_id` must be non-empty
- `expected_decision_label` must be one of the `03g` label enum values
- `expected_recommended_route` must be one of the `03g` route enum values
- result `status` must be one of: `pass`, `fail`, `warning`
- retrieval results must be rank-ordered and include `chunk_id`
- rank metric values must be internally consistent:
  - if `hit_at_1=true`, then `hit_at_3=true` and `hit_at_5=true`
  - if `expected_chunk_found=false`, then `expected_chunk_rank` is `null`
- rank evaluation behavior is fixed to actual rank capture plus `hit_at_1`, `hit_at_3`, `hit_at_5`
- custom expected-rank target thresholds are out of scope for this step
- every evaluated case must emit `status`
- `status=pass` requires `failure_category=null` and `failure_reason=null`
- `status=fail` requires one primary `failure_category`
- `status=fail` requires a short human-readable `failure_reason`
- `status=warning` requires no failed expectation/contract check
- `status=warning` requires `failure_category=null` and `failure_reason=null`
- if any failed expectation/contract check occurs, `status` must be `fail` even if warning conditions are also present

Failure category intent examples:
- `EXPECTED_CHUNK_NOT_FOUND`: expected chunk missing from retrieved results.
- `EXPECTED_CHUNK_RANK_TOO_LOW`: expected chunk found but below acceptable top-k expectation for case pass criteria.
- `DECISION_LABEL_MISMATCH`: actual decision label differs from expected fixture label.
- `RECOMMENDED_ROUTE_MISMATCH`: actual route differs from expected fixture route.
- `MISSING_CASE_IN_03F_OUTPUT`: required case not found in `03f` output.
- `MISSING_CASE_IN_03G_OUTPUT`: required case not found in `03g` output.
- `MALFORMED_FIXTURE_CASE`: fixture record violates required contract.

## Non-Contract Assumptions
- fixture authoring quality affects metric trustworthiness
- exact threshold values in `03g` remain placeholders until later tuning cycles
- this contract assumes deterministic matching keys can align fixture cases with `03f` and `03g` records
- this contract does not define any answer-generation interface

## Engineering Rules Alignment
When implemented, all contract models should use Pydantic and type hints.
No live data is required; fixtures remain synthetic.
