# Secrets Workflow

## One-Time Setup on a New Machine

```powershell
cd D:\StudyBook
.\scripts\env\bootstrap_all.ps1
```

## Encrypt Secret Files and Remove Plaintext

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\scripts\env\bootstrap_all.ps1 -DeletePlaintextSecrets
```

## Files You Should Keep

- `config/secrets/shared.secrets.enc.json`
- `config/secrets/asuspc.secrets.enc.json`
- `config/secrets/dell-laptop.secrets.enc.json`

## Files You Should Not Keep Long-Term

- `config/secrets/*.secrets.json` (plaintext)

If plaintext appears, encrypt again and delete plaintext.
