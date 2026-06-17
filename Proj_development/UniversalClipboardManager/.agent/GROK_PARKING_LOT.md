# GROK Parking Lot — Universal Clipboard Manager

**Last updated:** 2026-06-17

Out-of-scope findings and ideas parked for future runs. Not active work.

---

## Parked Ideas

### P-001: Settings UI panel
- In-app editor for hotkeys instead of manual JSON edit
- **Why parked:** Not requested; JSON editing works for single user

### P-002: Snippet categories / tags
- Organize growing snippet list
- **Why parked:** Current flat list sufficient for small utility

### P-003: Search/filter in snippet list
- Useful if snippet count grows large
- **Why parked:** No user pain reported yet

### P-004: Sync snippets across machines
- Cloud or git-based sync
- **Why parked:** Explicitly out of current scope (local JSON tool)

### P-005: Replace pyperclip with Qt clipboard API
- Reduce dependency; better Unicode on Windows
- **Why parked:** pyperclip works; refactor risk without user ask

---

## Parked Observations

### P-006: Typo in `setp_project.ps1` filename
- Script name is `setp_project.ps1` (not `setup_project.ps1`)
- **Note:** Keep actual filename when documenting/running

### P-007: Typo in legacy `.agent/project_context.md`
- Title says "Univeral" not "Universal"
- **Note:** Grok files use correct spelling; fix legacy file only if user wants

### P-008: Python 3.14 in `__pycache__`
- `clipboard_app.cpython-314.pyc` suggests Python 3.14 used locally
- **Note:** Verify compatibility if dep issues arise

### P-009: StudyBook parent venv vs project venv
- User activates `C:\py_venv\proj_educate` at StudyBook root, then project `.venv`
- App runtime uses project `.venv` via `run_app.bat`, not parent venv
- **Note:** Don't confuse the two when installing packages

---

## How to Promote

Move item to `GROK_OPEN_LOOPS.md` or `GROK_PENDING_TASK.md` when user requests work.