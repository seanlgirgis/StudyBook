# LIFEVAULT_VAULT_ITEM_MODEL.md

## Purpose

Define the 1000-foot object model where LifeVault is not only folder ingestion; it is a broad personal vault system centered on intentional items.

## Core Concept: `vault_item`

A `vault_item` is the human-level thing intentionally stored.

Supported `vault_item_type` values:

- `folder`
- `file`
- `note`
- `note_folder`
- `url`
- `code_folder`
- `image_collection`
- `binary_archive`
- `media_collection`
- `contact`
- `email_import_source`
- `email_thread`
- `physical_item`
- `physical_container`
- `job_record`
- `prompt_record`
- `project`
- `task_group`
- `task`
- `secret_reference`

## Membership First, Promotion Optional

- Files inside folder-backed `vault_item`s are members first.
- Members are not automatically competing top-level `vault_item`s.
- Any member can later be promoted into its own `vault_item` when needed.

## Avoid Single-Tree Lock-In

Do not force all `vault_item`s into one strict parent-child tree as the core model.

Use:

- `vault_item` as intentional saved object
- member records for folder-backed contents
- relationship/link records for cross-item connections
- physical containment modeled separately for physical inventory

## Copy-First Principle

LifeVault is copy-first, not pointer-first.

When the same file belongs to multiple stories/items:

- copy it intentionally
- track duplicate candidates/relationships
- track intentional duplicates
- track duplicate storage cost
- track cleanup candidates

## Duplicate Rules

Across different `vault_item`s:

- warning/tracking by default
- may be intentional
- never auto-delete

Inside same folder-backed `vault_item`:

- stronger cleanup candidate
- still explicit human approval required

## Lifecycle States

- `hot`
- `warm`
- `cold`
- `archive`
- `quarantine`

Definitions:

- `cold`: searchable memory, default for most stored items
- `warm`: maintenance/work queue visibility
- `hot`: currently active/priority
- `archive`: keep but hide from normal work
- `quarantine`: do not use unless reviewed

Defaults:

- ordinary `vault_item` -> `cold`
- note -> `hot`
- system maintenance task -> `warm`

## Notes as First-Class Items

Notes are first-class `vault_item`s and physical Markdown files.

Defaults:

- `vault_item_type=note`
- `lifecycle_status=hot`
- editable Markdown file
- reindex after edits

Note folders are supported and can apply shared policy.

Portable note package shape:

```text
note_folder/
  note.md
  assets/
  note_manifest.json
```

Markdown should use relative asset links for portability.

Detailed note model/contracts:

- `docs/architecture/LIFEVAULT_NOTE_MODEL.md`
- `docs/contracts/NOTE_AND_NOTE_FOLDER_CONTRACT.md`
- `docs/contracts/NOTE_ASSET_STORE_CONTRACT.md`

## Notes Asset Store

Global notes asset store:

- `D:\AI_Lab\LifeVault\notes_assets\`

Rules:

- deduplicate by SHA across notes
- content-addressed names
- original filename stored as metadata only
- append-only by default
- no normal delete/update/rename
- warn on large images and allow derivatives later

## Physical Inventory Capability

Physical inventory is a native capability.

Types:

- `physical_container`
- `physical_item`

Containment recursion exists only inside physical inventory.

Example:

- Room 10 -> Box 5 -> Allen key

## Contacts and Email

Contacts:

- DB-first ingest from exports
- fast ingest first, cleanup/merge later

Email/mbox:

- mbox is import source, not always final value object
- parse to messages/threads/contacts/attachments
- dedupe attachments
- promote important threads to `email_thread` items

## Task/Project/Maintenance Model

Hierarchy:

- Project -> Task Group -> Task

Tasks are actionable units and are also `vault_item`s.

Maintenance queue examples:

- duplicate cleanup
- contact merge
- email pruning
- attachment dedup review
- sensitivity review
- encryption pending
- backup verification
- cold storage review

Task fields:

- `intake_date` required
- `due_date` optional
- `age_days` computed

Detailed task/project model reference:

- `docs/architecture/LIFEVAULT_TASK_PROJECT_MODEL.md`

## Multi-Destination Storage Vision

Track eventual placements across:

- local vault
- OneDrive account 1
- OneDrive account 2
- backup drives/folders
- encrypted vault
- cold/archive storage
- quarantine

LifeVault should manage final location knowledge, not human memory alone.
