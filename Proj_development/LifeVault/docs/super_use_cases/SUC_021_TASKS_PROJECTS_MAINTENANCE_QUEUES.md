# SUC_021_TASKS_PROJECTS_MAINTENANCE_QUEUES.md

## Purpose

Define SUC_021 as the project-control capability that manages planning and operational work through Projects, Task Groups, and Tasks.

## Scope (v0 Design)

- Model task hierarchy and status/priority/date semantics.
- Model maintenance queues as system-generated task groups.
- Keep execution logic gated in existing scripts/workflows.

## Core Model

Hierarchy:

- Project -> Task Group -> Task

Task is the final actionable unit.

All three are valid `vault_item_type` values in v0 design:

- `project`
- `task_group`
- `task`

## Inputs

- operator goals and roadmap deltas
- capability state from super-use-case tracker
- system-generated maintenance observations

## Outputs

- structured task records
- queue states and priorities
- task notes paths
- project progress visibility

## Maintenance Queue Examples

- duplicate_review_queue
- contact_merge_queue
- email_prune_queue
- attachment_dedup_queue
- sensitivity_review_queue
- encryption_pending_queue
- backup_verify_queue
- cold_storage_review_queue
- note_reindex_queue
- physical_inventory_check_queue

## Defaults

- lifecycle default for project/task_group/task: `warm`
- task `intake_date` required
- task `due_date` optional and null by default for maintenance

## Safety

- Task records must not directly trigger destructive file actions.
- Execution still occurs only through explicit script/workflow approval gates.

## Relationship to Other Super Use Cases

- SUC_021 orchestrates and tracks progress across all SUCs.
- SUC_006 remains the first proven vertical slice and supplies practical maintenance queues.
- SUC_015 UI will later surface SUC_021 as operational command center.

## Initial Example

Project:

- `LifeVault Buildout`

Task groups:

- Foundation model
- Notes v0
- Encryption v0
- Streamlit dashboard
- Email/contacts planning
- Maintenance/reporting

Seed board reference:

- `docs/tasks/LIFEVAULT_PROJECT_TASK_SEED.md`
