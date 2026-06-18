# GROK_RUNBOOK.md

Operational runbook for Grok Build sessions in LifeVault.

## Two Roots (critical)

| Role | Path |
|------|------|
| **Dev repo** (code, docs, tests) | `D:\Workarea\StudyBook\Proj_development\LifeVault` |
| **Operational data** (DB, pods, vault) | `D:\AI_Lab\LifeVault` |

Primary DB: `D:\AI_Lab\LifeVault\db\lifevault.sqlite`

Never commit: real personal data, secrets, live DBs, backups, exports, reports, logs, pod manifests, text cache.

## Launch Grok Build

```powershell
pwsh -ExecutionPolicy Bypass -File "C:\scripts\start_grok_lifevault.ps1"
```

| Copy | Path |
|------|------|
| Runtime (daily use) | `C:\scripts\start_grok_lifevault.ps1` |
| Repo archive | `D:\Workarea\StudyBook\Proj_development\LifeVault\start_grok_lifevault.ps1` |

Keep both copies identical. Use `-NoNewWindow` to run in the current shell.

## Environment

From project root, before Python or tests:

```powershell
..\..\env_setter.ps1
```

Equivalent: `D:\Workarea\StudyBook\env_setter.ps1`

Common entrypoints: `python -m lifevault.<module>`

## Proven Vertical (v0)

`SUC_006` folder lifecycle: `UC_001` → `UC_009` (quarantine-only cleanup; no permanent delete).

Wrappers: `scripts/run_uc001_proposal.ps1` through `scripts/run_uc009_cleanup_quarantine.ps1`

## Streamlit Help Console (read-only)

- App: `app/streamlit/lifevault_help_console.py`
- Run: `scripts/run_streamlit_help_console.ps1`
- Docker: `scripts/start_streamlit_help_console_docker.ps1`

v0 is guidance-only — no shell execution or destructive actions from UI.

## Notes (partial ahead of tracker)

- `src/lifevault/notes.py`, `notes_cli.py`
- `scripts/run_notes_*.ps1`, `run_note_folder_*.ps1`

Tracker may still list `SUC_005` as `in_design` — reconcile docs before claiming done.

## Parent StudyBook

Project root is **Grok-only** (`GROK_*`, `Grok_PROJECT_PROFILE.md`, launcher). Codex files: `agents/codex/`. Parent `env_setter.ps1` applies for Python.

## Git

Sean manages Git. Repo had no `.git` at guardian onboarding (2026-06-17). Batch sync: `C:\scripts\gitqall.ps1` when repos are wired in.