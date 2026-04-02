# Environment Startup

## Daily Start (Auto-Detect Machine)

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\env_setter.ps1
```

## Explicit Machine Name

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\env_setter.ps1 -Machine asuspc
```

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\env_setter.ps1 -Machine dell-laptop
```

## Quick Verify

```powershell
echo $env:STUDYBOOK_MACHINE
echo $env:STUDYBOOK_ROOT
python --version
```

Expected: machine name prints, root prints `D:\StudyBook`, and python resolves to project venv.
