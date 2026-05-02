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
