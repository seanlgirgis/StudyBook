# NOTE_AND_NOTE_FOLDER_CONTRACT.md

## Purpose

Define note and note-folder contract shapes for SUC_005 design.

## Note Contract (v0 Design)

Required conceptual fields:

- `vault_item_id`
- `vault_item_type` = `note`
- `title`
- `lifecycle_status` (default `hot`)
- `retention_policy` (default `default_lifetime_user_use`)
- `sensitivity_level` (default `normal`)
- `public_hint` (optional but recommended)
- `story` (optional)
- `tags` (optional)
- `note_path` (physical markdown path)
- `filename_generated` (boolean)
- `template_id` (optional)
- `template_version` (optional)
- `created_at`
- `updated_at`

Physical file default policy:

- `note_<YYYYMMDD_HHMMSS>_<short_slug>.md`
- user override allowed with sanitization + no-overwrite enforcement

## Note Folder Contract (v0 Design)

Required conceptual fields:

- `vault_item_id`
- `vault_item_type` = `note_folder`
- `title`
- `lifecycle_status`
- `retention_policy`
- `sensitivity_level`
- `folder_path`
- `created_at`
- `updated_at`

Managed folder layout for v0 implementation:

- `note_folder_<YYYYMMDD_HHMMSS>_<short_slug>/`
- `_folder_manifest.json`
- `README.md`
- `notes/`

`README.md` frontmatter fields:

- `title`
- `vault_item_type: note_folder`
- `lifecycle_status: hot`
- `sensitivity_level: normal`
- `retention_policy_id: default_lifetime_user_use`
- `tags`
- `story`
- `created_at`

## Sensitive Note Pattern (Design-Only)

- `public_hint`: searchable metadata-safe summary
- `encrypted_body`: future protected payload field

No encryption implementation in this contract phase.

## Portable Retrieval Package Contract

```text
note_package/
  note.md
  assets/
  note_manifest.json
```

Rules:

- use relative links in markdown: `assets/<asset_filename>`
- avoid absolute machine paths in exported package
- package should open on another machine without path rewrite

## Reindex Expectation

Notes may be edited directly outside LifeVault.
LifeVault should later reindex note metadata/body according to approved indexing workflows.

## Template Tracking Rule

Notes should record the creating template (`template_id`, `template_version`) when applicable, but remain independently editable after creation.
