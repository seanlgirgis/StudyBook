# GROK Memory — Durable Facts

**Last updated:** 2026-06-17  
**Source:** `PROJECT_FULL_CONTEXT_AND_HISTORY.md`, repo inspection, user session

---

## Verified Machine State (2026-06-17)

- [x] Source repo exists at `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`
- [x] Deploy target exists at `C:\scripts\UniversalClipboardManager`
- [x] Startup shortcut exists: `C:\Users\shareuser\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\UniversalClipboardManager.lnk`
- [x] `settings.json` in source has `F10` / `F11` hotkeys
- [x] `clipboard_app.py` includes tray support and configurable hotkeys
- [x] Local `.venv` present in project directory
- [x] User machine: `asuspc`, Windows 10

---

## Hotkey History (Why F10/F11)

| Era | Show | Capture | Problem |
|-----|------|---------|---------|
| Original | `Ctrl+Shift+S` | — | Conflicted with other apps |
| Intermediate | various | `Ctrl+Shift+A` | Also unacceptable to user |
| **Current** | `F10` (+ `Ctrl+Alt+S` fallback) | `F11` (+ `Ctrl+Alt+A` fallback) | Function keys less likely to conflict |

Hotkeys are **runtime-configurable** via `settings.json`; code defaults are fallbacks only.

---

## Data Files — Treat As User Data

### `clipboard_data.json`
- Array of strings (snippets)
- Lives next to running script (`SCRIPT_DIR`)
- **Deploy overwrites** deployed copy when source file exists
- Do not wipe casually during dev

### `settings.json`
- `show_window_hotkeys`: list or string of pynput-format keys
- `capture_clipboard_hotkeys`: same
- Created automatically if missing (`ensure_settings_file()`)
- Malformed JSON → code defaults used

---

## Code Structure Memory (`clipboard_app.py`)

| Section | Classes / Functions |
|---------|---------------------|
| Paths | `SCRIPT_DIR`, `DATABASE_PATH`, `SETTINGS_PATH` |
| Settings | `load_settings()`, `ensure_settings_file()` |
| Data | `load_clipboard_data()`, `save_clipboard_data()` |
| Hotkeys | `HotkeySignals`, `HotkeyThread` |
| UI cards | `SnippetCard` |
| Editor | `SnippetDialog` |
| Main | `ClipboardManagerApp` |
| Entry | `__main__`: 1s delay, `setQuitOnLastWindowClosed(False)`, start hidden |

**Key behaviors:**
- `paste_snippet`: copy → hide → 200ms → Ctrl+V
- `add_from_clipboard`: read clipboard, skip empty/duplicate-of-top
- `closeEvent`: ignore → hide (tray keeps running)
- Tray: standard Qt icon `SP_FileDialogDetailedView`

---

## Script Behavior Memory

### `deploy.ps1`
- Copies listed files to `C:\scripts\UniversalClipboardManager`
- **Includes** `settings.json`
- Always overwrites `clipboard_data.json` from source if source exists

### `setp_project.ps1`
- Fresh install to `C:\scripts\<ProjectName>`
- Creates `.venv`, pip installs requirements
- **Does NOT** copy `settings.json` (gap — app creates defaults on first run)

### `install_startup.ps1`
- Creates minimized `.lnk` in Windows Startup → `launch_clipboard.bat`

### `cleanup_legacy_install.ps1`
- Stops `clipboard_app.py` processes
- Removes duplicate/suspicious startup shortcuts

### `launch_clipboard.bat` → `env_setter.ps1` → `run_app.bat`
- `run_app.bat` prefers `.venv\Scripts\pythonw.exe`

### `env_setter.ps1` (project-local)
- Activates `.\.venv`
- Sets `KB_INBOX_PATH` → `KB\00_Inbox`

---

## What This App Is NOT

- Not a passive clipboard history daemon (capture is explicit only)
- Not cross-platform (Windows-focused: tray, startup, pynput)
- Not a sync/cloud clipboard tool
- Not using StudyBook parent venv for runtime (uses own `.venv`)

---

## Grok Launcher (Dual-Copy Pattern)

Same pattern as `start_grok_learning.ps1`:

| Copy | Path | Role |
|------|------|------|
| Runtime | `D:\start_grok_ucm.ps1` | Daily use — frozen on D: |
| Repo | `...\UniversalClipboardManager\start_grok_ucm.ps1` | Git-tracked archive |

**Keep both identical** when changes are ever required.

**Startup command:**
```powershell
pwsh -ExecutionPolicy Bypass -File "D:\start_grok_ucm.ps1"
```

**Environment chain (in order):**
1. `D:\Workarea\StudyBook\env_setter.ps1 -NonInteractive` — StudyBook venv (`C:\py_venv\proj_educate`)
2. `<project>\env_setter.ps1` — local `.venv` + `KB_INBOX_PATH`
3. `grok --cwd <project>` with GROK bootstrap rules

---

## User Session Notes (2026-06-17)

- User wants **Grok** as the controlling agent for this directory
- Agent files use **`GROK_` prefix** in `.agent/`
- User ran StudyBook `env_setter.ps1` first (proj_educate venv)
- Initial `cd /D:/...` failed — Windows PowerShell needs `D:\...` syntax
- User asked Grok to study `PROJECT_FULL_CONTEXT_AND_HISTORY.md` and establish local memory

---

## Maintenance Triggers (Update Memory When…)

- Hotkeys or `settings.json` schema change
- Deploy path or script file lists change
- Tray/startup behavior changes
- Single-instance or icon work completed
- New agent conventions adopted