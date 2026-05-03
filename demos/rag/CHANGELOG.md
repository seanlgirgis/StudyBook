# CHANGELOG.md

## 2026-05-01
### Added
- Permanent project memory files: `DAILY_LOG.md`, `DECISIONS.md`, `KNOWN_ISSUES.md`, `CHANGELOG.md`.
- Milestone 1 static shell files and content in `pocs/01_static_site_shell`:
  - `website/index.html`
  - `website/assets/styles.css`
  - `website/assets/chat-widget.js`
  - `notes/what_this_teaches.md`
  - `notes/questions.md`
- `aux_scripts/` helper utilities:
  - `aux_scripts/README.md`
  - `aux_scripts/show_tree.ps1`
  - `aux_scripts/zip_folder_for_chatgpt.ps1`
  - `aux_scripts/check_poc_static_site.ps1`
  - `aux_scripts/snapshot_project_state.ps1`
- Milestone 1 Cloudflare static smoke-test record:
  - `pocs/01_static_site_shell/notes/cloudflare_static_smoke_test.md`

### Changed
- `AGENTS.md` now enforces:
  - environment bootstrap command before Python/pytest/pip/FastAPI/scripts
  - closed-loop reporting format after every task
  - expanded required read/update file sets
  - milestone stop-rule escalation behavior
- `PROJECT_STATE.md` now states the closed-loop project-control protocol exists.
- `TASK_BOARD.md` now marks permanent agent memory / closed-loop protocol as done.
- `HANDOFF.md` now explicitly keeps the next task at `pocs/01_static_site_shell` only.
- `pocs/01_static_site_shell/README.md` now documents purpose, files, run steps, learning outcomes, exclusions, and next step.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, and `HANDOFF.md` now reflect Milestone 1 static site shell completion and next review step.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect aux script utility support and validation workflow.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now include Milestone 1 Cloudflare static-hosting smoke-test documentation status.

## 2026-05-02
### Added
- Milestone 2 synthetic business documents and notes in `pocs/02_fake_business_docs`:
  - `data/home_services_demo/company_profile.md`
  - `data/home_services_demo/service_area.md`
  - `data/home_services_demo/business_hours.md`
  - `data/home_services_demo/hvac_repair_policy.md`
  - `data/home_services_demo/ac_replacement_estimates.md`
  - `data/home_services_demo/plumbing_services.md`
  - `data/home_services_demo/water_heater_policy.md`
  - `data/home_services_demo/appliance_repair_policy.md`
  - `data/home_services_demo/maintenance_plan.md`
  - `data/home_services_demo/coupon_policy.md`
  - `data/home_services_demo/scheduling_policy.md`
  - `data/home_services_demo/financing_policy.md`
  - `data/home_services_demo/warranty_policy.md`
  - `data/home_services_demo/escalation_rules.md`
  - `data/home_services_demo/intake_script.md`
  - `data/home_services_demo/faq.md`
  - `notes/retrieval_questions.md`
  - `notes/what_good_answers_should_include.md`
  - `notes/document_design_notes.md`
- Milestone 3 retrieval ladder scaffolding:
  - `pocs/03a_load_documents/`
  - `pocs/03b_chunk_documents/`
  - `pocs/03c_text_normalization/`
  - `pocs/03d_word_tfidf_index/`
  - `pocs/03e_char_tfidf_typo_search/`
  - `pocs/03f_hybrid_retrieval/`
  - `pocs/03g_retrieval_decision/`
  - `pocs/03h_retrieval_evaluation/`
  - `pocs/03_RETRIEVAL_LADDER.md`
  - `pocs/03a_load_documents/src/schemas.py`
  - `pocs/03a_load_documents/src/load_documents.py`
  - `pocs/03a_load_documents/tests/test_load_documents.py`
  - `pocs/03a_load_documents/outputs/loaded_documents.json`
  - `pocs/03a_load_documents/notes/what_this_teaches.md`
  - `pocs/03a_load_documents/notes/common_failures.md`

### Changed
- `pocs/02_fake_business_docs/README.md` now defines purpose, file map, synthetic warning, and next milestone.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect Milestone 2 completion and next-step retrieval POC direction.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect Milestone 3 retrieval-learning structure staging (no implementation yet).
- `pocs/03a_load_documents/README.md` and `requirements.txt` now reflect actual load-documents implementation and test commands.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect Milestone 3 step `03a_load_documents` completion.
- `pocs/03a_load_documents/src/schemas.py` and `pocs/03a_load_documents/src/load_documents.py` now include educational docstrings/comments without behavior changes.

## 2026-05-03
### Added
- Milestone 3 step `03b_chunk_documents` implementation files:
  - `pocs/03b_chunk_documents/src/schemas.py`
  - `pocs/03b_chunk_documents/src/chunk_documents.py`
  - `pocs/03b_chunk_documents/tests/test_chunk_documents.py`
  - `pocs/03b_chunk_documents/NOTES.md`
  - `pocs/03b_chunk_documents/outputs/chunked_documents.json`
- Milestone 3 step `03c_text_normalization` implementation files:
  - `pocs/03c_text_normalization/src/schemas.py`
  - `pocs/03c_text_normalization/src/normalize_text.py`
  - `pocs/03c_text_normalization/tests/test_normalize_text.py`
  - `pocs/03c_text_normalization/outputs/normalized_chunks.json`
- Milestone 3 step `03d_word_tfidf_index` implementation files:
  - `pocs/03d_word_tfidf_index/src/schemas.py`
  - `pocs/03d_word_tfidf_index/src/build_tfidf_index.py`
  - `pocs/03d_word_tfidf_index/tests/test_build_tfidf_index.py`
  - `pocs/03d_word_tfidf_index/outputs/tfidf_index.joblib`
  - `pocs/03d_word_tfidf_index/outputs/index_metadata.json`
- Milestone 3 step `03e_char_tfidf_typo_search` implementation files:
  - `pocs/03e_char_tfidf_typo_search/src/schemas.py`
  - `pocs/03e_char_tfidf_typo_search/src/build_char_tfidf_index.py`
  - `pocs/03e_char_tfidf_typo_search/tests/test_build_char_tfidf_index.py`
  - `pocs/03e_char_tfidf_typo_search/outputs/char_tfidf_index.joblib`
  - `pocs/03e_char_tfidf_typo_search/outputs/char_index_metadata.json`
  - `pocs/03e_char_tfidf_typo_search/outputs/sample_typo_search_results.json`

### Changed
- `pocs/03b_chunk_documents/README.md` now documents real commands, expected output, and stage boundaries.
- `pocs/03b_chunk_documents/requirements.txt` now includes `pytest>=8.0`.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect Milestone 3 step `03b_chunk_documents` completion and next-step gating to `03c_text_normalization` after approval.
- `pocs/03b_chunk_documents/src/chunk_documents.py` now uses boundary-aware chunking with fallback order: section heading -> paragraph -> newline -> sentence -> word -> hard split.
- `pocs/03b_chunk_documents/tests/test_chunk_documents.py` now includes boundary-quality checks for no mid-word chunk starts/ends.
- `pocs/03b_chunk_documents/README.md` and `pocs/03b_chunk_documents/NOTES.md` now document the refinement from size-first chunking to clean boundary-aware chunking.
- `PROJECT_STATE.md`, `HANDOFF.md`, and `DAILY_LOG.md` now record final 03b closure status and validation results: `python .\pocs\03b_chunk_documents\src\chunk_documents.py` PASS, `pytest -v` PASS (8 passed in 0.15s), 16 input documents, 23 chunks.
- `pocs/03c_text_normalization/README.md` now documents actual 03c behavior, I/O paths, normalization rules, and run commands.
- `pocs/03c_text_normalization/requirements.txt` now includes `pytest>=8.0` with `pydantic>=2.0`.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect 03c completion and next-step gating to discussion of `03d_word_tfidf_index` only.
- `pocs/03c_text_normalization` now preserves original chunk fields and adds normalized fields with rules: Unicode normalization (`NFKC`), smart punctuation handling, dash cleanup, lowercasing, punctuation-to-space cleanup, whitespace collapse, and AC term normalization (`A/C`/`a/c` -> `ac`, `air-conditioning` -> `air conditioning`).
- `pocs/03d_word_tfidf_index/README.md` now documents actual 03d behavior, I/O paths, vectorizer configuration, and out-of-scope boundaries.
- `pocs/03d_word_tfidf_index/requirements.txt` now includes runtime/test dependencies: `pydantic`, `scikit-learn`, `joblib`, and `pytest`.
- `pocs/03d_word_tfidf_index` now builds/saves a reusable TF-IDF artifact (`vectorizer`, `matrix`, `chunk_ids`, `metadata`) from 03c normalized chunks with guaranteed row-order alignment.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect 03d completion and next-step gating to discussion of `03e_char_tfidf_typo_search` only.
- `PROJECT_STATE.md` and `HANDOFF.md` now include a product-direction note titled `Product Direction Add-On: Guided Customer Input` covering autocomplete, autocorrect-style typo assistance, intent buttons, and ambiguity-clarification choices.
- `TASK_BOARD.md` now includes Guided Customer Input as a future backlog item, explicitly outside current 03e implementation scope.
- `pocs/03e_char_tfidf_typo_search/README.md` now documents the full 03e learning model: word-vs-char TF-IDF, typo-rescue scope, candidate-match boundaries, and next-step guidance.
- `pocs/03e_char_tfidf_typo_search/requirements.txt` now includes runtime/test dependencies: `pydantic`, `scikit-learn`, `joblib`, and `pytest`.
- `pocs/03e_char_tfidf_typo_search` now builds/saves a reusable character TF-IDF artifact (`vectorizer`, `matrix`, `chunk_ids`, `metadata`) from 03c normalized chunks with guaranteed row-order alignment and writes sample typo candidate matches.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `DAILY_LOG.md`, and `HANDOFF.md` now reflect 03e completion and next-step gating to discussion of `03f_hybrid_retrieval` only.
- `PROJECT_STATE.md` and `HANDOFF.md` now include a closure snapshot section summarizing PASS status for the completed 03a->03e ladder and preserved learning points.
- `TASK_BOARD.md` now includes explicit `03f_hybrid_retrieval` discussion-only planning before any implementation.
- `DAILY_LOG.md` now records a closure/update-only pass confirming no POC code changes and no 03f implementation.
- `pocs/03f_hybrid_retrieval/README.md` now standardizes the planned runner name to `src/run_hybrid_search.py` (documentation only; no implementation).
- `AGENTS.md`, `PROJECT_STATE.md`, and `HANDOFF.md` now include a standing POC documentation structure rule requiring `README.md`, `docs/DESIGN.md`, `docs/CONTRACT.md`, `docs/TEST_PLAN.md`, `src/`, `tests/`, and `outputs/`.
- `AGENTS.md`, `PROJECT_STATE.md`, and `HANDOFF.md` now include a standing POC acceptance gate requiring working code, passing tests, sample output, and complete usage/design/contract/test-plan documentation.
- `pocs/03f_hybrid_retrieval/README.md` now records that schema/contracts are implemented while retrieval/search logic remains pending.
- `pocs/03f_hybrid_retrieval/docs/CONTRACT.md` now aligns with implemented schema names: `HybridRetrievalConfig`, `HybridSearchQuery`, `HybridSearchResult`, `HybridSearchResponse`, and `retrieval_sources` values `word`/`char`.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `HANDOFF.md`, and `DAILY_LOG.md` now reflect 03f schema/contracts completion and that full retrieval logic is still not implemented.

### Added
- `pocs/03f_hybrid_retrieval/src/schemas.py`
- `pocs/03f_hybrid_retrieval/tests/test_schemas.py`
- `pocs/03f_hybrid_retrieval/outputs/.gitkeep`
- `pocs/03f_hybrid_retrieval/src/hybrid_retrieval.py`
- `pocs/03f_hybrid_retrieval/tests/test_hybrid_retrieval.py`
- `pocs/03f_hybrid_retrieval/src/run_hybrid_search.py`

### Changed
- `pocs/03f_hybrid_retrieval/requirements.txt` now includes `scikit-learn` and `joblib` for reusable hybrid retrieval core execution.
- `pocs/03f_hybrid_retrieval/README.md` now marks core retrieval module and tests implemented, with runner/output generation still pending.
- `pocs/03f_hybrid_retrieval/docs/DESIGN.md` now documents implemented core functions and reuse of 03c normalization behavior.
- `pocs/03f_hybrid_retrieval/docs/CONTRACT.md` now includes required artifact keys and top-k/normalization contract notes.
- `pocs/03f_hybrid_retrieval/docs/TEST_PLAN.md` now records implemented unit coverage for core retrieval behavior.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `HANDOFF.md`, and `DAILY_LOG.md` now reflect completion of the 03f reusable core retrieval step and remaining runner/output work.
- `pocs/03f_hybrid_retrieval/README.md`, `docs/DESIGN.md`, `docs/CONTRACT.md`, and `docs/TEST_PLAN.md` now reflect runner implementation and sample-output generation behavior.
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `HANDOFF.md`, and `DAILY_LOG.md` now reflect 03f runner completion and sample output generation status.
- 03f documentation wording is now present-tense for implemented behavior (inputs read, output written, current commands).
- `PROJECT_STATE.md`, `TASK_BOARD.md`, `HANDOFF.md`, and `DAILY_LOG.md` now mark `03f_hybrid_retrieval` as PASS/completed and set next step to `03g_retrieval_decision` planning only.
