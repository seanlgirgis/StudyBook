# GROK Decision Log — Universal Clipboard Manager

**Last updated:** 2026-06-17

Chronological record of durable decisions. Newest first.

---

## 2026-06-17 — Dual-copy Grok launcher (`start_grok_ucm.ps1`)

**Decision:** Add `start_grok_ucm.ps1` in repo + `D:\start_grok_ucm.ps1` runtime copy, mirroring learning project pattern.

**Rationale:** User keeps frozen D: launcher for daily use; git-tracked repo copy for archive. Intentional duplication despite design smell.

**Env chain:** StudyBook `env_setter.ps1` (proj_educate venv) → project `env_setter.ps1` (local .venv).

**Status:** Active

---

## 2026-06-17 — Grok agent file namespace

**Decision:** Create project-local agent memory files with `GROK_` prefix in `.agent/`.

**Rationale:** User designated Grok as controlling agent for this directory. Parent StudyBook `agents/shared/*` tree does not exist in this subproject. Local prefixed files avoid collision with other agents and `.agent/project_context.md`.

**Files created:** `GROK_INDEX.md` and companion memory files (see `GROK_FILE_MAP.md`).

**Status:** Active

---

## 2026-06-12 — Tray-first application model

**Decision:** App starts hidden; system tray is primary entry; `setQuitOnLastWindowClosed(False)`.

**Rationale:** User wants always-available clipboard helper without occupying desktop space.

**Implementation:** `ClipboardManagerApp.__init__` ends with `self.hide()`; tray menu + activation handlers.

**Status:** Active

---

## 2026-06-12 — Configurable hotkeys via JSON

**Decision:** Hotkeys loaded from `settings.json` at startup; code defaults are fallbacks only.

**Rationale:** Avoid code edits when shortcuts conflict with other applications.

**Format:** pynput strings, lists per action group (`show_window_hotkeys`, `capture_clipboard_hotkeys`).

**Status:** Active

---

## 2026-06 — F10 / F11 primary hotkeys

**Decision:** Primary show = `F10`, primary capture = `F11`; fallbacks `Ctrl+Alt+S` / `Ctrl+Alt+A`.

**Rationale:** `Ctrl+Shift+S` and `Ctrl+Shift+A` conflicted with user's other tools.

**Status:** Active (reflected in code defaults and `settings.json`)

---

## 2026-06 — Dual-path deployment model

**Decision:** Maintain separate source repo and deployed install at `C:\scripts\UniversalClipboardManager`.

**Rationale:** StudyBook development layout vs. stable Windows startup/runtime location.

**Workflow:** Edit source → `deploy.ps1` → restart deployed process.

**Status:** Active

---

## 2026-04 — KB inbox integration

**Decision:** `env_setter.ps1` sets `KB_INBOX_PATH` to `KB\00_Inbox`.

**Rationale:** Tie project into StudyBook Second Brain ingestion pipeline.

**Status:** Active

---

## Template (Future Entries)

```
## YYYY-MM-DD — Title
**Decision:** ...
**Rationale:** ...
**Alternatives considered:** ...
**Status:** Active | Superseded | Reverted
```