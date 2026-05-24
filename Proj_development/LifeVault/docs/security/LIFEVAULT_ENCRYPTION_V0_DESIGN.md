# LIFEVAULT_ENCRYPTION_V0_DESIGN.md

## Purpose

Define v0 encryption direction for LifeVault sensitive records before implementation.

## Scope

- SUC_010 Secrets and Sensitive Records
- SUC_014 Encryption, Decryption, and Secure View
- SUC_005 sensitive note dependency

Design-only in this bite.

## Sensitivity Model

- `normal`
- `sensitive`

`normal`:
- plaintext local storage allowed
- body searchable

`sensitive`:
- searchable metadata/public_hint allowed
- payload/body must be encrypted
- decrypt/view requires unlock session

## v0 Sensitive Target

First implementation target later is sensitive notes only:
- create sensitive note with `public_hint` + `encrypted_body`
- search by metadata/public_hint
- decrypt/view only after unlock
- store payload outside markdown plaintext using protected layout contract

Out of scope for v0 implementation target:
- full file encryption
- DB-wide encryption
- OneDrive/cloud encryption sync

## Key/Password Direction

- use master-password unlock concept
- do not require manual secret key file shuffling in v0 design
- implementation should use modern key derivation later
- key-loss/recovery risk must be explicit in UX and policy docs
- session-state token (if used) must be metadata-only and secret-free

## At-Rest and Travel Target

Sensitive payload should eventually be:
- encrypted at rest
- encrypted in travel/cloud
- decrypted only into controlled secure-use area

## Safety Limits

- encryption is not backup
- password/key loss can cause permanent loss
- avoid storing critical secrets only in experimental flows until restore is proven
- no auto delete behavior
- no plaintext secret in normal note body
- no AI processing of encrypted payload unless explicitly unlocked/approved

## References

- `docs/security/LIFEVAULT_SENSITIVE_NOTE_V0_CONTRACT.md`
- `docs/security/LIFEVAULT_UNLOCK_SESSION_POLICY.md`
- `docs/security/LIFEVAULT_UNLOCK_SESSION_STATE_CONTRACT.md`
- `docs/security/SENSITIVE_NOTE_STORAGE_LAYOUT_V0.md`
- `docs/security/SENSITIVE_NOTE_MINIMAL_IMPLEMENTATION_PLAN_V0.md`
- `docs/security/LIFEVAULT_SECURITY_BACKLOG.md`
- `docs/contracts/SENSITIVE_NOTE_COMMAND_CONTRACT.md`
- `docs/super_use_cases/SUC_010_ACCEPTANCE_CHECKLIST.md`
