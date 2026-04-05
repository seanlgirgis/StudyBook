# StudyBook Agent Cheat Sheet

Quick reference for daily Qwen Code sessions.

## Start of Session

```powershell
cd D:\StudyBook
# If env not loaded:
.\env_setter.ps1   # Uses seed + passphrase automatically
```

## First Prompt to Qwen

```
Operate under D:\StudyBook rules.
Read: CONTROL_PROTOCOL.md → agents/shared/context_index.md → open_loops.md → approval_matrix.md → ADR-INDEX.md → pending_task.md (if any) → agent_status.md (if any).
Execute one scoped task. Bounded autonomy. No commit/push. Use seed-backed secrets only. Update agent_status.md + task_register + open_loops at end.
```

## Secrets (Quick)

| Task | Command |
|------|---------|
| Add non-sensitive secret | `.\scripts\env\set_secret.ps1 -Machine asuspc -Entry "KEY=value"` |
| Add sensitive secret | `.\scripts\env\set_secret.ps1 -Machine asuspc -PromptSecretKey "KEY"` |
| Bootstrap all | `.\scripts\env\bootstrap_all.ps1` |

**CRITICAL**: Passphrase entered ONCE per machine (during seed registration).  
**NEVER ask user for passphrase again** - `env_setter.ps1` auto-loads from seed.

**Never**: plaintext secrets in tracked files, chat, or terminal output.

## Job-Site Login Secrets (Canonical)

Use the repo skill flow to avoid key mismatches:

Save login:
`.\agents\skills\jobsite-login-secrets\scripts\set_jobsite_login.ps1 -SiteKey dynatrace -Email "sean.lgirgis@gmail.com" -Url "https://career41.sapsf.com/" -Machine asuspc`

Retrieve password (copies to clipboard):
`.\agents\skills\jobsite-login-secrets\scripts\get_jobsite_login.ps1 -SiteKey dynatrace -Machine asuspc -ShowInfo`

Rule:
- Always use canonical keys `JOBSITE_<SITEKEY>_{URL,USER,PASSWORD}`.
- Do not create new ad-hoc keys like `SAPSF_*` for job-site credentials.

## Command Safety

| Safe (no approval) | Needs Approval |
|--------------------|----------------|
| `rg`, `git status/diff/log` | `git commit/push/rebase/reset` |
| Read/edit files in `D:\StudyBook` | Mass delete/move |
| Build/test/lint | External writes (cloud/DB) |
| | Anything outside repo |

## End of Session (Required)

Update these files:
- `agents/shared/agent_status.md` — run summary
- `agents/shared/task_register.md` — mark task done/blocked
- `agents/shared/open_loops.md` — close or add loops

## Key Paths

| Purpose | Path |
|---------|------|
| Encrypted secrets | `config/secrets/*.enc.json` |
| Seed file (local) | `config/secrets/.local/studybook.secret.seed.dpapi.json` |
| Machine config | `config/machines/asuspc.psd1` |
| ADRs | `docs/adr/` |
| Agent memory | `agents/shared/` |

## Validation Rule

If something fails:
1. Try up to 3 scoped fixes
2. Capture actual outputs
3. Log blocker in `agent_status.md` if still failing

---

**Full protocol**: See `agents/QWEN_AGENT_HANDOFF.md`



