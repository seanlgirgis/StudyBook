# AWS Access and Credential Portability

## Purpose

Document how StudyBook should access AWS and how to transport credentials securely across machines.

## Local AWS Login (Preferred)

1. Install AWS CLI.
2. Configure a non-root IAM profile on your machine:

```powershell
aws configure --profile study
```

3. Validate immediately:

```powershell
aws sts get-caller-identity --profile study
```

## Register Local Seed Once (Recommended)

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<your-passphrase>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force
```

## Encrypt AWS Credentials into StudyBook Secrets

This packages your local `~/.aws/credentials` and `~/.aws/config` into an encrypted StudyBook secret bundle.

```powershell
cd D:\StudyBook
.\scripts\env\package_aws_credentials.ps1 -PreferredProfile study -DeletePlaintext -NonInteractive
```

Output bundle:
- `config/secrets/aws.profiles.secrets.enc.json`

## Restore on Another Machine

```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<same-passphrase>"
.\scripts\env\restore_aws_credentials.ps1 -BackupExisting -NonInteractive
```

Then validate:

```powershell
aws sts get-caller-identity --profile study
```

## Python Connection Proof

```powershell
python D:\StudyBook\poc\connection_proofs\python\aws_connection_proof.py --profile study
```

## Auto Profile Resolution

- The AWS proof script resolves profile in this order: `--profile` arg, `AWS_PROFILE`/`AWS_DEFAULT_PROFILE`, then local credential profiles (prefers `study`, then `default`, then first available).
- This prevents hardcoded-profile failures across agents and machines.

## Notes

- If you use local seed mode, run tooling under the same Windows user context that created the seed file.
- Do not store plaintext AWS keys in tracked markdown, notebooks, or `.env.example`.
- Keep only encrypted secret bundles in git.
- If a specific workload needs another profile (for example `de_learner` for Redshift), pass `--profile` explicitly.
