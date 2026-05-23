# LIFEVAULT_MIGRATION_V0_SPEC.md

## 1. Migration Identity

- `migration_id`: `0001_lifevault_core_schema`
- Target database: `lifevault.sqlite`
- Target location by policy: `D:\AI_Lab\LifeVault\db\lifevault.sqlite`
- Migration purpose: create the v0 LifeVault core operational schema

This document is a specification only. No migration code is executed in this bite.

## 2. DDL Outline (SQLite Style)

```sql
-- Always enable foreign keys explicitly in migration/runtime sessions
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  migration_id TEXT NOT NULL UNIQUE,
  applied_at TEXT NOT NULL,
  checksum TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS sources (
  source_id TEXT PRIMARY KEY,
  source_type TEXT NOT NULL CHECK (source_type IN (
    'local_folder','onedrive_dirty','onedrive_clean','external_drive','code_repo','export','other'
  )),
  source_name TEXT NOT NULL,
  root_ref TEXT,
  remote_name TEXT,
  description TEXT,
  is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(source_type, source_name)
);

CREATE TABLE IF NOT EXISTS pods (
  pod_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  pod_name TEXT NOT NULL,
  event_name TEXT,
  pod_status TEXT NOT NULL CHECK (pod_status IN (
    'proposed','onboarded_needs_review','reviewed','archived','error'
  )),
  story_context TEXT,
  intake_notes TEXT,
  sensitivity_level TEXT NOT NULL DEFAULT 'unknown' CHECK (sensitivity_level IN (
    'unknown','public','normal','private','sensitive','highly_sensitive'
  )),
  storage_temperature TEXT NOT NULL DEFAULT 'unknown' CHECK (storage_temperature IN (
    'unknown','hot','warm','cold'
  )),
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(source_id, pod_name),
  FOREIGN KEY(source_id) REFERENCES sources(source_id) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS files (
  file_id TEXT PRIMARY KEY,
  sha256 TEXT NOT NULL,
  hash_algo TEXT NOT NULL DEFAULT 'sha256',
  filename TEXT,
  ext TEXT,
  size_bytes INTEGER,
  mime_type TEXT,
  file_status TEXT NOT NULL DEFAULT 'observed' CHECK (file_status IN (
    'observed','copied_to_pod','needs_review','approved','skipped','duplicate_candidate','published','error'
  )),
  review_status TEXT NOT NULL DEFAULT 'needs_review' CHECK (review_status IN (
    'needs_review','approved','skipped','duplicate_review','sensitive_review','archive'
  )),
  publish_status TEXT NOT NULL DEFAULT 'not_published' CHECK (publish_status IN (
    'not_published','publish_approved','published','verified','failed'
  )),
  sensitivity_level TEXT NOT NULL DEFAULT 'unknown' CHECK (sensitivity_level IN (
    'unknown','public','normal','private','sensitive','highly_sensitive'
  )),
  storage_temperature TEXT NOT NULL DEFAULT 'unknown' CHECK (storage_temperature IN (
    'unknown','hot','warm','cold'
  )),
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(sha256, hash_algo)
);

CREATE TABLE IF NOT EXISTS file_instances (
  instance_id TEXT PRIMARY KEY,
  file_id TEXT NOT NULL,
  source_id TEXT,
  pod_id TEXT,
  instance_role TEXT NOT NULL,
  instance_path TEXT NOT NULL,
  path_is_absolute INTEGER NOT NULL DEFAULT 0 CHECK (path_is_absolute IN (0,1)),
  path_platform TEXT,
  observed_at TEXT,
  is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0,1)),
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(file_id, instance_path, instance_role),
  FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
  FOREIGN KEY(source_id) REFERENCES sources(source_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
  FOREIGN KEY(pod_id) REFERENCES pods(pod_id) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS vault_locations (
  vault_location_id TEXT PRIMARY KEY,
  file_id TEXT NOT NULL,
  vault_path TEXT NOT NULL,
  publish_status TEXT NOT NULL CHECK (publish_status IN (
    'not_published','publish_approved','published','verified','failed'
  )),
  approved_by TEXT,
  approved_at TEXT,
  publish_batch_id TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(file_id, vault_path),
  FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS tags (
  tag_id TEXT PRIMARY KEY,
  tag_name TEXT NOT NULL UNIQUE,
  tag_group TEXT,
  description TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT
);

CREATE TABLE IF NOT EXISTS file_tags (
  file_id TEXT NOT NULL,
  tag_id TEXT NOT NULL,
  created_at TEXT NOT NULL,
  assigned_by TEXT,
  PRIMARY KEY(file_id, tag_id),
  FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
  FOREIGN KEY(tag_id) REFERENCES tags(tag_id) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS review_decisions (
  decision_id TEXT PRIMARY KEY,
  file_id TEXT NOT NULL,
  decision_type TEXT NOT NULL,
  review_status TEXT NOT NULL CHECK (review_status IN (
    'needs_review','approved','skipped','duplicate_review','sensitive_review','archive'
  )),
  publish_status TEXT NOT NULL CHECK (publish_status IN (
    'not_published','publish_approved','published','verified','failed'
  )),
  decided_by TEXT,
  decision_note TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS duplicate_groups (
  duplicate_group_id TEXT PRIMARY KEY,
  group_method TEXT NOT NULL,
  group_status TEXT NOT NULL,
  confidence_score REAL,
  note TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT
);

CREATE TABLE IF NOT EXISTS duplicate_group_members (
  duplicate_group_id TEXT NOT NULL,
  file_id TEXT NOT NULL,
  member_role TEXT,
  is_canonical_candidate INTEGER NOT NULL DEFAULT 0 CHECK (is_canonical_candidate IN (0,1)),
  created_at TEXT NOT NULL,
  PRIMARY KEY(duplicate_group_id, file_id),
  FOREIGN KEY(duplicate_group_id) REFERENCES duplicate_groups(duplicate_group_id) ON DELETE RESTRICT ON UPDATE NO ACTION,
  FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS audit_log (
  audit_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  event_time TEXT NOT NULL,
  actor TEXT,
  target_table TEXT,
  target_id TEXT,
  event_status TEXT,
  event_payload_json TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS text_cache_index (
  text_index_id TEXT PRIMARY KEY,
  file_id TEXT NOT NULL,
  cache_ref TEXT,
  extract_status TEXT NOT NULL,
  extract_engine TEXT,
  last_extracted_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(file_id, cache_ref),
  FOREIGN KEY(file_id) REFERENCES files(file_id) ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS export_snapshots (
  export_id TEXT PRIMARY KEY,
  export_type TEXT NOT NULL,
  artifact_path TEXT NOT NULL,
  checksum_sha256 TEXT,
  row_count INTEGER,
  trigger_reason TEXT,
  export_time TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(export_type, artifact_path)
);
```

## 3. Enum/CHECK Constraints

Canonical CHECK sets for v0:

- `sensitivity_level`: `unknown`, `public`, `normal`, `private`, `sensitive`, `highly_sensitive`
- `storage_temperature`: `unknown`, `hot`, `warm`, `cold`
- `pod_status`: `proposed`, `onboarded_needs_review`, `reviewed`, `archived`, `error`
- `file_status`: `observed`, `copied_to_pod`, `needs_review`, `approved`, `skipped`, `duplicate_candidate`, `published`, `error`
- `review_status`: `needs_review`, `approved`, `skipped`, `duplicate_review`, `sensitive_review`, `archive`
- `publish_status`: `not_published`, `publish_approved`, `published`, `verified`, `failed`
- `source_type`: `local_folder`, `onedrive_dirty`, `onedrive_clean`, `external_drive`, `code_repo`, `export`, `other`

## 4. Index Names

Planned indexes (besides PK/UNIQUE implicit indexes):

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

Representative SQL outline:

```sql
CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(source_type);
CREATE INDEX IF NOT EXISTS idx_pods_status ON pods(pod_status);
CREATE INDEX IF NOT EXISTS idx_pods_event_name ON pods(event_name);
CREATE INDEX IF NOT EXISTS idx_files_sha256 ON files(sha256);
CREATE INDEX IF NOT EXISTS idx_files_filename ON files(filename);
CREATE INDEX IF NOT EXISTS idx_files_sensitivity ON files(sensitivity_level);
CREATE INDEX IF NOT EXISTS idx_file_instances_file_id ON file_instances(file_id);
CREATE INDEX IF NOT EXISTS idx_file_instances_source_id ON file_instances(source_id);
CREATE INDEX IF NOT EXISTS idx_file_instances_path ON file_instances(instance_path);
CREATE INDEX IF NOT EXISTS idx_vault_locations_file_id ON vault_locations(file_id);
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(tag_name);
CREATE INDEX IF NOT EXISTS idx_file_tags_file_id ON file_tags(file_id);
CREATE INDEX IF NOT EXISTS idx_review_decisions_file_id ON review_decisions(file_id);
CREATE INDEX IF NOT EXISTS idx_duplicate_members_group_id ON duplicate_group_members(duplicate_group_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX IF NOT EXISTS idx_text_cache_file_id ON text_cache_index(file_id);
CREATE INDEX IF NOT EXISTS idx_export_snapshots_created_at ON export_snapshots(created_at);
```

## 5. Foreign-Key Rules

- SQLite FK enforcement must be explicitly enabled: `PRAGMA foreign_keys = ON`.
- Deletion policy is conservative.
- Prefer `RESTRICT`/`NO ACTION` for most relationships.
- Do not cascade-delete files, pods, audit history, or vault mappings casually.

## 6. Timestamp Rules

- `created_at` is required on core records.
- `updated_at` is present where mutable state exists.
- Timestamps are ISO-8601 text.

## 7. Path Policy

- Local absolute paths may be stored for provenance.
- Local paths are machine-specific.
- Vault paths are logical, portable destinations.
- Code must not assume ASUS-only absolute paths.
- Configuration resolves machine-local roots.

## 8. Sensitive Metadata Warning

Likely sensitive tables:

- `pods`
- `files`
- `file_instances`
- `vault_locations`
- `review_decisions`
- `audit_log`
- `text_cache_index`
- `export_snapshots`

## 9. Migration Acceptance Checks

Future migration runner must verify:

1. DB file exists only after explicit migration command.
2. `PRAGMA foreign_key_check;` returns no rows.
3. `schema_migrations` contains `0001_lifevault_core_schema`.
4. All expected tables exist.
5. All expected indexes exist.
6. Enum CHECK constraints are present where practical.
7. Fake-data insert/read/delete validation succeeds.
8. Tests do not require real file paths.
9. No OneDrive operations occur.

## 10. Rollback Policy

- v0 rollback is allowed only for empty/test DBs.
- Do not drop a populated real LifeVault DB without backup and explicit approval.
- Preferred rollback method is backup restore, not destructive schema surgery.

## 11. Relationship to Backup Policy

Reference:

- `docs/LIFEVAULT_DATABASE_BACKUP_SYNC_POLICY.md`

Requirement:

- Before any future schema migration on a real DB, backup must run first.

## 12. Relationship to Schema Plan

Reference:

- `docs/LIFEVAULT_SCHEMA_V0_PLAN.md`
- `docs/LIFEVAULT_MIGRATION_TEST_PLAN_V0.md`
- `docs/LIFEVAULT_MIGRATION_RUNNER_DESIGN.md`
