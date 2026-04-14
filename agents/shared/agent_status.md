# Agent Status

## Current Run (2026-04-13)

**Task ID:** TB-20260413-10  
**Task Type:** SYNC  
**Goal:** Persist durable cross-machine reminder to bootstrap/start the index UI Docker stack on request.

### Factual Summary

- Updated `agents/shared/user_profile.md` with a new cross-machine reminder:
  - If user asks to "create the docker in there and start it for me", treat it as instruction to bootstrap and run StudyBook index UI Docker stack.
- Refreshed StudyBook command shortcuts in user profile to current CSV/CLI/Streamlit workflow (removed outdated xlsx wording).

### Validation

- Confirmed `agents/shared/user_profile.md` now contains:
  - `run_index_ui_docker.ps1` usage
  - compose file path reference
  - target URL reminder

### Assumptions

- User wants this preference durable in repo memory for future sessions/machines.

### Risks

- None; documentation-only memory update.

### Next Step

- Commit/push when requested.

---

**Run completed:** 2026-04-13  
**Status:** DONE
