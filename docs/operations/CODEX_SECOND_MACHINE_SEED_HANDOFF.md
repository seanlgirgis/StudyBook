# Codex Handoff: Second-Machine Seed + Env Bootstrap Recovery

## Purpose

Use this handoff on the second machine to resolve StudyBook env startup and seed decryption setup end-to-end.

Context:
- Repo uses encrypted secrets as system of record (`config/secrets/*.enc.json`).
- Local seed file is DPAPI `CurrentUser` scoped and **not portable**.
- New machine must register local seed once using the same passphrase used for encrypted secret files.

## Current Symptom Seen On Second Machine

Observed error when running:
- `.\scripts\env\bootstrap_all.ps1`

Error:
- `Test-SecretJsonReady : A parameter cannot be found that matches parameter name 'AsHashtable'.`

Likely cause:
- Windows PowerShell version compatibility issue (`ConvertFrom-Json -AsHashtable` unavailable).
  - If you see `Unable to find type [System.Security.Cryptography.ProtectedData]`, you're in PowerShell 7 without the assembly loaded.
  - If you see `Padding is invalid and cannot be removed`, the encrypted secret file was created with a different passphrase.

## Expected End State

1. `bootstrap_all.ps1` runs without `-AsHashtable` parameter failure.
2. local seed exists at:
   - `C:\StudyBook\config\secrets\.local\studybook.secret.seed.dpapi.json`
3. `.\env_setter.ps1 -NonInteractive` succeeds and prints:
   - `Secrets Loaded: True`
4. Future runs of `.\env_setter.ps1` do **not** prompt for the passphrase.

## What Codex Should Do (Exact Plan)

1. Verify shell/runtime context.
2. Apply/confirm compatibility patch for JSON parsing in env scripts.
3. Run bootstrap.
4. Register seed once on this machine/user.
5. Validate noninteractive env setup.
6. If any failure remains, diagnose with `whoami` + seed path checks and resolve.

## Step-by-Step Commands

Run from `C:\StudyBook`.

### 1) Quick Diagnostics

```powershell
whoami
$PSVersionTable.PSVersion
```

### 2) Sync/Fix Scripts

Preferred:
- pull latest from repo containing compatibility fix.

Files expected to include fix:
- `scripts/env/env_core.ps1`
- `scripts/env/bootstrap_all.ps1`
- `scripts/env/set_secret.ps1`
- `scripts/env/set_site_login.ps1`
- `scripts/env/copy_site_password.ps1`
- `scripts/env/seed_status.ps1`
- `scripts/env/restore_aws_credentials.ps1`

Compatibility fix behavior:
- introduce helper that converts JSON to hashtable in both older and newer PowerShell.
- replace direct caller usage of `ConvertFrom-Json -AsHashtable` with helper calls.
 - add ProtectedData assembly load fallback so DPAPI works in PowerShell 7.

### 3) Run Bootstrap

```powershell
.\scripts\env\bootstrap_all.ps1
```

### 4) Register Local Seed Once (Second Machine)

```powershell
$env:STUDYBOOK_SECRET_PASSPHRASE = "<same-passphrase-used-for-encrypted-secrets>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force
Remove-Item Env:STUDYBOOK_SECRET_PASSPHRASE
```

### 5) Validate Env Startup

```powershell
.\env_setter.ps1 -NonInteractive
```

Expected:
- `Secrets Loaded: True`

Optional cleanup:

```powershell
Remove-Item Env:STUDYBOOK_SECRET_PASSPHRASE
```

## Recovery Paths

### A) Still getting seed/decrypt failure

Run:

```powershell
whoami
Test-Path C:\StudyBook\config\secrets\.local\studybook.secret.seed.dpapi.json
.\scripts\env\seed_status.ps1 -AsJson
```

Interpretation:
- If seed exists but decrypt fails with `Key not valid for use in specified state`, this is usually user-context mismatch.
- Switch to the same normal Windows user context (non-service/non-elevated mismatch) and rerun.
- If you see `Padding is invalid and cannot be removed`, the passphrase does not match the encrypted file. Re-encrypt the failing file with the correct passphrase.

Re-encrypt shared secrets:

```powershell
.\scripts\env\encrypt_secrets.ps1 -InputFile config\secrets\shared.secrets.json -OutputFile config\secrets\shared.secrets.enc.json
```

Re-encrypt machine secrets (example: inspiron16):

```powershell
.\scripts\env\encrypt_secrets.ps1 -InputFile config\secrets\inspiron16.secrets.json -OutputFile config\secrets\inspiron16.secrets.enc.json
```

### B) Seed missing/corrupt

Re-register:

```powershell
$env:STUDYBOOK_SECRET_PASSPHRASE = "<same-passphrase>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force
.\env_setter.ps1 -NonInteractive
```

### C) Immediate temporary bypass if patch is not yet synced

Run in PowerShell 7 (`pwsh`) temporarily, then still apply the compatibility fix for durable support.

### D) ProtectedData type missing in PowerShell 7

If `register_secret_seed.ps1` fails with `Unable to find type [System.Security.Cryptography.ProtectedData]`, update to the latest repo (or add the assembly load fallback in `scripts/env/env_core.ps1`).

## Guardrails

- Do not store plaintext secrets in tracked files.
- Do not copy seed file between machines.
- Do not rely on chat memory; use repo files as source of truth.

## Codex Prompt To Paste On Second Machine

```text
Use docs/operations/CODEX_SECOND_MACHINE_SEED_HANDOFF.md as the task contract.
Resolve second-machine StudyBook env bootstrap + seed setup end-to-end.
Current blocker is: Test-SecretJsonReady parameter error about AsHashtable.
Apply/confirm PowerShell compatibility fix in scripts/env, run bootstrap, register local seed once, and validate env_setter noninteractive until Secrets Loaded is true.
If blocked, run whoami + seed diagnostics and fix user-context mismatch.
```
