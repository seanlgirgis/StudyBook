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

## Closure Snapshot (03a-03e)
- `03a_load_documents` PASS (16 docs loaded; output JSON written)
- `03b_chunk_documents` PASS (boundary-aware chunking; 23 chunks; 8 tests passed)
- `03c_text_normalization` PASS (`normalized_text` + `normalized_character_count`; 6 tests passed)
- `03d_word_tfidf_index` PASS (word TF-IDF; matrix `23 x 2002`; 9 tests passed)
- `03e_char_tfidf_typo_search` PASS (character typo-tolerant TF-IDF; matrix `23 x 5779`; 11 tests passed)
- Learning lock-in: word TF-IDF (`03d`) is the clean-word baseline.
- Learning lock-in: character TF-IDF (`03e`) is typo-tolerant candidate matching.
- Learning lock-in: `03e` returns candidates only and does not decide final intent.
- Design law to preserve: every POC should be standalone, configurable, reusable, and chainable

## Next Task
Next suggested step is discussion/scoping for `pocs/03f_hybrid_retrieval` only.
Do not implement `03f` until explicit approval.
Do not start backend, RAG, integrated, AWS, or real-data work yet.

## 03f Discussion Starter (No Implementation Yet)
- What hybrid retrieval means in this project.
- Why hybrid retrieval comes after `03d` word TF-IDF and `03e` char TF-IDF.
- What `03f` should combine from prior artifacts.
- How scoring might work at a high level.
- What `03f` should read/write.
- What `03f` should explicitly not do.

## Constraints
- no backend logic yet
- no integrated solution work yet
- no AI calls yet
- keep it simple and runnable locally
- no TF-IDF, no search, no embeddings, no FastAPI, no Docker, no AWS, no integrated app
