# GROK Command Allowlist — Universal Clipboard Manager

**Last updated:** 2026-06-17

Commands Grok may run without extra approval in this project context.

---

## Navigation & Listing

```powershell
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
Get-ChildItem
Get-Content <file>
```

---

## Environment

```powershell
cd D:\Workarea\StudyBook
.\env_setter.ps1

cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\env_setter.ps1
```

---

## Run & Test (Local)

```powershell
.\run_app.bat
.\.venv\Scripts\python.exe -m py_compile clipboard_app.py
.\.venv\Scripts\python.exe -c "import clipboard_app"
```

**Note:** Full GUI test launches `pythonw` — prefer compile/import for non-interactive validation.

---

## Deploy & Install

```powershell
.\deploy.ps1
.\setp_project.ps1
.\install_startup.ps1
.\cleanup_legacy_install.ps1
```

---

## Process Inspection (Read-Only)

```powershell
Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" |
  Where-Object { $_.CommandLine -like '*clipboard_app*' }

Get-Process pythonw -ErrorAction SilentlyContinue
```

---

## Pip / Venv (Bounded)

```powershell
.\.venv\Scripts\pip.exe list
.\.venv\Scripts\pip.exe install -r requirements.txt
python -m venv .venv
```

---

## Git (Read + Normal Commits in Repo)

```powershell
git status
git diff
git log --oneline -10
```

**Ask before:** `git push --force`, `git reset --hard`, branch deletion

---

## File Search (Repo)

```powershell
# ripgrep / Select-String for code search
Select-String -Path clipboard_app.py -Pattern "pattern"
```

---

## Requires Explicit User Approval

| Action | Reason |
|--------|--------|
| `Stop-Process -Force` on broad filters | May kill unrelated Python apps |
| Delete `clipboard_data.json` contents | User data loss |
| Edit `%APPDATA%\...\Startup\*.lnk` manually | System startup impact |
| `pip install` unpinned new major deps | Runtime stability |
| Network pip unless deps missing | Supply chain / env policy |

---

## Validation Commands (Default for Code Changes)

```powershell
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\.venv\Scripts\python.exe -m py_compile clipboard_app.py
```

Optional after deploy:

```powershell
Test-Path C:\scripts\UniversalClipboardManager\clipboard_app.py
Test-Path C:\scripts\UniversalClipboardManager\settings.json
```