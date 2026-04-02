## Task ID
- TB-20260402-06

## Topic
- Finalize StudyBook-only infra reproducibility baseline, remove active plan drift to deleted target path, and update continuity artifacts for handoff

## Task Type
- MIGRATION

## Reasoning Depth
- deep

## Risk Level
- medium

## Allowed Scope
- bounded (autonomy override: extended)

## Files Read
- CONTROL_PROTOCOL.md
- agents/shared/context_index.md
- agents/shared/open_loops.md
- agents/shared/approval_matrix.md
- agents/shared/command_allowlist.md
- docs/adr/ADR-INDEX.md
- agents/shared/pending_task.md
- agents/shared/agent_status.md
- agents/shared/decision_log.md
- agents/shared/task_register.md
- docs/programs/zero_to_hero/EXECUTION_SYSTEM.md
- docs/programs/zero_to_hero/MIGRATION_BOARD.md
- docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md
- _infra/docker/*.yml
- _infra/seeds/*.py
- _infra/env/.env.example
- _infra/README.md

## Files Modified
- .gitignore
- _infra/README.md
- _infra/scripts/infra_up.ps1
- _infra/scripts/infra_down.ps1
- _infra/scripts/infra_seed.ps1
- _infra/scripts/infra_health.ps1
- docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md
- docs/programs/zero_to_hero/EXECUTION_SYSTEM.md
- docs/programs/zero_to_hero/MIGRATION_BOARD.md
- docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md
- agents/shared/context_index.md
- agents/shared/decision_log.md
- agents/shared/open_loops.md
- agents/shared/pending_task.md
- agents/shared/task_register.md
- agents/shared/agent_status.md

## Plan
1. Verify current control state and detect any remaining references to deleted runtime target path in active plan artifacts.
2. Harden StudyBook infra reproducibility by adding lifecycle scripts (`up/down/seed/health`) and cloud account metadata registry.
3. Validate scripts and compose rendering against live Docker stack.
4. Retarget migration docs/board to StudyBook-only execution path and update continuity files.

## What Was Done
- Confirmed live Docker stack contract with `docker ps` and aligned it to StudyBook `_infra` compose definitions.
- Added infra script pack:
  - `_infra/scripts/infra_up.ps1`
  - `_infra/scripts/infra_down.ps1`
  - `_infra/scripts/infra_seed.ps1`
  - `_infra/scripts/infra_health.ps1`
- Added cloud metadata baseline:
  - `docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md`
  - includes non-secret provider registry and secret key mapping policy.
- Updated `_infra/README.md` to script-driven reproducibility flow and explicit port contract.
- Updated `.gitignore` for local-only infra/cloud overlays.
- Retargeted active planning files from deleted path to StudyBook and refreshed statuses/evidence:
  - `EXECUTION_SYSTEM.md`
  - `MIGRATION_BOARD.md`
  - `TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md`
- Updated continuity artifacts for handoff:
  - `context_index.md`
  - `open_loops.md`
  - `task_register.md`
  - `pending_task.md` (next task: `TB-20260402-07` for notebook shift/lift)
  - `decision_log.md` (`DEC-012`)

## Validation
- command: `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"` (escalated)
- result: confirmed all expected containers and host ports are running and match StudyBook compose contract.

- command: `pwsh -NoProfile -File D:\StudyBook\_infra\scripts\infra_health.ps1 -AsJson` (escalated)
- result: success (`exit 0`), all configured services reported `Overall: true`.

- command: `docker compose -f D:\StudyBook\_infra\docker\docker-compose.yml --env-file D:\StudyBook\_infra\env\.env.example config`
- result: success (`exit 0`), rendered full compose contract.

- command: parser checks for all new PowerShell scripts
- result: `infra_up.ps1`, `infra_down.ps1`, `infra_seed.ps1`, `infra_health.ps1` parse OK.

## Decisions
- Added DEC-012 in `agents/shared/decision_log.md`.

## Assumptions
- Current running Docker stack in screenshot and live `docker ps` is the desired baseline contract for reproducibility.
- Cloud account details should be tracked as metadata only in repo, while secrets remain encrypted/off-doc.

## Issues / Risks
- Seed scripts were not executed in this run (can be heavy and environment-dependent); runtime data-seed validation still pending next infra verification cycle.
- Broad secret scanning across migrated notebooks/prompts is still an active gate (`M-014`, `C-002`) and must run during notebook/prompt migration.

## Parking Lot Added
- none

## Open Loops Updated
- LOOP-004 open: execute `M-011` notebook migration batch.
- LOOP-005 in_progress: complete cloud secret routing + sanitization gate.

## Next Step
- Execute TB-20260402-07 (`BATCH-MIG-02A`): shift/lift validated Technologies notebooks into `D:\StudyBook\tracks` + `interview`, then run smoke checks and update board evidence.
