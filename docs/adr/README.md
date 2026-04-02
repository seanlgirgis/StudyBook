# Architecture Decision Records (ADR)

This folder is the architecture decision source of truth.

## Purpose

- Preserve major design decisions as durable, auditable records.
- Separate design intent from execution notes.
- Make reasoning reviewable across machines and sessions.

## Scope

Write an ADR when a decision changes architecture, control policy, security posture, portability model, or long-term operating behavior.

## Naming

- File format: `ADR-0001-short-kebab-title.md`
- Index file: `docs/adr/ADR-INDEX.md`

## Lifecycle

- `Proposed`
- `Accepted`
- `Superseded`
- `Deprecated`

## Immutability Rule

- Accepted ADRs are immutable in intent.
- Do not rewrite history in place.
- If the decision changes, create a new ADR and mark the old one `Superseded`.
- Minor typo fixes are allowed if intent is unchanged.

## Required Sections

- Title
- Status
- Date
- Decision Makers
- Context
- Decision
- Consequences
- Alternatives Considered
- Links

## Workflow

1. Create ADR draft from template.
2. Review and approve.
3. Mark `Accepted`.
4. Add entry in `ADR-INDEX.md`.
5. Add cross-reference in `agents/shared/decision_log.md`.

Optional helper:

```powershell
.\scripts\adr\new_adr.ps1 -Title "Your decision title" -TaskId TB-YYYYMMDD-XX -DecisionId DEC-###
```
