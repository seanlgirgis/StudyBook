# StudyBook Migration Execution System

## Objective
Build `D:\StudyBook` as the single reproducible DE/AI runtime repository using an infra-first migration flow from `D:\Workspace`.

## Canonical Target
- Target repository: `D:\StudyBook`
- Deprecated target removed: `D:\ZeroToHero_DE_AI` (deleted per user instruction)

## Non-Negotiables
- Treat this as migration, not full regeneration.
- Create assets only when needed by the active batch.
- Keep secrets out of tracked files; use encrypted secret flow and env placeholders.
- Every change must map to a board item with validation evidence.

## Current Baseline (Verified)
- Reproducible infra exists in `D:\StudyBook\_infra`:
  - Compose topology: `core.yml`, `streaming.yml`, `pipeline.yml`, `observability.yml`, `docker-compose.yml`
  - Seed layer: `seed_core.py`, `seed_tech_telemetry.py`
  - Script pack: `infra_up.ps1`, `infra_down.ps1`, `infra_seed.ps1`, `infra_health.ps1`
  - Env template: `_infra\env\.env.example`
- Validation checks passing:
  - `docker compose -f D:\StudyBook\_infra\docker\docker-compose.yml --env-file D:\StudyBook\_infra\env\.env.example config`
  - `pwsh -NoProfile -File D:\StudyBook\_infra\scripts\infra_health.ps1 -AsJson`
- Cloud account metadata baseline exists:
  - `docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md`

## Program Gates
- Gate G1: infra compose + scripts are reproducible from repo files.
- Gate G2: cloud account metadata is tracked without plaintext secrets.
- Gate G3: migration board tracks source, target, status, and evidence per item.
- Gate G4: prompt/notebook migration follows inventory + classification rules.
- Gate G5: continuity artifacts stay current for incoming code agents.

## Workstream 1: Infra Reproducibility

### I-001 Compose Contract
- Keep split compose topology in `_infra\docker\` and one full compose.
- Preserve stable service/container names and port contract.

### I-002 Runtime Script Contract
- Startup: `_infra\scripts\infra_up.ps1`
- Teardown: `_infra\scripts\infra_down.ps1`
- Seeds: `_infra\scripts\infra_seed.ps1`
- Health: `_infra\scripts\infra_health.ps1`

### I-003 Seed Contract
- `seed_core.py` owns `telemetry.*` seed model.
- `seed_tech_telemetry.py` owns simplified `public.*` seed model.
- Both scripts remain deterministic and idempotent.

### I-004 Verification Pack
- Infra health output must be machine-readable (`-AsJson`).
- Service checks include container presence + host port readiness.

### I-005 Security Hardening
- No hardcoded credentials in tracked prompts/notebooks/docs.
- Use env variable references and encrypted secret files only.

## Workstream 2: Migration Execution

### M-001 Inventory and Classification
- Sources:
  - `D:\Workspace`
  - `D:\StudyBook\temp\TalksWithClaude.md`
- Classification tags:
  - `migrate_as_is`
  - `migrate_with_adaptation`
  - `create_new`
  - `archive_or_drop`

### M-002 Ordered Flow
1. Infra executable foundation in `D:\StudyBook\_infra` (complete)
2. Validated notebook migration into canonical track paths
3. Prompt migration to legacy archive + canonical prompt outputs
4. Missing-asset creation only where inventory confirms no source
5. Security cleanup + reproducibility re-validation

## Workstream 3: Agent Continuity
- Start files for any agent:
  - `AGENTS.md`
  - `CONTROL_PROTOCOL.md`
  - `docs/programs/zero_to_hero/EXECUTION_SYSTEM.md`
  - `docs/programs/zero_to_hero/MIGRATION_BOARD.md`
  - `docs/programs/zero_to_hero/TALKS_WITH_CLAUDE_EXTRACT_AND_SHIFT_LIFT_PLAN.md`
- End-of-run files to update:
  - `agents/shared/agent_status.md`
  - `agents/shared/task_register.md`
  - `agents/shared/open_loops.md`
  - `agents/shared/decision_log.md` (when decisions are made)

## Completion Definition
Program is complete when:
- Infra can be rendered, started, seeded, and health-checked from repo assets.
- No plaintext credentials remain in migrated tracked artifacts.
- Critical migration board items are resolved with evidence.
- Continuity artifacts are sufficient for immediate handoff to any code agent.
