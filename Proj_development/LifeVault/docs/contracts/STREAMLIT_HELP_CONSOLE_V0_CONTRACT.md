# STREAMLIT_HELP_CONSOLE_V0_CONTRACT.md

## Purpose

Define the contract for the first Streamlit Help/Operator Console behavior.

## Contract Scope

Applies to SUC_015 v0 read-only console only.

## Required Views

1. Start Here
2. Runbook Helper
3. Current Capability Status
4. Read-only Notes Search
5. Safety Panel
6. Project Task Seed Viewer

## Runbook Helper Contract

Input:
- workflow selection

Output:
- exact PowerShell command template
- link/reference to relevant runbook/use-case docs

Constraint:
- UI must not execute command in v0

## Capability Status Contract

Must include status visibility for at least:
- SUC_006 file/folder lifecycle v0
- SUC_005 notes create/search v0
- note_folder create/list/search v0
- sensitive note Phase 0 status
- encryption not implemented
- OneDrive/cloud sync not implemented

## Read-only Notes Search Contract

Search scope:
- title
- tags
- story
- normal note body
- sensitive public_hint metadata

Search output fields:
- title
- path
- tags
- story
- match_type
- sensitivity_level
- unlock_required (for sensitive notes)

Forbidden display:
- protected body payload
- decrypted sensitive content

## Safety Panel Contract

Must always show:
- Phase 0 sensitive notes are not real encryption
- do not use real secrets in Phase 0 flow
- no OneDrive/rclone actions in UI
- no destructive/write actions in UI

## Hard v0 Prohibitions

The app must not perform:
- delete/move/cleanup/publish actions
- DB writes
- shell command execution
- unlock/decrypt/view of protected payload
- cloud sync/upload

## Acceptance Gates

- app runs in Docker
- docker compose uses `restart: unless-stopped`
- required views are present
- command templates display correctly
- Phase 1 may keep notes search as static guidance only
- sensitive metadata-only handling is preserved in design
- no protected-body output
- no write/destructive side effects
- no shell execution from UI

## Phase 1 Implementation Note

Implemented first app skeleton:

- `app/streamlit/lifevault_help_console.py`
- static/docs-backed sections
- no command execution
- no DB write/destructive/cloud/decrypt actions

## Phase 2 Read-Only Upgrade

- sidebar navigation added (`Home`, `Capability Status`, `Command Builder`, `Notes Inventory`, `Safety`, `Next Tasks`)
- command builders generate copyable commands only
- notes inventory reads markdown/file structure only
- protected payload files are not read/displayed
