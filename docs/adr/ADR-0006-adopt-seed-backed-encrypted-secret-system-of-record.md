# ADR-0006: Adopt Seed-Backed Encrypted Secret System Of Record

## Status
- Accepted

## Date
- 2026-04-02

## Decision Makers
- Project owner
- Code agent execution layer

## Context
- Sensitive values are frequently needed across proofs, scripts, and agent runs.
- Repeated manual confirmation and plaintext staging slow execution and increase leakage risk.
- StudyBook already has encrypted secret files and DPAPI seed support.

## Decision
- Treat `config/secrets/*.enc.json` as the system of record for sensitive values.
- Use seed-backed, noninteractive secret updates by default.
- Add direct encrypted updater `scripts/env/set_secret.ps1` for KEY=VALUE writes without tracked plaintext files.
- Keep non-secret identifiers only in registry/docs.

## Consequences
- Positive:
- Sensitive updates become fast and repeatable for all agents.
- Reduced plaintext drift in repo and setup docs.
- Improves cross-machine continuity with encrypted portability model.
- Negative:
- Secret updates now depend on seed/passphrase readiness.
- Neutral:
- Additional secret helper script to maintain.

## Alternatives Considered
- Continue using plaintext `*.secrets.json` staging then encrypt.
- Keep sensitive values only in transient shell variables.

## Supersedes
- none

## Superseded By
- none

## Links
- Task: `TB-20260402-20`
- Decision Log: `agents/shared/decision_log.md`
- Docs: `docs/operations/secrets_workflow.md`
