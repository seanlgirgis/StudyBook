# Job-Site Credentials Workflow

Use this runbook for storing and retrieving job-site credentials in StudyBook encrypted secrets with one consistent key pattern.

## Canonical Keys

For each site key, store exactly:

- `JOBSITE_<SITEKEY>_URL`
- `JOBSITE_<SITEKEY>_USER`
- `JOBSITE_<SITEKEY>_PASSWORD`

Example for Dynatrace:

- `JOBSITE_DYNATRACE_URL`
- `JOBSITE_DYNATRACE_USER`
- `JOBSITE_DYNATRACE_PASSWORD`

## Recommended Commands

From `D:\StudyBook`:

Save login (prompts for password securely):

```powershell
.\agents\skills\jobsite-login-secrets\scripts\set_jobsite_login.ps1 -SiteKey dynatrace -Email "sean.lgirgis@gmail.com" -Url "https://career41.sapsf.com/" -Machine asuspc
```

Retrieve password (copies to clipboard) and show URL/user:

```powershell
.\agents\skills\jobsite-login-secrets\scripts\get_jobsite_login.ps1 -SiteKey dynatrace -Machine asuspc -ShowInfo
```

## Important Rules

- Keep `-Machine` explicit.
- Do not save job-site credentials under non-canonical names such as `SAPSF_*`.
- Never print raw password values into chat or logs.

## Troubleshooting

If you see:

`No password key found for site 'dynatrace' (expected key: JOBSITE_DYNATRACE_PASSWORD)`

Then credentials were saved under different keys. Re-save with `set_jobsite_login.ps1` above.
