# Agent Status

## Current Run (2026-04-12)

**Task ID:** TB-20260412-02  
**Task Type:** FIX  
**Goal:** Resolve `ConvertFrom-Json -AsHashtable` failures on Windows PowerShell 5.1 during env/seed bootstrap flows on a second machine.

### Factual Summary

- Added cross-version JSON helper support to `scripts/env/env_core.ps1`:
  - `ConvertFrom-JsonToHashtable`
  - `ConvertTo-NestedHashtable`
- Updated env scripts to use the compatibility helper instead of direct `ConvertFrom-Json -AsHashtable` in caller code:
  - `scripts/env/bootstrap_all.ps1`
  - `scripts/env/set_secret.ps1`
  - `scripts/env/set_site_login.ps1`
  - `scripts/env/copy_site_password.ps1`
  - `scripts/env/seed_status.ps1`
  - `scripts/env/restore_aws_credentials.ps1`

### Files Updated

- `scripts/env/env_core.ps1`
- `scripts/env/bootstrap_all.ps1`
- `scripts/env/set_secret.ps1`
- `scripts/env/set_site_login.ps1`
- `scripts/env/copy_site_password.ps1`
- `scripts/env/seed_status.ps1`
- `scripts/env/restore_aws_credentials.ps1`
- `agents/shared/task_register.md`
- `agents/shared/open_loops.md`
- `agents/shared/agent_status.md`

### Validation

- Ran:
  - `.\scripts\env\bootstrap_all.ps1 -NonInteractive -SkipValidation`
- Result:
  - Script completed successfully with no `-AsHashtable` parameter-binding failure.

### Assumptions

- Target machine is running a PowerShell edition/version where `ConvertFrom-Json -AsHashtable` is unavailable.

### Risks

- Low risk. JSON conversion behavior is preserved; helper uses native `-AsHashtable` when available and falls back to recursive conversion otherwise.

### Next Step

- Pull/sync these script changes on machine #2, then rerun:
  - `.\scripts\env\bootstrap_all.ps1`
  - seed registration + `.\env_setter.ps1 -NonInteractive`

---

**Run completed:** 2026-04-12  
**Status:** DONE
