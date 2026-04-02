# StudyBook

## Agent Control Bootstrap

This repository now uses a strict control layer to keep agent work scoped and resumable.

Primary files:
- `AGENTS.md`
- `CONTROL_PROTOCOL.md`
- `agents/shared/pending_task.md`
- `agents/shared/agent_status.md`
- `agents/shared/task_register.md`
- `agents/shared/context_index.md`
- `agents/shared/open_loops.md`
- `agents/shared/decision_log.md`
- `agents/shared/parking_lot.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`

Quick run order:
1. Write task details in `agents/shared/pending_task.md`
2. Execute the task under `CONTROL_PROTOCOL.md`
3. Overwrite `agents/shared/agent_status.md`
4. Update `agents/shared/task_register.md` and `agents/shared/open_loops.md`

## Portable Environment

Environment bootstrap is now machine-aware and path-portable:
- `env_setter.ps1`
- `config/env/base.psd1`
- `config/machines/asuspc.psd1`
- `config/machines/dell-laptop.psd1`
- `scripts/env/bootstrap_all.ps1`
- `docs/PORTABLE_ENV.md`

## Architecture Decisions

Architecture-grade decision tracking lives in:
- `docs/adr/README.md`
- `docs/adr/ADR-INDEX.md`
- `docs/adr/ADR-0001-adopt-bounded-autonomy-control-protocol.md`
- `docs/adr/ADR-0002-adopt-approval-matrix-and-command-allowlist.md`
- `docs/adr/ADR-0003-adopt-portable-config-driven-environment-bootstrap.md`
- `docs/adr/ADR-0004-adopt-guided-bootstrap-entrypoint.md`

Create new ADR quickly with:

```powershell
.\scripts\adr\new_adr.ps1 -Title "Your decision title" -TaskId TB-YYYYMMDD-XX -DecisionId DEC-###
```

## Operations

Runbooks are under:
- `docs/operations/README.md`
