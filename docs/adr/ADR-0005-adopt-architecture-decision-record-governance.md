# ADR-0005: Adopt Architecture Decision Record Governance

## Status
- Accepted

## Date
- 2026-04-01

## Decision Makers
- Project owner
- Code agent execution layer

## Context
- Prior decisions were tracked mainly in `agents/shared/decision_log.md`.
- A stronger architecture audit trail is required with immutable records and supersession flow.

## Decision
- Adopt ADR governance under `docs/adr/`.
- Use `docs/adr/ADR-INDEX.md` as canonical registry.
- Keep `agents/shared/decision_log.md` as operational mirror linking to ADRs.
- Add helper command `scripts/adr/new_adr.ps1` for consistent ADR creation.

## Consequences
- Positive:
- Architecture decisions become reviewable, durable, and immutable by policy.
- Supersession paths are explicit.
- Negative:
- Slightly more process overhead for architecture changes.
- Neutral:
- Two related records now exist (ADR and decision log) and must stay linked.

## Alternatives Considered
- Keep only operational decision log without ADRs.
- Track architecture decisions in ad hoc markdown notes.

## Supersedes
- none

## Superseded By
- none

## Links
- Task: `TB-20260401-06`
- Decision Log: `agents/shared/decision_log.md`
- Index: `docs/adr/ADR-INDEX.md`
