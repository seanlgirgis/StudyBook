# LIFEVAULT_UNLOCK_SESSION_STATE_CONTRACT.md

## Purpose

Define minimal unlock/lock session-state rules before crypto implementation.

## Unlock Session Goal

- user enters master password once per unlock session
- default duration is 240 minutes (4 hours)
- decrypt/view operations may proceed while session is valid
- user should not re-enter password for each normal sensitive view during valid session

## Password and Key Safety

Never store in token/session files:

- master password
- plaintext password
- raw decrypted master key
- plaintext sensitive payload (`encrypted_body` value)

Related protected storage:

- `docs/security/SENSITIVE_NOTE_STORAGE_LAYOUT_V0.md`

## Session State Options (Design Comparison)

- process-local memory only
  - strongest non-persistence posture
  - session dies with process restart
- local session token metadata file
  - enables state continuity/inspection
  - must store metadata only, never secrets
- OS keychain later
  - better secret handling if platform integration is added
- encrypted key bundle later
  - portability path for multi-machine workflows with explicit controls

v0 preferred direction:

- decrypted key material stays process-local/in memory (when implemented)
- optional token file stores metadata only

## Session Token File (Metadata Only)

If a local token file exists, allowed fields:

- `session_id`
- `created_at`
- `unlocked_until`
- `machine_id` or local context marker
- `scope`
- `status`

Forbidden fields:

- password/plaintext password
- raw key/decrypted key bytes
- sensitive payload/body data

Suggested location:

- `D:\AI_Lab\LifeVault\security\sessions\`
- or local temp/session path if safer for implementation context

## Expiration Semantics

Session is valid only when all are true:

- current time is before `unlocked_until`
- `status` is `active`
- machine/context marker matches expected local marker (if used)

After expiration:

- decrypt/view requires unlock again

## Manual Lock Semantics

Manual lock should:

- mark token inactive or remove token file
- clear in-memory key material (when implementation exists)
- require unlock for future sensitive views

## Audit Event Concepts

Future audit events:

- `unlock_started`
- `unlock_expired`
- `manual_lock`
- `sensitive_note_viewed`
- `sensitive_note_created`
- `sensitive_note_update_encrypted`

Audit events must never include secret payload/body.

## Dangerous Actions During Unlocked Session

Even when unlocked, explicit approval is still required for:

- exporting plaintext sensitive payload
- deleting encrypted payload
- changing key/password configuration
- uploading plaintext sensitive content to cloud
- disabling encryption protections

## Multi-Machine Behavior

- unlock session is local to one machine/session context
- unlocking on one machine does not unlock other machines
- portable encrypted key-bundle behavior is deferred to future design

## Acceptance Contract Hooks

Session-state design must support:

- password entered once per session
- no password stored
- no raw key stored in token metadata
- expiration enforcement
- manual lock invalidation
- secret-safe audit event model
- approval gates for dangerous actions even during unlocked window
