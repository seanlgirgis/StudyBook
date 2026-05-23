# LIFEVAULT_MIGRATION_TEST_PLAN_V0.md

## Scope

Fake-data-only test plan for migration `0001_lifevault_core_schema`.
This plan validates migration behavior without touching the real operational DB.

- Do not use `D:\AI_Lab\LifeVault\db\lifevault.sqlite`.
- Use temporary/local test DBs only (for example temp directory paths).
- No OneDrive/rclone operations.

## Migration Under Test

- `migration_id`: `0001_lifevault_core_schema`
- Target DB name: `lifevault.sqlite`
- Production policy path (not used in tests): `D:\AI_Lab\LifeVault\db\lifevault.sqlite`

## Test Environment Rules

- Create ephemeral SQLite DB file in temp path.
- Enable foreign keys with `PRAGMA foreign_keys = ON`.
- Use synthetic IDs, paths, names, and content hashes.
- No real personal files, no real paths required.

## 1) Table Existence Tests

Verify that all required tables exist after migration apply:

- `schema_migrations`
- `sources`
- `pods`
- `files`
- `file_instances`
- `vault_locations`
- `tags`
- `file_tags`
- `review_decisions`
- `duplicate_groups`
- `duplicate_group_members`
- `audit_log`
- `text_cache_index`
- `export_snapshots`

Suggested validation query pattern:

```sql
SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?;
```

Pass criteria:

- Every expected table is present.
- No missing core table.

## 2) schema_migrations Record Test

Verify migration tracking row exists:

- `migration_id = '0001_lifevault_core_schema'`
- `applied_at` is populated.

Suggested check:

```sql
SELECT migration_id, applied_at FROM schema_migrations WHERE migration_id = '0001_lifevault_core_schema';
```

Pass criteria:

- Exactly one matching row.
- `applied_at` non-empty.

## 3) Foreign Key Behavior Tests

Prerequisite:

```sql
PRAGMA foreign_keys = ON;
```

Test cases:

- Insert child row with nonexistent parent should fail:
  - `pods.source_id` -> `sources.source_id`
  - `file_instances.file_id` -> `files.file_id`
  - `file_tags.tag_id` -> `tags.tag_id`
- Parent delete with dependent child should fail under RESTRICT/NO ACTION.

Pass criteria:

- FK-invalid inserts fail.
- Restricted parent deletes fail.
- `PRAGMA foreign_key_check;` returns zero rows after valid setup.

## 4) CHECK Constraint Tests

For each constrained enum/status column, test one valid and one invalid value.

Columns/sets:

- `sensitivity_level`: `unknown`, `public`, `normal`, `private`, `sensitive`, `highly_sensitive`
- `storage_temperature`: `unknown`, `hot`, `warm`, `cold`
- `pod_status`: `proposed`, `onboarded_needs_review`, `reviewed`, `archived`, `error`
- `file_status`: `observed`, `copied_to_pod`, `needs_review`, `approved`, `skipped`, `duplicate_candidate`, `published`, `error`
- `review_status`: `needs_review`, `approved`, `skipped`, `duplicate_review`, `sensitive_review`, `archive`
- `publish_status`: `not_published`, `publish_approved`, `published`, `verified`, `failed`
- `source_type`: `local_folder`, `onedrive_dirty`, `onedrive_clean`, `external_drive`, `code_repo`, `export`, `other`

Pass criteria:

- Valid values insert/update successfully.
- Invalid values are rejected by CHECK constraints.

## 5) Index Presence Tests

Verify expected indexes exist:

- `idx_sources_type`
- `idx_pods_status`
- `idx_pods_event_name`
- `idx_files_sha256`
- `idx_files_filename`
- `idx_files_sensitivity`
- `idx_file_instances_file_id`
- `idx_file_instances_source_id`
- `idx_file_instances_path`
- `idx_vault_locations_file_id`
- `idx_tags_name`
- `idx_file_tags_file_id`
- `idx_review_decisions_file_id`
- `idx_duplicate_members_group_id`
- `idx_audit_log_created_at`
- `idx_text_cache_file_id`
- `idx_export_snapshots_created_at`

Suggested query:

```sql
SELECT name FROM sqlite_master WHERE type = 'index' AND name = ?;
```

Pass criteria:

- Every required index name is present.

## 6) Fake Lifecycle Insert/Read Test

Run a small synthetic lifecycle:

1. Insert one `sources` row.
2. Insert one `pods` row tied to source.
3. Insert one `files` row with fake hash and statuses.
4. Insert one `file_instances` row for pod copy path.
5. Insert one `review_decisions` row.
6. Insert one `vault_locations` row with `publish_approved`.
7. Insert one `audit_log` row for review/publish event.
8. Query join across source -> pod -> file_instance -> file -> review.

Pass criteria:

- Inserts succeed with valid fake data.
- Read query returns expected linked record set.
- No real file access required.

## 7) Rollback / Empty Test DB Procedure

Allowed rollback context:

- Empty or disposable test DB only.

Procedure:

1. Create temporary DB.
2. Apply migration.
3. Validate schema quickly.
4. Close DB handle.
5. Delete temp DB file as cleanup.

Rules:

- Do not apply destructive rollback to populated real DBs.
- Real rollback strategy is backup restore per policy.

## 8) Acceptance Criteria

Migration is accepted for implementation readiness when all are true:

1. All required tables exist.
2. `schema_migrations` records `0001_lifevault_core_schema`.
3. FK checks pass and invalid FK actions fail.
4. CHECK constraints enforce canonical enums/statuses.
5. All required indexes exist.
6. Fake lifecycle insert/read succeeds.
7. Rollback procedure validated on disposable DB only.
8. No real DB path is touched.
9. No OneDrive/rclone operations occur.

## References

- `docs/LIFEVAULT_SCHEMA_V0_PLAN.md`
- `docs/LIFEVAULT_MIGRATION_V0_SPEC.md`
- `docs/LIFEVAULT_MIGRATION_RUNNER_DESIGN.md`
- `docs/LIFEVAULT_DATABASE_BACKUP_SYNC_POLICY.md`
- `docs/LIFEVAULT_OPERATIONS_RUNBOOK.md`
