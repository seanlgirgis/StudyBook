# 03f Hybrid Retrieval Test Plan

## Current Step Acceptance Checks
- confirm `src/hybrid_retrieval.py` exists and exposes reusable library functions
- confirm `src/run_hybrid_search.py` exists and stays thin (orchestration only)
- confirm runner writes `outputs/sample_hybrid_search_results.json`
- confirm no `03d`/`03e` artifacts are modified in this step

## Implemented Unit Test Coverage
- missing artifact file fails clearly
- missing artifact keys fail clearly
- `search_index_artifact` returns ranked candidates
- merge behavior for word-only, char-only, and both-source matches
- default score blending uses `0.65` / `0.35`
- final merged ranking is sorted descending by `hybrid_score`
- `hybrid_search` returns `HybridSearchResponse`
- no customer answer/final-intent fields are generated

## Future Clean Query Examples
- `ac maintenance plan`
- `water heater replacement cost`
- `emergency plumbing service`
- `furnace not heating`

Expected behavior:
- strong word TF-IDF contribution
- char TF-IDF still contributes where relevant

## Future Typo Query Examples
- `ac maintenence plan`
- `watr heater leakng`
- `emergncy plumming service`
- `heater repaid`

Expected behavior:
- char TF-IDF improves candidate recall
- hybrid scoring still returns stable ranked results

## Future Merge Behavior Tests
- candidate appears in both retrievers -> both scores retained
- candidate appears only in word retriever -> `char_score = 0.0`
- candidate appears only in char retriever -> `word_score = 0.0`
- duplicate `chunk_id` entries collapse into one merged record

## Future Weighting Tests
- default weights produce expected `hybrid_score`
- custom weights override defaults
- guardrails enforce valid weight ranges and non-negative values
- optional normalization check: `word_weight + char_weight = 1.0` policy behavior

## Future Missing Artifact Tests
- missing word artifact path produces clear failure message
- missing char artifact path produces clear failure message
- malformed joblib payload produces explicit contract error

## Future Output Schema Validation Tests
- each result contains required fields:
  - `rank`, `chunk_id`, `hybrid_score`, `word_score`, `char_score`
  - `word_weight`, `char_weight`, `retrieval_sources`
  - `source_file`, `title`, `section`, `text`, `normalized_text`
- numeric score fields are valid floats
- `retrieval_sources` is a non-empty list when score contribution exists
- final result list is sorted by descending `hybrid_score`

