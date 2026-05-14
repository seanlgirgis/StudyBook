# AGENTS.md

## Purpose
This file is a compatibility entrypoint.

Primary operating rules are in:
- `CONTROL_PROTOCOL.md`

If anything conflicts, `CONTROL_PROTOCOL.md` wins.

## Required Startup Order
Before execution, read in this order:
1. `CONTROL_PROTOCOL.md`
2. `agents/shared/context_index.md`
3. `agents/shared/open_loops.md`
4. `agents/shared/approval_matrix.md`
5. `agents/shared/command_allowlist.md`
6. `docs/adr/ADR-INDEX.md`
7. `agents/shared/pending_task.md` (if present)
8. `agents/shared/agent_status.md` (if present)
9. `agents/shared/decision_log.md` (if present)

## Working Rule
- Repository files are the source of truth.
- Do not rely on chat memory.
- Execute one scoped task per run.
- Park side findings in `agents/shared/parking_lot.md`.

## Project Intent
This repository supports short-time interview readiness and long-term cloud observability readiness.
