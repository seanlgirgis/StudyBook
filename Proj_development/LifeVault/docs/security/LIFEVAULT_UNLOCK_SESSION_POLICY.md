# LIFEVAULT_UNLOCK_SESSION_POLICY.md

## Purpose

Define unlock session behavior for sensitive operations.

## Default Session

- default unlock window: `4 hours`
- configurable in future implementation

## Session Behavior

- unlock enables decrypt/view for sensitive payloads
- on timeout, decrypt/view requires unlock again
- lock state should not hide searchable safe metadata
- session token/state (if persisted) must remain metadata-only

## Session Scope

v0 intended scope:
- sensitive notes (`encrypted_body`)

Future scope:
- sensitive files
- secure view workflows
- controlled decrypt/export lanes

## Security Notes

- shorter sessions reduce exposure risk
- longer sessions improve usability but increase risk window
- session events should be auditable in future implementation
- secrets/keys must never be logged

## Recovery Risk Note

- password/key loss can make data unrecoverable
- recovery plan must be documented before broad rollout

Related command contract:

- `docs/contracts/SENSITIVE_NOTE_COMMAND_CONTRACT.md`
- `docs/security/LIFEVAULT_UNLOCK_SESSION_STATE_CONTRACT.md`
