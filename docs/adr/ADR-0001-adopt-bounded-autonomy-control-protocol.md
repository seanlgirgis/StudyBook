# ADR-0001: Adopt Bounded-Autonomy Control Protocol

## Status
- Accepted

## Date
- 2026-04-01

## Decision Makers
- Project owner
- Code agent execution layer

## Context
- Prior workflow was over-constrained and required one-by-one instructions.
- This created low throughput and repeated stalls.
- Durable repo memory was needed to offset weak chat/session memory.

## Decision
- Adopt `CONTROL_PROTOCOL.md` with bounded autonomy as default.
- Keep strict safety gates for high-risk actions.
- Require continuity artifacts (`agent_status`, `task_register`, `open_loops`).

## Consequences
- Positive:
- Faster execution with retained control.
- Reduced prompt micromanagement overhead.
- Better resumability across sessions.
- Negative:
- Requires discipline to keep continuity files current.
- Neutral:
- Some tasks still require explicit approval due to risk class.

## Alternatives Considered
- Keep strict one-file execution for all tasks.
- Full open autonomy without explicit guardrails.

## Supersedes
- none

## Superseded By
- none

## Links
- Task: `TB-20260401-02`
- Decision Log: `agents/shared/decision_log.md`
- Protocol: `CONTROL_PROTOCOL.md`
