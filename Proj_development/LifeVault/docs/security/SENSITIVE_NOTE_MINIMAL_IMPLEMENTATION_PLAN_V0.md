# SENSITIVE_NOTE_MINIMAL_IMPLEMENTATION_PLAN_V0.md

## Purpose

Define the smallest safe phased path to implement sensitive notes without over-claiming encryption maturity.

## Scope

- SUC_010 Secrets and Sensitive Records
- SUC_014 Encryption/Unlock
- SUC_005 note dependency

Design/planning only.

## Phase 0: Non-Crypto Layout Validation (First Recommended Implementation)

Deliverables:
- fake/demo sensitive note package only
- no real secrets
- no crypto claim

Package shape:

```text
sensitive_note_folder/
  note.md
  protected/
    encrypted_body.lvenc
    encrypted_body_manifest.json
```

Rules:
- `note.md` includes safe metadata + `public_hint` only
- `encrypted_body.lvenc` uses non-secret placeholder ciphertext text/blob
- manifest includes non-secret metadata only
- validate search safety and no plaintext leakage

## Phase 1: Toy Local Encryption Spike (Experimental)

- test-only non-secret strings
- clearly marked non-production
- prove round-trip concept only
- no real secrets
- no production security claim

## Phase 2: Real Encryption Candidate (Review-Gated)

Before coding:
- dependency/security review required
- library vetting required

Target properties:
- key derivation
- salt
- nonce/IV
- authenticated encryption
- recovery-loss warnings

## Phase 3: Unlock/Session Integration

- password entered once per session
- default session 240 minutes
- no password/raw key in session files
- session-state follows metadata-only token contract

## Phase 4: Sensitive Note CLI Surface

- `sensitive-note create/search/view`
- search metadata/public_hint only
- view requires unlock
- no secret body in normal output/logs

## Acceptance Gates

- normal notes unaffected
- sensitive package created without plaintext secret body in `note.md`
- search finds `public_hint`
- search does not find protected plaintext
- manifest contains no plaintext secret
- create/search output never prints encrypted body or plaintext secret
- tests use fake values only
- no real secrets in tests
- no cloud sync
- no DB migration unless separately approved
- no destructive actions

## Testing Plan

All tests use `tmp_path` only.

Required checks:
- inspect generated files for forbidden plaintext marker
- public_hint search succeeds
- protected fake-body plaintext search fails
- manifest contains ciphertext hash only
- existing normal-note tests remain green

## Safety Warnings

- Phase 0 is not encryption
- placeholder `encrypted_body.lvenc` is not secure
- do not store real secrets until real crypto phase is implemented and reviewed

## Phase Status

- Phase 0: implemented (layout-only, no real encryption)
- Phase 1+: deferred
