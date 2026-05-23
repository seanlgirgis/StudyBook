# UC_004_INDEX_POD_TO_DATABASE_WORKFLOW_SPEC.md

## Scope

Design/spec for UC_004 pod-to-database indexing.
This is specification-only and does not execute DB writes in this bite.

Implementation references:

- `src/lifevault/uc004_index_pod.py`
- `src/lifevault/uc004_cli.py`
- `scripts/run_uc004_index_pod.ps1`

## Purpose

Given a UC_003 onboarding pod, write pod/file/instance/review metadata into `lifevault.sqlite` so pod content becomes searchable and trackable without hydrating/opening file contents.

## 1. Inputs

- `PodPath`
- optional `DBPath`
- explicit approval flag for DB indexing
- optional dry-run flag

## 2. Preconditions

- Pod path exists.
- `_pod_profile.json` exists.
- `_pod_manifest.csv` exists.
- `_review.csv` exists.
- `_source_proposal_snapshot.json` exists.
- Database exists and migration `0001_lifevault_core_schema` is applied.
- Backup policy acknowledged before indexing real DB.
- No OneDrive/rclone required.
- No content extraction required.

## 3. What UC_004 Writes

Expected table mapping targets:

- `sources`
- `pods`
- `files`
- `file_instances`
- `tags` / `file_tags` (only when needed)
- `review_decisions`
- `duplicate_groups`
- `duplicate_group_members`
- `audit_log`

Out of scope for UC_004:

- document text
- embeddings
- text cache content

## 4. File Identity Rule (v0)

Use pod manifest metadata as baseline.

If hash support is unavailable, provisional identity may be path/size/mtime based, but this increases duplicate ambiguity.

Recommended v0 rule:

- Compute `sha256` from pod copies (safe because pod is controlled copy, not source mutation).
- Store identity in `files` and instance locations in `file_instances`.

## 5. Review Policy

- Rows from `_review.csv` default to `review_decision=needs_review`.
- `approved_for_database_index` may be false in CSV, but UC_004 DB write still requires explicit operator approval flag.
- `approved_for_vault_publish` remains false unless later workflow updates it.
- DB indexing does not imply vault publish approval.

## 6. Metadata Quality Issue (Current Real Pod)

Known current values in real pod context:

- `project = apod`
- `category = Uncategorized`
- `event_name = initial_intake`
- `suggested_vault_path = LifeVault/01_Knowledge`

UC_004 v0 may index these with review-needed status and preserve later correction/update path.

## 7. Dry-Run Behavior

Dry-run must:

- Read pod artifacts.
- Validate required files/columns.
- Summarize intended inserts/updates by table.
- Report record counts and key identifiers.
- Perform zero DB writes.

## 8. Safety Rules

- No file copy.
- No file move.
- No file delete.
- No file rename.
- No OneDrive/rclone.
- No source cleanup.
- No content extraction.
- No text cache writes.
- No vault publish.
- No DB write unless explicit approval flag is present.
- Real DB path requires explicit `--real-db-confirm`.

## 9. Idempotency Rule (v0)

- Refuse duplicate `pod_id` indexing by default.
- Reindex/update mode may be added later with explicit reindex flag and clear merge rules.
- v0 behavior is fail-fast on existing `pod_id`.
- Current implementation target is temp-only DB operation; real DB mode is blocked in this bite.

Duplicate-group modeling note (v0):

- Duplicate candidates are discovered at file-instance/path level from pod manifest rows.
- `duplicate_group_members` currently stores unique `file_id` membership (file-level), not per-instance membership.
- When two paths resolve to the same `sha256`, group member rows may be fewer than duplicate candidate paths.
- UC_004 should record both `instance_count` and `unique_file_count` in duplicate group notes for reviewer clarity.

## 10. Acceptance Criteria

- Temp DB indexing succeeds first.
- Dry-run performs zero writes.
- Real DB dry-run requires `--real-db-confirm`.
- Real DB approved indexing requires both `--approved` and `--real-db-confirm`.
- Pod rows searchable by `pod_id`, story, and project.
- File rows searchable by filename and sensitivity.
- Review decisions imported as `needs_review`.
- `vault_publish_status` remains `not_published`.
- No OneDrive/rclone activity.

## 11. Test Plan (Future Implementation)

All tests use `tmp_path` only.

- Create temp DB and apply migration.
- Create fake pod package.
- Dry-run writes nothing.
- Approved indexing writes expected rows.
- Duplicate pod indexing is refused.
- Missing manifest fails safely.
- Bad review CSV fails safely.
- No `D:\AI_Lab\LifeVault` path touched in tests.

## 12. Relationship to Next Use Cases

- UC_005 searches indexed metadata.
- UC_006 publishes approved files to vault.
- UC_007 verifies vault copy.
- UC_008 handles source cleanup after verification.
