# GROK Open Loops — Universal Clipboard Manager

**Last updated:** 2026-06-17

Tracked unfinished work, suggested enhancements, and maintenance debt.  
**This file is the enhancement backlog** — no separate todo file. Grok reminds Sean on session open; marks items done here when completed.

---

## Session-Open Reminder Protocol

**Grok must do this every time this project is opened** (via `start_grok_ucm.ps1`, Grok Build, or any UCM session):

1. Read this file after `GROK_INDEX.md` and `GROK_AGENT_STATUS.md`.
2. If any row in **Suggested Enhancements Backlog** has `Status: pending` or `in_progress`, give Sean a **short numbered reminder** (one line per item, priority order).
3. Do **not** start work unless Sean asks — reminder only.
4. When an enhancement is completed:
   - Set `Status: done` and fill `Done` date below
   - Move the full entry to **Closed** section
   - Log in `GROK_DECISION_LOG.md` if architectural
   - Update `GROK_AGENT_STATUS.md`

**Last reminded:** 2026-06-17  
**Open enhancement count:** 4 pending (OL-004, OL-001, OL-005, OL-002)

---

## Suggested Enhancements Backlog

*User-requested: track here, remind on open, mark done when implemented.*

| ID | Enhancement | Priority | Status | Done | Files / notes |
|----|-------------|----------|--------|------|---------------|
| **OL-004** | Add `settings.json` to `setp_project.ps1` copy list (parity with `deploy.ps1`) | 1 | **pending** | — | `setp_project.ps1` — quick win |
| **OL-001** | Single-instance guard (no duplicate `pythonw.exe` / tray icons) | 2 | **pending** | — | `clipboard_app.py` — mutex / `QLocalServer` |
| **OL-005** | Safer deploy: don't overwrite deployed `clipboard_data.json` from source | 3 | **pending** | — | `deploy.ps1` — preserve target or flag |
| **OL-002** | Custom tray `.ico` instead of generic Qt pixmap | 4 | **pending** | — | `clipboard_app.py` + asset — polish |

### Detail — OL-004 (pending)
- **Severity:** Low–Medium
- **Impact:** Fresh `setp_project.ps1` install won't copy hotkey config; app creates defaults on first run
- **Fix:** Add `settings.json` to `$filesToCopy` array

### Detail — OL-001 (pending)
- **Severity:** Medium
- **Symptom:** Multiple `pythonw.exe` during restart; duplicate tray icons
- **Workaround until done:** `cleanup_legacy_install.ps1` before relaunch

### Detail — OL-005 (pending)
- **Severity:** Medium (operational)
- **Risk:** Dev repo snippets overwrite production at `C:\scripts\...` on deploy
- **Workaround until done:** Backup deployed `clipboard_data.json` before deploy

### Detail — OL-002 (pending)
- **Severity:** Low
- **Current:** `QStyle.StandardPixmap.SP_FileDialogDetailedView`
- **Note:** Branding polish — only if Sean wants it

---

## Open — Other (Not in Enhancement Queue)

### OL-003: Passive clipboard monitoring
- **Severity:** N/A (feature gap, not bug)
- **State:** Capture is on-demand (`F11`) only
- **Note:** Do not implement unless Sean explicitly requests

### OL-006: Parent StudyBook agent files not in subproject
- **Severity:** Low
- **State:** Resolved by Grok `GROK_*` files; optional parent sync only if requested

### OL-007: `PROJECT_FULL_CONTEXT_AND_HISTORY.md` untracked in git
- **Severity:** Low
- **Action:** Sean may commit when ready

---

## Closed (Done — For Reference)

| ID | Item | Closed |
|----|------|--------|
| CL-001 | Hotkey conflict (`Ctrl+Shift+S/A`) | 2026-06 — moved to F10/F11 |
| CL-002 | Non-configurable hotkeys | 2026-06 — `settings.json` |
| CL-003 | No tray integration | 2026-06 — tray + hidden start |
| CL-004 | `deploy.ps1` omitted settings | 2026-06 — now copies `settings.json` |
| CL-005 | Grok agent onboarding | 2026-06-17 — `GROK_*` files created |
| CL-006 | Grok launcher dual-copy | 2026-06-17 — `start_grok_ucm.ps1` |

*When an OL-* item is done, move its row here and remove from backlog table above.*