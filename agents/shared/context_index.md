# Context Index

Purpose: compact durable memory map for fast session bootstrap.

## Project North Star

- Shift/lift from legacy project with stronger agent control and fewer stalls.
- Balance autonomy with safety guardrails.

## Canonical Control Files

- `AGENTS.md`
- `CONTROL_PROTOCOL.md`
- `agents/shared/pending_task.md`
- `agents/shared/agent_status.md`
- `agents/shared/task_register.md`
- `agents/shared/open_loops.md`
- `agents/shared/decision_log.md`
- `agents/shared/parking_lot.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `docs/adr/ADR-INDEX.md`

## Current Working Agreements

- Use `Allowed Scope: bounded` by default for velocity.
- Use `Reasoning Depth: deep` for migration and architecture decisions.
- Stop only for high-risk ambiguity, not for routine implementation details.

## Portable Environment Files

- `env_setter.ps1`
- `scripts/env/env_core.ps1`
- `scripts/env/bootstrap_all.ps1`
- `config/env/base.psd1`
- `config/machines/asuspc.psd1`
- `config/machines/dell-laptop.psd1`
- `docs/PORTABLE_ENV.md`
- `config/secrets/shared.secrets.enc.json`
- `config/secrets/asuspc.secrets.enc.json`
- `config/secrets/dell-laptop.secrets.enc.json`
- `config/secrets/workspace-import.sources.md`

## Architecture Tracking Files

- `docs/adr/README.md`
- `docs/adr/ADR-INDEX.md`
- `docs/adr/TEMPLATE.md`
- `scripts/adr/new_adr.ps1`

## Operational Runbooks

- `docs/operations/README.md`
- `docs/operations/env_startup.md`
- `docs/operations/secrets_workflow.md`
- `docs/operations/subscription_tracker.md`

## Last Updated

- 2026-04-01
