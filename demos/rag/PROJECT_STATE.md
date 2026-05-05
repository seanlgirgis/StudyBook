# PROJECT_STATE.md

## Current Milestone
Milestone 4 (Step 04e) — Live service integration layer completed and PASS (`pocs/04e`)

## Current Focus
`04e` integration is implemented and closed as PASS.
The validated 04d deterministic evidence pipeline is now exposed behind a FastAPI service layer with schema-validated request handling, structured answer responses, and timing metrics in live endpoint responses.
Validation for 04e API integration: `. D:\Workarea\StudyBook\env_setter.ps1; pytest -v .\pocs\04e\tests` -> `5 passed`.

## 04e Closure Status
`04e` is marked PASS:
- implementation files:
  - `pocs/04e/src/app.py`
  - `pocs/04e/src/routes.py`
  - `pocs/04e/src/service.py`
- tests:
  - `pocs/04e/tests/test_api.py`
- API docs:
  - `pocs/04e/docs/CONTRACT.md`
  - `pocs/04e/docs/TEST_PLAN.md`
- sample output:
  - `pocs/04e/outputs/sample_api_responses.json`
- implemented behavior:
  - endpoint layer for submitting query/context and receiving structured RAG responses
  - pipeline integration using existing 04d harness/mock evidence/scenario timing
  - timing metrics returned in API response payloads
  - schema validation at request boundary and deterministic pipeline validation in service flow
  - basic logging and HTTP error handling (`400` known service validation errors, `422` request validation errors, `500` fallback)
- validation evidence:
  - command: `. D:\Workarea\StudyBook\env_setter.ps1; pytest -v .\pocs\04e\tests`
  - result: `5 passed`
- non-goals preserved:
  - no threshold tuning
  - no LLM calls
  - no customer answer generation
  - no modifications to 03f/03g artifacts
  - no movement into `integrated/servicecall-ai`

## 04d Closure Status
`04d` expansion pack is marked PASS:
- implementation updates:
  - `pocs/04d/src/pipeline_test_harness.py` (per-scenario execution timing)
  - `pocs/04d/src/mock_evidence_sets.py` (scenario expansion + lightweight performance batch generator)
  - `pocs/04d/src/schemas.py`
  - `pocs/04d/tests/test_harness.py`
  - `pocs/04d/tests/test_runner.py`
  - `pocs/04d/outputs/sample_pipeline_runs.json` (timing + expanded scenario results)
- expanded scenarios:
  - `failure-insufficient-evidence`
  - `failure-escalation-required`
  - `negative-bad-citation` (expected failure path)
  - lightweight batch generator for performance testing
- validation evidence:
  - command: `. D:\Workarea\StudyBook\env_setter.ps1; pytest -v .\pocs\04d\tests`
  - result: `6 passed`
- non-goals preserved:
  - no threshold tuning
  - no LLM calls
  - no customer answer generation
  - no move into `integrated/servicecall-ai`
  - no rebuild/modification of `03d`/`03e`/`03f`/`03g` artifacts

## 04b Closure Status
`04b_answer_contract_schemas` is marked PASS:
- implementation files:
  - `pocs/04b_answer_contract_schemas/src/__init__.py`
  - `pocs/04b_answer_contract_schemas/src/schemas.py`
  - `pocs/04b_answer_contract_schemas/tests/conftest.py`
  - `pocs/04b_answer_contract_schemas/tests/test_schemas.py`
- design files (unchanged authority set):
  - `pocs/04b_answer_contract_schemas/README.md`
  - `pocs/04b_answer_contract_schemas/docs/DESIGN.md`
  - `pocs/04b_answer_contract_schemas/docs/CONTRACT.md`
  - `pocs/04b_answer_contract_schemas/docs/TEST_PLAN.md`
- implemented behavior:
  - strict Pydantic enums/models for answer assembly contract
  - full top-level branch validation with strict `outcome_type` <-> `route_applied` mapping
  - citation cross-validation by `chunk_id` with selected-text-first and retrieved-text fallback
  - normalized-exact citation matching rules
  - evidence gating with `evidence_attempted`
  - claim/support-status validation, clarification requirements, escalation safety validation, and insufficient-evidence anti-answer guard
- validation evidence:
  - command: `. 'D:\Workarea\StudyBook\env_setter.ps1'; pytest -v .\pocs\04b_answer_contract_schemas\tests`
  - result: `31 passed`
- non-goals preserved:
  - no LLM calls
  - no customer-facing answer generation
  - no threshold tuning
  - no modifications to `03d`/`03e`/`03f`/`03g`/`03h`
  - no movement into `integrated/servicecall-ai`

## 04a Closure Status
`04a_answer_contract_design` is marked PASS:
- design docs complete:
  - `pocs/04a_answer_contract_design/README.md`
  - `pocs/04a_answer_contract_design/docs/DESIGN.md`
  - `pocs/04a_answer_contract_design/docs/CONTRACT.md`
  - `pocs/04a_answer_contract_design/docs/TEST_PLAN.md`
- design patch completed:
  - all outcome examples use full top-level `AnswerAssemblyOutcome` shape
  - `SelectedEvidenceItem` includes `selected_text`
  - citation spans must resolve against `selected_text` or original retrieved evidence `text` by `chunk_id`
  - document-derived `factual`, `instructional`, and `policy` claims require citations
  - conversational glue text does not require citations
  - escalation enums added for `severity` and `handoff_target`
  - `TEST_PLAN` updated for these validation rules
- non-goals preserved:
  - no Python code
  - no `src/`, `tests/`, or `outputs/`
  - no LLM calls
  - no customer-facing answer generation
  - no threshold tuning
  - no modifications to `03d`/`03e`/`03f`/`03g`/`03h`
  - no movement into `integrated/servicecall-ai`

## Closure Snapshot (03a-03e)
- `03a_load_documents` PASS
- loaded 16 synthetic markdown business documents
- wrote `pocs/03a_load_documents/outputs/loaded_documents.json`
- `03b_chunk_documents` PASS
- boundary-aware chunking
- wrote `pocs/03b_chunk_documents/outputs/chunked_documents.json`
- final chunk result: 23
- tests: 8 passed
- `03c_text_normalization` PASS
- wrote `pocs/03c_text_normalization/outputs/normalized_chunks.json`
- preserved original text and added `normalized_text` + `normalized_character_count`
- tests: 6 passed
- `03d_word_tfidf_index` PASS
- built word-level TF-IDF index
- wrote `pocs/03d_word_tfidf_index/outputs/tfidf_index.joblib`
- wrote `pocs/03d_word_tfidf_index/outputs/index_metadata.json`
- matrix shape: `23 x 2002`
- tests: 9 passed
- `03e_char_tfidf_typo_search` PASS
- built character-level typo-tolerant TF-IDF index
- wrote `pocs/03e_char_tfidf_typo_search/outputs/char_tfidf_index.joblib`
- wrote `pocs/03e_char_tfidf_typo_search/outputs/char_index_metadata.json`
- wrote `pocs/03e_char_tfidf_typo_search/outputs/sample_typo_search_results.json`
- matrix shape: `23 x 5779`
- tests: 11 passed

## Key Learnings Preserved
- `03d` word TF-IDF handles clean wording and exact business terms.
- `03e` character TF-IDF helps with misspellings and messy customer typing.
- `03e` returns candidate matches only; it does not decide final intent.
- Guided Customer Input is future direction: autocomplete, autocorrect-style help, service-intent buttons, and clarification choices.
- Guided input supports retrieval and does not replace backend retrieval.
- Design law to preserve: every POC should be standalone, configurable, reusable, and chainable.

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
- every meaningful POC should include: `README.md`, `docs/DESIGN.md`, `docs/CONTRACT.md`, `docs/TEST_PLAN.md`, `src/`, `tests/`, `outputs/`
- POC completion gate: code works, tests pass, sample output exists, and docs (`README`, `DESIGN`, `CONTRACT`, `TEST_PLAN`) are complete
- design-first rule: start with `README`, `DESIGN`, `CONTRACT`, and `TEST_PLAN` before implementation unless explicitly approved otherwise

## Next Recommended Task
`04d` expansion pack is complete.
Next discussion should deliberately choose the next scoped step before implementation.
Possible next directions:
- `03i` threshold review / tuning analysis (still no auto tuning)
- `04` answer assembly with citations
- `04a`/`04b`/`04d` retrospective and hardening pass before moving on

## 03h Closure Status
`03h_retrieval_evaluation` is marked PASS:
- design docs complete:
  - `pocs/03h_retrieval_evaluation/README.md`
  - `pocs/03h_retrieval_evaluation/docs/DESIGN.md`
  - `pocs/03h_retrieval_evaluation/docs/CONTRACT.md`
  - `pocs/03h_retrieval_evaluation/docs/TEST_PLAN.md`
- implementation complete:
  - fixture schema + fixture loader
  - upstream `03f`/`03g` loaders
  - case alignment helper (`normalized_query` with `query` fallback)
  - per-case evaluator
  - aggregate summary calculator
  - output writers
  - minimal runner
  - runner smoke test
- validation:
  - `. D:\Workarea\StudyBook\env_setter.ps1; pytest -v .\pocs\03h_retrieval_evaluation\tests` -> PASS (`49 passed in 0.66s`)
  - `python .\pocs\03h_retrieval_evaluation\src\run_retrieval_evaluation.py` -> PASS
  - processed `3` cases: `3 passed / 0 failed / 0 warning`
- outputs:
  - `pocs/03h_retrieval_evaluation/outputs/evaluation_report.json`
  - `pocs/03h_retrieval_evaluation/outputs/evaluation_summary.md`

## 03g Closure Status
`03g_retrieval_decision` is marked PASS:
- design docs complete:
  - `pocs/03g_retrieval_decision/README.md`
  - `pocs/03g_retrieval_decision/docs/DESIGN.md`
  - `pocs/03g_retrieval_decision/docs/CONTRACT.md`
  - `pocs/03g_retrieval_decision/docs/TEST_PLAN.md`
- implementation complete:
  - `pocs/03g_retrieval_decision/src/schemas.py`
  - `pocs/03g_retrieval_decision/src/retrieval_decision.py`
  - `pocs/03g_retrieval_decision/src/run_retrieval_decision.py`
  - `pocs/03g_retrieval_decision/config/decision_config.json`
  - `pocs/03g_retrieval_decision/tests/test_retrieval_decision.py`
  - `pocs/03g_retrieval_decision/outputs/sample_retrieval_decisions.json`
- validation:
  - `pytest -v .\pocs\03g_retrieval_decision\tests` -> PASS (`14 passed`)
  - `python .\pocs\03g_retrieval_decision\src\run_retrieval_decision.py` -> PASS (`6` queries processed)

## 2026-05-04 Update - 04c/04d Design Artifact Persistence
- Persisted design artifacts for \'04c_schema_validation_integration\' and \'04d_full_rag_pipeline_testing\'.
- Created/updated README + DESIGN/CONTRACT/TEST_PLAN for both POCs from thread-approved content.
- Implementation for 04d harness remains in progress and should continue in next execution slice.


## 2026-05-04 Update - 04d Expansion Pack PASS
-  4d remains PASS and is expanded with timing + scenario-depth coverage.
- Implemented: per-scenario execution timing in pocs/04d/src/pipeline_test_harness.py.
- Implemented scenario expansion in pocs/04d/src/mock_evidence_sets.py:
  - ailure-insufficient-evidence`n  - ailure-escalation-required`n  - 
egative-bad-citation (expected failure path)
  - uild_performance_batch(...) lightweight batch generator
- Updated pocs/04d/src/schemas.py and tests:
  - pocs/04d/tests/test_harness.py`n  - pocs/04d/tests/test_runner.py`n- Output refreshed: pocs/04d/outputs/sample_pipeline_runs.json with per-scenario xecution_time_ms.
- Validation: . D:\Workarea\StudyBook\env_setter.ps1; pytest -q .\pocs\04d\tests; python .\pocs\04d\src\run_pipeline_tests.py -> PASS (6 passed).


## 2026-05-04 Update - 04f Kickoff Initialized
- Milestone 4 next step  4f is now initialized as a design-first POC for deployment-ready service integration.
- Created POC structure: pocs/04f/src, pocs/04f/tests, pocs/04f/docs, pocs/04f/outputs.
- Persisted kickoff prompt at pocs/04f/outputs/POC_04f_kickoff_prompt.md.
- Seeded initial docs for design-first progression:
  - pocs/04f/README.md
  - pocs/04f/docs/DESIGN.md
  - pocs/04f/docs/CONTRACT.md
  - pocs/04f/docs/TEST_PLAN.md
- Implementation and closure validation for 04f remain pending.

## 2026-05-04 Update - 04f Thread Initialization (Deterministic Docker-First Teaching)
- Initialized a dedicated 04f thread teaching artifact at `pocs/04f/outputs/POC_04f_THREAD_INIT.md`.
- Captured step-by-step deterministic Docker-first workflow:
  - build image
  - run container
  - run in-container pytest
  - run `/health` and `/ping` smoke checks
  - persist logs and outputs
- Explicitly documented teaching scope across `src/`, `tests/`, `docs/`, and `outputs/`.
- Marked `pocs/04f/outputs/POC_04f_SUMMARY.md` as the snapshot teaching reference.
- Emphasized reproducibility and deterministic behavior preservation for repeatable onboarding.

## 2026-05-04 Update - 04f Teaching Memory (Docker-First Deterministic Reference)
Purpose: persistent reference for future teaching, extension, and debugging of POC 04f.

Persisted reference points:
- Fully implemented Docker-first automation script: `pocs/04f/integrate_04f_docker.ps1`
- Deterministic FastAPI endpoints: `GET /health`, `GET /ping`
- In-container pytest integration currently includes placeholder test coverage
- Docker runtime identifiers:
  - image: `poc_04f_service`
  - container: `poc_04f_service_run`
- Smoke tests verified and reproducible evidence persisted under `pocs/04f/outputs/`
- Teaching folder structure anchor:
  - `pocs/04f/src/`
  - `pocs/04f/tests/`
  - `pocs/04f/docs/`
  - `pocs/04f/outputs/`
- Snapshot documentation source of truth:
  - `pocs/04f/outputs/POC_04f_SUMMARY.md`
- Teaching/extension guidance source:
  - `pocs/04f/outputs/POC_04f_THREAD_INIT.md`

## 2026-05-04 Update - 04f Workflow Diagram Artifact Added
- Added teaching-first visual workflow artifact: `pocs/04f/outputs/POC_04f_WORKFLOW_DIAGRAM.md`.
- Diagram captures verified deterministic Docker-first flow:
  - `src/app.py` -> `integrate_04f_docker.ps1` -> Docker build (`poc_04f_service`) -> container run (`poc_04f_service_run`) -> in-container pytest + smoke checks -> output/log artifacts -> summary snapshot.
- Explicit deterministic endpoint labels included:
  - `/health` -> `{"ok": true}`
  - `/ping` -> `{"ok": true}`
- References included for completeness:
  - `POC_04f_SUMMARY.md`
  - `POC_04f_THREAD_INIT.md`
  - `POC_04f_kickoff_prompt.md`

## 2026-05-05 Update - 04f Phase 1 Multi-Sentence Query Handling
- Implemented Phase 1 local logic update for complex multi-sentence customer queries in `pocs/04f`.
- `parse_intent` now:
  - splits multi-sentence input,
  - drops greeting/small-talk segments,
  - scores remaining segments for service-domain keywords,
  - returns focused `intent_text` for retrieval.
- Added Pydantic model `IntentParseResult` for structured intent output.
- Retrieval path now explicitly uses stopwords config in app initialization:
  - `pocs/04f/src/app.py` loads `config/stopwords.json`.
- Retriever reliability improved for local environments:
  - Levenshtein fallback to `SequenceMatcher` when `python-Levenshtein` is unavailable.
  - Porter stemmer fallback when `nltk` is unavailable.
- Updated standalone interactive CLI `pocs/04f/interactive_grok_test.py`:
  - uses `parse_intent` -> `SimpleRetriever` -> `generate_response`,
  - logs entries to `pocs/04f/outputs/ask_logs.json`,
  - prints extracted `intent_text` and discarded segments for visibility.
- Added tests:
  - `pocs/04f/tests/test_phase1_multisentence.py`
- Validation:
  - `. D:\Workarea\StudyBook\env_setter.ps1; pytest -q pocs/04f/tests/test_phase1_multisentence.py` -> PASS (`2 passed`).
  - Interactive CLI multi-sentence run verified with irrelevant context and correct retrieval behavior.
- Scope preserved:
  - no website implementation,
  - no Docker changes,
  - standalone local logic only.

## 2026-05-05 Update - 04g Local LLM Container POC Documentation
- 04g started as a standalone local LLM container POC (separate from 04f RAG/fuzzy/intent lane).
- Documented successful Docker build/run path for Mistral 7B-class local container service.
- Documented model mount path: `C:\LLM_models\Mistral7B` -> `/app/llm_model`.
- Documented successful endpoint validation: `/health` and `/infer` responded.
- Documented scripted smoke validation: `pocs/04g/llm/smoke_test_llm.py` PASS.
- Captured current limitations: latency and occasional over-generation.
- Next recommended step: tighten generation stop behavior, then mount/connect KB for retrieval in a later scoped step.
