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
