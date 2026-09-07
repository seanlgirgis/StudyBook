# AGENTS.md

Auto-load pointer. Grok files live under `.agent\`.

## Read at session start (in order)

1. `D:\Workarea\Grok_DIRECTOR\Grok_SEAN.md`
2. `D:\Workarea\Grok_DIRECTOR\Grok_SEAN_NOW.md`
3. `.agent/GROK_INDEX.md`
4. `.agent/GROK_CONTEXT.md` / `.agent/GROK_OPEN_LOOPS.md` as needed
5. Task paths only

Source: this folder. Runtime: `C:\scripts\UniversalClipboardManager` (deploy before expecting app changes). Launcher: `C:\scripts\start_grok_ucm.ps1`
