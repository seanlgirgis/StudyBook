# Secrets Workflow

## One-Time Setup on a New Machine

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

## Encrypt Secret Files and Remove Plaintext

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
