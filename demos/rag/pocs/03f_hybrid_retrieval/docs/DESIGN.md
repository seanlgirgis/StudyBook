# 03f Hybrid Retrieval Design

## Problem Statement
`03d` and `03e` each provide useful but partial retrieval behavior:
- word-level TF-IDF is strong for clean, exact business wording
- character-level TF-IDF is strong for misspellings and noisy typing

The project needs one retrieval output that benefits from both signals without jumping ahead to intent or answer generation.

## Why 03f Comes After 03d and 03e
`03f` depends on two already-built artifacts:
- word index from `03d`
- character index from `03e`

Without both artifacts, there is no hybrid signal to combine. This sequencing preserves the learning ladder and keeps each POC standalone and chainable.

## Architecture Flow
1. load `03d` word TF-IDF artifact
2. load `03e` char TF-IDF artifact
3. accept a customer-style query string
4. normalize query with reusable `03c` normalization behavior
5. compute word retrieval scores against chunk corpus
6. compute char retrieval scores against chunk corpus
7. merge candidates by shared `chunk_id`
8. compute `hybrid_score` per candidate
9. sort descending by `hybrid_score`
10. return ranked retrieval candidates for downstream use

## Current Core Implementation
Implemented in `src/hybrid_retrieval.py`:
- `load_index_artifact(path)`:
  - loads joblib artifact
  - validates required keys: `vectorizer`, `matrix`, `chunk_ids`, `metadata`
  - validates row/count alignment
- `search_index_artifact(query, artifact, top_k)`:
  - transforms query with stored vectorizer
  - computes cosine similarity against stored matrix
  - returns ranked candidates with `chunk_id`, `score`, and `metadata`
- `merge_retrieval_results(word_results, char_results, config)`:
  - merges by `chunk_id`
  - fills missing component scores with `0.0`
  - computes weighted `hybrid_score`
  - sets retrieval sources (`word`, `char`, or both)
  - returns validated `HybridSearchResult` objects
- `hybrid_search(query, word_index_path, char_index_path, config)`:
  - validates input query via Pydantic
  - applies reusable 03c normalization
  - loads both artifacts
  - searches both artifacts
  - merges + ranks + top-k limits
  - returns validated `HybridSearchResponse`

Not implemented in this stage:
- integration with downstream 03g decision logic

## Word Retrieval Signal
Word signal captures:
- exact service terms (for example, repair, maintenance, thermostat)
- clearer precision when query wording is clean
- interpretable term-level matching behavior

## Character Retrieval Signal
Character signal captures:
- typo and misspelling tolerance
- partial-token and near-spelling similarity
- resilience for messy user text input

## Hybrid Scoring Strategy
Default weighted blend:
- `hybrid_score = (0.65 * word_score) + (0.35 * char_score)`

Rationale:
- word signal keeps precision prioritized
- char signal boosts robustness for noisy queries

If a candidate is absent in one retriever, missing component score is treated as `0.0` before blending.

## Configurability
Current configuration surface:
- `word_weight` (default `0.65`)
- `char_weight` (default `0.35`)
- top-k cutoff for each retriever before merge
- final top-k return size

Config values should be explicit and documented so the POC is reusable and deterministic.

## Boundaries and Non-Goals
`03f` is retrieval-only.

Non-goals:
- no intent classification
- no answer generation
- no user clarification prompting
- no LLM or external API call
- no index rebuilding
- no movement into `integrated/servicecall-ai`

## Future Handoff to 03g_retrieval_decision
`03f` should hand off a ranked, transparent candidate list with component scores.

`03g_retrieval_decision` can then decide:
- confidence thresholds
- candidate sufficiency checks
- fallback/escalation routing

That decision logic is intentionally out of scope for `03f`.

