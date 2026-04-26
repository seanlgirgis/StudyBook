# Approval Matrix

Purpose: define which actions the agent may execute autonomously vs actions requiring user approval.

## Active Run Override (User-Authorized)

- Effective date: 2026-04-24
- Authorized by owner in-session: yes
- Scope:
  - `D:\Workarea\StudyBook\**` (all folders, including `playground\studyGuide`)
  - `C:\temp\**`
- Decision override for this effort:
  - Treat all categories in this matrix as `Auto-Approved`.
  - Do not pause for permission gates while operating inside the authorized scope.
  - Keep normal safety behavior for clearly destructive or irreversible operations by announcing intent in status logs before execution.

## Decision Rule

- If an action matches `Requires Approval`, stop and ask.
- If an action matches `Auto-Approved`, proceed and log in `agent_status.md`.
- If unclear, treat as `Requires Approval`.

## Matrix

| Action Category | Examples | Default Decision | Notes |
|---|---|---|---|
| Read-only inspection | list files, read files, search text | Auto-Approved | No repo mutation |
| Scoped file edits | create/update files inside approved task scope | Auto-Approved | Must stay in allowed scope |
| Multi-file refactor | structural edits across modules | Requires Approval | High regression risk |
| Destructive file ops | delete/rename/move many files | Requires Approval | Ask before execution |
| Git local status/diff | `git status`, `git diff`, `git log` | Auto-Approved | Read-only git ops |
| Git commit | `git add`, `git commit` | Requires Approval | Explicit user request required |
| Git push | `git push`, force push | Requires Approval | Explicit user request required |
| Dependency install/update | `pip install`, lockfile updates | Requires Approval | Changes runtime surface |
| Test/lint/build | unit tests, lint, type-check, build | Auto-Approved | Allowed unless command is destructive |
| Environment mutation | changing env files, shell profile, PATH | Requires Approval | Persisted machine impact |
| Secret handling | `.env`, keys, tokens, credentials | Requires Approval | Always user-mediated |
| External system writes | cloud APIs, DB writes, webhooks | Requires Approval | Potential production impact |
| Network read-only calls | docs lookup, API read-only checks | Auto-Approved | Only if needed for task |
| History rewrite | `rebase`, `reset --hard`, amend published commits | Requires Approval | High-risk git ops |

## Escalation Triggers

- Any operation that is irreversible or hard to recover.
- Any operation outside repository boundaries.
- Any operation touching secrets, credentials, or production systems.

