# LIFEVAULT_MIGRATION_RUNNER_DESIGN.md

## 1. Purpose

Define how a future migration runner will safely apply SQLite schema migrations, starting with temporary/test DBs only.

## 2. Scope for v0

The first runner implementation must support:

- Apply `0001_lifevault_core_schema` to a specified SQLite DB path.
- Temp/test DB operation first.
- `schema_migrations` tracking.
- Idempotency check.
- Transaction-wrapped migration.
- `PRAGMA foreign_keys = ON`.
- Post-migration validation.
- Clear logging.
- No OneDrive/rclone operations.

## 3. Non-goals for v0

- No real LifeVault DB creation unless explicitly invoked later.
- No backup automation yet.
- No encryption yet.
- No vector DB.
- No ingestion.
- No file processing.

## 4. Runner Command Shape

Primary command:

- `python -m lifevault.migrate --db-path <path> --apply 0001_lifevault_core_schema`

Optional future commands:

- `python -m lifevault.migrate --db-path <path> --status`
- `python -m lifevault.migrate --db-path <path> --validate`
- `python -m lifevault.migrate --db-path <path> --dry-run`

## 5. Safety Gates

Real DB mode (future) must enforce:

- Refuse to run on `D:\AI_Lab\LifeVault\db\lifevault.sqlite` unless `--real-db-confirm` is provided.
- Require backup confirmation for existing real DBs.
- Refuse if DB path is inside Git repo.
- Log migration action.
- Require explicit approval for destructive rollback.

## 6. Idempotency

Rules:

- If migration ID already exists in `schema_migrations`, do not reapply DDL.
- Validate schema still matches expected state.
- Return clean "already applied/valid" status.

## 7. Transaction Boundary

Rules:

- Apply schema changes in one transaction where practical.
- On failure, rollback transaction.
- No partial schema should be accepted.

## 8. Logging

- Emit clear console logs (start, action, success/failure, validation summary).
- Future file logs under `D:\AI_Lab\LifeVault\logs`.
- Never log secrets/tokens.

## 9. Validation

After migration, runner must validate:

- Expected tables exist.
- Expected indexes exist.
- `schema_migrations` contains migration ID.
- `PRAGMA foreign_key_check` returns no rows.
- Fake insert/read validation occurs in tests only.

## 10. Dry-run Behavior

Dry-run must:

- Report intended migration.
- Report target DB path.
- Report whether DB currently exists.
- Not write schema.
- Not create DB file.

## 11. Test Strategy

Reference:

- `docs/LIFEVAULT_MIGRATION_TEST_PLAN_V0.md`

Requirement:

- Implementation must pass migration tests using temp SQLite DBs only before any real DB usage.

## 12. Relationship to Backup Policy

Reference:

- `docs/LIFEVAULT_DATABASE_BACKUP_SYNC_POLICY.md`

Requirement:

- Any future real DB migration must require backup before apply.

## 13. Relationship to Operations Runbook

Reference:

- `docs/LIFEVAULT_OPERATIONS_RUNBOOK.md`

Requirement:

- Runner usage for real DBs must follow writer-mode and backup cadence rules.

## 14. Future Implementation Files

Likely future files:

- `src/lifevault/migrate.py`
- `src/lifevault/schema_v0.py`
- `tests/test_migration_v0.py`

## 15. Acceptance Criteria

Future migration-runner implementation is accepted only if:

- Tests pass on temp DBs.
- No real DB path is touched by tests.
- No OneDrive/rclone calls occur.
- Dry-run performs zero writes.
- Migration apply is idempotent.
- Invalid CHECK values fail.
- Invalid FK inserts fail.
- Validation catches missing tables/indexes.

Implementation tasklist reference:

- `docs/LIFEVAULT_MIGRATION_IMPLEMENTATION_TASKLIST_V0.md`
