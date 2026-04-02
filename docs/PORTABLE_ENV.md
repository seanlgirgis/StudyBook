# Portable Environment

This project supports machine-specific runtime settings with a shared bootstrap.

## Files

- `env_setter.ps1`
- `scripts/env/env_core.ps1`
- `scripts/env/bootstrap_all.ps1`
- `config/env/base.psd1`
- `config/machines/*.psd1`
- `config/secrets/*.secrets.enc.json` (encrypted, optional)

## One-Command Guided Setup

Run:

```powershell
.\scripts\env\bootstrap_all.ps1
```

This command:
1. Creates machine profile if missing.
2. Creates plaintext secret templates if missing.
3. Optionally encrypts ready secret files.
4. Runs `env_setter.ps1` validation.

Useful flags:

```powershell
.\scripts\env\bootstrap_all.ps1 -MachineName dell-laptop -DeletePlaintextSecrets
.\scripts\env\bootstrap_all.ps1 -NonInteractive -SkipValidation
```

## Bootstrap Flow

1. Detect machine (`STUDYBOOK_MACHINE` override or `COMPUTERNAME`).
2. Load `config/env/base.psd1`.
3. Merge machine profile from `config/machines/<machine>.psd1`.
4. Merge optional local override `config/machines/<machine>.local.psd1`.
5. Set process environment variables.
6. Activate venv from merged config.
7. Decrypt optional secret files and export them to process env vars.

## Machine Setup

Create a machine file:

```powershell
.\scripts\env\init_machine_profile.ps1
```

Edit generated file under `config/machines/`.

## Secrets Setup

1. Create plaintext JSON:

```powershell
Copy-Item config\secrets\secrets.template.json config\secrets\shared.secrets.json
```

2. Fill real values in `config\secrets\shared.secrets.json`.

3. Encrypt:

```powershell
.\scripts\env\encrypt_secrets.ps1 -InputFile config\secrets\shared.secrets.json -OutputFile config\secrets\shared.secrets.enc.json -DeleteInput
```

4. Set passphrase at runtime:

```powershell
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\env_setter.ps1
```

## Notes

- Only encrypted secret files should be committed.
- Plaintext secret files are gitignored.
- All project paths should be consumed via environment variables or relative paths.
