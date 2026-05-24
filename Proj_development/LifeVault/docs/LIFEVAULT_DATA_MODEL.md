# LIFEVAULT_DATA_MODEL.md

## Core Entities

- `sources`: origin systems/locations for ingested material.
- `pods`: onboarding pod metadata with story/context.
- `files`: content identity records.
- `file_instances`: observed/copied path instances for files.
- `vault_locations`: approved final vault destinations.
- `tags` and `file_tags`: controlled labels and mappings.
- `review_decisions`: human review and publish decisions.
- `duplicate_groups` and `duplicate_group_members`: duplicate analysis structures.
- `audit_log`: immutable-ish operational event history.
- `text_cache_index`: extracted text pointer placeholders (no full text in v0).
- `export_snapshots`: backup/export/snapshot artifact records.

## Schema Reference

- Detailed table-by-table v0 design is defined in `docs/LIFEVAULT_SCHEMA_V0_PLAN.md`.
- Metadata-based sensitivity and content-based sensitivity are separate lifecycle stages.
- Full extracted text is not part of UC_001/UC_002; content sensitivity workflows require explicit approval and controlled storage policy.
- UC_004 indexing behavior and table-mapping workflow are defined in `docs/use_cases/UC_004_INDEX_POD_TO_DATABASE_WORKFLOW_SPEC.md`.
- UC_005 search reads these indexed metadata entities only; no document-content hydration is required in v0.
- UC_006 review updates are instance/path-aware at workflow level and stored in review metadata without file operations.
- UC_006B readiness reporting classifies each file instance into publish-ready or blocked states without writing DB rows.
- UC_007 updates publish status only for successfully copied ready-to-publish items and records audit events.
- UC_008 verifies source/destination size+SHA256 from UC_007 manifest and updates publish status to `verified` only on match.
- UC_009 (future implementation) will produce quarantine manifests and audit entries; v0 policy is quarantine-only, not permanent deletion.
- UC_009 now records quarantine-manifest outcomes and audit events in temp-only implementation; no permanent delete behavior exists in v0.
- Current v0 duplicate membership is file-level (`duplicate_group_members.file_id`), while duplicate candidates originate from file-instance/path observations in pod manifests.
- v0 indexing should preserve instance-vs-file counts in duplicate group notes for review clarity; future schema may add explicit instance-level duplicate membership.
