# DAILY_LOG.md

## 2026-05-01
- Established permanent project memory files: `DAILY_LOG.md`, `DECISIONS.md`, `KNOWN_ISSUES.md`, `CHANGELOG.md`.
- Strengthened `AGENTS.md` with explicit environment bootstrap, closed-loop reporting, read/update file obligations, and stop rule examples.
- Updated `PROJECT_STATE.md` to record that the closed-loop project-control protocol now exists.
- Updated `TASK_BOARD.md` to mark "add permanent agent memory / closed-loop protocol" as done.
- Updated `HANDOFF.md` to keep next task pinned to `pocs/01_static_site_shell`.

## Validation
- Confirmed environment bootstrap details by running `. D:\Workarea\StudyBook\env_setter.ps1` and checking Python path/version.
- Confirmed required root control files exist after updates.

## 2026-05-01 (Milestone 1)
- Implemented `pocs/01_static_site_shell` website shell using synthetic business content for North Texas Comfort & Home Services.
- Added required page sections: Hero, Services, Why Choose Us, Maintenance Plan, Coupons / Offers, Service Area, and Contact / Schedule.
- Implemented floating bottom-right chat widget with open/close actions, starter messages, user input handling, and hardcoded placeholder assistant replies.
- Added explicit text in UI that future versions will connect to FastAPI and RAG backend.
- Updated Milestone memory/control files (`PROJECT_STATE.md`, `TASK_BOARD.md`, `HANDOFF.md`, `CHANGELOG.md`) to reflect Milestone 1 completion status.

## Validation (Milestone 1)
- Confirmed required Milestone 1 files exist under `pocs/01_static_site_shell`.
- Confirmed `website/index.html` references `assets/styles.css` and `assets/chat-widget.js`.
- Confirmed no backend/API endpoint usage in Milestone 1 files.
- Confirmed no external CDN dependencies in Milestone 1 files.

## 2026-05-01 (Aux Script Utilities)
- Created `aux_scripts/` helper script set for read-only tree inspection, zip packaging for sharing, static POC validation, and control-file snapshots.
- Added `aux_scripts/README.md` with usage examples and scope notes that scripts are helper utilities only.
- Updated project memory/control files to reflect availability of helper tooling.

## Validation (Aux Script Utilities)
- Ran PowerShell parser checks on all new scripts with no syntax errors.
- Ran `.\aux_scripts\show_tree.ps1 -Path ".\pocs\01_static_site_shell"` successfully.
- Ran `.\aux_scripts\check_poc_static_site.ps1` successfully with PASS.
- Did not run zip script in validation flow; script behavior was reviewed for source safety (copy-only, no source deletion).

## 2026-05-02 (Milestone 1 Cloudflare Smoke Test Record)
- Added a documentation record for Milestone 1 static-hosting smoke test:
  - `pocs/01_static_site_shell/notes/cloudflare_static_smoke_test.md`
- Captured temporary hosting details:
  - URL: `https://lively-term-09e9.seanlgirgis.workers.dev/`
  - Method: Cloudflare Workers static upload
  - Result: PASS
  - Devices: PC and phone
- Documented explicit boundary: accepted as temporary static smoke test only and does not replace later FastAPI + Docker + ECS Fargate + GitHub Actions CI/CD + CloudWatch milestones.
- Updated project memory files to reflect this Milestone 1 validation evidence.

## Validation (Milestone 1 Cloudflare Smoke Test Record)
- Confirmed smoke test note file exists.
- Confirmed deployed URL is present in the new note.
- Confirmed this task changed documentation only (no app/backend/RAG/integrated code edits).

## 2026-05-02 (Milestone 2 Synthetic Business Docs)
- Implemented Milestone 2 documentation corpus under `pocs/02_fake_business_docs`.
- Populated 16 business policy docs in `data/home_services_demo` for HVAC-first service operations and secondary service boundaries.
- Added/updated learning and evaluation notes:
  - `notes/retrieval_questions.md` with 24 sample questions, expected sources, and action type (answer/fallback/escalate)
  - `notes/what_good_answers_should_include.md`
  - `notes/document_design_notes.md`
- Updated `README.md` for Milestone 2 with purpose, file list, synthetic warning, usage, exclusions, and next milestone.
- Updated project memory files to reflect Milestone 2 completion status.

## Validation (Milestone 2 Synthetic Business Docs)
- Confirmed all required Milestone 2 files exist.
- Confirmed every business document has non-empty content (not heading-only placeholders).
- Confirmed retrieval question set includes at least 20 questions (24 provided).
- Confirmed synthetic-demo labeling is present in business documents.
- Confirmed no integrated/servicecall-ai files were changed in this task scope.
- Confirmed no backend/FastAPI/RAG/API implementation files were changed in this task scope.

## 2026-05-02 (Milestone 3 Retrieval Ladder Scaffolding)
- Created staged retrieval-learning folder shells:
  - `pocs/03a_load_documents`
  - `pocs/03b_chunk_documents`
  - `pocs/03c_text_normalization`
  - `pocs/03d_word_tfidf_index`
  - `pocs/03e_char_tfidf_typo_search`
  - `pocs/03f_hybrid_retrieval`
  - `pocs/03g_retrieval_decision`
  - `pocs/03h_retrieval_evaluation`
- Added starter `README.md` and `requirements.txt` in each stage.
- Added empty subfolders (`src/`, `tests/`, `outputs/`, `notes/`) with `keepIt.keep` placeholders.
- Added overview document `pocs/03_RETRIEVAL_LADDER.md`.
- Kept this task structure-only; no retrieval implementation code added.

## Validation (Milestone 3 Retrieval Ladder Scaffolding)
- Confirmed all 8 POC stage folders exist.
- Confirmed each stage has `README.md`, `requirements.txt`, `src/`, `tests/`, `outputs/`, `notes/`.
- Confirmed `pocs/03_RETRIEVAL_LADDER.md` exists.
- Confirmed no integrated/servicecall-ai files changed in this task scope.
- Confirmed no backend/FastAPI/AWS/Docker work added in this task scope.

## 2026-05-02 (Milestone 3 Step 03a - Load Documents)
- Implemented `pocs/03a_load_documents` loader POC only.
- Added `SourceDocument` Pydantic model with field validation in `src/schemas.py`.
- Added loader script in `src/load_documents.py`:
  - markdown discovery
  - title extraction
  - file-to-model conversion
  - batch load
  - JSON output writing
  - CLI summary output
- Added tests in `tests/test_load_documents.py`.
- Added learning notes:
  - `notes/what_this_teaches.md`
  - `notes/common_failures.md`
- Generated `outputs/loaded_documents.json` from synthetic business docs corpus.

## Validation (Milestone 3 Step 03a - Load Documents)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\src\load_documents.py` (PASS, loaded 16 markdown files)
  - `pytest -v` (PASS, 3 tests passed)
- Confirmed output JSON exists and contains 16 documents.
- Confirmed no integrated/servicecall-ai paths were touched.
- Confirmed no TF-IDF/search/chunking/AI/backend logic was added.

## 2026-05-02 (Milestone 3 Step 03a - Educational Comments)
- Added educational module docstrings and targeted inline comments to:
  - `pocs/03a_load_documents/src/schemas.py`
  - `pocs/03a_load_documents/src/load_documents.py`
- Clarified Pydantic contract purpose, field meanings, plain-English validation rules, and 03a flow:
  - markdown files -> `SourceDocument` objects -> `outputs/loaded_documents.json`
- Explicitly documented that 03a does not chunk, search, retrieve, or call AI, and that output feeds `03b_chunk_documents`.
- Kept runtime behavior unchanged.

## Validation (Milestone 3 Step 03a - Educational Comments)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\src\load_documents.py` (PASS, loaded 16 markdown files, wrote output JSON)
  - `pytest -v` (PASS, 3 tests passed)
- Confirmed `outputs/loaded_documents.json` exists and contains 16 documents.
- Confirmed no forbidden scope areas were touched.

## 2026-05-03 (Milestone 3 Step 03b - Chunk Documents)
- Implemented `pocs/03b_chunk_documents` only.
- Added Pydantic chunking contracts in `src/schemas.py`:
  - `LoadedDocument` input validation for 03a records
  - `DocumentChunk` output validation with required metadata fields
  - `character_count == len(text)` validation on chunks
- Added chunking pipeline script in `src/chunk_documents.py`:
  - reads `..\03a_load_documents\outputs\loaded_documents.json`
  - performs paragraph-aware chunking
  - uses target chunk size `800` characters with overlap `100`
  - emits stable chunk ids: `{document_id}__chunk_{chunk_index:03d}`
  - writes `outputs/chunked_documents.json`
- Added readable tests in `tests/test_chunk_documents.py`.
- Updated `README.md` with learning-first documentation and explicit out-of-scope boundaries.
- Added `NOTES.md` for concise implementation notes.

## Validation (Milestone 3 Step 03b - Chunk Documents)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\src\chunk_documents.py` (PASS, loaded 16 documents and generated 24 chunks)
  - `pytest -v` (PASS, 6 tests passed)
- Confirmed `outputs/chunked_documents.json` exists and is populated with validated chunk records.
- Confirmed no forbidden scope areas were touched (`integrated/servicecall-ai`, backend/FastAPI, Docker/AWS/CI-CD, or 03c+ implementation).

## 2026-05-03 (Milestone 3 Step 03b - Boundary-Aware Refinement)
- Refined `03b_chunk_documents` from mostly size-based splitting to boundary-aware splitting.
- Implemented chunk-end fallback order:
  - section heading -> paragraph -> newline -> sentence -> word -> hard split
- Improved overlap start alignment so chunks do not start in the middle of words.
- Preserved:
  - `TARGET_CHUNK_SIZE=800`
  - `OVERLAP_SIZE=100`
  - stable chunk IDs
  - metadata on every chunk
  - output file path `outputs/chunked_documents.json`
- Confirmed previously observed bad split in `ac_replacement_estimates` is resolved:
  - no chunk ends with `ex`
  - no chunk starts with `irst recommendation.`

## Validation (Milestone 3 Step 03b - Boundary-Aware Refinement)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\src\chunk_documents.py` (PASS, loaded 16 documents and generated 23 chunks)
  - `pytest -v` (PASS, 8 tests passed in 0.15s)
- Confirmed no forbidden scope areas were touched (`integrated/servicecall-ai`, backend/FastAPI, Docker/AWS/CI-CD, or 03c+ implementation).

## 2026-05-03 (Milestone 3 Step 03b - Final Closure)
- Closed `pocs/03b_chunk_documents` as complete with final verified status.
- Final verified state:
  - input: `pocs/03a_load_documents/outputs/loaded_documents.json`
  - input documents: 16
  - output: `pocs/03b_chunk_documents/outputs/chunked_documents.json`
  - output chunks: 23
  - script command PASS: `python .\pocs\03b_chunk_documents\src\chunk_documents.py`
  - test command PASS: `pytest -v` (`8 passed in 0.15s`)
- Final algorithm record:
  - boundary-aware chunking (not blind size-only)
  - target chunk size `800`, approximate overlap `100`
  - fallback order: section heading -> paragraph -> newline -> sentence -> word -> hard split
  - cleaned overlap starts to avoid mid-word chunk starts
  - stable chunk IDs and full metadata preserved on every chunk

## 2026-05-03 (Milestone 3 Step 03c - Text Normalization)
- Implemented `pocs/03c_text_normalization` only.
- Added Pydantic schema contracts in `pocs/03c_text_normalization/src/schemas.py`:
  - `DocumentChunk` input validation for 03b records
  - `NormalizedChunk` output validation with `normalized_text` and `normalized_character_count`
  - validation rules for non-empty text fields and count consistency
- Added normalization pipeline script in `pocs/03c_text_normalization/src/normalize_text.py`:
  - reads `pocs/03b_chunk_documents/outputs/chunked_documents.json`
  - preserves original fields (`chunk_id`, `document_id`, `source_file`, `source_path`, `title`, `chunk_index`, `text`, `character_count`)
  - adds `normalized_text` and `normalized_character_count`
  - applies normalization rules:
    - Unicode normalization (`NFKC`)
    - smart quotes/apostrophes to plain quotes/apostrophes
    - long dash cleanup
    - lowercasing
    - punctuation replacement with spaces
    - whitespace collapse and trim
    - business-term handling (`A/C`/`a/c` -> `ac`, `air-conditioning` -> `air conditioning`)
  - writes `pocs/03c_text_normalization/outputs/normalized_chunks.json`
  - prints input path, output path, chunk counts, and before/after sample
- Added tests in `pocs/03c_text_normalization/tests/test_normalize_text.py`.
- Updated `pocs/03c_text_normalization/README.md` and `requirements.txt` for real implementation and usage.
- Updated project memory files for 03c completion and next-step suggestion (03d discussion only).

## Validation (Milestone 3 Step 03c - Text Normalization)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\pocs\03c_text_normalization\src\normalize_text.py` (PASS, read 23 chunks and wrote 23 normalized chunks)
  - `pytest -v .\pocs\03c_text_normalization\tests` (PASS, 6 tests passed in 0.18s)
- Confirmed `outputs/normalized_chunks.json` exists and is populated with validated normalized records.
- Confirmed no forbidden scope areas were touched (`integrated/servicecall-ai`, backend/FastAPI, TF-IDF/search/embeddings, Docker/AWS/CI-CD).

## 2026-05-03 (Milestone 3 Step 03d - Word TF-IDF Index)
- Implemented `pocs/03d_word_tfidf_index` only.
- Added Pydantic schema contract in `pocs/03d_word_tfidf_index/src/schemas.py` for required normalized chunk fields:
  - `chunk_id`, `document_id`, `source_file`, `source_path`, `title`, `chunk_index`
  - `text`, `character_count`
  - `normalized_text`, `normalized_character_count`
- Added standalone, chainable builder script in `pocs/03d_word_tfidf_index/src/build_tfidf_index.py`:
  - relative default paths + argparse overrides (`--input`, `--index-output`, `--metadata-output`)
  - clear missing-file and invalid-record failures
  - TF-IDF build with `TfidfVectorizer`:
    - `analyzer=\"word\"`
    - `ngram_range=(1, 2)`
    - `lowercase=False`
    - `min_df=1`
    - `max_df=1.0`
  - artifact save to `outputs/tfidf_index.joblib` with:
    - `vectorizer`
    - `matrix`
    - `chunk_ids`
    - `metadata`
  - human-readable metadata save to `outputs/index_metadata.json`
  - row-order contract preserved: matrix row `i` aligns with `chunk_ids[i]` and `metadata[i]`
- Added tests in `pocs/03d_word_tfidf_index/tests/test_build_tfidf_index.py`:
  - record loading
  - missing-field validation failure
  - row-count correctness
  - chunk ID order preservation
  - expected vocabulary terms
  - joblib artifact persistence
  - metadata JSON persistence
  - preservation of original + normalized text in artifact metadata
  - tiny TF-IDF ranking smoke test
- Updated `pocs/03d_word_tfidf_index/README.md` and `requirements.txt` for real implementation behavior and commands.
- Updated project memory files to mark 03d complete and set next suggested step to 03e discussion only.

## Validation (Milestone 3 Step 03d - Word TF-IDF Index)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\pocs\03d_word_tfidf_index\src\build_tfidf_index.py` (PASS)
    - input chunks: `23`
    - matrix shape: `(23, 2002)`
    - vocabulary size: `2002`
    - outputs:
      - `pocs/03d_word_tfidf_index/outputs/tfidf_index.joblib`
      - `pocs/03d_word_tfidf_index/outputs/index_metadata.json`
  - `pytest -v .\pocs\03d_word_tfidf_index\tests` (PASS, 9 tests passed in 1.08s)
- Confirmed no forbidden scope areas were touched (`integrated/servicecall-ai`, chatbot/LLM/embeddings/BM25/hybrid retrieval, FastAPI, Docker, AWS, CI-CD).

## 2026-05-03 (Project Direction Note - Guided Customer Input)
- Updated project tracking/state documentation to add a future product direction note:
  - `Product Direction Add-On: Guided Customer Input`
- Added the section to `PROJECT_STATE.md` and `HANDOFF.md` with scope notes:
  - autocomplete suggestions while typing
  - autocorrect-style typo assistance
  - service-intent suggestion buttons
  - clarification choices for ambiguous input
  - example disambiguation for `heater repaid`
- Recorded that this direction:
  - does not replace retrieval
  - supports retrieval by improving input quality
  - still depends on robust backend retrieval for messy input (word TF-IDF, character TF-IDF, hybrid retrieval, later semantic search)
  - is future product direction only, not current 03e implementation
- Updated `TASK_BOARD.md` backlog and `CHANGELOG.md` to reflect the added direction note.

## Validation (Project Direction Note - Guided Customer Input)
- Confirmed this task changed documentation/tracking files only.
- Confirmed no POC code files under `pocs/*/src` or `pocs/*/tests` were modified by this task.

## 2026-05-03 (Milestone 3 Step 03e - Character TF-IDF Typo Search)
- Implemented `pocs/03e_char_tfidf_typo_search` only.
- Added Pydantic schema contract in `pocs/03e_char_tfidf_typo_search/src/schemas.py` for required normalized chunk fields:
  - `chunk_id`, `document_id`, `source_file`, `source_path`, `title`, `chunk_index`
  - `text`, `character_count`
  - `normalized_text`, `normalized_character_count`
- Added standalone, chainable builder script in `pocs/03e_char_tfidf_typo_search/src/build_char_tfidf_index.py`:
  - relative default paths + argparse overrides (`--input`, `--index-output`, `--metadata-output`, `--sample-results-output`)
  - clear missing-file and invalid-record failures
  - character TF-IDF build with `TfidfVectorizer`:
    - `analyzer=\"char_wb\"`
    - `ngram_range=(3, 5)`
    - `lowercase=False`
    - `min_df=1`
    - `max_df=1.0`
  - artifact save to `outputs/char_tfidf_index.joblib` with:
    - `vectorizer`
    - `matrix`
    - `chunk_ids`
    - `metadata`
  - metadata save to `outputs/char_index_metadata.json`
  - sample typo-search candidate results save to `outputs/sample_typo_search_results.json`
  - row-order contract preserved: matrix row `i` aligns with `chunk_ids[i]` and `metadata[i]`
- Added tests in `pocs/03e_char_tfidf_typo_search/tests/test_build_char_tfidf_index.py`:
  - record loading
  - missing-field validation failure
  - row-count correctness
  - chunk ID order preservation
  - vectorizer analyzer/params verification
  - joblib artifact persistence
  - metadata JSON persistence
  - preservation of original + normalized text in artifact metadata
  - typo query ranking smoke tests (`ac repiar`, `watr heater`)
  - sample typo results generation structure
- Updated `pocs/03e_char_tfidf_typo_search/README.md` and `requirements.txt` for implementation behavior and learning guidance.
- Updated project memory files to mark 03e complete and set next suggested step to 03f discussion only.

## Validation (Milestone 3 Step 03e - Character TF-IDF Typo Search)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\pocs\03e_char_tfidf_typo_search\src\build_char_tfidf_index.py` (PASS)
    - input chunks: `23`
    - matrix shape: `(23, 5779)`
    - vocabulary size: `5779`
    - outputs:
      - `pocs/03e_char_tfidf_typo_search/outputs/char_tfidf_index.joblib`
      - `pocs/03e_char_tfidf_typo_search/outputs/char_index_metadata.json`
      - `pocs/03e_char_tfidf_typo_search/outputs/sample_typo_search_results.json`
  - `pytest -v .\pocs\03e_char_tfidf_typo_search\tests` (PASS, 11 tests passed in 1.03s)
- Confirmed no forbidden scope areas were touched (`integrated/servicecall-ai`, LLM/embeddings/FAISS/BM25/hybrid retrieval implementation, frontend autocomplete/autocorrect UI, FastAPI, Docker, AWS, CI-CD).

## 2026-05-03 (Closure Pass After 03e)
- Ran a closure/update-only pass on project memory files after completing `03e_char_tfidf_typo_search`.
- Captured completed ladder summary (`03a` to `03e`) with PASS status and final artifact outputs:
  - `03a`: 16 docs loaded -> `loaded_documents.json`
  - `03b`: boundary-aware chunking -> `chunked_documents.json` (23 chunks, 8 tests passed)
  - `03c`: normalization -> `normalized_chunks.json` (6 tests passed)
  - `03d`: word TF-IDF -> `tfidf_index.joblib` + `index_metadata.json` (matrix `23 x 2002`, 9 tests passed)
  - `03e`: char TF-IDF typo search -> `char_tfidf_index.joblib` + `char_index_metadata.json` + `sample_typo_search_results.json` (matrix `23 x 5779`, 11 tests passed)
- Re-affirmed key learning:
  - word TF-IDF handles clean wording and exact business terms
  - character TF-IDF helps with misspellings/messy typing
  - `03e` returns candidate matches only, not final intent decisions
- Re-affirmed product direction:
  - Guided Customer Input supports retrieval (autocomplete, autocorrect-style help, intent buttons, clarifications) and does not replace backend retrieval.
- Re-affirmed design law:
  - every POC should be standalone, configurable, reusable, and chainable.
- Set next recommended step to `03f_hybrid_retrieval` discussion only (no implementation).

## Validation (Closure Pass After 03e)
- Confirmed this pass updated tracking/state files only.
- Confirmed no POC source/test implementation changes were made in this pass.
- Confirmed `03f_hybrid_retrieval` was not implemented.
