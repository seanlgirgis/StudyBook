# ADR-0002: Adopt Approval Matrix and Command Allowlist

## Status
- Accepted

## Date
- 2026-04-01

## Decision Makers
- Project owner
- Code agent execution layer

## Context
- Trust needed explicit boundaries for what the agent can do autonomously.
- Implicit policy in prompts was hard to audit and inconsistent across sessions.

## Decision
- Create and maintain:
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- Enforce approval for destructive, credential-sensitive, and external-write actions.

## Consequences
- Positive:
- Clear trust boundaries and predictable escalation behavior.
- Easier review/audit of safety decisions.
- Negative:
- Initial policy tuning is required as workflows evolve.
- Neutral:
- More governance files to maintain.

## Alternatives Considered
- Keep approval rules embedded only in protocol text.
- Use ad hoc chat approvals without persistent policy files.

## Supersedes
- none

## Superseded By
- none

## Links
- Task: `TB-20260401-03`
- Decision Log: `agents/shared/decision_log.md`
- Policy files: `agents/shared/approval_matrix.md`, `agents/shared/command_allowlist.md`
