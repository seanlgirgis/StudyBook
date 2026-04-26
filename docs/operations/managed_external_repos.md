# Managed External Repositories

StudyBook manages two external repos as sibling repositories so daily work stays in one launchpad:

- JobSearch: `..\jobsearch` (`https://github.com/seanlgirgis/jobsearch`)
- Website: `..\seanlgirgis.github.io` (`https://github.com/seanlgirgis/seanlgirgis.github.io`)

## Why This Pattern

- Keep independent Git history per repo (clean commits/pushes).
- Avoid project hopping while preserving separation of concerns.
- Make cross-machine restore deterministic from one command.
- Enforce relative-path portability (`{PROJECT_ROOT}\temp\...`) instead of machine-specific absolute paths.

## Canonical Environment Keys

Set by `config/env/base.psd1` (and can be overridden per machine):

- `STUDYBOOK_JOBSEARCH_ROOT = "{PROJECT_ROOT}\..\jobsearch"`
- `STUDYBOOK_WEBSITE_ROOT = "{PROJECT_ROOT}\..\seanlgirgis.github.io"`

## One-Command Restore On Any Machine

```powershell
cd D:\Workarea\StudyBook
pwsh .\scripts\ops\restore_managed_repos.ps1
```

To also fast-forward existing clones:

```powershell
pwsh .\scripts\ops\restore_managed_repos.ps1 -UpdateExisting
```

## JobSearch Launch

```powershell
pwsh .\scripts\ops\open_jobsearch.ps1
```

This resolves `STUDYBOOK_JOBSEARCH_ROOT` and starts JobSearch from the managed path.

## Relative-Path Rule

- Repo scripts and machine profiles should use `{PROJECT_ROOT}` tokens and sibling-relative paths.
- Avoid hardcoded roots like `C:\jobsearch` or user-specific locations in tracked files.
- If a local override is needed, use `config/machines/<machine>.local.psd1` and keep it untracked.
