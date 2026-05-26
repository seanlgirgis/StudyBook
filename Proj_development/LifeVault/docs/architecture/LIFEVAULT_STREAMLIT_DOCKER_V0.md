# LIFEVAULT_STREAMLIT_DOCKER_V0.md

## Purpose

Define Docker-first runtime design for the LifeVault Streamlit Help/Operator Console v0.

## Ownership and Location

Prefer LifeVault-owned structure:

```text
app/streamlit/
docker/streamlit_dashboard/
```

Equivalent clear LifeVault-local structure is acceptable if consistent.

## v0 Container Intent

- provide repeatable local run environment
- emphasize read-only workflows
- avoid hidden machine dependencies

## Mount Strategy (v0)

Prefer read-only bind mounts for:
- LifeVault repository docs/code needed for display
- `D:\AI_Lab\LifeVault` notes/data inputs where practical

v0 should not require operational writes under `D:\AI_Lab\LifeVault`.

## App Runtime Behavior

- app reads docs/status/notes metadata
- app renders command templates only
- app does not execute shell commands in v0
- app does not perform DB writes
- app does not perform OneDrive/rclone actions

## Security and Safety

- no secrets in container logs
- no sensitive protected-body display in UI
- no unlock/decrypt operations in v0
- no destructive operations exposed in UI

## Suggested v0 Startup Shape

- docker compose service for streamlit app
- explicit mounted paths
- explicit environment variables for repo root / notes root
- read-only flag on mounts where supported
- service restart policy: `unless-stopped`
- startup helper script launches compose detached
- optional Windows scheduled task starts helper at user logon with delay

## Acceptance Markers

- Streamlit app starts in Docker
- app can read docs and note metadata
- app remains read-only by design
- no command execution side effects
- no cloud interactions

## Startup/Autostart Operations

Scripts:

- `scripts/start_streamlit_help_console_docker.ps1`
- `scripts/stop_streamlit_help_console_docker.ps1`
- `scripts/status_streamlit_help_console_docker.ps1`
- `scripts/install_streamlit_help_console_startup_task.ps1`
- `scripts/uninstall_streamlit_help_console_startup_task.ps1`

Verification target:

- `http://localhost:8501`
