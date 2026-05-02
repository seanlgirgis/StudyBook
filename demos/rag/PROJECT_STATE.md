# PROJECT_STATE.md

## Current Milestone
Milestone 2 — Synthetic business document corpus (`pocs/02_fake_business_docs`)

## Current Focus
Deliver and validate synthetic home-services policy documents for retrieval, citation, fallback, escalation, and intake behavior testing.

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

## What Is Not Yet Implemented
- retrieval logic
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
Build a basic retrieval POC that answers from `pocs/02_fake_business_docs` with source citations and safe fallback behavior.
