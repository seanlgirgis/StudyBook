# GROK_AGENTS.md

Grok Build agent entrypoint for `D:\Workarea\StudyBook\local_memory`.

## Purpose

This folder is Sean's small local memory / personal notes vault for commands, paths, login steps, file locations, learning notes, and repeatable how-to answers.

## GROK_ Prefix Rule

Always use the `GROK_` prefix for Grok-specific memory files to avoid mixing with Claude/ChatGPT artifacts:

| File | Role |
|------|------|
| `GROK_MEMORY.md` | Grok session memories and nuggets |
| `GROK_AGENTS.md` | Grok agent rules (this file) |
| `GROK_RUNBOOK.md` | Grok operational runbook (env, commands, workflows) |
| `GROK_CURRENT_STATE.md` | Grok session state and active context |

Do not write Grok session state into non-prefixed agent files unless the user explicitly asks.

## Shared Repository Rules

Primary operating rules for all agents live in `CONTROL_PROTOCOL.md`. If anything conflicts, `CONTROL_PROTOCOL.md` wins.

Design and architecture decisions for this vault are documented in `LOCAL_MEMORY_HANDOFF.md` (Codex handoff, 2026-06-15). Use it to understand where memories live, how writes work, and what this project is not.

## Required Startup Order

Before execution in a Grok Build session, read in this order:

1. `GROK_AGENTS.md` (this file)
2. `GROK_RUNBOOK.md`
3. `GROK_CURRENT_STATE.md`
4. `GROK_MEMORY.md`
5. `LOCAL_MEMORY_HANDOFF.md` — vault design, storage layout, write model
6. `CONTROL_PROTOCOL.md`
7. `agents/shared/context_index.md`
8. `agents/shared/open_loops.md` (if present)
9. `agents/shared/approval_matrix.md`
10. `agents/shared/command_allowlist.md`
11. `docs/adr/ADR-INDEX.md`
12. `docs/planning/PLANNING_INDEX.md` (if planning or architecture work)
13. `agents/shared/pending_task.md` (if present)
14. `agents/shared/agent_status.md` (if present)
15. `agents/shared/decision_log.md` (if present)

## Working Rules

- Repository files are the source of truth; do not rely on chat memory.
- Operate **repository-first**, not chat-memory-first.
- Search local repository files first before answering lookup questions.
- Return stored answers directly for lookup questions; cite the source file path.
- Never invent or silently normalize local usernames, passwords, ports, database names, paths, commands, or special text.
- If a fact is missing, say exactly: `I do not have this stored yet.`
- Execute one scoped task per run.
- Park side findings in `agents/shared/parking_lot.md`.
- When the user says `remember`, `store`, `save`, or `add a nugget`, persist to the most relevant file by topic:
  - `runbooks/` — domain commands and how-tos (canonical shared memory)
  - `locations/` — paths and file locations
  - `chat_captures/` — external reference material (raw + derived notes)
  - `GROK_MEMORY.md` — Grok-specific session notes only
- When the user says `store secret` or `save secret`, use `scripts/store_text_secret.ps1` or `scripts/store_secret_file.ps1`; update `runbooks/secret_registry.md` via the script; never write secret values into Git-tracked files.
- Preserve exact commands, names, paths, and special text; confirm the save location.
- Allowed without extra approval: reading/searching repo, updating markdown memory on user request, creating missing agent-control files in this repo.
- Pause and clarify before: deleting memory, rewriting stored facts when replacement is unclear, changing files outside this repo.

## Collaboration With Sean

When Sean asks for an opinion, give an **honest assessment** — not blind agreement.

- Push back when an idea has gaps, risks, or a simpler alternative.
- Do not implement something questionable just because it was suggested.
- Distinguish clearly: **recommendation** vs **what Sean asked for**.
- If Sean explicitly chooses a path after hearing tradeoffs, execute that choice.
- Planning and architecture discussions belong in `docs/planning/` until accepted as ADRs.

## Planning Artifacts

Exploratory thinking lives under `docs/planning/` (see `PLANNING_INDEX.md`). Accepted decisions graduate to `docs/adr/`. Operational facts graduate to `runbooks/`.

## Environment

Before running any Python commands in this project, always run:

```powershell
D:\Workarea\StudyBook\env_setter.ps1
```

This activates the correct local Python venv for StudyBook.