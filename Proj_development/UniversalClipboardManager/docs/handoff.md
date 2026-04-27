# Universal Clipboard Manager - Project Handoff

## Overview
The **Universal Clipboard Manager** is a productivity tool designed to manage, store, and quickly retrieve text snippets. It features global hotkey support, automatic clipboard capture, and an "auto-paste" mechanism to streamline workflows.

## How It Works

### 1. Core Architecture
- **GUI Layer**: Built with **PyQt6**. The main window (`ClipboardManagerApp`) manages a scrollable list of "Snippet Cards".
- **Background Listener**: Uses the **`pynput`** library to monitor keyboard events globally. This allows the app to respond to hotkeys even when it is hidden or not in focus.
- **Clipboard Interaction**: Uses **`pyperclip`** to read from and write to the system clipboard.
- **Persistence**: Snippets are stored in `clipboard_data.json` in the root directory.

### 2. Operational Logic
- **Hotkey `Ctrl+Shift+S`**: Toggles the visibility of the application.
- **Hotkey `Ctrl+Alt+A`**: Triggers a "Capture" event. The app reads the current system clipboard and immediately adds it as a new snippet at the top of the list.
- **Auto-Paste Flow**: When a user clicks the "Copy" button on a snippet:
  1. The text is copied to the system clipboard.
  2. The app window hides itself.
  3. The app simulates a `Ctrl+V` keypress after a short delay (200ms) to paste the content into the previously active application.

### 3. Environment & Setup
- **Starter Script**: `env_setter.ps1` must be run first. It:
  - Activates the virtual environment at `c:\py_venv\commonEnv`.
  - Sets the `KB_INBOX_PATH` environment variable to `C:\pyproj\KB\00_Inbox` (integration with the Second Brain system).
- **Startup**: `install_startup.ps1` configures the application to launch automatically when Windows starts.
- **Launchers**:
  - `launch_clipboard.bat`: Main batch entry point.
  - `run_app.bat`: Quick execution script.

## File Inventory & Descriptions

| File | Description |
| :--- | :--- |
| `clipboard_app.py` | **Main Application Logic**. Contains the PyQt6 UI, Hotkey thread, and file I/O. |
| `clipboard_data.json` | JSON database storing all saved snippets. |
| `env_setter.ps1` | Environment bootstrap script (Venv activation & KB paths). |
| `install_startup.ps1` | Adds the application to the Windows Startup folder. |
| `setp_project.ps1` | Project initialization and dependency setup. |
| `deploy.ps1` | Deployment and update script. |
| `cleanup_legacy_install.ps1` | Removes old versions or conflicting installations. |
| `launch_clipboard.bat` | Batch file to start the app in the correct environment. |
| `requirements.txt` | Python dependencies (`PyQt6`, `pyperclip`, `pynput`). |
| `.agent/project_context.md` | Internal context for AI agents regarding KB integration. |

## Knowledge Base (KB) Integration
The project is configured to interact with a "Second Brain" system. 
- The `KB_INBOX_PATH` (`C:\pyproj\KB\00_Inbox`) is the designated drop-zone for any generated documentation or notes that need to be ingested into the broader knowledge system.

## Recommendations for Maintenance
- **Venv Sensitivity**: Ensure `c:\py_venv\commonEnv` exists and has the required packages installed via `requirements.txt`.
- **Hotkey Conflicts**: If `Ctrl+Shift+S` or `Ctrl+Alt+A` are used by other apps, they can be modified in the `HotkeyThread` class within `clipboard_app.py`.
