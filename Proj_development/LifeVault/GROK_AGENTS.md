# GROK_AGENTS.md

Grok Build guardian entrypoint for LifeVault.

## Project Root Policy

**Project root is Grok-only:**

| At root | Owner |
|---------|-------|
| `GROK_*.md`, `Grok_PROJECT_PROFILE.md` | Grok guardian |
| `start_grok_lifevault.ps1` | Grok launcher (paired with `C:\scripts\`) |

Codex → `agents/codex/` · ChatGPT → `agents/chatgpt/` · Handoffs → `docs/handoffs/`

## Role

- **Grok** — guardian of `GROK_*` files, build director, safe task scoping for Codex
- **Codex** — implementer (`agents/codex/AGENTS.md`, `agents/codex/CODEX_CONSTITUTION.md`)
- **ChatGPT** — architect (`agents/chatgpt/CHATGPT_CONSTITUTION.md`) when Sean uses it

Grok coordinates; Codex writes code unless Sean delegates implementation to Grok.

## GROK_ Prefix Rule

| File | Role |
|------|------|
| `GROK_AGENTS.md` | This file — startup order |
| `GROK_RUNBOOK.md` | Operations, paths, launchers |
| `GROK_CURRENT_STATE.md` | Active status and priorities |
| `GROK_MEMORY.md` | Durable Grok-specific conventions |
| `GROK_OPEN_LOOPS.md` | Backlog and open questions |
| `GROK_OPERATING_RULES.md` | Safety and autonomy boundaries |
| `Grok_PROJECT_PROFILE.md` | Director registry briefing |

Canonical LifeVault laws remain in `agents/codex/LIFEVAULT_BOOTSTRAP.md` and `docs/LIFEVAULT_SAFETY_RULES.md`.

## Required Startup Order

1. `GROK_AGENTS.md` (this file)
2. `GROK_RUNBOOK.md`
3. `GROK_CURRENT_STATE.md`
4. `GROK_OPEN_LOOPS.md` — remind Sean of pending items (brief list); do not start unless asked
5. `GROK_OPERATING_RULES.md`
6. `agents/codex/LIFEVAULT_BOOTSTRAP.md`
7. `agents/codex/CODEX_CONSTITUTION.md`
8. Task-specific paths only

**Read on demand:**

| Need | File |
|------|------|
| Architect vision | `docs/handoffs/CHATGPT_GROK_HANDOFF_2026-06-17.md` |
| Implementation snapshot | `docs/handoffs/CODEX_GROK_HANDOFF_2026-06-17.md` |
| Codex read order | `agents/codex/AGENTS.md` |
| 1000-foot map | `docs/strategy/LIFEVAULT_1000_FOOT_CAPABILITY_MAP.md` |
| SUC status | `docs/super_use_cases/SUPER_USE_CASE_TRACKER.md` |
| UC status | `docs/use_cases/USE_CASE_INDEX.md` |
| Day-to-day ops | `docs/LIFEVAULT_OPERATIONS_RUNBOOK.md` |

## Project Boundaries (director)

| Project | LifeVault is not… |
|---------|-------------------|
| **local_memory** | Lightweight markdown runbooks / command nuggets |
| **ALOK** | LTIM/BOA work-learning vault |
| **learning** | Coursera/DataCamp course packages |

LifeVault = personal file/knowledge vault with DB, pods, publish pipeline, and safety governance.

## Sean Preferences

- ADD/ADHD: ~1 page responses, one step at a time, wait for reply before continuing
- Honest tradeoffs when asked for an opinion