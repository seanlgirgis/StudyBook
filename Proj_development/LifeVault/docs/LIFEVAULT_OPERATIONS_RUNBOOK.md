# LIFEVAULT_OPERATIONS_RUNBOOK.md

## Purpose

Define safe day-to-day LifeVault operations for Sean, ChatGPT, and Codex.
This runbook is operational guidance only and does not implement scripts.
Schema/migration references:
- `docs/LIFEVAULT_SCHEMA_V0_PLAN.md`
- `docs/LIFEVAULT_MIGRATION_V0_SPEC.md`
- `docs/LIFEVAULT_MIGRATION_TEST_PLAN_V0.md`
- `docs/LIFEVAULT_MIGRATION_RUNNER_DESIGN.md`
- `docs/LIFEVAULT_MIGRATION_IMPLEMENTATION_TASKLIST_V0.md`
Use-case/requirements references:
- `docs/use_cases/USE_CASE_INDEX.md`
- `docs/use_cases/USE_CASE_TEMPLATE.md`
- `docs/requirements/BUSINESS_REQUIREMENTS.md`
- `docs/requirements/TECHNICAL_REQUIREMENTS.md`
- `docs/requirements/SAFETY_REQUIREMENTS.md`
- `docs/requirements/DATA_REQUIREMENTS.md`
Super use case references:
- `docs/super_use_cases/SUPER_USE_CASE_INDEX.md`
- `docs/super_use_cases/SUPER_USE_CASE_001_LOCAL_FOLDER_LIFECYCLE.md`
Strategy/architecture references:
- `docs/strategy/LIFEVAULT_1000_FOOT_CAPABILITY_MAP.md`
- `docs/architecture/LIFEVAULT_VAULT_ITEM_MODEL.md`
- `docs/architecture/LIFEVAULT_POLICY_MODEL.md`
Security planning references:
- `docs/security/LIFEVAULT_SECURITY_BACKLOG.md`

## 1. Operating Modes

### Design Mode

- Used for architecture, policy, and documentation decisions only.
- No ingestion, publish, or operational DB mutation.

### Builder Mode

- Codex updates code/docs/tests in the repository.
- Validate changes with tests before checkpointing.

### Writer Mode

- Active machine can create pods, update DB, run ingestion, and later publish vault files.
- v0 designated first writer: ASUS PC.

### Reader/Search Mode

- Other machines may search restored/exported metadata.
- Do not write to live operational DB from reader/search machines.

### Recovery Mode

- Used to restore LifeVault capability on a new machine.
- Start with read-only posture until integrity is confirmed.

## 2. Writer-Mode Promotion Checklist

Before any machine becomes writer:

1. Repository is current (latest intended branch/commit).
2. Tests pass.
3. `config/paths.local.json` is correct for that machine.
4. rclone remotes verified if remote vault access is needed.
5. Latest DB backup restored or current DB state confirmed.
6. No other machine is writing.
7. Fresh backup taken before write operation.

## 3. Backup Cadence

Recommended backup timing:

- Before risky operations.
- Before schema migrations.
- Before vault publish.
- After meaningful ingestion sessions.
- End-of-day when LifeVault usage is heavy.
- Use `scripts/backup_lifevault_db.ps1` for real operational backups.
- Use `scripts/smoke_backup_lifevault_db_temp.ps1` to validate backup workflow in temp paths.

## 4. Restore Drill

1. Clone/pull LifeVault repo.
2. Initialize env with `..\..\env_setter.ps1`.
3. Configure `config/paths.local.json`.
4. Create operational folders.
5. Restore `lifevault.sqlite` from `db_backups`.
6. Verify checksum.
7. Run read-only DB validation.
8. Verify rclone remotes if vault access is needed.
9. Start in Reader/Search Mode first.

## 5. Failure Response Checklist

### DB backup fails

- Stop write operations.
- Capture error log and timestamp.
- Retry using approved method; do not use ad hoc live-file copy as default.
- Escalate before continuing risky work.

### Checksum mismatch

- Treat backup as untrusted.
- Do not promote as restore source.
- Recreate backup and revalidate checksum.

### rclone remote unavailable

- Keep operations local-only.
- Validate network/auth context.
- Re-verify remotes before any workflow needing vault access.

### OneDrive auth expired

- Pause remote-dependent operations.
- Re-authenticate through approved operator workflow.
- Re-run safe read checks before proceeding.

### Accidental file in repo

- Stop and assess sensitivity.
- Remove from tracking via approved safe Git workflow.
- Rotate/revoke secrets if applicable.

### Accidental local config committed

- Treat as sensitive exposure if machine-specific/private values leaked.
- Remove from tracking and update ignore policy if needed.
- Rotate/revoke any exposed credentials/tokens.

### Duplicate writer conflict suspected

- Freeze writes immediately.
- Identify active writer machine and last known good backup.
- Resolve authority to one writer before resuming.

### Vault publish failure (future)

- Halt publish pipeline.
- Preserve logs and publish attempt metadata.
- Restore to pre-publish checkpoint/backups as needed.

### Streamlit/control center error (future)

- Switch to documented CLI/manual-safe workflow.
- Capture error details and reproduction context.
- Resume only with known-safe operations.

## 6. Agent Responsibilities

### ChatGPT

- Decide next safe bite.
- Explain current state and risk.
- Write Codex prompts.
- Protect scope.

### Codex

- Read `agents/codex/AGENTS.md` first.
- Use tested scripts.
- Report files changed.
- Run tests.
- Avoid risky operations unless explicitly authorized.

### Sean

- Approve risky transitions.
- Confirm story/context.
- Decide vault meaning and acceptance.
- Control when to commit.

## 7. Commit/Checkpoint Policy

- Run tests before commit.
- Run `git status --short` before commit.
- Use `gitqall.ps1` when checkpoint is accepted.
- Do not commit real DB, backups, exports, logs, pods, text cache, or secrets.

## 8. Current v0 Status

- LifeVault repository foundation exists.
- Operational root: `D:\AI_Lab\LifeVault`.
- Primary DB planned: `D:\AI_Lab\LifeVault\db\lifevault.sqlite`.
- DB backup/sync policy is documented.
- No ingestion implemented yet in this new LifeVault repo.
- No vault publish implementation yet.
- No real file processing yet.

## 9. Validation Checkpoint Note

- After a real UC_001 proposal run is accepted, the next safe stage is UC_003 pod creation design/review.
- Do not jump directly to UC_011 content inspection without explicit approval and content-scan policy controls.
- UC_003 design reference: `docs/use_cases/UC_003_CREATE_ONBOARDING_POD_WORKFLOW_SPEC.md`.
- Move-to-store behavior is decomposed operationally: copy -> verify -> audit/status -> explicit approval -> cleanup (UC_008).
- UC_003 remains strictly copy-only and does not perform source cleanup/free-space operations.
- UC_004 DB indexing must run temp-first, support dry-run no-write mode, and require explicit approval for real DB writes.
- Current UC_004 implementation is temp-only and rejects the real DB path in this phase.
- Smoke/temp scripts should support configurable temp roots and avoid C: for larger ASUS PC workloads when `D:\\temp` is available.
- Real DB initialization is a separate operation from UC_004 indexing; initialize DB schema first, then index real pods later under explicit approval workflow.
- For real DB UC_004 runs, use `--real-db-confirm`; run dry-run first, then approved indexing only after review.
- UC_005 is read-only metadata search: use DB read-only query mode, no file hydration, no content extraction, and no DB writes.
- UC_006 is metadata-only review/decision workflow: no copy/move/delete/rename, no OneDrive/rclone, and DB writes require explicit approval flags.
- UC_006B publish-readiness review is read-only and must be run before UC_007 to confirm `ready_to_publish` vs blocked items.
- Encryption is deferred in v0 but tracked in security backlog; local/plain publish scope must be treated as interim only.
- UC_007 v0 publish scope is local copy-only (no OneDrive/rclone), and sensitive/highly_sensitive rows require explicit approval gates.
- UC_007 implementation is currently temp-only validated; use dry-run before approved publish in real workflows.
- UC_008 verification must pass before any UC_009 cleanup workflow is allowed; cleanup remains blocked until verification evidence exists.
- UC_009 v0 cleanup policy is quarantine-only (no permanent delete), approval-gated, and must never run as whole-folder cleanup.
- UC_009 implementation is currently temp-only validated; run dry-run before approved quarantine in any real workflow.
- LV_ingest_folder v0 is the first operator workflow: UC_001 proposal -> explicit approval gate -> UC_003 pod copy.
