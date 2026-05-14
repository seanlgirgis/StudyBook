# CONTROL_PROTOCOL

## Mission
Build practical Python + SQL + data tooling fluency for observability work.

## Ground Rules
- Repository files are source of truth.
- Keep outputs short, operator-oriented, and runnable.
- Prefer tutorials, recipes, and runbooks over theory.
- One scoped task per run.
- Side findings go to `agents/shared/parking_lot.md`.

## Startup Order (Required)
1. `CONTROL_PROTOCOL.md`
2. `agents/shared/context_index.md`
3. `agents/shared/open_loops.md`
4. `agents/shared/approval_matrix.md`
5. `agents/shared/command_allowlist.md`
6. `docs/adr/ADR-INDEX.md`
7. `agents/shared/pending_task.md` (if present)
8. `agents/shared/agent_status.md` (if present)
9. `agents/shared/decision_log.md` (if present)

## Interview Safety
- Use truth-based framing.
- Add explicit "Do not overclaim" notes for adjacent tools.
- Tie cloud-native topics back to enterprise APM/capacity experience.

## Execution Cadence
- Local first with Docker.
- Cloud second with AWS credits.
- Every lab should produce: setup, command(s), expected output, rollback/cleanup.
