# QWEN_AGENT_HANDOFF.md

Purpose: give Qwen Code a strict, repo-native operating contract for `D:\StudyBook`.

## 1) First-Run Read Order (Mandatory)

Before making any edits or running write commands, read files in this exact order:

1. `D:\StudyBook\CONTROL_PROTOCOL.md`
2. `D:\StudyBook\agents\shared\context_index.md`
3. `D:\StudyBook\agents\shared\open_loops.md`
4. `D:\StudyBook\agents\shared\approval_matrix.md`
5. `D:\StudyBook\agents\shared\command_allowlist.md`
6. `D:\StudyBook\docs\adr\ADR-INDEX.md`
7. `D:\StudyBook\agents\shared\pending_task.md` (if present)
8. `D:\StudyBook\agents\shared\agent_status.md` (if present)
9. `D:\StudyBook\agents\shared\decision_log.md` (if present)

Authority precedence:
1. Direct user instruction for current run
2. `CONTROL_PROTOCOL.md`
3. `pending_task.md`
4. `context_index.md`
5. latest `agent_status.md`

If anything conflicts with `AGENTS.md`, follow `CONTROL_PROTOCOL.md`.

## 2) Core Operating Rules

- Repository files are source of truth. Do not rely on chat memory.
- Execute one scoped task per run.
- Stay in objective scope; do not branch into side quests.
- Use bounded autonomy by default unless `pending_task.md` overrides.
- Ask before destructive actions, secret/credential changes, external writes, or history rewrite.
- Do not commit or push unless user explicitly asks.

## 3) Required Run Artifacts (Every Run)

At end of each run, update:

- `D:\StudyBook\agents\shared\agent_status.md` (overwrite with factual run summary)
- `D:\StudyBook\agents\shared\task_register.md` (status in_progress -> done/blocked)
- `D:\StudyBook\agents\shared\open_loops.md` (close or add loops)

When architecture behavior changes:
- update/add ADR in `D:\StudyBook\docs\adr\`
- update `D:\StudyBook\docs\adr\ADR-INDEX.md`
- add summary entry in `D:\StudyBook\agents\shared\decision_log.md`

## 4) Secrets System (Critical)

### Policy

- Encrypted StudyBook secrets are the system of record.
- Never store secrets in tracked docs, notebooks, prompts, code comments, or chat logs.
- Never print secret values in terminal output.
- Use seed-backed encrypted updates only.

### Seed-backed decryption model (CRITICAL)

- Local seed file (gitignored):
  - `D:\StudyBook\config\secrets\.local\studybook.secret.seed.dpapi.json`
- Seed is DPAPI-encrypted (CurrentUser).
- **Passphrase is entered ONCE per machine during seed registration.**
- **After seed is registered, NEVER ask user for passphrase again.**
- `env_setter.ps1` auto-decrypts seed → loads passphrase → decrypts secrets.
- Must run under same Windows user context that registered the seed.
- First diagnostic command when seed decrypt fails: `whoami` (DPAPI CurrentUser mismatch is the expected cause in sandbox/non-owner sessions).
- Never request passphrase again if seed exists; resolve the Windows user-context mismatch instead.

### Standard commands

Bootstrap:
```powershell
cd D:\StudyBook
.\scripts\env\bootstrap_all.ps1
```

Register seed once (using passphrase already set in env):
```powershell
cd D:\StudyBook
$env:STUDYBOOK_SECRET_PASSPHRASE = "<passphrase>"
.\scripts\env\register_secret_seed.ps1 -NonInteractive -Force
```

Update encrypted secret directly (non-sensitive inline):
```powershell
cd D:\StudyBook
.\scripts\env\set_secret.ps1 -Machine asuspc -NonInteractive -Entry "DATABRICKS_HOST=https://..."
```

Update sensitive secret via secure prompt:
```powershell
cd D:\StudyBook
.\scripts\env\set_secret.ps1 -Machine asuspc -PromptSecretKey "DATABRICKS_TOKEN"
```

Encrypt and remove plaintext secret files if any exist:
```powershell
cd D:\StudyBook
.\scripts\env\bootstrap_all.ps1 -DeletePlaintextSecrets
```

Optional seed removal:
```powershell
cd D:\StudyBook
.\scripts\env\remove_secret_seed.ps1 -Force
```


### Job-site login credentials (canonical)

For job-board/company-site credentials, use the skill scripts under:
- `D:\StudyBook\agents\skills\jobsite-login-secrets\scripts\`

Save:
```powershell
cd D:\StudyBook
.\agents\skills\jobsite-login-secrets\scripts\set_jobsite_login.ps1 -SiteKey dynatrace -Email "sean.lgirgis@gmail.com" -Url "https://career41.sapsf.com/" -Machine asuspc
```

Retrieve password (clipboard) + user/url info:
```powershell
cd D:\StudyBook
.\agents\skills\jobsite-login-secrets\scripts\get_jobsite_login.ps1 -SiteKey dynatrace -Machine asuspc -ShowInfo
```

Always use canonical key pattern:
- `JOBSITE_<SITEKEY>_URL`
- `JOBSITE_<SITEKEY>_USER`
- `JOBSITE_<SITEKEY>_PASSWORD`

Do not create new ad-hoc job-site keys like `SAPSF_*`.

### Encrypted secret files to keep

- `D:\StudyBook\config\secrets\shared.secrets.enc.json`
- `D:\StudyBook\config\secrets\asuspc.secrets.enc.json`
- `D:\StudyBook\config\secrets\dell-laptop.secrets.enc.json`
- `D:\StudyBook\config\secrets\aws.profiles.secrets.enc.json` (if AWS portability is used)

### Files not to keep long-term

- `D:\StudyBook\config\secrets\*.secrets.json` (plaintext)
- Any local plaintext key/token dump files

If found, encrypt and delete plaintext immediately.

## 5) Command Safety Profile

Default safe:
- `rg`, `rg --files`
- `Get-ChildItem`, `Get-Content`, `Select-String`
- `git status`, `git diff`, `git log`, `git show`, `git rev-parse`
- test/lint/build in repo scope

Needs explicit user approval:
- `git commit`, `git push`, `git rebase`, `git reset --hard`, `git clean -fd`
- mass delete/move
- touching keychains/credential stores
- writes to cloud/db/external systems
- write commands outside `D:\StudyBook`

If unclear, treat as approval-required.

## 6) Validation Rule

If behavior changes:
- run real validation commands
- capture actual outputs
- retry up to 3 scoped fixes

If still failing:
- stop and log exact failure + blocker in `agent_status.md`

## 7) Practical Start Prompt For Qwen

Use this as your first prompt in Qwen:

```text
Operate as StudyBook agent under D:\StudyBook rules.
First read in order:
CONTROL_PROTOCOL.md,
agents/shared/context_index.md,
agents/shared/open_loops.md,
agents/shared/approval_matrix.md,
agents/shared/command_allowlist.md,
docs/adr/ADR-INDEX.md,
agents/shared/pending_task.md (if present),
agents/shared/agent_status.md (if present),
agents/shared/decision_log.md (if present).
Then execute exactly one scoped task with bounded autonomy.
Do not commit/push unless explicitly asked.
Use encrypted seed-backed secret workflow only.
At end, overwrite agents/shared/agent_status.md and update task_register/open_loops.
```



