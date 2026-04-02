# ADR-0004: Adopt Guided Bootstrap Entrypoint

## Status
- Accepted

## Date
- 2026-04-01

## Decision Makers
- Project owner
- Code agent execution layer

## Context
- Manual setup required multiple scripts and steps.
- This increased onboarding errors across machines.

## Decision
- Provide a single guided command:
- `scripts/env/bootstrap_all.ps1`
- It orchestrates machine profile setup, secret template prep/encryption, and validation.

## Consequences
- Positive:
- Lower setup friction and fewer missed steps.
- Repeatable onboarding for AsusPC, Dell, and future machines.
- Negative:
- Script complexity is higher than isolated helper scripts.
- Neutral:
- Manual scripts are still available for granular control.

## Alternatives Considered
- Keep only separate scripts (`init_machine_profile`, `encrypt_secrets`) with manual orchestration.

## Supersedes
- none

## Superseded By
- none

## Links
- Task: `TB-20260401-05`
- Decision Log: `agents/shared/decision_log.md`
- Script: `scripts/env/bootstrap_all.ps1`
