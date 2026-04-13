# JobSearch Launchpad

Use StudyBook as the launchpad while keeping JobSearch runtime in its own repo.

## Machine-Configurable JobSearch Root

Set this key per machine in:
- `config/machines/<machine>.psd1`
- or (preferred for personal overrides) `config/machines/<machine>.local.psd1`

Required key under `Environment`:

```powershell
STUDYBOOK_JOBSEARCH_ROOT = "{PROJECT_ROOT}\temp\jobsearch"
```

Example for another machine:

```powershell
STUDYBOOK_JOBSEARCH_ROOT = "{PROJECT_ROOT}\temp\jobsearch"
```

## Launcher Scripts

### 1) Open JobSearch shell from StudyBook

```powershell
pwsh .\scripts\ops\open_jobsearch.ps1
```

What it does:
- loads StudyBook machine config,
- resolves `STUDYBOOK_JOBSEARCH_ROOT`,
- `cd` into JobSearch root,
- runs JobSearch `env_setter.ps1`.

Options:

```powershell
pwsh .\scripts\ops\open_jobsearch.ps1 -Machine asuspc
pwsh .\scripts\ops\open_jobsearch.ps1 -NoActivate
pwsh .\scripts\ops\open_jobsearch.ps1 -NoCd
```

### 2) Run JobSearch auto pipeline from StudyBook

```powershell
pwsh .\scripts\ops\run_jobsearch_pipeline.ps1 -IntakeFile "intake\00024.example.md" -Method "LinkedIn"
```

Resume from existing UUID:

```powershell
pwsh .\scripts\ops\run_jobsearch_pipeline.ps1 -Uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -Method "LinkedIn"
```

Optional flags:

```powershell
-Model grok-3
-Version v1
-NoMove
-Machine <machine-name>
```

## Notes

- This design intentionally keeps JobSearch in its own operational repository.
- StudyBook acts as the single launchpad and manager.
- Default canonical path is `D:\StudyBook\temp\jobsearch` (resolved from `{PROJECT_ROOT}`).
