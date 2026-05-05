# DAILY_LOG.md

## 2026-05-04 (Milestone 4 Step 04e - Live Service Integration PASS)
- Closed `pocs/04e` as PASS.
- Implemented FastAPI integration layer around the validated deterministic 04d pipeline:
  - `pocs/04e/src/app.py`
  - `pocs/04e/src/routes.py`
  - `pocs/04e/src/service.py`
- Implemented API test coverage:
  - `pocs/04e/tests/test_api.py`
  - endpoint correctness (`/v1/health`, `/v1/query`, `/v1/answer`)
  - timing metric presence checks
  - unknown scenario error handling
  - request contract validation behavior
- Added API docs:
  - `pocs/04e/docs/CONTRACT.md`
  - `pocs/04e/docs/TEST_PLAN.md`
- Added sample API request/response artifact:
  - `pocs/04e/outputs/sample_api_responses.json`
- Validation evidence:
  - `. D:\Workarea\StudyBook\env_setter.ps1; pytest -v .\pocs\04e\tests` -> PASS (`5 passed`)
- Non-goals preserved:
  - no threshold tuning
  - no LLM calls
  - no customer answer generation
  - no modification of 03f/03g artifacts
  - no move into `integrated/servicecall-ai`

## 2026-05-04 (Milestone 4 Step 04d - Expansion Pack PASS)
- Closed `pocs/04d` expansion pack as PASS.
- Implemented deliverables:
  - updated `pipeline_test_harness.py` with per-scenario execution timing
  - expanded mock evidence scenarios:
    - `failure-insufficient-evidence`
    - `failure-escalation-required`
    - `negative-bad-citation` (expected failure)
  - added lightweight batch generator for performance testing
  - updated `schemas.py`, `test_harness.py`, and `test_runner.py`
  - refreshed `outputs/sample_pipeline_runs.json` with timing + expanded scenario results
- Validation evidence:
  - `. D:\Workarea\StudyBook\env_setter.ps1; pytest -v .\pocs\04d\tests` -> PASS (`6 passed`)
- Non-goals preserved:
  - no threshold tuning
  - no LLM calls
  - no customer answer generation
  - no movement into `integrated/servicecall-ai`
  - no rebuild/modification of `03d`/`03e`/`03f`/`03g` artifacts

## 2026-05-04 (Milestone 4 Step 04b - Answer Contract Schemas PASS)
- Closed `pocs/04b_answer_contract_schemas` as PASS.
- Recorded implemented files:
  - `pocs/04b_answer_contract_schemas/src/__init__.py`
  - `pocs/04b_answer_contract_schemas/src/schemas.py`
  - `pocs/04b_answer_contract_schemas/tests/conftest.py`
  - `pocs/04b_answer_contract_schemas/tests/test_schemas.py`
- Confirmed purpose:
  - converts approved `04a` answer assembly contract into strict Pydantic schema models and validation tests
- Recorded implementation coverage:
  - strict enums/models for contract objects
  - branch exclusivity and full top-level outcome validation
  - strict `outcome_type` <-> `route_applied` mapping
  - citation cross-validation by `chunk_id` with selected-text-first and retrieved-text fallback
  - normalized-exact citation matching
  - request-level evidence gating via `evidence_attempted`
  - claim/support-status boundaries
  - escalation safety validation
  - clarification requirements
  - insufficient-evidence anti-answer guard
- Validation evidence:
  - `. 'D:\Workarea\StudyBook\env_setter.ps1'; pytest -v .\pocs\04b_answer_contract_schemas\tests` -> PASS (`31 passed`)
- Non-goals preserved:
  - no LLM calls
  - no customer-facing answer generation
  - no threshold tuning
  - no modifications to `03d`/`03e`/`03f`/`03g`/`03h`
  - no movement into `integrated/servicecall-ai`

## 2026-05-03 (Milestone 4 Step 04a - Answer Contract Design PASS)
- Closed `pocs/04a_answer_contract_design` as PASS (design-only).
- Recorded completed design-document set:
  - `pocs/04a_answer_contract_design/README.md`
  - `pocs/04a_answer_contract_design/docs/DESIGN.md`
  - `pocs/04a_answer_contract_design/docs/CONTRACT.md`
  - `pocs/04a_answer_contract_design/docs/TEST_PLAN.md`
- Recorded contract patch completion:
  - all outcome examples now use full top-level `AnswerAssemblyOutcome` shape
  - `SelectedEvidenceItem` now includes `selected_text`
  - citation span traceability clarified (`selected_text` or original retrieved `text` by `chunk_id`)
  - document-derived `factual`, `instructional`, and `policy` claim citation requirement clarified
  - conversational glue text citation exemption clarified
  - escalation enums added for `severity` and `handoff_target`
  - `TEST_PLAN` expanded for these validation checks
- Non-goals preserved:
  - no Python code
  - no `src/`, `tests/`, `outputs/`
  - no LLM calls
  - no customer-facing answer generation
  - no threshold tuning
  - no modifications to `03d`/`03e`/`03f`/`03g`/`03h`
  - no movement into `integrated/servicecall-ai`

## 2026-05-03 (Milestone 3 Step 03h - Final Closure PASS)
- Closed `pocs/03h_retrieval_evaluation` as PASS.
- Recorded completed 03h documentation set:
  - `README.md`
  - `docs/DESIGN.md`
  - `docs/CONTRACT.md`
  - `docs/TEST_PLAN.md`
- Recorded completed implementation slices:
  - fixture schema and fixture loader
  - upstream `03f`/`03g` loaders
  - alignment helper with `normalized_query` primary and `query` fallback
  - per-case evaluator (`expected_chunk_found`, `expected_chunk_rank`, `hit@1`, `hit@3`, `hit@5`, decision/route checks)
  - aggregate summary metrics
  - output-writing layer (`evaluation_report.json`, `evaluation_summary.md`)
  - minimal runner and runner smoke test
- Validation evidence captured:
  - `. D:\Workarea\StudyBook\env_setter.ps1; pytest -v .\pocs\03h_retrieval_evaluation\tests` -> PASS (`49 passed in 0.66s`)
  - `python .\pocs\03h_retrieval_evaluation\src\run_retrieval_evaluation.py` -> PASS
  - runner result: `Total cases: 3`, `Passed: 3`, `Failed: 0`, `Warning: 0`, `Pass rate: 1.000000`
- Output artifacts confirmed:
  - `pocs/03h_retrieval_evaluation/outputs/evaluation_report.json`
  - `pocs/03h_retrieval_evaluation/outputs/evaluation_summary.md`
- Non-goals preserved:
  - no threshold tuning
  - no LLM calls
  - no customer answer generation
  - no `integrated/servicecall-ai` movement
  - no rebuild/modification of `03d`/`03e`/`03f`/`03g` artifacts

## 2026-05-03 (Milestone 3 Step 03g - Closure and Tracking Update)
- Performed closure/tracking-only update after `03g_retrieval_decision` implementation and validation.
- Marked `03g_retrieval_decision` as PASS in project memory files.
- Recorded completed 03g deliverables:
  - design docs complete (`README`, `docs/DESIGN.md`, `docs/CONTRACT.md`, `docs/TEST_PLAN.md`)
  - implementation complete (`src/`, `tests/`, `outputs/`, plus `config/decision_config.json`)
- Recorded validation results:
  - `pytest -v .\pocs\03g_retrieval_decision\tests` -> PASS (`14 passed`)
  - `python .\pocs\03g_retrieval_decision\src\run_retrieval_decision.py` -> PASS (`6` queries processed)
- Set next step framing to `03h_retrieval_evaluation` discussion/scope only.
- Confirmed this pass made no logic changes to 03g.

## 2026-05-03 (Milestone 3 Step 03f - Final Acceptance Cleanup)
- Updated 03f docs to present tense where runner/sample output now exist.
- Verified expected 03f files exist:
  - requirements, README, docs (`DESIGN`, `CONTRACT`, `TEST_PLAN`)
  - source (`schemas.py`, `hybrid_retrieval.py`, `run_hybrid_search.py`)
  - tests (`test_schemas.py`, `test_hybrid_retrieval.py`)
  - output (`outputs/sample_hybrid_search_results.json`)
- Validated sample output structure:
  - `poc = 03f_hybrid_retrieval`
  - config `word_weight=0.65`, `char_weight=0.35`, `top_k=5`
  - `6` sample queries
  - every query has results with required `HybridSearchResult` fields
- Validation commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
  - `pytest -v .\pocs\03f_hybrid_retrieval\tests` -> PASS (`16 passed`)
  - `python .\pocs\03f_hybrid_retrieval\src\run_hybrid_search.py` -> PASS
- Marked `03f_hybrid_retrieval` as PASS/completed in tracking files.
- Confirmed no customer answers or final intent decisions were generated.

## 2026-05-03 (Milestone 3 Step 03f - Runner and Sample Output)
- Added thin runner: `pocs/03f_hybrid_retrieval/src/run_hybrid_search.py`.
- Runner reuses existing `HybridRetrievalConfig` and `hybrid_search` (no duplicated core logic).
- Runner executes sample queries and writes:
  - `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json`
- Updated `03f` docs (`README`, `DESIGN`, `CONTRACT`, `TEST_PLAN`) and project tracking files to reflect runner completion.

## 2026-05-03 (Milestone 3 Step 03f - Reusable Core Retrieval Module)
- Implemented `pocs/03f_hybrid_retrieval/src/hybrid_retrieval.py` with reusable functions:
  - `load_index_artifact`
  - `search_index_artifact`
  - `merge_retrieval_results`
  - `hybrid_search`
- Reused query normalization behavior from `03c_text_normalization` via imported normalization function.
- Added core module tests in `pocs/03f_hybrid_retrieval/tests/test_hybrid_retrieval.py`.
- Updated `03f` README and docs (`DESIGN`, `CONTRACT`, `TEST_PLAN`) for current implementation status.
- Updated tracking files to reflect that 03f core logic is implemented while runner/output writing is still pending.

## 2026-05-03 (Milestone 3 Step 03f - Schemas and Contract Tests)
- Implemented `pocs/03f_hybrid_retrieval/src/schemas.py` with Pydantic models:
  - `HybridRetrievalConfig`
  - `HybridSearchQuery`
  - `HybridSearchResult`
  - `HybridSearchResponse`
- Added validation coverage in `pocs/03f_hybrid_retrieval/tests/test_schemas.py`.
- Updated `pocs/03f_hybrid_retrieval/docs/CONTRACT.md` to align with exact model names and `retrieval_sources` values (`word` / `char`).
- Updated `pocs/03f_hybrid_retrieval/README.md` implementation status to show schema/contracts now implemented.
- Updated tracking files to reflect: `03f` schema/contracts complete, full retrieval logic not implemented yet.

## 2026-05-03 (03f Documentation Cleanup and Rule Standardization)
- Standardized planned `03f_hybrid_retrieval` runner script naming in docs to `src/run_hybrid_search.py`.
- Added standing POC documentation structure rule to control/tracking docs.
- Added standing POC acceptance gate to control/tracking docs.
- Kept this task documentation/tracking only with no Python implementation changes.

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

## 2026-05-04
- Persisted thread design artifacts for POC 04c and POC 04d into repository docs.
- Created pocs/04c_schema_validation_integration with README and docs package.
- Updated pocs/04d_full_rag_pipeline_testing README/docs to match approved design summary.


## 2026-05-04 - POC 04d Expansion Pack
- Expanded pocs/04d deterministic pipeline harness with per-scenario timing metrics (xecution_time_ms).
- Added new explicit failure-safe scenarios in mock_evidence_sets.py:
  - ailure-insufficient-evidence`n  - ailure-escalation-required`n- Preserved designed failing case 
egative-bad-citation as expected-failure validation.
- Added lightweight performance batch generator uild_performance_batch(batch_size=...) for multi-scenario throughput checks.
- Updated scenario/result schema and tests (	est_harness.py, 	est_runner.py) to validate expanded coverage and timing fields.
- Regenerated output artifact: pocs/04d/outputs/sample_pipeline_runs.json.
- Validation command: . D:\Workarea\StudyBook\env_setter.ps1; pytest -q .\pocs\04d\tests; python .\pocs\04d\src\run_pipeline_tests.py`n- Validation result: 6 passed.


## 2026-05-04 - POC 04f Kickoff Persistence
- Created pocs/04f baseline structure with src/, 	ests/, docs/, outputs/.
- Persisted approved kickoff prompt to pocs/04f/outputs/POC_04f_kickoff_prompt.md.
- Added design-first starter docs:
  - pocs/04f/README.md
  - pocs/04f/docs/DESIGN.md
  - pocs/04f/docs/CONTRACT.md
  - pocs/04f/docs/TEST_PLAN.md
- No service code or tests implemented yet in 04f during this slice.

## 2026-05-04 - 04f deterministic Docker-first teaching thread initialization
- Created `pocs/04f/outputs/POC_04f_THREAD_INIT.md` to initialize a teaching-oriented Codex thread for POC 04f.
- Included deterministic endpoint references (`/health`, `/ping`), Docker build/run, in-container pytest, and smoke test workflow.
- Added guidance for folder roles (`src/`, `tests/`, `docs/`, `outputs/`), placeholder tests, log structure, and teaching extensions.
- Updated `pocs/04f/outputs/POC_04f_SUMMARY.md` title to mark it as `(Teaching Reference)` snapshot.

## 2026-05-04 - Persisted 04f teaching/debug memory
- Persisted Docker-first deterministic reference details for POC 04f into project memory files.
- Captured script, endpoints, pytest-in-container status, image/container naming, smoke/log/output evidence paths, and teaching snapshot references.
- This entry is intended as durable context for future teaching, extension, and debugging threads.

## 2026-05-04 - 04f workflow diagram documentation artifact
- Created `pocs/04f/outputs/POC_04f_WORKFLOW_DIAGRAM.md`.
- Added Mermaid onboarding diagram covering source/tests, Docker build+run, in-container pytest, deterministic `/health` and `/ping` smoke checks, and evidence outputs.
- Included concise teaching explanation and extension guidance.
- Referenced summary/thread-init/kickoff artifacts for full documentation continuity.

## 2026-05-05 - 04f Phase 1 multi-sentence query handling
- Updated `pocs/04f/src/service.py` with Pydantic `IntentParseResult` and deterministic multi-sentence intent extraction.
- Added greeting/small-talk suppression and service-keyword segment scoring to keep retrieval focused on the main problem statement.
- Updated `pocs/04f/src/app.py` to initialize `SimpleRetriever` with explicit stopwords file (`config/stopwords.json`).
- Updated `pocs/04f/src/retriever.py` with runtime fallbacks:
  - Levenshtein -> `difflib.SequenceMatcher` when dependency is unavailable.
  - Porter stemmer -> lightweight fallback stemmer when `nltk` is unavailable.
- Rebuilt `pocs/04f/interactive_grok_test.py` for standalone local flow:
  - query -> parse_intent -> retriever -> generate_response,
  - appends logs to `pocs/04f/outputs/ask_logs.json`.
- Added tests: `pocs/04f/tests/test_phase1_multisentence.py`.
- Validation:
  - `. D:\Workarea\StudyBook\env_setter.ps1; pytest -q pocs/04f/tests/test_phase1_multisentence.py` -> PASS (`2 passed`).
  - Scripted CLI run with irrelevant-context multi-sentence queries showed expected intent extraction and relevant retrieval.
- Out-of-scope maintained: no website changes, no Docker changes.

## 2026-05-05 - POC 04g Local LLM Container Documentation
- Added complete design-first documentation set for `pocs/04g`:
  - `README.md`
  - `docs/DESIGN.md`
  - `docs/CONTRACT.md`
  - `docs/TEST_PLAN.md`
- Added smoke-test evidence artifact:
  - `pocs/04g/outputs/SMOKE_TEST_RESULT.md`
- Captured factual status only:
  - standalone Mistral 7B container build/run succeeded
  - model files mounted from `C:\LLM_models\Mistral7B`
  - `/health` and `/infer` passed
  - smoke script passed
- Preserved scope guardrails:
  - no behavior refactor
  - no integrated-lane move
  - no production-readiness claim

## 2026-05-05 - 04h Local RAG Orchestrator Kickoff (Local Python/FastAPI)
- Created new POC: `pocs/04h_local_rag_orchestrator`.
- Added design-first docs:
  - `README.md`
  - `docs/DESIGN.md`
  - `docs/CONTRACT.md`
  - `docs/TEST_PLAN.md`
- Added synthetic KB and orchestrator modules:
  - `data/knowledge_base.json`
  - `src/kb_loader.py`
  - `src/retriever.py`
  - `src/llm_gateway.py`
  - `src/service.py`
  - `src/app.py`
- Added tests and smoke:
  - `tests/test_kb_loader.py`
  - `tests/test_retriever.py`
  - `tests/test_service.py`
  - `smoke_test_04h.py`
  - `outputs/SMOKE_TEST_RESULT.md`
- Validation:
  - `. D:\Workarea\StudyBook\env_setter.ps1; python -m pytest -q pocs/04h_local_rag_orchestrator/tests` -> PASS (`7 passed`)
  - local `uvicorn src.app:app --host 127.0.0.1 --port 8010` + `python .\smoke_test_04h.py` -> PASS
- Scope guardrails preserved:
  - no Docker for 04h
  - no changes to `pocs/04f`, `pocs/04g`, runtime behavior in `pocs/04g-quantized`
  - no integrated-lane changes
