# Troubleshooting

## Canonical key pattern

Always use:

- `JOBSITE_<SITEKEY>_URL`
- `JOBSITE_<SITEKEY>_USER`
- `JOBSITE_<SITEKEY>_PASSWORD`

Example for Dynatrace:

- `JOBSITE_DYNATRACE_URL`
- `JOBSITE_DYNATRACE_USER`
- `JOBSITE_DYNATRACE_PASSWORD`

## Common failure modes

1. `No password key found for site 'dynatrace'`
- Cause: credentials saved with non-canonical keys (for example `SAPSF_PASSWORD`).
- Fix: run `set_jobsite_login.ps1` and save under canonical `JOBSITE_*` keys.

2. Password not prompted while saving
- Cause: only `-Entry` was used (URL/user only).
- Fix: run password save with `-PromptSecretKey` via `set_jobsite_login.ps1`.

3. Decrypt/seed/passphrase errors
- Cause: passphrase source not available for current shell context.
- Fix: verify seed/passphrase setup, then rerun save/retrieve.

## Quick commands

Save:

```powershell
.\agents\skills\jobsite-login-secrets\scripts\set_jobsite_login.ps1 -SiteKey dynatrace -Email "sean.lgirgis@gmail.com" -Url "https://career41.sapsf.com/" -Machine asuspc
```

Retrieve:

```powershell
.\agents\skills\jobsite-login-secrets\scripts\get_jobsite_login.ps1 -SiteKey dynatrace -Machine asuspc -ShowInfo
```
