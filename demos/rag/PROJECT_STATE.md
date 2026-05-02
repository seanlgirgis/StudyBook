# PROJECT_STATE.md

## Current Milestone
Milestone 3 (Staged) — Retrieval learning ladder scaffolding (`pocs/03a_*` to `pocs/03h_*`)

## Current Focus
Stage a baby-step retrieval learning ladder with folder structure and starter documentation only (no retrieval logic implementation yet).

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

## What Is Not Yet Implemented
- retrieval logic
- TF-IDF indexing and search implementation
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
After approval, begin Milestone 3 implementation in order, starting with `pocs/03a_load_documents` only.
