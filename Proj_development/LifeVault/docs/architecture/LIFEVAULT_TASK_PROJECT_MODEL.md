# LIFEVAULT_TASK_PROJECT_MODEL.md

## Purpose

Define Tasks / Projects / Maintenance Queues v0 as the project-control layer for LifeVault capability delivery and operations.

## 1. Task Hierarchy

LifeVault supports:

- Project
  - Task Group
    - Task

Task is the final actionable unit.

## 2. `vault_item` Relationship

For v0 design, all three are valid `vault_item_type` values:

- `project`
- `task_group`
- `task`

Reason: each must support title, story, lifecycle status, retention policy, notes, search, and relationships.

## 3. Maintenance Queues

Maintenance queues are system-generated task groups.

Examples:

- `duplicate_review_queue`
- `contact_merge_queue`
- `email_prune_queue`
- `attachment_dedup_queue`
- `sensitivity_review_queue`
- `encryption_pending_queue`
- `backup_verify_queue`
- `cold_storage_review_queue`
- `note_reindex_queue`
- `physical_inventory_check_queue`

## 4. Minimal Task Model (v0 Design)

- `task_id`
- `vault_item_id`
- `project_id`
- `task_group_id`
- `title`
- `description`
- `task_type`
- `status`
- `priority`
- `intake_date`
- `due_date`
- `completed_at`
- `age_days` (calculated from `intake_date`)
- `source_system`
- `related_vault_item_id`
- `related_group_id`
- `notes_path` (optional)
- `created_at`
- `updated_at`

## 5. Status Values

- `open`
- `in_progress`
- `blocked`
- `done`
- `dismissed`
- `deferred`

## 6. Priority Values

- `P0`
- `P1`
- `P2`
- `P3`

## 7. Date Rules

- Every task requires `intake_date`.
- `due_date` is optional.
- Maintenance tasks default `due_date = null`.
- `age_days` is computed.

## 8. Task Notes

Each task may have an editable Markdown note.

Example path:

- `D:\AI_Lab\LifeVault\tasks_hot\<project_slug>\<task_group_slug>\<task_slug>\task.md`

Design pattern:

- DB tracks structured task state.
- Markdown stores rich decisions, commands, context, and operator/AI reasoning.

## 9. Lifecycle Defaults

- `project` default lifecycle: `warm`
- `task_group` default lifecycle: `warm`
- `task` default lifecycle: `warm`

Manual overrides:

- active work may be set `hot`
- completed/dismissed work may be transitioned to `cold`/`archive`

## 10. Role in Cyclical Development

LifeVault is built cyclically, not by perfecting one lane forever.

Tasks are the control layer to compare:

- current capability state
- target capability state
- next implementation bite

## 11. First Example Project (v0 Planning)

Project:

- `LifeVault Buildout`

Task Groups:

- `Foundation model`
- `Notes v0`
- `Encryption v0`
- `Streamlit dashboard`
- `Email/contacts planning`
- `Maintenance/reporting`

Example Tasks:

- Document vault_item model
- Document policy model
- Design note v0
- Design task model
- Design sensitive unlock model
- Build read-only dashboard

Seed board reference:

- `docs/tasks/LIFEVAULT_PROJECT_TASK_SEED.md`

## 12. Safety

- Tasks recommend work; they do not execute destructive actions.
- Scripts execute only with explicit workflow approval gates.
- No automatic delete/move/rename should be triggered by task creation alone.
