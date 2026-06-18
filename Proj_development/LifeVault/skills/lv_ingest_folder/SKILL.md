# LV_ingest_folder

## Startup Reads

Before operating:
- Read `agents/codex/AGENTS.md`
- Read `agents/codex/LIFEVAULT_BOOTSTRAP.md`
- Read `agents/codex/CODEX_CONSTITUTION.md`
- Read `docs/use_cases/UC_001_ingest_folder_proposal.md`
- Read `docs/use_cases/UC_003_create_onboarding_pod.md`
- Read `docs/validation/UC_001_REAL_APOD_ACCEPTANCE.md` when relevant

## v0 Workflow

1. Run UC_001 first.
2. Summarize proposal:
- proposal path
- file count
- highest sensitivity
- duplicate candidate count
- recommended next action
- suggested metadata
3. Require explicit approval before UC_003.
4. Run UC_003 only if explicitly approved.
5. Stop after pod creation and summary.

## v0 Boundary

- UC_001 + UC_003 only.
- No DB writes.
- No OneDrive/rclone.
- No publish.
- No source cleanup/move/delete/rename/sync.