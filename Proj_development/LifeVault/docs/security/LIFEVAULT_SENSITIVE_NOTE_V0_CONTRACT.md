# LIFEVAULT_SENSITIVE_NOTE_V0_CONTRACT.md

## Purpose

Define the sensitive-note contract for v0 encryption phase planning.

## Sensitive Note Structure

Sensitive notes use:

- `public_hint`
- `encrypted_body`
- protected storage layout (`note.md` + `protected/encrypted_body.lvenc` + manifest)

`public_hint`:
- visible
- searchable
- safe descriptor only

`encrypted_body`:
- protected payload
- not searchable as plaintext
- viewable only after unlock session

## Search Rules

Search may match sensitive notes by:
- title
- tags
- story
- public_hint
- lifecycle status
- item type

Search must not expose `encrypted_body`.

## Metadata Defaults

- `vault_item_type = note`
- `lifecycle_status = hot` (unless changed)
- `sensitivity_level = sensitive`
- `retention_policy_id = default_lifetime_user_use`

## Viewing Rules

- unlock session required to decrypt/view protected payload
- timeout ends protected-view access
- metadata remains searchable while locked

## Non-Goals

- no file-wide encryption in this v0 note contract
- no DB-wide encryption claim
- no cloud sync behavior in this contract

## Acceptance Checklist

- sensitive note metadata is searchable
- encrypted payload is not plaintext-searchable
- unlock required before decrypt/view
- unlock timeout is enforced by policy
- normal notes remain unaffected

Command contract reference:

- `docs/contracts/SENSITIVE_NOTE_COMMAND_CONTRACT.md`
- `docs/security/SENSITIVE_NOTE_STORAGE_LAYOUT_V0.md`
