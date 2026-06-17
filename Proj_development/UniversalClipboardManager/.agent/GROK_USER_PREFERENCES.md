# GROK User Preferences — Universal Clipboard Manager

**Last updated:** 2026-06-17

Inferred from user messages, project history, and StudyBook parent context.

---

## Agent Assignment

- **User wants Grok** as the controlling agent for `UniversalClipboardManager`
- Agent files use **`GROK_` prefix** — Grok-owned durable memory
- User encouraged creating **as much memory as needed** — comprehensive `GROK_*` suite is intentional

---

## Working Environment

| Preference | Detail |
|------------|--------|
| OS | Windows 10 (`asuspc`) |
| Shell | PowerShell (Windows PowerShell / pwsh) |
| StudyBook root | `D:\Workarea\StudyBook` |
| StudyBook venv | `C:\py_venv\proj_educate` via `D:\Workarea\StudyBook\env_setter.ps1` (venv startup file) |
| Grok launcher | `D:\start_grok_ucm.ps1` (runtime); repo copy at project root |
| Dual-copy pattern | Intentional — frozen D: copy + git-tracked repo copy; keep identical |
| Project path | `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager` |
| Path syntax | `D:\...` not `/D:/...` in PowerShell |

---

## App Usage Preferences (From Project History)

| Topic | User preference |
|-------|-----------------|
| Hotkeys | Function keys preferred (`F10` show, `F11` capture) — avoid `Ctrl+Shift+*` |
| Hotkey config | Edit `settings.json`, not code, when possible |
| App presence | Tray-based background utility — not always-visible window |
| Startup | Auto-launch on Windows login |
| Capture mode | On-demand capture — not passive clipboard spying |
| Deploy | Separate stable install at `C:\scripts\UniversalClipboardManager` |

---

## Communication Style (From User Rules)

- Execute commands yourself — don't tell user what to run
- Concise, high-quality technical prose
- Code citations with `startLine:endLine:filepath` format
- Minimal scope changes — no drive-by refactors
- Don't create markdown files user didn't ask for *(exception: user explicitly asked for GROK agent files)*

---

## Integration Preferences

- KB docs drop to `KB\00_Inbox` (`KB_INBOX_PATH`)
- Project is part of larger StudyBook workspace
- `PROJECT_FULL_CONTEXT_AND_HISTORY.md` is authoritative narrative history — Grok should read it but maintain operational state in `GROK_*`

---

## Risk Sensitivities

- **Snippet data** — `clipboard_data.json` is real user content
- **Global hotkeys** — conflicts with daily tools are unacceptable; test shortcut changes carefully
- **Duplicate instances** — user has seen this during restarts; prefer clean single instance

---

## Enhancement Tracking Preference

- **No separate todo file** — backlog lives in `GROK_OPEN_LOOPS.md`
- **Remind on project open** — short numbered list of pending enhancements; don't start unless Sean asks
- **Mark done in memory** — when implemented, update backlog status + Closed section in `GROK_OPEN_LOOPS.md`

---

## Open Questions for User (Optional Future Clarification)

- Should `clipboard_data.json` stay in git or be gitignored (deploy-only user data)?
- Should Grok update `docs/handoff.md` automatically after changes, or only on request?