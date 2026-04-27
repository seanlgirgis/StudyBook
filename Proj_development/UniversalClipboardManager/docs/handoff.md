# Universal Clipboard Manager - Project Handoff

## Overview
The **Universal Clipboard Manager** stores and reuses text snippets with global hotkeys.  
It supports two separate keyboard actions:
1. Show/hide the snippet picker window.
2. Capture current system clipboard text into the snippet list.

## Current State (Updated: 2026-04-27)
- Hotkeys are now **configurable** via `settings.json`.
- Two distinct actions are mapped to separate shortcut groups:
  - Show window: `Ctrl+Shift+S` (fallback `Ctrl+Alt+S`)
  - Capture clipboard to manager: `F11` (fallback `Ctrl+Alt+A`)
- `deploy.ps1` now copies `settings.json` into the deployed directory.
- Installed/deployed config was synced to match codebase defaults.
- App was restarted after config updates so new key mappings take effect.

## How It Works

### 1. Core Architecture
- **GUI Layer**: Built with **PyQt6** in `ClipboardManagerApp`.
- **Background Listener**: Uses **`pynput.keyboard.GlobalHotKeys`** in a dedicated `HotkeyThread`.
- **Clipboard I/O**: Uses **`pyperclip`** for read/write.
- **Persistence**:
  - Snippets: `clipboard_data.json`
  - Hotkey config: `settings.json`

### 2. Operational Logic
- **Show/Hide Action** (`toggle_visibility`):
  - Default keys: `Ctrl+Shift+S`, `Ctrl+Alt+S`
- **Capture Action** (`add_from_clipboard`):
  - Default keys: `F11`, `Ctrl+Alt+A`
  - Reads current clipboard text and inserts it at index 0 when non-empty and not duplicate of the newest entry.
- **Copy-and-Paste Flow** (`paste_snippet`):
  1. Copy selected snippet to system clipboard.
  2. Hide manager window.
  3. Wait ~200ms.
  4. Simulate `Ctrl+V`.

### 3. Hotkey Configuration
- Config file: `settings.json` in project root (also deployed to install folder).
- Expected structure:
```json
{
  "show_window_hotkeys": ["<ctrl>+<shift>+s", "<ctrl>+<alt>+s"],
  "capture_clipboard_hotkeys": ["<f11>", "<ctrl>+<alt>+a"]
}
```
- On startup:
  - If `settings.json` is missing, app creates it with defaults.
  - If malformed or invalid, app falls back to safe defaults.

## Environment, Run, and Deploy

### Local project path
- `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`

### Deployment target
- `C:\scripts\UniversalClipboardManager`

### Scripts
- `run_app.bat`: starts app via local `.venv\Scripts\pythonw.exe` if present, otherwise system `pythonw`.
- `deploy.ps1`: copies app files to `C:\scripts\UniversalClipboardManager` (now includes `settings.json`).
- `install_startup.ps1`: creates Startup shortcut to auto-launch app at login.
- `env_setter.ps1`: venv + KB environment setup.

## File Inventory & Descriptions

| File | Description |
| :--- | :--- |
| `clipboard_app.py` | Main application (UI, hotkey thread, settings loader, clipboard behavior). |
| `settings.json` | Configurable hotkeys for show/capture actions. |
| `clipboard_data.json` | Stored snippet list. |
| `deploy.ps1` | Deployment script to `C:\scripts\UniversalClipboardManager`. |
| `install_startup.ps1` | Startup shortcut installer. |
| `run_app.bat` | App launcher. |
| `launch_clipboard.bat` | Wrapper launcher used by startup flow. |
| `requirements.txt` | Python dependencies (`PyQt6`, `pyperclip`, `pynput`). |
| `.agent/project_context.md` | Agent context for KB integration. |

## Knowledge Base (KB) Integration
- `KB_INBOX_PATH` points to `.\KB\00_Inbox`.
- Use this as the drop-zone for external notes/docs intended for Second Brain ingestion.

## Maintenance Notes
- Ensure virtual environment exists at `.\.venv` and dependencies from `requirements.txt` are installed.
- If global hotkeys conflict with other apps, edit `settings.json` instead of code.
- After editing `settings.json`, restart the app process to load new bindings.
