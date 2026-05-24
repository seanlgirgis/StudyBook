# NOTE_TEMPLATE_CONTRACT.md

## Purpose

Define managed note template contracts for SUC_005 Note and Knowledge Memory v0 design.

## Template Location

- `D:\AI_Lab\LifeVault\note_templates\`

Templates are managed LifeVault records/files, not loose ad hoc files.

## Template Contract Fields

- `template_id`
- `template_name`
- `template_type`
- `description`
- `version`
- `status` (`active` / `retired`)
- `default_frontmatter`
- `body_skeleton`
- `created_at`
- `updated_at`

## Starter Templates

- `quick_note`
- `project_note`
- `decision_note`
- `task_note`
- `sensitive_note`
- `email_summary_note`
- `meeting_note`
- `study_note`
- `physical_item_note`

## Frontmatter Contract (Template-Oriented)

Templates should include frontmatter fields such as:

- `title`
- `vault_item_type`
- `template_id`
- `template_version`
- `lifecycle_status`
- `sensitivity_level`
- `retention_policy_id`
- `tags`
- `story`
- `related_vault_item_id`
- `created_at`

## Template Evolution Rules

- Templates may be updated over time.
- Existing notes created from older templates must remain valid/editable.
- Notes should record `template_id` and `template_version` used at creation.
- After creation, notes are editable independent artifacts.

## Sensitive Template Pattern

`sensitive_note` should support:

- `public_hint` (searchable safe descriptor)
- `encrypted_body` (future protected payload)

Encryption/decryption remains deferred in this design phase.
