# LIFEVAULT_SCHEMA_V0_PLAN.md

## Scope

Design-only SQLite v0 schema plan for LifeVault.
No DB creation, migrations, or data processing is performed in this bite.

Primary planned DB location:

- `D:\AI_Lab\LifeVault\db\lifevault.sqlite`

Migration specification reference:

- `docs/LIFEVAULT_MIGRATION_V0_SPEC.md`

## Global Design Decisions

- File identity is separate from location:
  - `files` = content identity.
  - `file_instances` = observed/copied locations.
- Do not store full real document text in v0.
  - Use `text_cache_index` placeholders only.
- Story/context is captured at pod level first, with optional file-level notes later.
- Controlled enums include:
  - `sensitivity_level`: `public`, `normal`, `private`, `sensitive`, `highly_sensitive`, `unknown`
  - `storage_temperature`: `hot`, `warm`, `cold`, `unknown`
- Status fields used across model:
  - `pod_status`, `file_status`, `review_status`, `publish_status`
- Timestamp pattern:
  - `created_at` required on core tables.
  - `updated_at` included where mutable state is expected.
- Portable path strategy:
  - Paths are stored as text.
  - Absolute local paths are machine-specific and interpreted via config.

## Migration Order (v0)

1. `schema_migrations`
2. `sources`
3. `pods`
4. `files`
5. `file_instances`
6. `vault_locations`
7. `tags`
8. `file_tags`
9. `review_decisions`
10. `duplicate_groups`
11. `duplicate_group_members`
12. `audit_log`
13. `text_cache_index`
14. `export_snapshots`

## Table Plans

### 1) schema_migrations

- Purpose: track applied schema versions.
- Key columns: `version`, `name`, `applied_at`, `checksum`.
- Required columns:
  - `version` INTEGER
  - `name` TEXT
  - `applied_at` TEXT (ISO8601)
- Optional columns:
  - `checksum` TEXT
  - `notes` TEXT
- Primary key: `version`
- Foreign keys: none
- Unique constraints: `name` UNIQUE
- Useful indexes: none beyond PK/UNIQUE
- Example row:
  - `(1, '0001_init_core', '2026-05-23T10:00:00Z', 'sha256:abc...', 'initial v0')`
- Sensitive metadata: low (operational history only)

### 2) sources

- Purpose: track source origins (local folder, dirty OneDrive, clean vault, external drive, future Gmail export).
- Key columns: `source_id`, `source_type`, `source_name`, `root_ref`, `is_active`.
- Required columns:
  - `source_id` TEXT
  - `source_type` TEXT
  - `source_name` TEXT
  - `created_at` TEXT
- Optional columns:
  - `root_ref` TEXT
  - `remote_name` TEXT
  - `description` TEXT
  - `is_active` INTEGER
  - `updated_at` TEXT
- Primary key: `source_id`
- Foreign keys: none
- Unique constraints: (`source_type`, `source_name`) UNIQUE
- Useful indexes:
  - `idx_sources_type` on `source_type`
  - `idx_sources_active` on `is_active`
- Example row:
  - `('src_001','onedrive_dirty','Dirty OneDrive','/','onedrive_dirty','Primary dirty remote',1,'2026-05-23T10:10:00Z',NULL)`
- Sensitive metadata: medium (source naming/location hints)

### 3) pods

- Purpose: track ingestion/onboarding pods.
- Key columns: `pod_id`, `source_id`, `pod_name`, `pod_status`, `story_context`.
- Required columns:
  - `pod_id` TEXT
  - `source_id` TEXT
  - `pod_name` TEXT
  - `pod_status` TEXT
  - `created_at` TEXT
- Optional columns:
  - `story_context` TEXT
  - `intake_notes` TEXT
  - `sensitivity_level` TEXT
  - `storage_temperature` TEXT
  - `updated_at` TEXT
- Primary key: `pod_id`
- Foreign keys:
  - `source_id` -> `sources(source_id)`
- Unique constraints: (`source_id`, `pod_name`) UNIQUE
- Useful indexes:
  - `idx_pods_source` on `source_id`
  - `idx_pods_status` on `pod_status`
- Example row:
  - `('pod_20260523_001','src_001','boa_ltimindtree_intake','open','Legacy project context collection','initial triage','private','warm','2026-05-23T11:00:00Z',NULL)`
- Sensitive metadata: high (story/context and intake notes)

### 4) files

- Purpose: track unique file/content identity.
- Key columns: `file_id`, `content_hash`, `size_bytes`, `mime_type`, `file_status`.
- Required columns:
  - `file_id` TEXT
  - `content_hash` TEXT
  - `created_at` TEXT
- Optional columns:
  - `hash_algo` TEXT
  - `size_bytes` INTEGER
  - `mime_type` TEXT
  - `ext` TEXT
  - `file_status` TEXT
  - `sensitivity_level` TEXT
  - `storage_temperature` TEXT
  - `updated_at` TEXT
- Primary key: `file_id`
- Foreign keys: none
- Unique constraints: (`content_hash`, `hash_algo`) UNIQUE
- Useful indexes:
  - `idx_files_status` on `file_status`
  - `idx_files_sensitivity` on `sensitivity_level`
- Example row:
  - `('file_001','9f86d081...','sha256',1048576,'application/pdf','.pdf','active','private','warm','2026-05-23T11:10:00Z',NULL)`
- Sensitive metadata: medium/high (classification and type hints)

### 5) file_instances

- Purpose: track observed/copied file locations (source path, pod copy path, vault path, local cache path).
- Key columns: `instance_id`, `file_id`, `source_id`, `pod_id`, `instance_path`, `instance_role`.
- Required columns:
  - `instance_id` TEXT
  - `file_id` TEXT
  - `instance_path` TEXT
  - `instance_role` TEXT
  - `created_at` TEXT
- Optional columns:
  - `source_id` TEXT
  - `pod_id` TEXT
  - `path_is_absolute` INTEGER
  - `path_platform` TEXT
  - `observed_at` TEXT
  - `is_current` INTEGER
  - `updated_at` TEXT
- Primary key: `instance_id`
- Foreign keys:
  - `file_id` -> `files(file_id)`
  - `source_id` -> `sources(source_id)`
  - `pod_id` -> `pods(pod_id)`
- Unique constraints: (`file_id`, `instance_path`, `instance_role`) UNIQUE
- Useful indexes:
  - `idx_instances_file` on `file_id`
  - `idx_instances_pod` on `pod_id`
  - `idx_instances_role` on `instance_role`
- Example row:
  - `('inst_001','file_001','src_001','pod_20260523_001','onboarding\\pods\\pod_20260523_001\\doc1.pdf','pod_copy',0,'windows','2026-05-23T11:15:00Z',1,NULL)`
- Sensitive metadata: high (real path clues)

### 6) vault_locations

- Purpose: track approved final vault destinations.
- Key columns: `vault_location_id`, `file_id`, `vault_path`, `publish_status`.
- Required columns:
  - `vault_location_id` TEXT
  - `file_id` TEXT
  - `vault_path` TEXT
  - `publish_status` TEXT
  - `created_at` TEXT
- Optional columns:
  - `approved_by` TEXT
  - `approved_at` TEXT
  - `publish_batch_id` TEXT
  - `updated_at` TEXT
- Primary key: `vault_location_id`
- Foreign keys:
  - `file_id` -> `files(file_id)`
- Unique constraints: (`file_id`, `vault_path`) UNIQUE
- Useful indexes:
  - `idx_vault_locations_publish_status` on `publish_status`
  - `idx_vault_locations_path` on `vault_path`
- Example row:
  - `('vl_001','file_001','LifeVault/01_Knowledge/Finance/statement_2024.pdf','approved','sean','2026-05-23T12:00:00Z','batch_001','2026-05-23T11:50:00Z',NULL)`
- Sensitive metadata: high (destination taxonomy and meaning)

### 7) tags

- Purpose: controlled/simple tags.
- Key columns: `tag_id`, `tag_name`.
- Required columns:
  - `tag_id` TEXT
  - `tag_name` TEXT
  - `created_at` TEXT
- Optional columns:
  - `tag_group` TEXT
  - `description` TEXT
  - `updated_at` TEXT
- Primary key: `tag_id`
- Foreign keys: none
- Unique constraints: `tag_name` UNIQUE
- Useful indexes:
  - `idx_tags_group` on `tag_group`
- Example row:
  - `('tag_001','tax','domain','Tax-related materials','2026-05-23T12:05:00Z',NULL)`
- Sensitive metadata: low/medium

### 8) file_tags

- Purpose: many-to-many mapping between files and tags.
- Key columns: `file_id`, `tag_id`.
- Required columns:
  - `file_id` TEXT
  - `tag_id` TEXT
  - `created_at` TEXT
- Optional columns:
  - `assigned_by` TEXT
- Primary key: composite (`file_id`, `tag_id`)
- Foreign keys:
  - `file_id` -> `files(file_id)`
  - `tag_id` -> `tags(tag_id)`
- Unique constraints: covered by PK
- Useful indexes:
  - `idx_file_tags_tag` on `tag_id`
- Example row:
  - `('file_001','tag_001','2026-05-23T12:06:00Z','sean')`
- Sensitive metadata: medium (classification inference)

### 9) review_decisions

- Purpose: track human decisions (`keep`, `skip`, `duplicate_review`, `archive`, `sensitive_review`, `publish_approved`).
- Key columns: `decision_id`, `file_id`, `decision_type`, `review_status`, `publish_status`.
- Required columns:
  - `decision_id` TEXT
  - `file_id` TEXT
  - `decision_type` TEXT
  - `created_at` TEXT
- Optional columns:
  - `review_status` TEXT
  - `publish_status` TEXT
  - `decided_by` TEXT
  - `decision_note` TEXT
  - `updated_at` TEXT
- Primary key: `decision_id`
- Foreign keys:
  - `file_id` -> `files(file_id)`
- Unique constraints: none (decision history allowed)
- Useful indexes:
  - `idx_review_file` on `file_id`
  - `idx_review_type` on `decision_type`
  - `idx_review_publish_status` on `publish_status`
- Example row:
  - `('rev_001','file_001','publish_approved','reviewed','approved','sean','ready for vault placement','2026-05-23T12:10:00Z',NULL)`
- Sensitive metadata: high (human judgment and notes)

### 10) duplicate_groups

- Purpose: track duplicate candidate groups.
- Key columns: `duplicate_group_id`, `group_method`, `group_status`.
- Required columns:
  - `duplicate_group_id` TEXT
  - `group_method` TEXT
  - `group_status` TEXT
  - `created_at` TEXT
- Optional columns:
  - `confidence_score` REAL
  - `note` TEXT
  - `updated_at` TEXT
- Primary key: `duplicate_group_id`
- Foreign keys: none
- Unique constraints: none
- Useful indexes:
  - `idx_dup_groups_status` on `group_status`
- Example row:
  - `('dup_001','hash_exact','open',1.0,'auto-created exact hash group','2026-05-23T12:20:00Z',NULL)`
- Sensitive metadata: medium

### 11) duplicate_group_members

- Purpose: map files into duplicate groups.
- Key columns: `duplicate_group_id`, `file_id`, `member_role`.
- Required columns:
  - `duplicate_group_id` TEXT
  - `file_id` TEXT
  - `created_at` TEXT
- Optional columns:
  - `member_role` TEXT
  - `is_canonical_candidate` INTEGER
- Primary key: composite (`duplicate_group_id`, `file_id`)
- Foreign keys:
  - `duplicate_group_id` -> `duplicate_groups(duplicate_group_id)`
  - `file_id` -> `files(file_id)`
- Unique constraints: covered by PK
- Useful indexes:
  - `idx_dup_members_file` on `file_id`
- Example row:
  - `('dup_001','file_001','candidate',1,'2026-05-23T12:21:00Z')`
- Sensitive metadata: medium

### 12) audit_log

- Purpose: immutable-ish event history for ingestion, review, backup, publish, restore.
- Key columns: `audit_id`, `event_type`, `event_time`, `actor`, `target_table`, `target_id`.
- Required columns:
  - `audit_id` TEXT
  - `event_type` TEXT
  - `event_time` TEXT
  - `created_at` TEXT
- Optional columns:
  - `actor` TEXT
  - `target_table` TEXT
  - `target_id` TEXT
  - `event_status` TEXT
  - `event_payload_json` TEXT
- Primary key: `audit_id`
- Foreign keys: none (kept flexible for durability)
- Unique constraints: none
- Useful indexes:
  - `idx_audit_event_time` on `event_time`
  - `idx_audit_event_type` on `event_type`
  - `idx_audit_target` on (`target_table`, `target_id`)
- Example row:
  - `('aud_001','backup_completed','2026-05-23T12:30:00Z','codex','export_snapshots','exp_001','success','{"checksum":"ok"}','2026-05-23T12:30:00Z')`
- Sensitive metadata: high (history payload may expose context)

### 13) text_cache_index

- Purpose: pointer/index for extracted text cache (future), without storing full real text.
- Key columns: `text_index_id`, `file_id`, `cache_ref`, `extract_status`.
- Required columns:
  - `text_index_id` TEXT
  - `file_id` TEXT
  - `extract_status` TEXT
  - `created_at` TEXT
- Optional columns:
  - `cache_ref` TEXT
  - `extract_engine` TEXT
  - `last_extracted_at` TEXT
  - `updated_at` TEXT
- Primary key: `text_index_id`
- Foreign keys:
  - `file_id` -> `files(file_id)`
- Unique constraints: (`file_id`, `cache_ref`) UNIQUE
- Useful indexes:
  - `idx_text_index_status` on `extract_status`
- Example row:
  - `('txt_001','file_001','text_cache\\file_001.txt','planned','tika_future',NULL,'2026-05-23T12:40:00Z',NULL)`
- Sensitive metadata: medium/high (pointer to potential sensitive extracts)

### 14) export_snapshots

- Purpose: track generated exports, backups, and snapshots.
- Key columns: `export_id`, `export_type`, `artifact_path`, `checksum_sha256`, `export_time`.
- Required columns:
  - `export_id` TEXT
  - `export_type` TEXT
  - `artifact_path` TEXT
  - `export_time` TEXT
  - `created_at` TEXT
- Optional columns:
  - `checksum_sha256` TEXT
  - `row_count` INTEGER
  - `trigger_reason` TEXT
  - `updated_at` TEXT
- Primary key: `export_id`
- Foreign keys: none
- Unique constraints: (`export_type`, `artifact_path`) UNIQUE
- Useful indexes:
  - `idx_exports_time` on `export_time`
  - `idx_exports_type` on `export_type`
- Example row:
  - `('exp_001','db_backup','db_backups\\lifevault_20260523_123000.sqlite','abc123...','2026-05-23T12:30:00Z','2026-05-23T12:30:00Z',NULL,'before_migration')`
- Sensitive metadata: high (artifact names/paths and activity trail)

## v0 Status Fields (Proposed)

- `pod_status` values: `proposed`, `onboarded_needs_review`, `reviewed`, `archived`, `error`.
- `file_status` values: `observed`, `copied_to_pod`, `needs_review`, `approved`, `skipped`, `duplicate_candidate`, `published`, `error`.
- `review_status` values: `needs_review`, `approved`, `skipped`, `duplicate_review`, `sensitive_review`, `archive`.
- `publish_status` values: `not_published`, `publish_approved`, `published`, `verified`, `failed`.

## Privacy and Git Policy Notes

- Real operational DBs must not be committed to Git.
- Real exports/backups must not be committed to Git.
- Fake/sample DBs are allowed only when data is fully synthetic.

## Future Extensions (Not in v0)

- `people`
- `organizations`
- `events`
- `topics`
- `document_text`
- `document_chunks`
- `document_fts`
- `embeddings`
- `secrets_review`
- `retention_policy`
