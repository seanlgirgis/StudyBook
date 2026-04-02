# Context Index

Purpose: compact durable memory map for fast session bootstrap.

## Project North Star

- Build `D:\StudyBook` as the canonical, reproducible DE/AI runtime repo.
- Execute migration as controlled shift/lift from `D:\Workspace`.
- Keep autonomy high with explicit safety guardrails and durable run artifacts.

## Canonical Control Files

- `AGENTS.md`
- `CONTROL_PROTOCOL.md`
- `agents/shared/pending_task.md`
- `agents/shared/agent_status.md`
- `agents/shared/task_register.md`
- `agents/shared/open_loops.md`
- `agents/shared/decision_log.md`
- `agents/shared/parking_lot.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `docs/adr/ADR-INDEX.md`

## Current Working Agreements

- Use `Allowed Scope: bounded` by default for velocity.
- Use `Reasoning Depth: deep` for migration and architecture decisions.
- Stop only for high-risk ambiguity, not for routine implementation details.
- Canonical runtime target is `D:\StudyBook` (deprecated path deleted).
- Standing owner directive (2026-04-02): treat encrypted StudyBook secrets as system of record for sensitive values; use seed-backed secret updates by default and avoid storing sensitive values in tracked files/chat.

## Portable Environment Files

- `env_setter.ps1`
- `scripts/env/env_core.ps1`
- `scripts/env/bootstrap_all.ps1`
- `scripts/env/register_secret_seed.ps1`
- `scripts/env/remove_secret_seed.ps1`
- `scripts/env/package_aws_credentials.ps1`
- `scripts/env/restore_aws_credentials.ps1`
- `config/env/base.psd1`
- `config/machines/asuspc.psd1`
- `config/machines/dell-laptop.psd1`
- `docs/PORTABLE_ENV.md`
- `config/secrets/shared.secrets.enc.json`
- `config/secrets/asuspc.secrets.enc.json`
- `config/secrets/dell-laptop.secrets.enc.json`
- `config/secrets/workspace-import.sources.md`
- `docs/operations/secrets_workflow.md`
- `docs/operations/aws_credentials_workflow.md`

## Infra Reproducibility Files

- `_infra/docker/docker-compose.yml`
- `_infra/docker/core.yml`
- `_infra/docker/streaming.yml`
- `_infra/docker/pipeline.yml`
- `_infra/docker/observability.yml`
- `_infra/env/.env.example`
- `_infra/scripts/infra_up.ps1`
- `_infra/scripts/infra_down.ps1`
- `_infra/scripts/infra_seed.ps1`
- `_infra/scripts/infra_health.ps1`
- `_infra/seeds/seed_core.py`
- `_infra/seeds/seed_tech_telemetry.py`
- `_infra/README.md`

## ZeroToHero Program Files

- `docs/programs/zero_to_hero/EXECUTION_SYSTEM.md`
- `docs/programs/zero_to_hero/MIGRATION_BOARD.md`
- `docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md`
- `docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md`

## Coding Challenges Migration Memory

- M-002/M-002b completed on 2026-04-02 via:
  - `scripts/migration/run_m002_coding_assets.ps1 -Execute -DeleteSource`
- Canonical coding root:
  - `D:\StudyBook\coding_challenges`
- Migration evidence run:
  - `D:\StudyBook\coding_challenges\_migration_meta\run_20260402_113935`
- Emergency rollback snapshot:
  - `C:\Users\shareuser\migration_backups\m002_backup_20260402_113935`
- Authoritative runbook:
  - `docs/programs/zero_to_hero/CODING_ASSETS_MIGRATION_SOLUTION.md`
- First planning outputs for study execution:
  - `coding_challenges/STUDY_MANUAL_V1.md`
  - `coding_challenges/ROADMAP_DRAFT_V1.md`
## Last Updated

- 2026-04-02


