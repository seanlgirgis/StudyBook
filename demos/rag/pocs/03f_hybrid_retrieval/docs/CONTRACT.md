# 03f Hybrid Retrieval Contract

## Expected Input Artifacts
- `pocs/03d_word_tfidf_index/outputs/tfidf_index.joblib`
- `pocs/03e_char_tfidf_typo_search/outputs/char_tfidf_index.joblib`

Both artifacts are expected to expose compatible chunk identity mapping via `chunk_id` and include required keys:
- `vectorizer`
- `matrix`
- `chunk_ids`
- `metadata`

## Expected Query Input Shape
Model: `HybridSearchQuery`

```json
{
  "query": "heater repaid"
}
```

Notes:
- `query` is customer-style free text.

## Expected Config Shape
Model: `HybridRetrievalConfig`

```json
{
  "word_weight": 0.65,
  "char_weight": 0.35,
  "top_k": 5
}
```

## Expected Result Object Shape
Model: `HybridSearchResult`

Each ranked candidate should contain the following required fields:
- `rank`
- `chunk_id`
- `hybrid_score`
- `word_score`
- `char_score`
- `word_weight`
- `char_weight`
- `retrieval_sources`
- `source_file`
- `title`
- `section` (if available)
- `text`
- `normalized_text`

## Expected Output File
- `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json`

## Expected Response Shape
Model: `HybridSearchResponse`

## Example JSON (One Query Result)

```json
{
  "query": "heater repaid",
  "normalized_query": "heater repaid",
  "config": {
    "word_weight": 0.65,
    "char_weight": 0.35,
    "top_k": 5
  },
  "results": [
    {
      "rank": 1,
      "chunk_id": "heating_repair_overview__chunk_000",
      "hybrid_score": 0.7421,
      "word_score": 0.6815,
      "char_score": 0.8548,
      "word_weight": 0.65,
      "char_weight": 0.35,
      "retrieval_sources": [
        "word",
        "char"
      ],
      "source_file": "heating_repair_overview.md",
      "title": "Heating Repair Services",
      "section": "Common Heating Issues",
      "text": "Our technicians diagnose and repair furnace and heater issues, including no-heat calls.",
      "normalized_text": "our technicians diagnose and repair furnace and heater issues including no heat calls"
    }
  ]
}
```

## Merge and Scoring Contract Notes
- candidates are merged by exact `chunk_id`
- missing `word_score` or `char_score` defaults to `0.0`
- `hybrid_score` is computed per candidate and used for final ranking
- `retrieval_sources` records which retrievers contributed non-zero score (`word` and/or `char`)
- final response is top-k limited by `config.top_k`
- query normalization uses reusable `03c` normalization behavior

## Runner Output Wrapper Shape
The runner (`src/run_hybrid_search.py`) writes a top-level JSON object:
- `poc`
- `description`
- `word_index_path`
- `char_index_path`
- `config`
- `queries`

Each `queries[]` item includes:
- `query`
- `normalized_query`
- `results` (list of `HybridSearchResult` rows)
