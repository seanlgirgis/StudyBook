# LIFEVAULT_BOOTSTRAP.md

**Location:** `agents/codex/` — project root is Grok guardian territory (`GROK_*`, `Grok_PROJECT_PROFILE.md`). Path references below are from project root unless noted.

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
  - `docs/architecture/LIFEVAULT_NOTE_MODEL.md`
  - `docs/architecture/LIFEVAULT_NOTE_FILENAME_POLICY.md`
  - `docs/architecture/LIFEVAULT_POLICY_MODEL.md`
  - `docs/architecture/LIFEVAULT_TASK_PROJECT_MODEL.md`
  - `docs/contracts/NOTE_AND_NOTE_FOLDER_CONTRACT.md`
  - `docs/contracts/NOTE_ASSET_STORE_CONTRACT.md`
  - `docs/security/LIFEVAULT_ENCRYPTION_V0_DESIGN.md`
  - `docs/security/LIFEVAULT_SENSITIVE_NOTE_V0_CONTRACT.md`
  - `docs/security/LIFEVAULT_UNLOCK_SESSION_POLICY.md`
  - `docs/security/LIFEVAULT_UNLOCK_SESSION_STATE_CONTRACT.md`
  - `docs/security/SENSITIVE_NOTE_STORAGE_LAYOUT_V0.md`
  - `docs/security/SENSITIVE_NOTE_MINIMAL_IMPLEMENTATION_PLAN_V0.md`
  - `docs/contracts/SENSITIVE_NOTE_COMMAND_CONTRACT.md`
  - `docs/super_use_cases/SUC_010_ACCEPTANCE_CHECKLIST.md`
  - `docs/super_use_cases/SUC_015_STREAMLIT_HELP_OPERATOR_CONSOLE.md`
  - `docs/architecture/LIFEVAULT_STREAMLIT_DOCKER_V0.md`
  - `docs/contracts/STREAMLIT_HELP_CONSOLE_V0_CONTRACT.md`
  - `app/streamlit/lifevault_help_console.py`
  - `app/streamlit/README.md`
  - `tests/test_streamlit_help_console_static.py`
  - `docker/streamlit_dashboard/Dockerfile`
  - `docker/streamlit_dashboard/docker-compose.yml`
  - `scripts/run_streamlit_help_console.ps1`
  - `scripts/start_streamlit_help_console_docker.ps1`
  - `scripts/stop_streamlit_help_console_docker.ps1`
  - `scripts/status_streamlit_help_console_docker.ps1`
  - `scripts/install_streamlit_help_console_startup_task.ps1`
  - `scripts/uninstall_streamlit_help_console_startup_task.ps1`
  - `docs/contracts/NOTE_TEMPLATE_CONTRACT.md`
  - `docs/contracts/NOTE_AND_NOTE_FOLDER_CONTRACT.md`
  - `docs/contracts/NOTE_TEMPLATE_CONTRACT.md`
  - `docs/contracts/NOTE_ASSET_STORE_CONTRACT.md`
  - `docs/tasks/LIFEVAULT_PROJECT_TASK_SEED.md`
  - `docs/super_use_cases/SUPER_USE_CASE_INDEX.md`
  - `docs/super_use_cases/SUC_005_NOTES_AND_KNOWLEDGE_MEMORY.md`
  - `docs/super_use_cases/SUC_005_ACCEPTANCE_CHECKLIST.md`
  - `src/lifevault/notes.py`
  - `src/lifevault/notes_cli.py`
  - `scripts/run_note_folder_create.ps1`
  - `scripts/run_note_folder_list.ps1`
  - `docs/super_use_cases/SUC_021_TASKS_PROJECTS_MAINTENANCE_QUEUES.md`
  - `docs/super_use_cases/SUPER_USE_CASE_001_LOCAL_FOLDER_LIFECYCLE.md`
  - `docs/super_use_cases/SUC_001_ACCEPTANCE_TEST_PLAN.md`
  - `docs/super_use_cases/SUC_001_OPERATOR_CHECKLIST.md`
