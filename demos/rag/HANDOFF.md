# HANDOFF.md

## Resume Point
Milestone 1 static website shell is implemented and smoke-tested, Milestone 2 synthetic business documents are populated, and Milestone 3 steps `03a_load_documents`, `03b_chunk_documents`, `03c_text_normalization`, `03d_word_tfidf_index`, and `03e_char_tfidf_typo_search` are implemented and validated.
`03e_char_tfidf_typo_search` reads `pocs/03c_text_normalization/outputs/normalized_chunks.json`, validates normalized chunk records, and builds/saves a reusable character TF-IDF typo-tolerant candidate retrieval catalog.
03e outputs:
- `pocs/03e_char_tfidf_typo_search/outputs/char_tfidf_index.joblib`
- `pocs/03e_char_tfidf_typo_search/outputs/char_index_metadata.json`
- `pocs/03e_char_tfidf_typo_search/outputs/sample_typo_search_results.json`
03e vectorizer config:
- `analyzer=\"char_wb\"`
- `ngram_range=(3, 5)`
- `lowercase=False`
- `min_df=1`
- `max_df=1.0`
03e artifact contents:
- `vectorizer`
- `matrix`
- `chunk_ids`
- `metadata`
Row-order mapping is preserved: matrix row `i` aligns with `chunk_ids[i]` and `metadata[i]`.
Sample typo candidate queries written:
- `ac repiar`
- `watr heater leaking`
- `maintenence plan`
- `air condishner not cooling`
- `heater repaid`
- `emergncy service`
Final 03e validation: 23 chunks indexed, matrix `(23, 5779)`, vocabulary size `5779`, `python .\pocs\03e_char_tfidf_typo_search\src\build_char_tfidf_index.py` PASS, and `pytest -v .\pocs\03e_char_tfidf_typo_search\tests` PASS (`11 passed in 1.03s`).
`03e_char_tfidf_typo_search` is complete and closed.

## Read First
1. AGENTS.md
2. PROJECT_STATE.md
3. TASK_BOARD.md
4. DECISIONS.md
5. KNOWN_ISSUES.md

## Product Direction Add-On: Guided Customer Input
ServiceCall AI should eventually help customers express their service need clearly before retrieval and answer generation.

- Include autocomplete suggestions while typing.
- Include autocorrect-style typo assistance.
- Include service-intent suggestion buttons.
- Include clarification choices when input is ambiguous.
- Example disambiguation flow:
  - Customer types: `heater repaid`
  - System asks:
    - A) Heating system repair
    - B) Water heater repair
    - C) Billing/payment help
    - D) Something else

This does not replace retrieval. This supports retrieval by improving input quality.
Backend retrieval should still handle messy input using word TF-IDF, character TF-IDF, hybrid retrieval, and later semantic search.
This belongs to future product direction, not current `03e` implementation.

## Next Task
Next suggested step is discussion/scoping for `pocs/03f_hybrid_retrieval` only.
Do not implement `03f` until explicit approval.
Do not start backend, RAG, integrated, AWS, or real-data work yet.

## Constraints
- no backend logic yet
- no integrated solution work yet
- no AI calls yet
- keep it simple and runnable locally
- no TF-IDF, no search, no embeddings, no FastAPI, no Docker, no AWS, no integrated app
