# GROK Agent Index — Universal Clipboard Manager

**Agent:** Grok  
**Project:** Universal Clipboard Manager  
**Repo path:** `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`  
**Last updated:** 2026-06-17  
**Status:** Onboarded — ready for scoped tasks

---

## Purpose

This file is the **single entry point** for Grok when working in this directory. Repository files are durable memory; chat is not. Read this index first on every session.

---

## Required Startup Read Order

1. `GROK_INDEX.md` (this file)
2. `GROK_CONTEXT.md` — what the app is and where it lives
3. `GROK_AGENT_STATUS.md` — last session state
4. `GROK_PENDING_TASK.md` — current task (if any)
5. `GROK_OPEN_LOOPS.md` — **enhancement backlog + remind Sean of pending items**
6. `GROK_OPERATING_RULES.md` — autonomy and safety boundaries

### Session-open reminder (mandatory)

After step 5, if `GROK_OPEN_LOOPS.md` has enhancements with `Status: pending`, give Sean a **brief numbered list** of suggested work (priority order). Do not start unless asked. Update `Last reminded` in that file.

**Read on demand:**

| Need | File |
|------|------|
| Architecture / code map | `GROK_ARCHITECTURE.md` |
| File inventory | `GROK_FILE_MAP.md` |
| Deploy / run / restart | `GROK_DEPLOY_RUNBOOK.md` |
| Safe commands | `GROK_COMMAND_ALLOWLIST.md` |
| Past decisions | `GROK_DECISION_LOG.md` |
| Out-of-scope findings | `GROK_PARKING_LOT.md` |
| User preferences | `GROK_USER_PREFERENCES.md` |
| Full narrative history | `../PROJECT_FULL_CONTEXT_AND_HISTORY.md` |
| Practical handoff | `../docs/handoff.md` |
| Legacy agent context | `project_context.md` |

---

## Parent Repo Protocol

This project lives inside `D:\Workarea\StudyBook`. Parent-level rules apply when they do not conflict with project-local GROK files:

- `D:\Workarea\StudyBook\CONTROL_PROTOCOL.md`
- `D:\Workarea\StudyBook\agents\shared\context_index.md`

**Local GROK files win** for Universal Clipboard Manager–specific work.

---

## Quick Facts

| Item | Value |
|------|-------|
| App type | Windows tray clipboard snippet manager (Python/PyQt6) |
| Source | `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager` |
| Deploy target | `C:\scripts\UniversalClipboardManager` |
| Main code | `clipboard_app.py` (~526 lines) |
| Snippet data | `clipboard_data.json` (user data — handle carefully) |
| Hotkey config | `settings.json` |
| Show/hide hotkey | `F10` (fallback `Ctrl+Alt+S`) |
| Capture hotkey | `F11` (fallback `Ctrl+Alt+A`) |
| Venv (local) | `.\.venv` |
| Venv (deployed) | `C:\scripts\UniversalClipboardManager\.venv` |
| KB inbox | `KB\00_Inbox` via `KB_INBOX_PATH` |
| Startup shortcut | Verified at `%APPDATA%\...\Startup\UniversalClipboardManager.lnk` |

---

## Grok Session Launcher (Preferred)

Two **identical** copies — keep in sync when editing:

| Copy | Path |
|------|------|
| **Runtime (use this)** | `D:\start_grok_ucm.ps1` |
| **Repo (git tracked)** | `start_grok_ucm.ps1` (project root) |

```powershell
pwsh -ExecutionPolicy Bypass -File "D:\start_grok_ucm.ps1"
```

**Env chain:** `D:\Workarea\StudyBook\env_setter.ps1` (StudyBook `proj_educate` venv) → project `env_setter.ps1` (local `.venv` + `KB_INBOX_PATH`) → Grok Build TUI.

---

## Typical Workflows

### Change code
1. Edit `clipboard_app.py` (or scripts)
2. Test locally: `.\env_setter.ps1` then `.\run_app.bat`
3. Deploy: `.\deploy.ps1`
4. Restart running instance (see `GROK_DEPLOY_RUNBOOK.md`)
5. Update `GROK_AGENT_STATUS.md` and relevant memory files

### Change hotkeys only
1. Edit `settings.json` (not code)
2. Deploy or copy to `C:\scripts\UniversalClipboardManager`
3. Restart app process

### Agent session end
1. Update `GROK_AGENT_STATUS.md`
2. Log decisions in `GROK_DECISION_LOG.md`
3. Park side findings in `GROK_PARKING_LOT.md`
4. Update `GROK_OPEN_LOOPS.md` if gaps found

---

## File Inventory (GROK_*)

All Grok agent files live in `.agent/`:

- `GROK_INDEX.md` — this file
- `GROK_CONTEXT.md`
- `GROK_MEMORY.md`
- `GROK_ARCHITECTURE.md`
- `GROK_FILE_MAP.md`
- `GROK_DEPLOY_RUNBOOK.md`
- `GROK_OPERATING_RULES.md`
- `GROK_COMMAND_ALLOWLIST.md`
- `GROK_OPEN_LOOPS.md`
- `GROK_DECISION_LOG.md`
- `GROK_PARKING_LOT.md`
- `GROK_AGENT_STATUS.md`
- `GROK_PENDING_TASK.md`
- `GROK_USER_PREFERENCES.md`