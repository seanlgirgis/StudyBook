# GROK_MEMORY.md

Durable Grok guardian conventions for LifeVault.

## Truth Sources

| Layer | Authority |
|-------|-----------|
| Implementation status | Codex handoff + `USE_CASE_INDEX.md` + tests on disk |
| Product north star | ChatGPT handoff + `LIFEVAULT_1000_FOOT_CAPABILITY_MAP.md` |
| Safety | `agents/codex/LIFEVAULT_BOOTSTRAP.md`, `agents/codex/CODEX_CONSTITUTION.md`, `GROK_OPERATING_RULES.md` |

When vision and code disagree, state both; do not silently pick one.

## Registry

- Director ID: `lifevault` (hybrid: application workflows + knowledge vault items)
- Dev: `D:\Workarea\StudyBook\Proj_development\LifeVault`
- Ops: `D:\AI_Lab\LifeVault`

## Agent Split

- Grok scopes tasks and protects architecture from drift
- Codex implements in repo; must not change retention/encryption/deletion policy alone
- ChatGPT architect optional; not required per session

## Merge Policy (2026-06-17)

Keep LifeVault **standalone**. Do not merge into `local_memory`. LifeVault may expose summaries to local_memory later; inverse is not true.

## Writer Model

v0 one-writer/many-reader for `lifevault.sqlite`. First writer machine: ASUS PC. No concurrent multi-machine live writes.

## Chat Exports

Sean chose to skip bulk chat exports. Handoffs + repo docs are sufficient unless he revisits.

## Root Layout (2026-06-17)

- Root: Grok guardian files only
- `agents/codex/`: Codex bootstrap
- `agents/chatgpt/`: ChatGPT constitution
- `docs/handoffs/`: migration handoffs

## Launcher

Runtime: `C:\scripts\start_grok_lifevault.ps1`  
Archive: `start_grok_lifevault.ps1` at project root