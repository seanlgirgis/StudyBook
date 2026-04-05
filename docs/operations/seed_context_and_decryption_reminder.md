# Seed Context And Decryption Reminder

Purpose: prevent repeated passphrase prompts and quickly diagnose seed decryption issues when switching machines, shells, or execution environments.

## Core Rule

- Seed-backed secrets are the source of truth.
- Passphrase is entered once during seed registration.
- After seed registration, do not ask for passphrase again.

## Why Decryption Can Fail Even With A Valid Seed

The seed file is encrypted with Windows DPAPI `CurrentUser`.
That means decryption works only under the same Windows user account that registered the seed.

If session user context changes (sandbox user, elevated shell, service account, different machine user), decrypt can fail with:

- `Key not valid for use in specified state.`

This usually indicates user-context mismatch, not a bad/missing passphrase.

## First Diagnostics (Always)

```powershell
cd D:\StudyBook
whoami
```

Then check seed presence:

```powershell
Test-Path D:\StudyBook\config\secrets\.local\studybook.secret.seed.dpapi.json
```

## Expected Healthy Flow (Owner Context)

```powershell
cd D:\StudyBook
.\env_setter.ps1 -NonInteractive
```

Expected output includes:

- `Secrets Loaded: True`

## Recovery By Scenario

1. Same machine, wrong user context
- Switch to the owner account/shell context that registered the seed.
- Re-run `.\env_setter.ps1 -NonInteractive`.

2. New machine (or seed never registered there)
- Register seed once on that machine/user:

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<passphrase>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force
```

Then:

```powershell
.\env_setter.ps1 -NonInteractive
```

3. Seed file missing/corrupted locally
- Re-register seed in owner context using the one-time registration command above.

## Hard Policy Reminder For Agents

- Do not interpret seed decrypt failure as permission to ask for passphrase repeatedly.
- Treat it as environment/user-context diagnosis first (`whoami`).
- Keep using encrypted secret files as system of record.
