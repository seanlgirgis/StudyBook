# LIFEVAULT_DATA_BOUNDARY.md

## Repository vs Operational Data

- Repository (`D:\Workarea\StudyBook\Proj_development\LifeVault`): code, scripts, docs, templates, tests.
- Operational root (`D:\AI_Lab\LifeVault`): onboarding pods, proposals, databases, logs, reports, text cache, exports.

## Rules

- No real personal data in Git.
- No token/secret material in Git.
- Config templates may be tracked; local secrets must stay local.