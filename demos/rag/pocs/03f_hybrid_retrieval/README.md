# 03f_hybrid_retrieval

## POC Name
`03f_hybrid_retrieval`

## Purpose
Create a hybrid retrieval layer that combines:
- clean word-level TF-IDF signal from `03d_word_tfidf_index`
- typo-tolerant character-level TF-IDF signal from `03e_char_tfidf_typo_search`

This POC is retrieval-only and candidate-ranking-only.

## Current Implementation Status
- implemented:
  - `src/schemas.py` data contracts
  - `tests/test_schemas.py` contract validation tests
  - `src/hybrid_retrieval.py` reusable core retrieval module
  - `tests/test_hybrid_retrieval.py` core retrieval unit tests
  - `src/run_hybrid_search.py` thin runner script
  - sample hybrid output generation to `outputs/sample_hybrid_search_results.json`
- not implemented yet:
  - retrieval decision logic (`03g_retrieval_decision`)
  - answer generation / intent decision / clarification flows

## Retrieval Ladder Position
- `03d_word_tfidf_index`: builds clean word retrieval artifact
- `03e_char_tfidf_typo_search`: builds typo-tolerant retrieval artifact
- `03f_hybrid_retrieval`: combines both retrieval signals into one ranked candidate list
- next handoff: `03g_retrieval_decision`

## Inputs It Reads
- `pocs/03d_word_tfidf_index/outputs/tfidf_index.joblib`
- `pocs/03e_char_tfidf_typo_search/outputs/char_tfidf_index.joblib`

## Output It Writes
- `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json`

## What 03f Does
- loads existing `03d` and `03e` index artifacts
- accepts customer-style query text
- runs word and character retrieval in parallel flow
- merges candidates by `chunk_id`
- computes weighted `hybrid_score`
- returns ranked candidate chunks with component scores and source metadata

## What 03f Does Not Do
- does not generate customer answers
- does not decide final service intent
- does not ask clarification questions
- does not call an LLM
- does not rebuild indexes
- does not move anything into `integrated/servicecall-ai`

## Default Scoring Design
`hybrid_score = (0.65 * word_score) + (0.35 * char_score)`

Weights are configurable via runner arguments and config.

## Commands

```powershell
# run unit tests
pytest -v .\pocs\03f_hybrid_retrieval\tests

# generate sample hybrid retrieval output
python .\pocs\03f_hybrid_retrieval\src\run_hybrid_search.py
```
