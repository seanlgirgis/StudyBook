# Secrets Workflow

## System Of Record Policy

- StudyBook encrypted secrets are the system of record for sensitive values.
- Do not store secrets in tracked docs, notebooks, prompts, or chat transcripts.
- For sensitive updates, write directly to `config/secrets/*.enc.json` via seed-backed scripts.

## One-Time Setup On A New Machine

```powershell
cd D:\StudyBook
.\scripts\env\bootstrap_all.ps1
```

## Register Local Seed (Set Passphrase Once)

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force
```

- Seed file path: `config/secrets/.local/studybook.secret.seed.dpapi.json`
- Seed is encrypted with Windows DPAPI (CurrentUser scope).
- Use the same Windows user context for decrypt/use (avoid elevated/sudo context changes).
- Seed file is gitignored and must remain local.

## Update Secrets Without Plaintext Files

Use `set_secret.ps1` to update encrypted machine secrets directly.

```powershell
cd D:\StudyBook
.\scripts\env\set_secret.ps1 -Machine asuspc -NonInteractive -Entry "DATABRICKS_HOST=https://dbc-9f35a83d-b4e7.cloud.databricks.com"
.\scripts\env\set_secret.ps1 -Machine asuspc -PromptSecretKey "DATABRICKS_TOKEN"
```

- Supports multiple entries in one call (array syntax): `-Entry "KEY1=VALUE1","KEY2=VALUE2"`.
- For sensitive values, prefer secure prompt mode: `-PromptSecretKey "DATABRICKS_TOKEN"`.
- Supports `-JsonFile` for bulk updates from a local JSON file.
- Script prints only key names, never values.

## Encrypt Secret Files And Remove Plaintext

```powershell
cd D:\StudyBook
.\scripts\env\bootstrap_all.ps1 -DeletePlaintextSecrets
```

## Files You Should Keep

- `config/secrets/shared.secrets.enc.json`
- `config/secrets/asuspc.secrets.enc.json`
- `config/secrets/dell-laptop.secrets.enc.json`
- `config/secrets/aws.profiles.secrets.enc.json` (if using AWS portability bundle)

## Files You Should Not Keep Long-Term

- `config/secrets/*.secrets.json` (plaintext)
- `config/secrets/.local/*` in git (kept local only)

If plaintext appears, encrypt again and delete plaintext.

## Optional Seed Removal / Rotation

```powershell
cd D:\StudyBook
.\scripts\env\remove_secret_seed.ps1 -Force
```
