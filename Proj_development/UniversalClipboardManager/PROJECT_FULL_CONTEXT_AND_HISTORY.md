# Universal Clipboard Manager - Full Project Context, History, and Current State

## Purpose of This Document

This file is a single, verbose, root-level record of the current repository, the deployed installation, the way the app works, how the environment is set up, what agent-related files exist, and the major changes that were made during the work on this project.

This document is intentionally written as an honest reconstruction from the repository contents and the confirmed machine state available while writing it.

That means:

- Facts that are visible in files are treated as confirmed.
- Facts that were directly verified on the machine are called out as verified.
- Conversation details that are not stored in the repo are summarized carefully rather than invented.
- If something expected by prior instructions is missing from the repo, that is stated directly.

The goal is to leave behind one file that a future human or agent can read to understand what this project is, where it lives, how it is deployed, how it is started, how its virtual environment is handled, what the current code does, and what changed recently.

## High-Level Summary

This project is a small Windows desktop utility written in Python. It acts as a clipboard snippet manager. It lets the user:

- keep a saved list of text snippets,
- bring up a window to browse those snippets,
- copy one of them back into the system clipboard,
- auto-paste the selected snippet into the previously active application,
- capture the current contents of the clipboard into the manager using a global hotkey,
- keep the app available through the Windows system tray,
- and configure the global shortcuts through a JSON settings file.

The application is built around:

- `PyQt6` for the user interface and system tray integration,
- `pynput` for global keyboard shortcuts,
- `pyperclip` for clipboard access,
- JSON files for local persistence.

## Important Paths

### Codebase location

The source repository is located at:

`D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`

### Deployment location

The deployed copy of the app is located at:

`C:\scripts\UniversalClipboardManager`

### Verified Windows startup shortcut

The Windows Startup shortcut was verified as present at:

`C:\Users\shareuser\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\UniversalClipboardManager.lnk`

This means the app is configured to start automatically when the user signs into Windows, assuming the shortcut target remains valid.

## What the Application Does

At its core, the app is a simple clipboard history and snippet launcher. It stores text items in a local JSON file and shows them in a vertical list. Each saved snippet appears as a card with buttons to:

- copy the snippet,
- edit the snippet,
- delete the snippet.

The key convenience feature is that when the user clicks `Copy`, the app:

1. puts the selected text into the Windows clipboard,
2. hides the main window,
3. waits briefly,
4. simulates `Ctrl+V`.

That means it is not only a storage app; it is meant to be used as a quick paste assistant during normal desktop work.

The second convenience feature is clipboard capture. The app can read whatever is currently in the system clipboard and save it into its list using a dedicated global hotkey or a tray menu action.

## Current User-Facing Behavior

As of the current code state, the app behaves like this:

- It starts as a tray-oriented application.
- It creates a system tray icon if the Windows tray is available.
- The main window starts hidden.
- Closing the window does not exit the process; it hides the window instead.
- The user can restore the window using a global show hotkey or by clicking the tray icon.
- The tray icon has a context menu with:
  - `Show / Hide`
  - `Capture Clipboard`
  - `Quit`

### Current default hotkeys

The current default hotkeys in the source code and `settings.json` are:

- Show or hide window:
  - primary: `F10`
  - fallback: `Ctrl+Alt+S`
- Capture current clipboard into manager:
  - primary: `F11`
  - fallback: `Ctrl+Alt+A`

These are configurable and are not hard-coded as the only possible runtime values. The app reads them from `settings.json` on startup.

## Honest Summary of What We Did Together

Based on the repository state and the visible progression of changes, the work that was done together included the following major steps.

### 1. We clarified the hotkey behavior

The app originally used hotkeys that did not fully match the intended workflow. There was a need to distinguish between two different actions:

- one shortcut to show the snippet selection window,
- another shortcut to take whatever is currently in the clipboard and add it into the manager.

That distinction is now present in the code.

### 2. We moved away from the original conflicting key choices

There was a practical hotkey conflict with the original show key combination using `Ctrl+Shift+S`, and there was also concern around `Ctrl+Shift+A`.

The project evolved through several shortcut adjustments, ending at:

- `F10` for show/hide,
- `F11` for capture.

These choices are now reflected in both the source code defaults and the configuration file.

### 3. We made hotkeys configurable

Instead of requiring code edits every time a hotkey conflicts with another application, the project now supports a `settings.json` file at the project root.

The code now:

- creates `settings.json` if it does not exist,
- loads the configured key lists at startup,
- falls back to safe defaults if the JSON is missing or invalid,
- shows the active shortcuts in a small label inside the main window.

This is a meaningful usability improvement because it separates user customization from source edits.

### 4. We aligned deployment with configuration

The deploy script was updated so that `settings.json` is copied into the deployed install directory at:

`C:\scripts\UniversalClipboardManager`

That matters because otherwise the deployed app could drift from the source repo configuration.

### 5. We shifted the app toward tray-based usage

The app now behaves like a tray utility rather than a normal always-open desktop window.

The code changes supporting that include:

- adding `QSystemTrayIcon`,
- adding a tray icon menu,
- allowing tray click or double-click to toggle the window,
- using `app.setQuitOnLastWindowClosed(False)` so hiding the last window does not shut down the program,
- starting the main window hidden.

This was specifically done so the app can live near the clock and remain available in the background.

### 6. We confirmed Windows startup behavior

The project already had `install_startup.ps1`, and the machine was checked to confirm that the startup shortcut exists in the Windows Startup folder.

So the intended behavior is:

- sign in to Windows,
- app starts automatically,
- app remains available via system tray.

### 7. We updated project documentation

The project already had `docs\handoff.md`, and that file was updated earlier to reflect the modern state:

- configurable hotkeys,
- `F10` and `F11`,
- tray behavior,
- deployment behavior,
- startup behavior.

### 8. We synchronized codebase and deployed instance

There was an explicit distinction made between:

- the codebase in `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`,
- the deployed runtime in `C:\scripts\UniversalClipboardManager`.

Changes were applied in the source repository, deployed forward into `C:\scripts\UniversalClipboardManager`, and the running app process was restarted to pick up those changes.

### 9. We noticed process duplication during restart work

During restart and validation, there were moments where multiple `pythonw.exe` processes appeared to be associated with the deployed app. This is worth recording honestly because it suggests the startup/restart path may occasionally produce duplicate running instances unless carefully managed.

The repo contains `cleanup_legacy_install.ps1`, which appears intended to help with exactly this sort of situation by:

- detecting running `clipboard_app.py` processes,
- stopping them,
- identifying duplicate or legacy Startup shortcuts,
- removing suspicious shortcuts.

That script is part of the project state and should be considered a maintenance tool for installed copies.

## Current Repository Contents

At the time this document was written, the top-level repository contained:

- `.agent\`
- `.venv\`
- `.vscode\`
- `docs\`
- `KB\`
- `.gitignore`
- `cleanup_legacy_install.ps1`
- `clipboard_app.py`
- `clipboard_data.json`
- `deploy.ps1`
- `env_setter.ps1`
- `install_startup.ps1`
- `launch_clipboard.bat`
- `requirements.txt`
- `run_app.bat`
- `setp_project.ps1`
- `settings.json`

There is also a `__pycache__` directory, which is normal for Python bytecode artifacts.

## Detailed Explanation of the Main Application Code

The main code is in:

`clipboard_app.py`

This file now contains several logical parts.

### 1. Path setup and persistence files

The code calculates `SCRIPT_DIR` so it can locate files relative to the running script. It then defines:

- `DATABASE_PATH` pointing to `clipboard_data.json`
- `SETTINGS_PATH` pointing to `settings.json`

This keeps the app self-contained whether it runs from the source folder or the deployed folder.

### 2. Default hotkey definitions

The file defines:

- `DEFAULT_SHOW_WINDOW_HOTKEYS`
- `DEFAULT_CAPTURE_CLIPBOARD_HOTKEYS`

At present those defaults are:

- show: `F10`, `Ctrl+Alt+S`
- capture: `F11`, `Ctrl+Alt+A`

### 3. Settings file handling

The code includes:

- `load_settings()`
- `ensure_settings_file()`

`load_settings()`:

- reads `settings.json`,
- accepts either a string or list for each hotkey group,
- normalizes values to lowercase strings,
- strips blanks,
- falls back to defaults if the file is missing or malformed.

`ensure_settings_file()`:

- creates a default `settings.json` if one is not already present.

This means the app is defensive and can still start even if the settings file is missing or damaged.

### 4. Clipboard data handling

The functions:

- `load_clipboard_data()`
- `save_clipboard_data(data)`

manage snippet persistence in `clipboard_data.json`.

`load_clipboard_data()` returns an empty list if the file is missing or broken. `save_clipboard_data()` writes the data back with indentation.

### 5. Global hotkey layer

The code defines:

- `HotkeySignals`
- `HotkeyThread`

`HotkeySignals` contains two Qt signals:

- `toggle_visibility`
- `add_from_clipboard`

`HotkeyThread`:

- runs a `pynput.keyboard.GlobalHotKeys` listener in the background,
- maps all configured show shortcuts to `toggle_visibility`,
- maps all configured capture shortcuts to `add_from_clipboard`,
- stops the listener when the app is shutting down.

This is the bridge between system-wide keyboard shortcuts and the Qt user interface.

### 6. Snippet card UI

Each saved item is rendered by `SnippetCard`.

Each card:

- shows the text in a read-only `QLineEdit`,
- offers `Copy`,
- offers `Edit`,
- offers delete via `X`.

The card delegates real actions to the parent main window.

### 7. Snippet editor dialog

`SnippetDialog` is the popup editor used for adding or editing text.

It contains:

- a `QTextEdit`,
- `OK` and `Cancel` buttons,
- a helper to return trimmed text.

### 8. Main window behavior

`ClipboardManagerApp` is the central controller.

Its responsibilities include:

- loading settings,
- loading snippet data,
- building the UI layout,
- creating the tray icon,
- starting the hotkey thread,
- handling add/edit/delete/copy behavior,
- toggling visibility,
- hiding instead of fully closing.

### 9. Tray behavior

The tray behavior is implemented by:

- `setup_system_tray()`
- `on_tray_icon_activated()`

This is a significant recent improvement. It changes the app from a simple floating utility window into a more native background desktop helper.

The code uses a standard Qt icon:

- `QStyle.StandardPixmap.SP_FileDialogDetailedView`

This means there is currently no custom `.ico` asset in the repository. The tray icon is functional, but it is not branded.

### 10. Copy-and-paste automation

`paste_snippet()`:

- copies text with `pyperclip.copy`,
- hides the window,
- processes Qt events,
- waits `0.2` seconds,
- simulates `Ctrl+V` using `pynput.keyboard.Controller`.

This is what makes snippet selection immediately useful in real workflows.

### 11. Clipboard capture behavior

`add_from_clipboard()`:

- reads the current clipboard text,
- strips whitespace,
- inserts it at the top of the list,
- avoids inserting it if it is empty,
- avoids inserting it if it matches the current top item.

So it is not a full historical clipboard monitor. It is an on-demand capture action triggered by the user.

### 12. Startup path in code

At the bottom of `clipboard_app.py`:

- the app waits one second before starting,
- creates `QApplication`,
- calls `app.setQuitOnLastWindowClosed(False)`,
- constructs the main window,
- connects cleanup of the hotkey thread to app exit,
- enters the event loop.

This is what enables tray persistence even when the main window is hidden.

## Configuration File: settings.json

The project currently contains:

```json
{
  "show_window_hotkeys": [
    "<f10>",
    "<ctrl>+<alt>+s"
  ],
  "capture_clipboard_hotkeys": [
    "<f11>",
    "<ctrl>+<alt>+a"
  ]
}
```

This file is now part of the expected runtime behavior. It is no longer just an optional extra; it is the user-editable configuration layer for shortcut behavior.

## Current Data File: clipboard_data.json

At the time this document was written, `clipboard_data.json` contains several saved string snippets. This confirms that the project stores real user data directly in the repository folder unless deployment redirects usage to the deployed copy.

That has two implications:

- the app is currently using local JSON persistence rather than a database,
- the snippet file should be treated as user data, not merely test data.

Future maintainers should be careful not to overwrite or erase `clipboard_data.json` casually.

## How the Virtual Environment Was Set Up

The user specifically asked not to forget this, so this section is explicit.

The project includes a setup script:

`setp_project.ps1`

This script is the main documented automation for preparing an installed runtime under `C:\scripts`.

### What `setp_project.ps1` does

It accepts parameters:

- `ProjectName`, defaulting to `UniversalClipboardManager`
- `InstallRoot`, defaulting to `C:\scripts`

It then:

1. calculates the install directory,
2. copies runtime project files into that install directory,
3. creates a virtual environment inside the install directory if one does not already exist,
4. installs dependencies from `requirements.txt`,
5. prints instructions for running and startup setup.

### Exact venv path used by setup

The virtual environment is expected at:

`C:\scripts\UniversalClipboardManager\.venv`

### Python command used

The script uses:

`python -m venv <venvPath>`

So it depends on a working Python installation already being available on the system path.

### Pip used after venv creation

The script then uses:

`<venvPath>\Scripts\pip.exe`

to install requirements.

### Requirements installed

According to `requirements.txt`, the environment installs:

- `pynput==1.8.1`
- `pyperclip==1.9.0`
- `PyQt6==6.9.1`
- `PyQt6-Qt6==6.9.1`
- `PyQt6_sip==13.10.2`
- `six==1.17.0`

### Important honest note about setup coverage

`setp_project.ps1` currently copies:

- `clipboard_app.py`
- `clipboard_data.json`
- `env_setter.ps1`
- `launch_clipboard.bat`
- `run_app.bat`
- `install_startup.ps1`
- `cleanup_legacy_install.ps1`
- `requirements.txt`

It does **not** currently include `settings.json` in its `filesToCopy` array, even though `deploy.ps1` does.

That means there is a small inconsistency in the project:

- `deploy.ps1` copies `settings.json`
- `setp_project.ps1` does not currently copy `settings.json`

This is an important maintenance note because a fresh setup using `setp_project.ps1` alone may not carry over the current hotkey config file unless the app creates it later from defaults.

## How the Runtime Environment Is Activated

The project includes:

`env_setter.ps1`

This script:

1. finds `.venv\Scripts\Activate.ps1`,
2. activates the local virtual environment,
3. prints the active Python path,
4. ensures the KB inbox folder exists,
5. sets `KB_INBOX_PATH`,
6. also assigns the same path to `$global:kbInboxPath`.

### KB path created or used

`env_setter.ps1` ensures:

`KB\00_Inbox`

exists under the project root.

### Environment variable set

It sets:

`KB_INBOX_PATH`

This is part of the project's "Second Brain" or knowledge-base integration.

## How the App Is Launched

### launch_clipboard.bat

`launch_clipboard.bat`:

- changes into the script directory,
- starts PowerShell hidden,
- runs `env_setter.ps1`,
- then runs `run_app.bat`.

This is the higher-level launcher intended to make sure the environment is prepared before the UI starts.

### run_app.bat

`run_app.bat`:

- checks for `.venv\Scripts\pythonw.exe`,
- if present, launches `clipboard_app.py` with it,
- otherwise falls back to plain `pythonw`.

This is the direct app runner.

## Deployment Flow

The project includes:

`deploy.ps1`

This script deploys the source app into:

`C:\scripts\UniversalClipboardManager`

### Files copied by deploy

`deploy.ps1` copies:

- `clipboard_app.py`
- `clipboard_data.json`
- `settings.json`
- `env_setter.ps1`
- `launch_clipboard.bat`
- `run_app.bat`
- `install_startup.ps1`
- `cleanup_legacy_install.ps1`
- `requirements.txt`

### Data-file handling during deploy

The script also has explicit handling for `clipboard_data.json`.

If a source data file exists, it copies it to the deployment target. If not, and the target file does not exist, it creates an empty `[]` file.

This means deploy is currently opinionated about user data and may overwrite the deployed clipboard data with the source copy if the source file exists.

That is a notable operational detail and should be remembered.

## Windows Startup Setup

The project includes:

`install_startup.ps1`

This script:

- points at the current folder as the install target,
- creates a `.lnk` shortcut in the Windows Startup folder,
- points that shortcut to `launch_clipboard.bat`,
- sets the shortcut window style to minimized.

The intended flow is:

1. deploy or install the app,
2. run `install_startup.ps1` from the installed directory,
3. Windows launches the app automatically on next login.

### Verified status on this machine

While writing this document, the presence of:

`C:\Users\shareuser\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\UniversalClipboardManager.lnk`

was explicitly verified.

So startup is not just theoretical; it appears to have been configured on this machine.

## Cleanup and Legacy-Install Handling

The project includes:

`cleanup_legacy_install.ps1`

This script is meant to help detect and remove old or conflicting installs.

It does two main things:

1. scans running processes whose command line mentions `clipboard_app.py`,
2. inspects Startup-folder shortcuts for duplicate or suspicious clipboard-related links.

It is designed to stop:

- processes running from the current project path,
- suspicious legacy processes from other locations.

It also removes duplicate startup shortcuts if they point to clipboard-related targets but are not named `UniversalClipboardManager.lnk`.

This is a useful support script, especially because duplicate background instances were observed during restart work.

## Agent-Related Files

The user specifically asked what the "agent files" are, so this section focuses on that.

### Confirmed agent folder contents

The repository contains:

`.agent\project_context.md`

This is the only file found under `.agent` during the file scan used to build this document.

### What `.agent\project_context.md` says

It describes:

- the project overview,
- `KB_INBOX_PATH`,
- the external documentation drop path,
- some brief interaction history about setup and KB integration.

It is not application runtime code. It is context for agents or automated helpers working in this repo.

### Important honesty note about missing expected control files

Earlier operating instructions referenced a broader control-file structure, including things like:

- `CONTROL_PROTOCOL.md`
- `agents/shared/context_index.md`
- `agents/shared/open_loops.md`
- `agents/shared/approval_matrix.md`
- `agents/shared/command_allowlist.md`
- `docs/adr/ADR-INDEX.md`
- and several other `agents/shared/*` files

Those files were **not** present in the repository root when the repo was inspected for this document.

So the honest current state is:

- the repo contains `.agent\project_context.md`,
- the repo does **not** currently contain the broader control-protocol file tree that some earlier instructions referenced.

This matters because future agents should not assume those files exist unless they are later added to the project.

## Documentation Files

### docs\handoff.md

This file already exists and acts as a practical handoff summary.

It documents:

- app purpose,
- current hotkeys,
- tray behavior,
- deployment path,
- startup path,
- file descriptions,
- maintenance notes.

The newer root-level document you are reading now is broader and more narrative than `docs\handoff.md`.

## Other Supporting Files

### requirements.txt

This pins the Python dependencies required to run the app.

### .gitignore

The `.gitignore` excludes:

- Python cache files,
- virtual environments such as `.venv`,
- IDE folders like `.idea`,
- local `.env` files,
- build output folders.

Interestingly, `.vscode` is commented out rather than actively ignored, meaning VS Code files may be intentionally kept in the repository depending on local practice.

## Current Hotkey Configuration and Why It Matters

The current configuration reflects real user feedback from practical usage:

- `Ctrl+Shift+S` conflicted with other apps.
- `Ctrl+Shift+A` was also not acceptable.
- the app therefore moved toward function-key-based defaults:
  - `F10` for showing the app,
  - `F11` for capturing clipboard content.

This is one of the most important recent user-driven changes because global shortcuts are only useful if they do not collide with existing daily tools.

## Current Confirmed Machine-Level State

The following were verified while building this document:

- the source repo exists at `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`
- the deployment target exists at `C:\scripts\UniversalClipboardManager`
- the startup shortcut exists in the Windows Startup folder
- the source repo contains `settings.json` with `F10` and `F11`
- the main code includes tray support and configurable hotkeys

These are not guesses; they were directly checked.

## Known Gaps, Risks, and Maintenance Notes

This section is intentionally candid.

### 1. Possible duplicate instances

During prior restart work, more than one `pythonw.exe` instance appeared tied to the app. The project has cleanup tooling, but the startup and restart process may still benefit from stronger single-instance protection in code.

There is currently no obvious lock-file or mutex-based single-instance guard in `clipboard_app.py`.

### 2. No custom tray icon asset

The tray icon uses a generic Qt standard icon rather than a custom project icon. This is fine functionally, but it is not polished branding.

### 3. Data overwrite risk in deploy

Because `deploy.ps1` copies `clipboard_data.json` from source to target when present, there is some risk of overwriting deployed user data with the source copy.

### 4. Setup/deploy inconsistency

`deploy.ps1` copies `settings.json`, but `setp_project.ps1` currently does not. That mismatch should probably be corrected in the future.

### 5. No persistent background clipboard monitoring

The app captures clipboard content only when explicitly triggered. It is not a full passive clipboard-history daemon.

That is not a bug, but it is an important behavior definition.

## Plain-English Summary for a New Person

If someone new opens this project, the quickest truthful summary is:

This is a Python/PyQt6 clipboard snippet manager for Windows. It stores snippets in JSON, lets you paste them back quickly, supports global hotkeys, can capture the current clipboard into its own list, and now behaves like a tray app that stays available by the clock. The source code lives in `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`, and the installed copy lives in `C:\scripts\UniversalClipboardManager`. The runtime uses a `.venv` virtual environment, set up by `setp_project.ps1`, and `install_startup.ps1` creates a Windows Startup shortcut so the app launches on login. The current default shortcuts are `F10` to show the window and `F11` to capture clipboard content. The main recent changes were configurable hotkeys, deployment of `settings.json`, tray integration, and startup/tray-oriented behavior.

## Final State Snapshot

At the time of writing this file, the project can be described as:

- a working Python desktop utility,
- deployed separately from the source repo,
- configured for Windows startup,
- configured for system tray use,
- using `F10` and `F11` as its primary hotkeys,
- storing snippets locally in JSON,
- using a local virtual environment,
- carrying a small amount of agent metadata in `.agent\project_context.md`,
- and containing maintenance scripts for setup, deploy, startup, and cleanup.

This document should be updated again whenever any of the following change:

- hotkeys,
- tray behavior,
- setup or deploy scripts,
- deployment path,
- startup behavior,
- virtual environment location,
- agent-file structure,
- or persistence model.
