# AGENTS.md

Auto-load pointer. On conflict, `CONTROL_PROTOCOL.md` wins.

## Read at session start (in order)

1. `D:\Workarea\Grok_DIRECTOR\Grok_SEAN.md`
2. `D:\Workarea\Grok_DIRECTOR\Grok_SEAN_NOW.md`
3. `GROK_AGENTS.md`
4. `CONTROL_PROTOCOL.md`
5. `GROK_RUNBOOK.md` / `GROK_MEMORY.md` / `GROK_CURRENT_STATE.md` as needed
6. Task paths only (`runbooks/`, `locations/`)

Repository files are the source of truth. Do not store secret values in markdown. Launcher: `C:\scripts\start_grok_local_memory.ps1`
