# SENSITIVE_NOTE_COMMAND_CONTRACT.md

## Purpose

Define the command-level contract for future sensitive-note operations (design-only).

## Scope

- SUC_010 Secrets and Sensitive Records
- SUC_014 unlock/encryption dependency
- SUC_005 notes dependency

No implementation in this document.

Phased implementation reference:

- `docs/security/SENSITIVE_NOTE_MINIMAL_IMPLEMENTATION_PLAN_V0.md`

## Command 1: Create Sensitive Note

Concept:

```text
lifevault sensitive-note create \
  --title "..." \
  --public-hint "..." \
  --tags "..." \
  --story "..." \
  --encrypted-body "..." \
  --notes-root "..." \
  [--unlock-session-minutes 240]
```

Behavior:
- create note metadata/frontmatter with `sensitivity_level=sensitive`
- default `lifecycle_status=hot`
- do not store secret payload as plaintext note body
- encrypted payload stored via protected layout contract (`protected/encrypted_body.lvenc` + manifest)
- output only safe metadata (path, title, public_hint, timestamps)
- never print secret payload

Phase 0 implementation mapping:

- current implementation command is `notes_cli create-sensitive-phase0`
- it validates layout/leak-prevention only and does not perform real encryption

## Command 2: Search Sensitive Notes

Concept:

```text
lifevault sensitive-note search \
  --query "..." \
  --notes-root "..."
```

Behavior:
- search only: title, story, tags, public_hint, lifecycle, item_type
- do not search encrypted payload plaintext
- return metadata-only rows
- include `unlock_required=true` for sensitive items

## Command 3: View Sensitive Note

Concept:

```text
lifevault sensitive-note view \
  --note-path "..." \
  --unlock
```

Behavior:
- requires valid unlock session
- decrypt/view allowed only after unlock
- do not expose sensitive payload in unrelated commands
- explicit view action required before showing payload

## Command 4: Unlock Session

Concept:

```text
lifevault unlock --session-minutes 240
```

Behavior:
- default session window is 240 minutes (4 hours)
- password entered once per session
- session enables decrypt/view actions
- destructive operations remain separately approval-gated
- if session token file exists, it stores metadata only (no password/key/secret payload)

## Command 5: Lock Session

Concept:

```text
lifevault lock
```

Behavior:
- immediately ends active unlock session
- future decrypt/view requires unlock again

## Safety Rules

- normal note workflow remains unaffected
- sensitive metadata remains searchable
- sensitive payload/body remains protected
- no plaintext secret in normal note body
- no AI processing of encrypted payload unless explicitly unlocked and approved later
- no cloud sync of plaintext sensitive payload
- no automatic delete behavior
- no full DB encryption claim in this phase
- password/key loss may cause irreversible data loss

## References

- `docs/security/LIFEVAULT_ENCRYPTION_V0_DESIGN.md`
- `docs/security/LIFEVAULT_SENSITIVE_NOTE_V0_CONTRACT.md`
- `docs/security/LIFEVAULT_UNLOCK_SESSION_POLICY.md`
- `docs/security/LIFEVAULT_UNLOCK_SESSION_STATE_CONTRACT.md`
- `docs/security/SENSITIVE_NOTE_STORAGE_LAYOUT_V0.md`
