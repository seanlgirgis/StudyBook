# LIFEVAULT_NOTE_FILENAME_POLICY.md

## Purpose

Define v0 filename policy for note storage identity and portability.

## 1. Identity Rule

- Filename is storage identity.
- Note title is human identity.
- Title/story/tags/vault_item_id/metadata are primary semantic identity.
- Filename must not be the only identity anchor.

## 2. Automatic Filename Generation

LifeVault generates note filenames automatically unless user explicitly requests one.

Recommended default:

- `note_<YYYYMMDD_HHMMSS>_<short_slug>.md`

Example:

- `note_20260524_142233_boa_followup.md`

## 3. Filename Stability

- If note title changes later, do not automatically rename the physical file.
- Prevent filename churn from title edits.

## 4. Filename Safety Rules

Filenames must:

- be Windows-safe
- avoid special characters
- avoid excessive length
- avoid collisions
- avoid permanent coupling to title text

Collision policy:

- append short suffix when needed

## 5. User Filename Override

If user requests explicit filename:

- sanitize filename
- refuse overwrite by default
- preserve title separately from filename
- maintain non-filename identity fields

## 6. Relationship to Notes Contracts

- `docs/architecture/LIFEVAULT_NOTE_MODEL.md`
- `docs/contracts/NOTE_AND_NOTE_FOLDER_CONTRACT.md`
- `docs/contracts/NOTE_TEMPLATE_CONTRACT.md`
