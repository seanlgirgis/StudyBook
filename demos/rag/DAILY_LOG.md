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
- Added Pydantic schemas in `src/schemas.py`:
  - `SourceDocument` input contract validation
  - `ChunkingConfig` validation for safe overlap settings
  - `ChunkDocument` output contract with offset integrity checks
- Added chunking pipeline script in `src/chunk_documents.py`:
  - loads `03a` output JSON
  - validates source documents
  - creates overlapping character-window chunks with deterministic ids
  - writes `outputs/chunk_documents.json`
- Added tests in `tests/test_chunk_documents.py`.
- Updated `README.md` with runnable commands and output expectations.
- Added learning notes:
  - `notes/what_this_teaches.md`
  - `notes/common_failures.md`

## Validation (Milestone 3 Step 03b - Chunk Documents)
- Ran bootstrap before Python commands:
  - `. D:\Workarea\StudyBook\env_setter.ps1`
- Ran:
  - `python .\src\chunk_documents.py` (PASS, loaded 16 documents and generated 42 chunks)
  - `pytest -v` (PASS, 3 tests passed)
- Confirmed `outputs/chunk_documents.json` exists and is populated with validated chunk records.
- Confirmed no forbidden scope areas were touched (`integrated/servicecall-ai`, backend/FastAPI, Docker/AWS/CI-CD, or 03c+ implementation).
