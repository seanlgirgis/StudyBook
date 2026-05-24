# LIFEVAULT_BOOTSTRAP.md

## Project Identity

- Active project name: `LifeVault`
- Deprecated name: `OneDriveClean`
- Mission: build a personal knowledge memory and file-governance system.

## Environment

- Project root: `D:\Workarea\StudyBook\Proj_development\LifeVault`
- Operational root: `D:\AI_Lab\LifeVault`
- Main operational DB: `D:\AI_Lab\LifeVault\db\lifevault.sqlite`
- Local DB backups: `D:\AI_Lab\LifeVault\db_backups`
- Export root: `D:\AI_Lab\LifeVault\exports`
- Initialize Python/test environment from project root with:
  - `..\..\env_setter.ps1`

## Core Laws

- AI suggests; human approves.
- No delete by default.
- No move by default.
- No rename by default.
- Copy only during early phases.
- No rclone sync.
- No file enters the clean vault outside LifeVault.
- The database is the searchable map.
- The clean vault is the final file source of truth.
- Onboarding pods are controlled working copies.
- Real personal data stays outside Git.
- Secrets and rclone tokens must never be committed.
- Support search without hydrating all OneDrive files locally.
- Writer model is v0 one-writer/many-reader; avoid simultaneous multi-machine writes to the live DB.

## Operations Reference

- Day-to-day operational procedures are defined in `docs/LIFEVAULT_OPERATIONS_RUNBOOK.md`.
- Super-use-case map and validated lifecycle are defined in:
  - `docs/strategy/LIFEVAULT_1000_FOOT_CAPABILITY_MAP.md`
  - `docs/architecture/LIFEVAULT_VAULT_ITEM_MODEL.md`
  - `docs/architecture/LIFEVAULT_POLICY_MODEL.md`
  - `docs/architecture/LIFEVAULT_TASK_PROJECT_MODEL.md`
  - `docs/tasks/LIFEVAULT_PROJECT_TASK_SEED.md`
  - `docs/super_use_cases/SUPER_USE_CASE_INDEX.md`
  - `docs/super_use_cases/SUC_021_TASKS_PROJECTS_MAINTENANCE_QUEUES.md`
  - `docs/super_use_cases/SUPER_USE_CASE_001_LOCAL_FOLDER_LIFECYCLE.md`
  - `docs/super_use_cases/SUC_001_ACCEPTANCE_TEST_PLAN.md`
  - `docs/super_use_cases/SUC_001_OPERATOR_CHECKLIST.md`
