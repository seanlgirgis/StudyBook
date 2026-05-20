# OBSERVABILITY_AGENT_CHARTER

Purpose:
- Operational charter for AI agents working in this Observability project.

Authority order:
1. Repository source files and explicit user instructions.
2. MOAG StudyBubble Training System Guide v2.
3. Local agent shared rules in `agents/shared/*`.

Core law:
- Keep `study_maps/Observability` as the learning product.
- Keep `tutorials/Observability` as the hands-on lab bench.
- Do not mix responsibilities.

Required startup read order for agent runs:
1. `CONTROL_PROTOCOL.md` (if present)
2. `agents/shared/context_index.md`
3. `agents/shared/open_loops.md`
4. `agents/shared/approval_matrix.md`
5. `agents/shared/command_allowlist.md`
6. `docs/adr/ADR-INDEX.md` (if present)
7. `agents/shared/pending_task.md` (if present)
8. `agents/shared/agent_status.md` (if present)
9. `agents/shared/decision_log.md` (if present)
10. `agents/shared/moag_training_system_rules.md`
11. `agents/shared/path_and_env_rules.md`

Execution defaults:
- Prefer relative paths from the current working container.
- Initialize StudyBook shell before Python/build commands:
  - `cd D:\Workarea\StudyBook`
  - `.\env_setter.ps1`
- Edit source files, never hand-edit generated map outputs.
- Prefer small, testable increments.
- Maintain `PROJECT_STATE.md` and `TASK_BOARD.md` after meaningful changes.
