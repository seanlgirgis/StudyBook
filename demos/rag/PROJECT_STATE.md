# PROJECT_STATE.md

## Current Milestone
Milestone 3 (Step 03e) — Character TF-IDF typo-search POC completed and closed (`pocs/03e_char_tfidf_typo_search`)

## Current Focus
`03e_char_tfidf_typo_search` is closed. Next suggested step is discussion/planning for `03f_hybrid_retrieval` only (not implemented).

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

## Control Protocol Status
A closed-loop project-control protocol is now in place via `AGENTS.md` + permanent memory files:
- `DAILY_LOG.md`
- `DECISIONS.md`
- `KNOWN_ISSUES.md`
- `CHANGELOG.md`

## What Exists
- project shell
- pocs/ structure
- integrated/ structure
- docs/ structure
- testing/ structure
- demo_scenarios/ structure
- `pocs/01_static_site_shell` static site shell
- floating chat widget placeholder (open/close + hardcoded responses)
- `aux_scripts/` helper utilities for tree view, zip packaging, static site checks, and control-file snapshots
- Cloudflare Workers static smoke test record for Milestone 1 (`pocs/01_static_site_shell/notes/cloudflare_static_smoke_test.md`)
- `pocs/02_fake_business_docs` synthetic business knowledge corpus and retrieval evaluation notes
- Milestone 3 retrieval ladder scaffolds:
  - `pocs/03a_load_documents`
  - `pocs/03b_chunk_documents`
  - `pocs/03c_text_normalization`
  - `pocs/03d_word_tfidf_index`
  - `pocs/03e_char_tfidf_typo_search`
  - `pocs/03f_hybrid_retrieval`
  - `pocs/03g_retrieval_decision`
  - `pocs/03h_retrieval_evaluation`
  - `pocs/03_RETRIEVAL_LADDER.md`
- `pocs/03a_load_documents` implementation:
  - Pydantic schema for `SourceDocument`
  - markdown discovery/loading script
  - loader tests
  - structured JSON output (`outputs/loaded_documents.json`)
  - educational module/function comments and docstrings for onboarding
- `pocs/03b_chunk_documents` implementation:
  - reads `pocs/03a_load_documents/outputs/loaded_documents.json`
  - validates loaded document records with Pydantic
  - boundary-aware chunking with target size `800` and overlap `100`
  - chunk-end fallback order: section heading -> paragraph -> newline -> sentence -> word -> hard split
  - cleaned overlap starts to avoid mid-word chunk starts
  - preserves chunk metadata (`chunk_id`, `document_id`, `source_file`, `source_path`, `title`, `chunk_index`, `text`, `character_count`)
  - chunking tests (8 passing tests)
  - structured JSON output (`outputs/chunked_documents.json`)
  - final verified status: 16 input documents, 23 output chunks, script PASS, tests PASS (`8 passed in 0.15s`)
  - inspection note confirmed clean `ac_replacement_estimates` boundary behavior (`## Estimate Process` start, no `ex` / `irst recommendation.` split artifact)
- `pocs/03c_text_normalization` implementation:
  - reads `pocs/03b_chunk_documents/outputs/chunked_documents.json`
  - validates 03b chunk records with Pydantic
  - preserves all chunk metadata fields and original `text`
  - adds `normalized_text` and `normalized_character_count`
  - normalization rules implemented:
    - Unicode normalization (`NFKC`)
    - smart quotes/apostrophes mapped to plain quotes/apostrophes where practical
    - long dashes converted to spaces
    - lowercasing
    - non-word punctuation replaced with spaces
    - repeated whitespace collapsed
    - leading/trailing whitespace stripped
    - no stemming, no stop-word removal, no number removal
  - business-term handling implemented:
    - `A/C` and `a/c` -> `ac`
    - `air-conditioning` -> `air conditioning`
  - writes `pocs/03c_text_normalization/outputs/normalized_chunks.json`
  - final verified status: 23 input chunks, 23 output chunks, script PASS, tests PASS (`6 passed in 0.18s`)
- `pocs/03d_word_tfidf_index` implementation:
  - reads `pocs/03c_text_normalization/outputs/normalized_chunks.json`
  - validates chunk records with Pydantic (`chunk_id`, source metadata, `text`, `normalized_text`, and count fields)
  - builds word-level TF-IDF index with `TfidfVectorizer` config:
    - `analyzer="word"`
    - `ngram_range=(1, 2)`
    - `lowercase=False`
    - `min_df=1`
    - `max_df=1.0`
  - writes `pocs/03d_word_tfidf_index/outputs/tfidf_index.joblib`
  - writes `pocs/03d_word_tfidf_index/outputs/index_metadata.json`
  - joblib artifact contents:
    - `vectorizer`
    - `matrix`
    - `chunk_ids`
    - `metadata`
  - row-order guarantee preserved: matrix row `i` aligns to `chunk_ids[i]` and `metadata[i]`
  - final verified status: 23 chunks indexed, matrix shape `(23, 2002)`, vocabulary size `2002`, script PASS, tests PASS (`9 passed in 1.08s`)
- `pocs/03e_char_tfidf_typo_search` implementation:
  - reads `pocs/03c_text_normalization/outputs/normalized_chunks.json`
  - validates chunk records with Pydantic (`chunk_id`, source metadata, `text`, `normalized_text`, and count fields)
  - builds typo-tolerant character TF-IDF index with `TfidfVectorizer` config:
    - `analyzer="char_wb"`
    - `ngram_range=(3, 5)`
    - `lowercase=False`
    - `min_df=1`
    - `max_df=1.0`
  - writes `pocs/03e_char_tfidf_typo_search/outputs/char_tfidf_index.joblib`
  - writes `pocs/03e_char_tfidf_typo_search/outputs/char_index_metadata.json`
  - writes `pocs/03e_char_tfidf_typo_search/outputs/sample_typo_search_results.json`
  - joblib artifact contents:
    - `vectorizer`
    - `matrix`
    - `chunk_ids`
    - `metadata`
  - row-order guarantee preserved: matrix row `i` aligns to `chunk_ids[i]` and `metadata[i]`
  - sample typo queries written as candidate matches only (no final intent decision):
    - `ac repiar`
    - `watr heater leaking`
    - `maintenence plan`
    - `air condishner not cooling`
    - `heater repaid`
    - `emergncy service`
  - final verified status: 23 chunks indexed, matrix shape `(23, 5779)`, vocabulary size `5779`, script PASS, tests PASS (`11 passed in 1.03s`)

## What Is Not Yet Implemented
- customer-facing TF-IDF search flow (word and char indexes exist; retrieval interface not yet built)
- hybrid retrieval implementation
- retrieval decision logic implementation
- retrieval evaluation harness implementation
- answer with citations implementation
- intake classification implementation
- lead scoring implementation
- urgency detection implementation
- fallback/escalation runtime implementation
- outcome logging implementation
- FastAPI app
- Docker setup
- ECS deployment
- CI/CD
- observability

## Current Rules
- work in pocs/ first
- no full app build yet
- use Pydantic everywhere
- synthetic data only
- follow closed-loop reporting and project-memory updates each task

## Next Recommended Task
Discuss and scope `pocs/03f_hybrid_retrieval` next. Do not implement `03f` until approved.
