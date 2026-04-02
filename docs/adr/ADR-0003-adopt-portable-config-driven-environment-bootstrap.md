# ADR-0003: Adopt Portable Config-Driven Environment Bootstrap

## Status
- Accepted

## Date
- 2026-04-01

## Decision Makers
- Project owner
- Code agent execution layer

## Context
- Project runs on multiple machines with different mounts and local constraints.
- Hardcoded paths reduce portability and increase setup friction.
- Secrets must be portable but not stored in plaintext.

## Decision
- Use config-driven bootstrap with base + per-machine merge:
- `config/env/base.psd1`
- `config/machines/*.psd1`
- Bootstrap through `env_setter.ps1` and `scripts/env/env_core.ps1`.
- Support encrypted secret files and runtime passphrase import.

## Consequences
- Positive:
- Environment setup is machine-agnostic and repeatable.
- Paths can remain relative or env-variable based across workflows.
- Encrypted secrets can be synced without plaintext leakage.
- Negative:
- Passphrase management becomes an operational dependency.
- Neutral:
- Bootstrap flow introduces more config files.

## Alternatives Considered
- Keep single hardcoded `env_setter.ps1`.
- Store machine-specific values and secrets only in local plaintext files.

## Supersedes
- none

## Superseded By
- none

## Links
- Task: `TB-20260401-04`
- Decision Log: `agents/shared/decision_log.md`
- Docs: `docs/PORTABLE_ENV.md`
