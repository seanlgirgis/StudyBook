# Command Allowlist

Purpose: define default-safe command families the agent can run without extra approval.

## Active Run Override (User-Authorized)

- Effective date: 2026-04-24
- Authorized by owner in-session: yes
- Scope:
  - `D:\Workarea\StudyBook\**` (all folders, including `playground\studyGuide`)
  - `C:\temp\**`
- Command policy override for this effort:
  - Approval-gated command families are allowed without additional permission prompts when they are needed to complete the requested work inside the authorized scope.
  - This includes write/edit commands, dependency setup, git commit/push, environment updates, and external integrations requested by the owner.

## Allowlist (Default)

- `rg`, `rg --files`
- `Get-ChildItem`, `Get-Content`, `Select-String`
- `git status`, `git diff`, `git log`, `git show`, `git rev-parse`
- Language-native test/lint/build commands inside repo scope
- Read-only helper scripts in repo scope

## Conditional Allowlist

Allowed only when the task explicitly requires it:

- `python <script>` execution for validation
- `pytest`, `npm test`, `pnpm test`, `mvn test`, `go test`, `cargo test`
- `pip install -r ...` or dependency sync commands

## Blocked Without Approval

- `git push`, `git commit`, `git rebase`, `git reset --hard`, `git clean -fd`
- Mass delete/move commands
- Commands touching credential stores, keychains, or secret files
- Commands writing to external systems (databases, cloud services, web APIs)
- Any command outside repository scope unless explicitly requested

## Path Scope Rule

- Prefer repo-relative paths.
- Do not run write commands outside `D:\Workarea\StudyBook` unless user approved.
- For the active run override, write commands are also approved under `C:\temp`.

## Logging Rule

- Record meaningful commands run in `agents/shared/agent_status.md` under validation/work summary.

