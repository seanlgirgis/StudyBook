# GROK File Map — Universal Clipboard Manager

**Last updated:** 2026-06-17

---

## Root — Application & Runtime

| File | Type | Purpose | Agent notes |
|------|------|---------|-------------|
| `clipboard_app.py` | Python | Main app (~526 lines) | Primary edit target for features/fixes |
| `clipboard_data.json` | Data | Snippet list (JSON array) | **User data** — deploy may overwrite |
| `settings.json` | Config | Hotkey bindings | User-editable; restart required |
| `requirements.txt` | Deps | Pinned Python packages | Edit when adding libraries |
| `.gitignore` | Git | Ignores `.venv`, `__pycache__`, etc. | `.vscode` commented out (may be tracked) |

---

## Root — Scripts & Launchers

| File | Purpose |
|------|---------|
| `start_grok_ucm.ps1` | **Repo copy** — Grok Build launcher (keep identical to `D:\start_grok_ucm.ps1`) |
| `D:\start_grok_ucm.ps1` | **Runtime copy** — frozen D: launcher (not in repo path) |
| `env_setter.ps1` | Activate local `.venv`; set `KB_INBOX_PATH` |
| `run_app.bat` | Launch `clipboard_app.py` via `pythonw` |
| `launch_clipboard.bat` | Hidden PS → env_setter → run_app (startup entry) |
| `deploy.ps1` | Copy app files to `C:\scripts\UniversalClipboardManager` |
| `setp_project.ps1` | Fresh install + venv create at `C:\scripts\...` |
| `install_startup.ps1` | Create Windows Startup shortcut |
| `cleanup_legacy_install.ps1` | Kill duplicate processes; clean bad shortcuts |

---

## Directories

| Path | Purpose |
|------|---------|
| `.agent/` | Agent context (`project_context.md`, `GROK_*.md`) |
| `.venv/` | Local Python virtual environment (gitignored) |
| `.vscode/` | VS Code workspace settings |
| `docs/` | Human documentation (`handoff.md`) |
| `KB/` | Knowledge base; `00_Inbox` for external doc drops |
| `__pycache__/` | Python bytecode (generated) |

---

## Documentation

| File | Audience | Content |
|------|----------|---------|
| `PROJECT_FULL_CONTEXT_AND_HISTORY.md` | Human + any agent | Verbose full history and machine verification |
| `docs/handoff.md` | Human + agent | Concise operational handoff |
| `.agent/project_context.md` | Legacy agents | KB integration brief |
| `.agent/GROK_*.md` | Grok agent | Durable Grok-specific memory |

---

## Deploy Copy Sets

### `deploy.ps1` copies:
`clipboard_app.py`, `clipboard_data.json`, `settings.json`, `env_setter.ps1`, `launch_clipboard.bat`, `run_app.bat`, `install_startup.ps1`, `cleanup_legacy_install.ps1`, `requirements.txt`

### `setp_project.ps1` copies (missing `settings.json`):
`clipboard_app.py`, `clipboard_data.json`, `env_setter.ps1`, `launch_clipboard.bat`, `run_app.bat`, `install_startup.ps1`, `cleanup_legacy_install.ps1`, `requirements.txt`

---

## Deployed Install (Not in Repo)

`C:\scripts\UniversalClipboardManager\` mirrors deploy output plus `.venv` created by setup.

---

## Files Grok Should Not Touch Without Reason

| File | Reason |
|------|--------|
| `clipboard_data.json` | Live user snippets |
| `.venv/` | Generated environment |
| `__pycache__/` | Generated |

---

## GROK Agent Files (`.agent/`)

| File | Role |
|------|------|
| `GROK_INDEX.md` | Entry point |
| `GROK_CONTEXT.md` | Project summary |
| `GROK_MEMORY.md` | Durable facts |
| `GROK_ARCHITECTURE.md` | Technical design |
| `GROK_FILE_MAP.md` | This file |
| `GROK_DEPLOY_RUNBOOK.md` | Ops procedures |
| `GROK_OPERATING_RULES.md` | Agent rules |
| `GROK_COMMAND_ALLOWLIST.md` | Approved commands |
| `GROK_OPEN_LOOPS.md` | Open work |
| `GROK_DECISION_LOG.md` | Decision history |
| `GROK_PARKING_LOT.md` | Parked findings |
| `GROK_AGENT_STATUS.md` | Session status |
| `GROK_PENDING_TASK.md` | Active task contract |
| `GROK_USER_PREFERENCES.md` | User working style |