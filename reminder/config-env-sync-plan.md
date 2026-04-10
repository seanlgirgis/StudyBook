# Git Sync Reminder: config/env on New Machines

Date: 2026-04-09
Context: Test-day pause note

## What we found
- `config/env/base.psd1` is required for cross-machine bootstrap.
- It is currently not syncing to GitHub because `.gitignore` contains `ENV/`.
- On Windows, repo setting `core.ignorecase=true` makes `ENV/` match `env/`, so `config/env/*` gets ignored.

## Why this matters
- A new machine clone may miss `config/env/base.psd1`.
- Missing this file can block expected environment bootstrap behavior.

## Agreed plan (post-test)
1. Track required non-secret config in Git:
   - Ensure `config/env/base.psd1` is committed.
2. Keep machine-local data out of Git:
   - Keep `config/machines/*.local.psd1` ignored.
   - Keep plaintext secrets ignored.
3. Keep encrypted secrets as portable system of record:
   - Use tracked encrypted secret files.
   - Register seed once per machine.
4. Bootstrap flow on new machine:
   - Clone repo.
   - Run `scripts/env/bootstrap_all.ps1`.
   - Run `./env_setter.ps1`.
5. Verify setup:
   - Run a lightweight proof command/script.

## Proposed minimal fix to apply after test
Add explicit unignore entries in `.gitignore` near `ENV/`:
- `!config/env/`
- `!config/env/*.psd1`

Then stage tracked file:
- `git add config/env/base.psd1`
