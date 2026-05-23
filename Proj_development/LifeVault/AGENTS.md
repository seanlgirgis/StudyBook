# AGENTS.md

## Purpose

This is the Codex session-start bootstrap file for LifeVault.

## Required Read Order

Read these files in order before taking action:
1. `LIFEVAULT_BOOTSTRAP.md`
2. `CODEX_CONSTITUTION.md`
3. `docs/LIFEVAULT_CHARTER.md`
4. `docs/LIFEVAULT_ARCHITECTURE.md`
5. `docs/LIFEVAULT_DATA_MODEL.md`
6. `docs/LIFEVAULT_SKILL_FAMILY.md`
7. `docs/LIFEVAULT_DATA_BOUNDARY.md`
8. `docs/LIFEVAULT_SAFETY_RULES.md`

## Operating Rules

- Always start from project root when possible.
- Run `..\..\env_setter.ps1` before Python commands and tests.
- Use config files for operational paths.
- Never commit real personal data.
- Never commit rclone tokens, credentials, or secrets.
- No delete, move, rename, sync, or upload unless explicitly authorized by the correct future workflow.