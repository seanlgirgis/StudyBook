# STUDYBOOK_FAST_GUIDE.md

Purpose: quick orientation for any agent or collaborator entering `D:\Workarea\StudyBook`.

## What This Project Is

- Canonical target repo for data engineering + AI learning/runtime assets.
- It is replacing and consolidating legacy material from `D:\Workspace`.
- It is designed to be reproducible, secure (encrypted secrets), and agent-friendly.

## What We Are Planning To Do

- Continue controlled migration waves from `D:\Workspace` into structured StudyBook tracks.
- Complete remaining security/migration loops (secret hygiene, residual legacy cleanup).
- Keep converting migrated content into study-ready outputs (manuals, roadmaps, nuggets).
- Maintain reproducible infra startup and connection proofs for tools/cloud services.

Primary plan and tracking live in:
- `D:\Workarea\StudyBook\docs\programs\zero_to_hero\MIGRATION_BOARD.md`
- `D:\Workarea\StudyBook\docs\programs\zero_to_hero\EXECUTION_SYSTEM.md`
- `D:\Workarea\StudyBook\agents\shared\task_register.md`
- `D:\Workarea\StudyBook\agents\shared\open_loops.md`

## What Has Been Done (High Level)

- Infra baseline is in place under `_infra` with compose splits, startup scripts, health checks, and seeding.
- Major migration waves completed on 2026-04-02:
- `M-002/M-002b` coding assets into `coding_challenges` with manifests and source cleanup.
- `M-011/M-013/M-008/M-015` technologies notebooks/prompts + interview + ML_AI moved with evidence artifacts.
- `M-012` databases notebooks/prompts migrated into `tracks/08_databases` and `_prompts/legacy/databases`.
- Cloud proofing and secret model established (AWS, Azure, Databricks, Snowflake, etc. tracked in board/registry).
- Snowflake micro-nuggets lane created in `tracks/08_databases/micro_nuggets/snowflake`.

## System Of Record And Agent Rules

Read this order before work:
1. `D:\Workarea\StudyBook\CONTROL_PROTOCOL.md`
2. `D:\Workarea\StudyBook\agents\shared\context_index.md`
3. `D:\Workarea\StudyBook\agents\shared\open_loops.md`
4. `D:\Workarea\StudyBook\agents\shared\approval_matrix.md`
5. `D:\Workarea\StudyBook\agents\shared\command_allowlist.md`
6. `D:\Workarea\StudyBook\docs\adr\ADR-INDEX.md`
7. `D:\Workarea\StudyBook\agents\shared\pending_task.md` (if present)
8. `D:\Workarea\StudyBook\agents\shared\agent_status.md` (if present)
9. `D:\Workarea\StudyBook\agents\shared\decision_log.md` (if present)

Core behavior:
- Repo files are truth, not chat memory.
- One scoped task per run.
- Stay in scope; park side findings in `agents/shared/parking_lot.md`.
- Do not commit/push unless explicitly asked.

## Secrets / Encryption-Decryption Model

- Encrypted StudyBook secrets are the sensitive-data system of record.
- Seed-backed local decryption is used via DPAPI-protected local seed file.
- Passphrase is intended to be entered once per machine during seed registration.

Key docs/scripts:
- `D:\Workarea\StudyBook\docs\operations\secrets_workflow.md`
- `D:\Workarea\StudyBook\scripts\env\register_secret_seed.ps1`
- `D:\Workarea\StudyBook\scripts\env\set_secret.ps1`
- `D:\Workarea\StudyBook\scripts\env\bootstrap_all.ps1`
- `D:\Workarea\StudyBook\config\secrets\*.enc.json`

## Significant Folders

- `D:\Workarea\StudyBook\_infra` infrastructure compose/env/scripts/seeds.
- `D:\Workarea\StudyBook\tracks` canonical learning tracks by topic.
- `D:\Workarea\StudyBook\coding_challenges` coding assets migrated from workspace.
- `D:\Workarea\StudyBook\_prompts` legacy and canonical prompt libraries.
- `D:\Workarea\StudyBook\interview` interview-focused assets.
- `D:\Workarea\StudyBook\poc\connection_proofs` proof scripts for cloud/services/docker.
- `D:\Workarea\StudyBook\agents` control/memory/handoff files for agent continuity.
- `D:\Workarea\StudyBook\docs\programs\zero_to_hero` migration strategy and board.
- sibling repos: `D:\Workarea\jobsearch` and `D:\Workarea\seanlgirgis.github.io`.

## Significant Files To Know First

- `D:\Workarea\StudyBook\AGENTS.md`
- `D:\Workarea\StudyBook\CONTROL_PROTOCOL.md`
- `D:\Workarea\StudyBook\agents\shared\context_index.md`
- `D:\Workarea\StudyBook\agents\shared\task_register.md`
- `D:\Workarea\StudyBook\agents\shared\open_loops.md`
- `D:\Workarea\StudyBook\docs\programs\zero_to_hero\MIGRATION_BOARD.md`
- `D:\Workarea\StudyBook\docs\programs\zero_to_hero\CLOUD_ACCOUNT_REGISTRY.md`
- `D:\Workarea\StudyBook\docs\operations\secrets_workflow.md`

## Helpful Notes

- Treat `D:\Workarea\StudyBook` as canonical runtime; avoid reintroducing `D:\Workspace` path dependencies.
- Keep runtime artifacts (volumes, generated large files) out of git-tracked paths.
- Always validate behavior changes with real commands and capture factual outcomes.
- Use migration scripts and metadata folders for reproducibility/auditability rather than ad-hoc moves.

## Quick Start Commands

```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1
Get-Content .\agents\shared\context_index.md -TotalCount 200
Get-Content .\docs\programs\zero_to_hero\MIGRATION_BOARD.md -TotalCount 200
```

Last updated: 2026-04-26

