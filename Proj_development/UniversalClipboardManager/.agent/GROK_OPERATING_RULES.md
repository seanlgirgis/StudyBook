# GROK Operating Rules — Universal Clipboard Manager

**Last updated:** 2026-06-17  
**Agent:** Grok

---

## Authority Order

1. Direct user instruction (current message)
2. `GROK_PENDING_TASK.md` (if present)
3. `GROK_OPERATING_RULES.md` (this file)
4. `GROK_INDEX.md` and other `GROK_*.md` files
5. Parent `D:\Workarea\StudyBook\CONTROL_PROTOCOL.md` (non-conflicting)
6. Chat memory (lowest — never trust alone)

---

## Scope

**In scope:** Everything under  
`D:\Workarea\StudyBook\Proj_development\UniversalClipboardManager`

**Related but separate:** Deployed runtime at `C:\scripts\UniversalClipboardManager` — modify via deploy scripts or explicit user request.

---

## Autonomy Budget (Default)

Per parent CONTROL_PROTOCOL, unless `GROK_PENDING_TASK.md` overrides:

| Permission | Limit |
|------------|-------|
| Files modified per run | Up to 8 related files |
| Subtasks | Up to 3 tightly related |
| Validation | Run allowed commands from `GROK_COMMAND_ALLOWLIST.md` |

**Ask before:**

- Mass delete or rewriting git history
- Overwriting `clipboard_data.json` with empty/test data
- Force-killing unrelated user processes
- Changing secrets or credentials
- Modifying Windows Startup shortcuts without user awareness

---

## Execution Principles

1. **Repository files are memory** — update `GROK_AGENT_STATUS.md`, `GROK_DECISION_LOG.md`, `GROK_OPEN_LOOPS.md` at session end
2. **One scoped task per run** — park side findings in `GROK_PARKING_LOT.md`
3. **Read before edit** — especially `clipboard_app.py` and affected scripts
4. **Deploy-aware** — code changes usually need `deploy.ps1` + restart to affect daily-use install
5. **User data care** — treat `clipboard_data.json` as production user content
6. **Execute, don't instruct** — run commands yourself per user rules
7. **Minimal diffs** — match existing style; no drive-by refactors

---

## Task Contract Template

When accepting work, record in `GROK_PENDING_TASK.md`:

```
Task ID: UCM-YYYYMMDD-XX
Task Type: FIX | ENHANCEMENT | REFACTOR | RESEARCH | SYNC | DEPLOY
Goal: ...
Non-Goals: ...
Files to Read: ...
Allowed Scope: strict | bounded
Validation Commands: ...
Definition of Done: ...
Risk Level: low | medium | high
```

If fields missing: assume `bounded` scope, `low` risk, continue unless high-risk ambiguity.

---

## Code Change Guidelines

| Change type | Typical files | Post-change |
|-------------|---------------|-------------|
| Feature/fix | `clipboard_app.py` | Local test → deploy → restart |
| Hotkey only | `settings.json` | Deploy → restart |
| Deploy path | `deploy.ps1`, `setp_project.ps1` | Update GROK memory + handoff |
| Deps | `requirements.txt` | pip install in both venvs if needed |
| Docs | `docs/handoff.md` only if user asks or major behavior change |

---

## Anti-Drift Rules

- Do not assume parent `agents/shared/*` files exist in this subproject
- Do not conflate StudyBook `proj_educate` venv with project `.venv` for app runtime
- Do not add passive clipboard monitoring unless explicitly requested
- Do not create non-`GROK_` agent files unless user asks
- Do not edit `PROJECT_FULL_CONTEXT_AND_HISTORY.md` unless user asks (Grok maintains `GROK_*` instead)

---

## Session Startup Checklist

- [ ] Read `GROK_INDEX.md`
- [ ] Read `GROK_AGENT_STATUS.md`
- [ ] Read `GROK_PENDING_TASK.md` (if task active)
- [ ] Read `GROK_OPEN_LOOPS.md`
- [ ] **Remind Sean** of pending enhancements (backlog table) — one line each, priority order; no work unless asked
- [ ] Set `Last reminded` date in `GROK_OPEN_LOOPS.md`
- [ ] Activate env if running commands: StudyBook `env_setter.ps1` then project `env_setter.ps1`

---

## Session Shutdown Checklist

- [ ] Update `GROK_AGENT_STATUS.md` with outcome
- [ ] Clear or update `GROK_PENDING_TASK.md`
- [ ] Log decisions in `GROK_DECISION_LOG.md`
- [ ] **If enhancement completed:** mark `done` + date in `GROK_OPEN_LOOPS.md`, move to Closed, decrement open count
- [ ] Update `GROK_OPEN_LOOPS.md` if new gaps found
- [ ] Park extras in `GROK_PARKING_LOT.md`