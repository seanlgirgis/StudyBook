# 03g Retrieval Decision Contract

## Contract Purpose
Define the expected data interface for deterministic retrieval-quality decisions based on `03f_hybrid_retrieval` output.

This contract is for documentation/design approval before implementation.

## Expected Upstream Input Artifact
- compatible with `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json`

Expected top-level shape (simplified):
- `poc`
- `description`
- `config` (hybrid retrieval config from 03f)
- `queries` (list of query result objects)

Each query object is expected to include:
- `query`
- `normalized_query`
- `results` (ranked list)

Each result item is expected to include at minimum:
- `rank`
- `chunk_id`
- `hybrid_score`
- `word_score`
- `char_score`
- `retrieval_sources`
- `source_file`
- `title`
- `section` (optional if not present in source)
- `text`
- `normalized_text`

## Expected 03g Config Shape
Model name (planned): `RetrievalDecisionConfig`

```json
{
  "strong_match_min_score": 0.55,
  "weak_match_min_score": 0.25,
  "no_match_max_score": 0.10,
  "min_score_gap_for_strong": 0.08,
  "close_score_delta": 0.03,
  "max_close_candidates_before_ambiguous": 2,
  "top_k_window": 5,
  "source_diversity_ambiguity_threshold": 3,
  "enable_needs_clarification": true
}
```

Notes:
- Numeric values are placeholders for design discussion and tuning.
- Final implementation should validate ranges with Pydantic.
- Placeholder thresholds must be tuned with later retrieval-evaluation fixtures and are not permanent truth values.

## Expected 03g Output Shape
Model name (planned): `RetrievalDecisionResult`

```json
{
  "query": "heater repaid",
  "normalized_query": "heater repaid",
  "decision_label": "ambiguous_match",
  "recommended_route": "clarification_path",
  "confidence_score": 0.47,
  "reason_codes": [
    "TOP_SCORE_MID",
    "SMALL_TOP_GAP",
    "MULTIPLE_CLOSE_CANDIDATES"
  ],
  "evidence": {
    "top_score": 0.49,
    "second_score": 0.46,
    "score_gap": 0.03,
    "close_candidate_count": 3,
    "top_k_considered": 5,
    "distinct_source_count": 3
  },
  "selected_chunk_ids": [
    "heating_repair_overview__chunk_000",
    "water_heater_repairs__chunk_001"
  ],
  "precedence_rule_applied": "CLARIFICATION_BEATS_AMBIGUOUS",
  "deterministic": true
}
```

## Decision Label Enum
Expected allowed values:
- `strong_match`
- `ambiguous_match`
- `weak_match`
- `no_match`
- `needs_clarification`

## Recommended Route Enum (Downstream Hint Only)
Expected allowed values:
- `answer_candidate_path`
- `clarification_path`
- `fallback_path`
- `no_answer_path`

Semantics:
- `decision_label` is the retrieval-quality classification output.
- `recommended_route` is a routing hint for later POCs and does not override the label.

## Precedence Contract
Planned precedence order:
1. `no_match`
2. `strong_match`
3. `needs_clarification`
4. `ambiguous_match`
5. `weak_match`

Expected behavior:
- `needs_clarification` may override states that otherwise look `ambiguous_match` or `weak_match` when clarification policy triggers.
- `no_match` must still beat clarification when evidence is below no-match floor.

## Reason Code Contract
Reason codes should be machine-readable constants for traceability.

Examples by label:
- `strong_match`:
  - `TOP_SCORE_STRONG`
  - `CLEAR_SCORE_GAP`
  - `LOW_CLOSE_CANDIDATE_COUNT`
- `ambiguous_match`:
  - `SMALL_TOP_GAP`
  - `MULTIPLE_CLOSE_CANDIDATES`
  - `TOP_SCORE_MID`
- `weak_match`:
  - `TOP_SCORE_LOW_NONZERO`
  - `BELOW_WEAK_CONFIDENCE_TARGET`
- `no_match`:
  - `NO_CANDIDATES`
  - `TOP_SCORE_BELOW_NO_MATCH_THRESHOLD`
- `needs_clarification`:
  - `QUERY_UNDERSPECIFIED_MULTI_SERVICE`
  - `CLARIFICATION_POLICY_TRIGGERED`
  - `AMBIGUITY_REQUIRES_CLARIFICATION`

## Output Collection Shape
Model name (planned): `RetrievalDecisionBatch`

```json
{
  "poc": "03g_retrieval_decision",
  "input_source": "pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json",
  "decision_config": {},
  "query_decisions": []
}
```

## Validation Expectations
- all labels must be in enum
- all recommended routes must be in route enum
- score fields must be numeric and bounded
- reason codes must be non-empty for every label, including `strong_match`
- `selected_chunk_ids` should be empty for `no_match`
- `precedence_rule_applied` should be present when precedence override behavior occurs
- `deterministic` must be `true` for this POC

## Non-Goals In Contract
This contract does not define:
- answer text
- intent classification
- live chat prompts
- escalation execution
