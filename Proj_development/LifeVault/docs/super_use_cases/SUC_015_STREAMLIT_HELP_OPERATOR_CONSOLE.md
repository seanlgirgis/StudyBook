# SUC_015_STREAMLIT_HELP_OPERATOR_CONSOLE.md

## Purpose

Define SUC_015 v0 as a **Help / Usability / Operator Console** for LifeVault.

This first app is guidance-first, not automation-first.

## v0 Identity

The Streamlit v0 app is:
- a safe read-only operator helper
- a workflow orientation layer
- a command/runbook assistant

The Streamlit v0 app is not:
- a destructive control plane
- a secrets viewer
- a cloud sync tool
- an auto shell executor

## Primary User Question

When Sean opens the app, he should quickly answer:

"What can I safely do now?"

## Sections

### A. Start Here

- what LifeVault is
- what is proven now
- what is not implemented yet
- safe next actions

### B. Runbook Helper (Command Generator Only)

User selects workflow and sees exact PowerShell commands:
- create note
- search notes
- create note folder
- list note folders
- create sensitive Phase 0 placeholder
- search sensitive public_hint metadata
- file/folder lifecycle runbook link

v0: display commands only, do not execute.

### C. Current Capability Status

Show clear status cards:
- file/folder lifecycle v0: proven
- notes create/search v0: implemented
- note_folder create/list/search v0: implemented
- sensitive note Phase 0: implemented (layout-only)
- real encryption: not implemented
- OneDrive/cloud sync: not implemented
- contacts/email/physical inventory: not implemented

### D. Read-Only Notes Search

- search normal notes
- search note folders
- search sensitive note metadata/public_hint only
- never display protected body
- show `unlock_required` for sensitive rows

### E. Safety Panel

Show persistent warnings:
- Phase 0 sensitive notes are not real encryption
- no real secrets in Phase 0
- no OneDrive upload from this app
- no destructive actions from this app

### F. Project Task Seed Viewer

- read `docs/tasks/LIFEVAULT_PROJECT_TASK_SEED.md`
- display major task groups and suggested next bites

## Read-Only Rule (Hard Boundary)

v0 app must not:
- delete
- move
- publish
- cleanup
- decrypt
- write DB
- write sensitive payload
- run shell commands automatically

v0 app may:
- read docs
- read notes and note-folder manifests
- render command templates
- display capability status
- run read-only note metadata/body search using existing logic

## Future Phases

- Phase 1: read-only help/operator console
- Phase 2: safer copy-command UX and guided command templates
- Phase 3: controlled write actions with explicit approvals
- Phase 4: unlock/sensitive views only after real crypto exists

## Acceptance Checklist (SUC_015 v0)

- starts in Docker
- has Start Here page
- shows current capabilities
- shows runbook helper commands
- supports read-only notes search
- shows sensitive metadata only
- does not display protected body
- no write/destructive actions
- no shell execution from UI
- no OneDrive/rclone actions
- repo tests remain green

## Phase 1 Status

- Streamlit app skeleton implemented as read-only help console.
- Sections included: Start Here, Current Capability Status, Runbook Helper, Safety Panel, Project Task Seed Viewer.
- Static/docs-backed content is used in this phase.
- Docker compose service configured with restart policy for reboot resilience.
- Optional scheduled task installer provided to start stack at user logon.

## Phase 2 Status

- interactive command builder added (still generate-only)
- read-only notes inventory added
- sidebar navigation introduced for usability
- app remains strictly read-only and non-executing
