# SENSITIVE_NOTE_STORAGE_LAYOUT_V0.md

## Purpose

Define the v0 storage layout contract for sensitive notes before crypto implementation.

Implementation sequencing reference:

- `docs/security/SENSITIVE_NOTE_MINIMAL_IMPLEMENTATION_PLAN_V0.md`

## Sensitive Note Package Layout

Recommended package:

```text
sensitive_note_folder/
  note.md
  protected/
    encrypted_body.lvenc
    encrypted_body_manifest.json
```

Rationale:
- metadata and `public_hint` stay searchable in `note.md`
- protected payload stays outside markdown plaintext
- encrypted payload and manifest are separately governable

## note.md Contract

Allowed in `note.md` frontmatter/body metadata:

- `title`
- `vault_item_type: note`
- `sensitivity_level: sensitive`
- `public_hint`
- `tags`
- `story`
- `lifecycle_status`
- `retention_policy_id`
- `encrypted_body_ref`
- `created_at`
- `updated_at`

Forbidden in `note.md`:

- raw SSN
- password
- API key
- recovery code
- sensitive body plaintext

## Protected Payload File

`protected/encrypted_body.lvenc` is the future encrypted payload.

v0 shape guidance:
- binary or base64 ciphertext format
- not human-readable
- never indexed as plaintext
- never printed by create/search outputs

## Encrypted Body Manifest

`protected/encrypted_body_manifest.json` may contain only non-secret metadata:

- `encrypted_body_id`
- `algorithm` (placeholder in v0)
- `created_at`
- `updated_at`
- `ciphertext_sha256`
- `size_bytes`
- `key_id` (placeholder)
- `version`

Plaintext hash note:
- avoid plaintext body hash by default in v0 due to privacy leakage risk
- if considered later, require explicit risk review and policy approval

Manifest must not include:
- plaintext sensitive body
- password
- raw key/decrypted key

## Search and Indexing Behavior

Search/index allowed:
- title
- public_hint
- story
- tags
- lifecycle
- sensitivity

Search/index forbidden:
- encrypted body plaintext
- decrypted temporary body
- raw protected payload bytes

## View/Decrypt Behavior (Future)

Future view behavior:
- requires active unlock session
- decrypt on explicit view action
- should support controlled secure-view path later
- must not write decrypted body back into `note.md`

## Update/Re-encrypt Behavior (Future)

Future update behavior:
- requires active unlock session
- decrypt protected payload for edit
- re-encrypt and replace protected payload
- update manifest metadata
- ensure no plaintext residue in normal note files

## Portable Package Behavior

Sensitive package can be copied/synced as files.

- metadata/public_hint remains searchable
- protected payload remains encrypted until unlock
- portability does not imply unlocked state portability

## Logging and Audit Rules

Never log:
- plaintext sensitive payload/body
- decrypted body
- password
- raw key/decrypted key

May log safe events:
- `sensitive_note_created`
- `sensitive_note_viewed`
- `sensitive_note_updated`
- `unlock_required`
- `unlock_expired`
- note path/id references

## Acceptance Hooks

Storage layout design should satisfy:
- `note.md` contains only safe metadata/public_hint
- `protected/` contains encrypted payload + non-secret manifest metadata
- search uses metadata/public_hint only
- no plaintext sensitive payload in note markdown
- no plaintext sensitive payload in manifest
- no plaintext sensitive payload in logs/output
- decrypt/view remains unlock-gated

Phase 0 implementation note:

- placeholder `encrypted_body.lvenc` is implemented as non-secret marker content only
- this is not encryption and must not be treated as secure storage
