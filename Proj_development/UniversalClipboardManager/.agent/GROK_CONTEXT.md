# GROK Context — Universal Clipboard Manager

**Last updated:** 2026-06-17

---

## One-Sentence Summary

A small Windows desktop utility that stores text snippets in JSON, exposes them via a PyQt6 tray app with global hotkeys, and auto-pastes selected snippets into the previously active application.

---

## What It Does For The User

1. **Store snippets** — saved text list in `clipboard_data.json`
2. **Browse & pick** — vertical card list in a popup window (`F10` to show/hide)
3. **Copy + auto-paste** — Copy button puts text on clipboard, hides window, simulates `Ctrl+V`
4. **Capture clipboard** — `F11` saves current system clipboard into the list (on-demand, not passive monitoring)
5. **Tray persistence** — runs in system tray; closing window hides, does not quit
6. **Configurable hotkeys** — `settings.json` without code edits

---

## Technology Stack

| Layer | Library / Tool |
|-------|----------------|
| UI | PyQt6 (`QMainWindow`, `QSystemTrayIcon`, dialogs) |
| Global hotkeys | `pynput.keyboard.GlobalHotKeys` in `HotkeyThread` |
| Clipboard I/O | `pyperclip` |
| Paste simulation | `pynput.keyboard.Controller` |
| Persistence | JSON files (no database) |
| Launcher | PowerShell + batch (`launch_clipboard.bat`, `run_app.bat`) |
| Python | 3.x via local `.venv` or deployed `.venv` |

**Pinned deps** (`requirements.txt`): `PyQt6==6.9.1`, `pynput==1.8.1`, `pyperclip==1.9.0`, plus transitive pins.

---

## Two Locations (Critical)

| Role | Path |
|------|------|
| **Source / dev** | `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager` |
| **Deployed / runtime** | `C:\scripts\UniversalClipboardManager` |

Changes made in source do **not** affect the running app until deployed and restarted.

---

## Environment Setup (User Machine)

The user activates StudyBook environment before working:

```powershell
D:
cd D:\Workarea\StudyBook
.\env_setter.ps1          # StudyBook-level venv: C:\py_venv\proj_educate
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\env_setter.ps1          # Project-local .venv activation + KB_INBOX_PATH
```

**Note:** Use `D:\...` paths in PowerShell, not `/D:/...` (that syntax fails on Windows).

---

## Integration With StudyBook

- Subproject under `Proj_development\UniversalClipboardManager`
- KB drop zone: `KB\00_Inbox` (env var `KB_INBOX_PATH`)
- External docs for Second Brain ingestion go to KB inbox
- Parent `CONTROL_PROTOCOL.md` applies for cross-repo work

---

## Current Maturity

**Working and deployed.** Recent improvements (2026-06):

- Configurable hotkeys via `settings.json`
- Tray-based background operation
- Separate show vs capture shortcut groups
- `F10` / `F11` defaults (moved away from `Ctrl+Shift+*` conflicts)
- `deploy.ps1` copies `settings.json`

**Not yet polished:**

- No single-instance guard (duplicate `pythonw.exe` possible)
- Generic Qt tray icon (no custom `.ico`)
- `setp_project.ps1` omits `settings.json` (inconsistency with `deploy.ps1`)

---

## Primary Reference Documents

| Document | Role |
|----------|------|
| `PROJECT_FULL_CONTEXT_AND_HISTORY.md` | Verbose narrative + verified machine state |
| `docs/handoff.md` | Concise operational handoff |
| `.agent/project_context.md` | Legacy minimal agent context (KB focus) |
| `.agent/GROK_*.md` | Grok agent durable memory (preferred for Grok sessions) |