# LIFEVAULT_DATA_BOUNDARY.md

## Repository vs Operational Data

- Repository (`D:\Workarea\StudyBook\Proj_development\LifeVault`): code, scripts, docs, templates, tests.
- Operational root (`D:\AI_Lab\LifeVault`): onboarding pods, proposals, databases, logs, reports, text cache, exports.
- Primary DB path: `D:\AI_Lab\LifeVault\db\lifevault.sqlite`
- Local backup path: `D:\AI_Lab\LifeVault\db_backups`
- Future private backup target: `onedrive_clean:LifeVault/99_System_Exports/LifeVault_Admin/`

## Rules

- No real personal data in Git.
- No token/secret material in Git.
- Config templates may be tracked; local secrets must stay local.
- Do not commit real DB files, real backups, real exports, reports, logs, pod manifests, or text cache artifacts.
- UC_003 pod creation boundaries and output layout are specified in `docs/use_cases/UC_003_CREATE_ONBOARDING_POD_WORKFLOW_SPEC.md`.
