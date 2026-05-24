# LIFEVAULT_NOTE_MODEL.md

## Purpose

Define the v0 note model as part of SUC_005 Notes and Knowledge Memory.

## 1. Notes as First-Class Vault Items

Notes are first-class `vault_item`s with:

- `vault_item_type=note`
- portable physical markdown representation
- searchable metadata and content (normal notes)

Note folders are also first-class:

- `vault_item_type=note_folder`

## 2. Physical Representation

Default note file:

- generated filename policy (default):
  - `note_<YYYYMMDD_HHMMSS>_<short_slug>.md`

Rationale:

- portable
- editable in many tools
- diff-friendly
- searchable and convertible later

Title/file rule:

- note title is human identity
- filename is storage identity
- title changes do not auto-rename files

## 3. Note Defaults

- `lifecycle_status = hot`
- `retention_policy = default_lifetime_user_use`
- `sensitivity_level = normal`

## 4. Note Folder Semantics

A note folder groups notes and may apply shared lifecycle/policy metadata.

Implemented note_folder v0 thin slice:

- create managed folder layout:
  - `_folder_manifest.json`
  - `README.md`
  - `notes/`
- create notes directly inside `<note_folder>/notes`
- list note folders with note counts
- search includes nested folder notes and reports `parent_note_folder`

## 5. Sensitive Note Pattern (Design-Only)

Use two-part note pattern:

- `public_hint`: searchable safe descriptor
- `encrypted_body`: protected payload for future encryption phase

Encryption/decryption remains deferred in this v0 design.

## 6. Search Model (v0)

Searchable fields:

- title
- public_hint
- tags
- story
- note body (normal notes)
- lifecycle status
- sensitivity
- related project/task/vault_item links

Deferred:

- encrypted body search until explicit future unlock/index policy.

Implemented Notes v0 thin slice:

- create markdown notes with managed filename policy
- parse frontmatter/body
- search by title/story/tags/body within configured notes root
- no DB writes in this bite
- no assets or encryption in this bite

## 7. Task Note Reuse

Task notes follow the same markdown-first principles, but remain tied to task records in SUC_021.

## References

- `docs/contracts/NOTE_AND_NOTE_FOLDER_CONTRACT.md`
- `docs/contracts/NOTE_ASSET_STORE_CONTRACT.md`
- `docs/contracts/NOTE_TEMPLATE_CONTRACT.md`
- `docs/architecture/LIFEVAULT_NOTE_FILENAME_POLICY.md`
- `docs/super_use_cases/SUC_005_NOTES_AND_KNOWLEDGE_MEMORY.md`
