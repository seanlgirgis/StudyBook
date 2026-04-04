# JobSearch System Assessment And Launchpad Decision

Date: 2026-04-03  
Scope reviewed: `C:\jobsearch`  
Execution env noted: venv at `C:\py_venv\JobSearch`, activation via `C:\jobsearch\env_setter.ps1`

## Executive Summary

Decision: **do not fully lift `C:\jobsearch` into `D:\StudyBook` right now**.

Recommended model: **single-launchpad federation**.
- Keep `C:\jobsearch` as its own operational repo (data + pipeline runtime).
- Use `D:\StudyBook` as the command center with documented entrypoints, operating runbooks, and cross-links.
- Add a lightweight StudyBook launcher wrapper (next step) so daily use still feels like one system.

Why this is best:
- JobSearch is a live operational pipeline with sensitive personal data and high-write local state.
- StudyBook is a broader learning/platform repo with different change cadence and governance goals.
- Full merge now increases coupling/risk without giving meaningful workflow benefits over a federated launchpad.

## What I Understand About `C:\jobsearch`

## Primary Purpose

Personal AI-assisted job application engine:
- duplicate detection (semantic),
- fit scoring,
- decision gate,
- resume tailoring + render,
- company research,
- cover letter generation + render,
- application status tracking.

## Runtime Model

- Flat-file-first architecture (no DB dependency).
- Vector search via local FAISS index.
- LLM calls via xAI Grok endpoint (OpenAI SDK wrapper).
- Per-job artifact folders under `data/jobs/NNNNN_uuid8/...`.
- Pipeline orchestration through scripts `00` to `12` plus auto/force runners.

## Key Paths

- Entry and env:
  - `C:\jobsearch\env_setter.ps1`
  - `C:\py_venv\JobSearch`
- Core scripts:
  - `C:\jobsearch\scripts\00_check_applied_before.py`
  - `...01_score_job.py` through `...09_update_application_status.py`
  - `...10_auto_pipeline.py`, `...10b_force_pipeline.py`
  - `...11_search_jobs.py`, `...12_update_job.py`
- AI client:
  - `C:\jobsearch\src\ai\grok_client.py`
- Data:
  - `C:\jobsearch\data\jobs` (50 job folders observed)
  - `C:\jobsearch\data\job_index` (FAISS + metadata)
  - `C:\jobsearch\data\master` (career source exports)
  - `C:\jobsearch\data\source_of_truth.json`

## Operational Docs Found

- `C:\jobsearch\docs\project_summary_for_claude.md`
- `C:\jobsearch\docs\pipeline-runner.md`
- `C:\jobsearch\user_guide\v0\...`

## Current State Signals (Observed)

- Project is substantial (`~837` files in repo tree).
- Data footprint is moderate (`~9.66 MB` under `data`).
- Pipeline docs are strong and actionable.
- Mixed script and data lifecycle in one repo (expected for this type of personal ops system).
- Git access from sandbox shows ownership/safe-directory friction (important for agent automation contexts).

## Keep vs Lift Analysis

## Option A: Full Lift Into StudyBook

Pros:
- One repo to open.
- Unified governance and memory.

Cons:
- Sensitive job-search artifacts, generated resumes/cover letters, and operational state become tightly coupled to learning repo.
- Higher risk of accidental commit leakage (personal outputs, metadata, API-adjacent artifacts).
- Different cadence conflict: job-search pipeline changes frequently and tactically; StudyBook changes strategically.
- Merge/migration complexity for scripts expecting fixed paths like `C:\jobsearch`.

Verdict: **Not recommended now**.

## Option B: Leave As-Is Forever

Pros:
- Zero migration risk.
- Existing automation remains stable.

Cons:
- Split brain for operations memory unless cross-linked.
- “One launchpad” goal not met ergonomically.

Verdict: workable but suboptimal UX.

## Option C (Recommended): Federated Single Launchpad

Pattern:
- Keep `C:\jobsearch` operationally independent.
- Add StudyBook-side control docs and launcher wrappers for seamless use.
- Standardize cross-repo operating contract.

Benefits:
- One practical launchpad experience.
- Minimal operational risk.
- Preserves clean boundaries and sensitive-state containment.

Verdict: **Recommended now**.

## Manager Decision

Decision ID (local): **JS-DEC-20260403-01**  
Decision: **Federate, do not fully merge.**

## Phase Plan

## Phase 1 (Now): Adopt Federated Launchpad

1. Add StudyBook runbook for JobSearch operations.
2. Add StudyBook helper scripts:
   - `open_jobsearch.ps1` (cd + env_setter bootstrap)
   - `run_jobsearch_pipeline.ps1` (safe wrapper around pipeline steps)
3. Add cross-links in StudyBook operations index.

## Phase 2 (Later): Selective Lift (Optional)

Move only low-risk assets into StudyBook if desired:
- architecture docs,
- teachables/templates,
- non-sensitive prompt packs.

Do not lift by default:
- `data/jobs/*` generated application artifacts,
- live index files and mutable operational logs,
- local `.env`/secret-bearing files.

## Phase 3 (If Needed): Full Consolidation Gate

Only consider full merge after:
- strict secrets policy enforcement,
- reproducible environment parity proven,
- path-abstraction complete (no hard-coded `C:\jobsearch` assumptions),
- data retention/privacy policy documented.

## Risks To Track

- Personal/sensitive content in generated artifacts.
- API key hygiene (`.env` discipline must stay strict).
- Auto-pipeline bypassing human gate (`10_auto_pipeline.py`) can produce noisy application quality if overused.
- Potential script drift due to duplicated/legacy folders (`scripts/keep/...`).

## Immediate Next Actions (When You Return)

1. Implement StudyBook launcher wrappers for JobSearch federation.
2. Create a `JOBSEARCH_OPERATIONS.md` runbook in StudyBook with your exact daily flow.
3. Add a “quality-before-apply” checklist that always includes `quality_check.py --strict`.
4. Optional cleanup plan in `C:\jobsearch`: archive legacy duplicate scripts and tighten `.gitignore` for generated job artifacts.

---

Bottom line: your JobSearch system is real and valuable as an operational engine.  
Best strategic move is to run it through StudyBook as a **single launchpad**, while keeping the engine itself in `C:\jobsearch` for safety, speed, and separation of concerns.
