# LIFEVAULT_MIGRATION_IMPLEMENTATION_TASKLIST_V0.md

## Scope

Implementation-planning checklist for v0 migration work.
This document is a tasklist only; no migration code is implemented in this bite.

Planned implementation targets (next bite):

- `src/lifevault/schema_v0.py`
- `src/lifevault/migrate.py`
- `tests/test_migration_v0.py`

## 1) Pre-Implementation Checks (Must Complete First)

1. Read `agents/codex/AGENTS.md`.
2. Read `agents/codex/LIFEVAULT_BOOTSTRAP.md`.
3. Read `agents/codex/CODEX_CONSTITUTION.md`.
4. Read `docs/LIFEVAULT_MIGRATION_V0_SPEC.md`.
5. Read `docs/LIFEVAULT_MIGRATION_TEST_PLAN_V0.md`.
6. Read `docs/LIFEVAULT_MIGRATION_RUNNER_DESIGN.md`.
7. Confirm implementation session will not touch real DB path:
   - `D:\AI_Lab\LifeVault\db\lifevault.sqlite`
8. Confirm no rclone/OneDrive operations are needed.

## 2) `schema_v0.py` Tasks

### 2.1 Module Constants

1. Define `MIGRATION_ID = "0001_lifevault_core_schema"`.
2. Define `EXPECTED_TABLES` as ordered list of v0 tables.
3. Define `EXPECTED_INDEXES` as list of expected index names.
4. Define `CREATE_TABLE_STATEMENTS` as explicit SQL strings.
5. Define `CREATE_INDEX_STATEMENTS` as explicit SQL strings.

### 2.2 Core Functions

1. Implement `apply_schema_v0(conn)`:
   - Enable `PRAGMA foreign_keys = ON`.
   - Ensure `schema_migrations` table exists first.
   - Start transaction.
   - Execute table DDL then index DDL.
   - Insert migration record if not already present.
   - Commit on success; rollback on failure.
2. Implement `validate_schema_v0(conn)`:
   - Enable `PRAGMA foreign_keys = ON`.
   - Check expected tables exist.
   - Check expected indexes exist.
   - Check migration record exists.
   - Run `PRAGMA foreign_key_check` and assert no rows.
   - Return structured validation result.

### 2.3 Guardrails

- Use Python `sqlite3` only.
- No real file paths required in SQL logic.
- No OneDrive/rclone code.
- No ingestion or external IO logic.

## 3) `migrate.py` Tasks

### 3.1 CLI Interface

Implement CLI shapes:

- `python -m lifevault.migrate --db-path <path> --apply 0001_lifevault_core_schema`
- `python -m lifevault.migrate --db-path <path> --status`
- `python -m lifevault.migrate --db-path <path> --validate`
- `python -m lifevault.migrate --db-path <path> --dry-run`

### 3.2 Argument and Safety Handling

1. Parse and validate command args (mutually exclusive action flags where appropriate).
2. Resolve repo root and reject DB paths inside repo root.
3. Reject real DB path unless `--real-db-confirm` is present.
4. Dry-run mode:
   - Print intended action/path/existence status.
   - Exit without creating parent dirs or DB file.
5. Apply mode:
   - Create parent dir only for provided temp/test path.
   - Connect via `sqlite3`.
   - Call `apply_schema_v0`.
   - Call `validate_schema_v0` post-apply.
6. Status mode:
   - Report whether DB exists and whether migration is present.
7. Validate mode:
   - Open DB and run `validate_schema_v0`.

### 3.3 Idempotency

- If migration already exists in `schema_migrations`, do not reapply DDL.
- Run validation and return clean status.

### 3.4 Explicit Exclusions

- No backup automation in v0 implementation.
- No upload/rclone/file ingestion.
- No delete/move/rename/sync behavior.

## 4) `tests/test_migration_v0.py` Tasks

All tests must use `tmp_path` only.

### 4.1 Setup Helpers

1. Add helper to build temp DB path under `tmp_path`.
2. Add helper to run CLI subprocess or module entrypoint for each mode.
3. Add helper to inspect `sqlite_master` and `schema_migrations`.

### 4.2 Required Test Cases

1. Migration creates all expected tables.
2. Migration creates all expected indexes.
3. `schema_migrations` contains `0001_lifevault_core_schema`.
4. Migration apply is idempotent.
5. Validate command passes after migration.
6. Foreign keys reject invalid references.
7. CHECK constraints reject invalid enum values.
8. Fake lifecycle insert/read works.
9. Dry-run does not create DB file.
10. Real DB path rejected without `--real-db-confirm`.
11. DB path inside repo root is rejected.
12. Tests do not touch `D:\AI_Lab\LifeVault`.

### 4.3 Test Data Rules

- Use fake IDs, fake paths, fake hashes.
- No real files.
- No network/rclone calls.

## 5) Acceptance Criteria for Implementation Bite

Implementation is acceptable only when:

1. `python -m pytest -q` passes.
2. No real DB is created.
3. `D:\AI_Lab\LifeVault\db\lifevault.sqlite` is not touched.
4. No OneDrive/rclone calls occur.
5. No real file processing occurs.
6. Behavior matches:
   - `docs/LIFEVAULT_MIGRATION_V0_SPEC.md`
   - `docs/LIFEVAULT_MIGRATION_TEST_PLAN_V0.md`
   - `docs/LIFEVAULT_MIGRATION_RUNNER_DESIGN.md`

## 6) Future Sequence After Implementation

1. Run migration CLI against temp DB manually.
2. Inspect resulting schema/tables/indexes.
3. Confirm idempotent re-run behavior manually.
4. Then design backup script plan.
5. Only later consider real DB creation under explicit approval.