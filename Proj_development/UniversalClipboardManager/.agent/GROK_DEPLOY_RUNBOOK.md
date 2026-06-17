# GROK Deploy & Run Runbook

**Last updated:** 2026-06-17  
**Machine:** `asuspc` (Windows)

---

## Prerequisites

- Python available on PATH (or existing `.venv`)
- PowerShell (user uses Windows PowerShell / pwsh)
- Write access to `C:\scripts\UniversalClipboardManager`

---

## Session Bootstrap (Development)

From a fresh shell:

```powershell
D:
cd D:\Workarea\StudyBook
.\env_setter.ps1
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\env_setter.ps1
```

**Path tip:** Use `D:\path\...` not `/D:/path/...` in PowerShell.

---

## Run Locally (Source Tree)

```powershell
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\env_setter.ps1
.\run_app.bat
```

Or direct:

```powershell
.\.venv\Scripts\pythonw.exe clipboard_app.py
```

App starts **hidden** in tray. Press `F10` to show window.

---

## Deploy to Runtime Install

```powershell
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\deploy.ps1
```

**Effect:** Overwrites files at `C:\scripts\UniversalClipboardManager` including `clipboard_data.json` and `settings.json` from source.

---

## Restart Deployed App (After Code/Config Change)

Hotkeys and code load at process start — **restart required**.

### Recommended sequence

```powershell
cd C:\scripts\UniversalClipboardManager
.\cleanup_legacy_install.ps1
.\launch_clipboard.bat
```

Or from source after deploy:

```powershell
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\cleanup_legacy_install.ps1   # if run from deployed copy, cd there first
```

Then launch deployed copy:

```powershell
cd C:\scripts\UniversalClipboardManager
.\launch_clipboard.bat
```

### Verify no duplicates

```powershell
Get-CimInstance Win32_Process -Filter "Name='pythonw.exe'" |
  Where-Object { $_.CommandLine -like '*clipboard_app.py*' } |
  Select-Object ProcessId, CommandLine
```

**Known risk:** Multiple instances possible — no single-instance guard in code.

---

## Fresh Install (New Machine / Clean Setup)

```powershell
cd D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager
.\setp_project.ps1
cd C:\scripts\UniversalClipboardManager
.\install_startup.ps1
```

**Gap:** `setp_project.ps1` does not copy `settings.json`. Either:
- run app once (creates defaults), or
- manually copy `settings.json`, or
- run `deploy.ps1` after setup

---

## Windows Startup

Install shortcut (from deployed directory):

```powershell
cd C:\scripts\UniversalClipboardManager
.\install_startup.ps1
```

Verified shortcut location:

`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\UniversalClipboardManager.lnk`

Target: `launch_clipboard.bat` (minimized window style)

---

## Change Hotkeys Only

1. Edit `settings.json` in source
2. `.\deploy.ps1`
3. Restart app (see above)

pynput format: lowercase, angle brackets, `+` joined modifiers  
Example: `"<ctrl>+<alt>+s"`

---

## Virtual Environment

| Location | Path |
|----------|------|
| Local dev | `D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager\.venv` |
| Deployed | `C:\scripts\UniversalClipboardManager\.venv` |

Recreate deps:

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

---

## Validation Checklist (Post-Change)

- [ ] App appears in system tray
- [ ] `F10` toggles window
- [ ] `F11` captures clipboard text to list
- [ ] Copy button pastes into previous app
- [ ] Only one `pythonw.exe` for `clipboard_app.py` (ideal)
- [ ] `settings.json` present in deployed dir
- [ ] Shortcuts hint label shows correct keys in UI

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Hotkeys dead | Old process / wrong settings | Restart; check `settings.json` |
| Two tray icons | Duplicate instances | `cleanup_legacy_install.ps1` |
| App not at login | Missing startup link | `install_startup.ps1` |
| Import errors | Stale/missing venv | Reinstall requirements |
| Deploy didn't update | Edited wrong tree | Confirm deploy target path |