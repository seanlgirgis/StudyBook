# aux_scripts

Small helper utilities for local project operations and validation.

These scripts are support tooling only. They are not app logic, backend logic, RAG logic, or deployment logic.

## Scripts

### `show_tree.ps1`
- Recursively prints a directory tree.
- Includes file sizes in KB.
- Excludes common junk folders:
  - `.git`
  - `__pycache__`
  - `.pytest_cache`
  - `.venv`
  - `node_modules`
  - `dist`
  - `build`
- Read-only script.

Example:

```powershell
.\aux_scripts\show_tree.ps1 -Path ".\pocs\01_static_site_shell"
```

### `zip_folder_for_chatgpt.ps1`
- Creates a timestamped zip from a required source folder.
- Writes output zip to the current user's `Downloads` folder.
- Zip file name includes source folder name and timestamp.
- Excludes the same junk folders listed above.
- Does not delete or modify source files.

Example:

```powershell
.\aux_scripts\zip_folder_for_chatgpt.ps1 -Path ".\pocs\01_static_site_shell"
```

### `check_poc_static_site.ps1`
- Validates the static site POC under `pocs/01_static_site_shell`.
- Confirms required files exist.
- Confirms `index.html` references `assets/styles.css` and `assets/chat-widget.js`.
- Confirms no backend/API patterns are present (`fetch`, `XMLHttpRequest`, `axios`, `/api`, `localhost`, `http://`, `https://`).
- Prints clear PASS/FAIL output.

Example:

```powershell
.\aux_scripts\check_poc_static_site.ps1
```

### `snapshot_project_state.ps1`
- Creates a timestamped snapshot folder at `aux_scripts/snapshots/`.
- Copies root control/memory files if they exist:
  - `AGENTS.md`
  - `PROJECT_STATE.md`
  - `TASK_BOARD.md`
  - `HANDOFF.md`
  - `DAILY_LOG.md`
  - `DECISIONS.md`
  - `KNOWN_ISSUES.md`
  - `CHANGELOG.md`
- Prints snapshot folder path.
- Does not modify source files.

Example:

```powershell
.\aux_scripts\snapshot_project_state.ps1
```
