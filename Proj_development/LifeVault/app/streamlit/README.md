# Streamlit Help Console v0

This app is the LifeVault SUC_015 Phase 1 read-only Help / Operator Console.

## Scope

- Read-only guidance UI
- Shows what is working now vs planned
- Shows interactive command builders (generate-only, no execution)
- Shows safety reminders and next-task orientation
- Shows read-only notes inventory summary

## Important

- No DB writes
- No shell execution from UI
- No OneDrive/rclone actions
- No decrypt/protected sensitive content view

## Run (PowerShell wrapper)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_streamlit_help_console.ps1
```

## Docker note

Shared StudyBook docker stacks exist under `D:\Workarea\StudyBook\docker`, but this app intentionally uses LifeVault-local Docker files under `docker/streamlit_dashboard`.

## Docker Service Control

Manual start:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_streamlit_help_console_docker.ps1
```

Manual stop:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop_streamlit_help_console_docker.ps1
```

Status:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\status_streamlit_help_console_docker.ps1
```

Install auto-start task:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_streamlit_help_console_startup_task.ps1
```

Uninstall auto-start task:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_streamlit_help_console_startup_task.ps1
```

Verify:

- open `http://localhost:8501`
