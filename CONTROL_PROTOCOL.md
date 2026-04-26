# CONTROL_PROTOCOL.md

## 1. Goal

Enable high-control, high-throughput agent execution in `D:\Workarea\StudyBook` without micromanagement.

## 2. Authority Order

1. Direct user instruction for the current run
2. `CONTROL_PROTOCOL.md`
3. `agents/shared/pending_task.md`
4. `agents/shared/context_index.md`
5. `agents/shared/agent_status.md` (latest)

## 3. Operating Model

- Use guardrails, not handcuffs.
- Agent can execute end-to-end within bounded autonomy.
- Repository files are durable memory; chat memory is not.
- Prefer progress in meaningful batches over one-file micromanagement.

## 4. Autonomy Budget (Default)

Unless explicitly overridden in `pending_task.md`, agent may:
- modify up to 8 related files in one run,
- run required validation commands,
- complete up to 3 tightly related subtasks under one objective.

Agent must ask before:
- destructive actions (mass delete, history rewrite, force push),
- secret/credential changes,
- production or external system writes.

## 5. Required Inputs Per Run

Read before edits:
- `CONTROL_PROTOCOL.md`
- `agents/shared/context_index.md`
- `agents/shared/open_loops.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `docs/adr/ADR-INDEX.md`
- `agents/shared/pending_task.md` (if present)
- latest `agents/shared/agent_status.md` (if present)

## 6. Task Contract

Each task should provide:
- `Task ID` (`TB-YYYYMMDD-XX`)
- `Task Type` (`MIGRATION`, `ENHANCEMENT`, `FIX`, `REFACTOR`, `RESEARCH`, `SYNC`)
- `Goal`
- `Non-Goals`
- `Files to Read`
- `Allowed Scope` (`strict` or `bounded`)
- `Validation Commands` (or `none`)
- `Definition of Done`
- `Reasoning Depth` (`standard` or `deep`)
- `Risk Level` (`low`, `medium`, `high`)

If fields are missing:
- make explicit assumptions,
- continue for `low`/`medium` risk,
- stop only for `high` risk ambiguity.

## 7. Memory and Continuity Rules

- Record durable decisions in `agents/shared/decision_log.md`.
- Record architecture-level decisions in ADRs under `docs/adr/`.
- Track unfinished work in `agents/shared/open_loops.md`.
- Capture out-of-scope findings in `agents/shared/parking_lot.md`.
- Keep `agents/shared/context_index.md` short and current.

## 8. Anti-Drift Rules

- Stay inside task objective and allowed scope.
- Do not chase side quests in the same run.
- If scope pressure appears, complete core objective first, then park extras.

## 9. Reasoning and Planning

For `deep` reasoning or `medium/high` risk:
- write a brief execution plan before edits:
1. intent
2. assumptions
3. risks
4. edit and validation strategy

## 10. Verification Rule

If behavior changes:
- run real validation commands,
- capture real output,
- retry up to 3 times with scoped fixes.

If still failing:
- stop and log exact failure in `agents/shared/agent_status.md`.

## 11. Status Artifact (Mandatory)

Overwrite `agents/shared/agent_status.md` every run.

Required: factual summary, validations run, outcomes, assumptions, risks, and next step.

## 12. Task Register Update

Update `agents/shared/task_register.md` each run:
- `in_progress` when starting,
- `done` or `blocked` at exit.

## 13. Git Discipline

- Do not commit/push unless explicitly requested.
- If asked to commit, include only in-scope files.

## 14. Definition of Done

A run is complete only when:
- primary objective is completed or clearly blocked,
- required validation is executed (or explicitly not required),
- `agent_status.md` is overwritten,
- `task_register.md` and `open_loops.md` are updated,
- side findings are parked without derailing the task.

## 15. Architecture Decision Rule

When a run introduces or changes architecture-level behavior:
- create or update an ADR in `docs/adr/`,
- add or update the entry in `docs/adr/ADR-INDEX.md`,
- add a linked summary entry in `agents/shared/decision_log.md`.

