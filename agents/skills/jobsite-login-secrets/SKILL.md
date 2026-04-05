---
name: jobsite-login-secrets
description: Save and retrieve job-site credentials in StudyBook encrypted secrets with one consistent key pattern. Use when adding a new login (for example Dynatrace/SAP SuccessFactors), retrieving a saved password, or fixing mismatched keys like SAPSF_* vs JOBSITE_SITE_*.
---

# Jobsite Login Secrets

## Goal

Use one canonical credential model for all job sites:

- `JOBSITE_<SITEKEY>_URL`
- `JOBSITE_<SITEKEY>_USER`
- `JOBSITE_<SITEKEY>_PASSWORD`

`<SITEKEY>` must be uppercase and underscore-safe (example: `dynatrace` -> `DYNATRACE`).

## Workflow

1. Save credentials:
```powershell
.\agents\skills\jobsite-login-secrets\scripts\set_jobsite_login.ps1 -SiteKey dynatrace -Email "sean.lgirgis@gmail.com" -Url "https://career41.sapsf.com/" -Machine asuspc
```

2. Retrieve password + info later:
```powershell
.\agents\skills\jobsite-login-secrets\scripts\get_jobsite_login.ps1 -SiteKey dynatrace -Machine asuspc -ShowInfo
```

3. Paste password from clipboard into the site login page.

## Rules

- Use `JOBSITE_*` keys only for job-site credentials.
- Do not mix with ad-hoc keys like `SAPSF_*` for new saves.
- If old `SAPSF_*` keys already exist, migrate them to `JOBSITE_DYNATRACE_*` once, then stop using the old names.
- Keep `-Machine` explicit to avoid writing to or reading from the wrong encrypted file.

## Troubleshooting

- Error: `No password key found ... JOBSITE_<SITE>_PASSWORD`
  Fix: Save again with this skill's `set_jobsite_login.ps1`.
- No prompt for password:
  Ensure you are running `set_jobsite_login.ps1` (not only `set_secret.ps1 -Entry ...`).
- Decrypt/passphrase errors:
  Check seed status and passphrase flow before retrying credential commands.

See detailed notes in [references/troubleshooting.md](references/troubleshooting.md).

