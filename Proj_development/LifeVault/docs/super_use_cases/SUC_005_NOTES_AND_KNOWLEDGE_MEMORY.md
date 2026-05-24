# SUC_005_NOTES_AND_KNOWLEDGE_MEMORY.md

## Purpose

Define SUC_005 as the note-centric knowledge memory capability, where notes and note folders are first-class vault items with portable markdown-backed storage.

## Scope (v0 Contract Design)

- Note and note-folder item semantics.
- Physical markdown note representation.
- Global note asset store rules.
- Note template management and template-version tracking.
- Note filename generation policy and safe override behavior.
- Portable retrieval package contract.
- Search boundaries for normal vs sensitive notes.

## Core Decisions

1. Notes are first-class `vault_item`s.
2. `note` and `note_folder` are valid `vault_item_type`s.
3. Notes are physical markdown files with generated safe filenames.
4. Notes default to `lifecycle_status=hot`.
5. Note folders can apply shared lifecycle/policy.
6. Sensitive note pattern uses `public_hint` + future `encrypted_body`.

## Inputs

- note title/content/story/tags
- optional note folder target
- optional assets/images
- optional related vault item/project/task links

## Outputs

- note vault item metadata
- physical markdown note file
- optional asset references
- optional portable note package export

## Search Intent (v0)

Search should support:

- title
- public_hint
- tags
- story
- note body for normal notes
- lifecycle status
- sensitivity
- related project/task/vault_item links

Sensitive encrypted bodies are deferred and not searchable until explicit future rules.

## Related Contracts

- `docs/contracts/NOTE_AND_NOTE_FOLDER_CONTRACT.md`
- `docs/contracts/NOTE_ASSET_STORE_CONTRACT.md`
- `docs/contracts/NOTE_TEMPLATE_CONTRACT.md`
- `docs/architecture/LIFEVAULT_NOTE_MODEL.md`
- `docs/architecture/LIFEVAULT_NOTE_FILENAME_POLICY.md`

## Safety

- design-only in this phase; no implementation side effects
- no encryption implementation in this bite
- no cloud sync/rclone usage in this bite

## Sensitive Notes Dependency

SUC_005 depends on SUC_010/SUC_014 policy for sensitive-note unlock behavior:

- sensitive notes keep metadata/public_hint searchable
- sensitive payload/body uses `encrypted_body` model
- decrypt/view requires unlock session (default 4 hours policy)

References:

- `docs/security/LIFEVAULT_ENCRYPTION_V0_DESIGN.md`
- `docs/security/LIFEVAULT_SENSITIVE_NOTE_V0_CONTRACT.md`
- `docs/security/LIFEVAULT_UNLOCK_SESSION_POLICY.md`
