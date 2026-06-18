# CODEX_CONSTITUTION.md

## Startup

- Read `agents/codex/AGENTS.md` first at session start.
- Follow the required file read order in `agents/codex/AGENTS.md`.

## Implementation Rules

- Prefer tested scripts over improvised risky file operations.
- Report all files created and changed.
- Run tests after code changes.
- Do not delete, move, rename, or source-sync files unless explicitly authorized by an approved workflow.
- Do not upload to OneDrive without an explicit publish workflow.
- Never commit secrets, tokens, or credentials.
- Do not casually copy or sync the live operational database to cloud storage.
- Do not commit real operational databases, database backups, real exports, reports, logs, pod manifests, or text cache artifacts.
- Use approved backup scripts (once implemented) rather than ad hoc DB copy approaches.
- Report any DB paths touched by implementation or validation work.
- Do not invent or imply unsupported multi-machine concurrent write workflows.
- Treat filename/metadata sensitivity and content sensitivity as separate stages.
- Do not implement content extraction/classification flows without explicit approval and storage/privacy/backup policy controls.

## Data Boundary

- Real operational data belongs under `D:\AI_Lab\LifeVault`.
- Keep personal data outside Git-tracked repository content.
- Follow operational procedures in `docs/LIFEVAULT_OPERATIONS_RUNBOOK.md`.
