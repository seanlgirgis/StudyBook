# SUC_010_ACCEPTANCE_CHECKLIST.md

## Purpose

Acceptance checklist for SUC_010 sensitive-note v0 behavior (design target).

## Preconditions

- sensitive-note command contract is approved
- unlock session policy is approved
- minimal phased plan is approved (`SENSITIVE_NOTE_MINIMAL_IMPLEMENTATION_PLAN_V0.md`)
- no real secrets used in tests

## Checklist

- [ ] Sensitive note can be created without leaking payload in logs/output.
- [ ] Sensitive note metadata includes `sensitivity_level=sensitive`.
- [ ] `note.md` contains safe metadata/public_hint only.
- [ ] Protected payload placeholder exists under `protected/` layout.
- [ ] `public_hint` is searchable.
- [ ] Encrypted payload is not plaintext-searchable.
- [ ] Search output contains metadata only.
- [ ] Search marks sensitive rows with `unlock_required=true`.
- [ ] View requires unlock session.
- [ ] Unlock session default is 4 hours (240 minutes).
- [ ] Manual `lock` concept is supported and ends session immediately.
- [ ] Password is entered once per session and is not stored in plaintext.
- [ ] Session token/state stores no raw key material.
- [ ] Session expiration invalidates sensitive view until unlock again.
- [ ] Audit events avoid secret payload/body values.
- [ ] Dangerous sensitive actions still require explicit approval gates while unlocked.
- [ ] Normal note create/search workflow remains unaffected.
- [ ] No real cloud sync is performed in this phase.
- [ ] No destructive behavior (delete/move/rename) is introduced.
- [ ] No full DB/file encryption claim is made for v0.
- [ ] No plaintext sensitive content appears in manifest metadata.

Phase 0 implementation status:

- [x] Layout-only sensitive package creation is implemented (`create-sensitive-phase0`).

## Safety Notes

- encryption is not backup
- password/key loss can cause data loss
- sensitive payload should not be processed by AI unless explicitly unlocked and approved
