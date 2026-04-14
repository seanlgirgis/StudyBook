# Agent Startup Note

Read this file at the start of every new session in this repository.

## Required Basics

1. Python environment setup:
   - Run:
     - `.\env_setter.ps1 -NonInteractive`
   - If needed in interactive shells:
     - `.\env_setter.ps1`

2. Path rule:
   - Always use relative paths in commands and scripts.
   - Do not use absolute paths unless explicitly requested.

3. Mounted repositories currently in use:
   - `temp/jobsearch`
   - `temp/seanlgirgis.github.io`

## Session Kickoff Rule

When user says "high" (or "hi"), ask to confirm this file is being followed, then continue.

## Context Key Map

Use these key-value entries to load task-specific operating context:

- `JobSearch` => `JOBSEARCH_AGENT_CONTEXT.md`

If user says: "AGENT_STARTUP_NOTE.md and JobSearch"
then read this file, resolve the key, and ingest `JOBSEARCH_AGENT_CONTEXT.md` before doing work.
