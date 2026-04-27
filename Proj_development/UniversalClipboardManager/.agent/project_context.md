# Univeral Clipboard Manager - Agent Context

## Project Overview
Universal Clipboard Manager allows syncing and managing clipboard content.

## Environment Variables
- `KB_INBOX_PATH`: Points to `.\KB\00_Inbox` under the project root. This is used for dropping files or notes for the Second Brain system.

## External Documentation Path
- **Path**: `.\KB\00_Inbox` (relative to project root)
- **Usage**: Use this path to generate external markdown notes, documentation, or reports related to this project that should be ingested by the Second Brain.

## Interaction History
- **Setup**: Added VS Code configuration (.vscode) and environment setter script updates.
- **KB Integration**: Added `KB_INBOX_PATH` to `env_setter.ps1` to facilitate interaction with the Knowledge Base.
