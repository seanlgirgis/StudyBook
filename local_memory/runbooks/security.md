# Security and Secret Vault

**System of record** for how `local_memory` stores, encrypts, backs up, and retrieves secrets.

Operational registry (pointers only): [secret_registry.md](secret_registry.md)

---

## How the system works

Three layers:

```text
[1] Git-tracked markdown     runbooks/, secret_registry.md  →  commands, notes, pointers only
[2] Git-ignored secrets/     vault + files                   →  real passwords and documents
[3] E: encrypted backup      V:\StudyBook_ignored_backup\    →  mirror of git-ignored files
```

**Flow — store a text secret**

1. You (or Grok) run `scripts/store_text_secret.ps1`.
2. Script unlocks vault using StudyBook seed/passphrase.
3. Value is merged into `secrets/vault.secrets.enc.json` (AES-encrypted).
4. Script writes a **pointer row** to `runbooks/secret_registry.md` (no value).
5. `secrets/` stays out of Git (`.gitignore`).
6. On `gitqall.ps1`, git-ignored `secrets/` copies to `V:\StudyBook_ignored_backup\current\`.

**Flow — store a secret file**

1. Run `scripts/store_secret_file.ps1` — copies file to `secrets/files/<ID>/`.
2. Registry row added with file path and open command.
3. Same gitignore + E: backup path as above.

**Flow — retrieve**

1. Search `runbooks/secret_registry.md` for the ID.
2. Text: run `get_text_secret.ps1` (masked by default).
3. File: open path under `secrets/files/<ID>/`.

---

## What goes where

| Kind | In Git? | Location |
|------|---------|----------|
| Commands, paths, notes | Yes | `runbooks/`, `locations/` |
| Passwords, API keys, tokens | **No** | `secrets/vault.secrets.enc.json` |
| Secret documents (PDF, scans) | **No** | `secrets/files/<ID>/` |
| Pointers (ID, purpose, load cmd) | Yes | `runbooks/secret_registry.md` |

**Classification**

| Tag | Meaning |
|-----|---------|
| `public` | Safe in repo and cloud prompts |
| `internal` | OK in repo; do not send to cloud |
| `secret` | Value in vault only; registry pointer in repo |

---

## Encryption

Reuses **StudyBook** secret infrastructure (no separate vault password).

**Unlock order**

1. **Seed file (usual):** `D:\Workarea\StudyBook\config\secrets\.local\studybook.secret.seed.dpapi.json`  
   DPAPI, machine/user-bound. One-time setup: `StudyBook\scripts\env\register_secret_seed.ps1`
2. **Env var:** `STUDYBOOK_SECRET_PASSPHRASE`
3. **Interactive prompt** if neither is available

**Vault file format:** AES-256-CBC, PBKDF2-SHA256 (150000 iterations) — same as `StudyBook\config\secrets\*.enc.json`.

**Check encryption is ready**

```powershell
pwsh -File D:\Workarea\StudyBook\scripts\env\seed_status.ps1
```

---

## Git ignore

| File | Rule |
|------|------|
| `local_memory/.gitignore` | Ignores `secrets/` |
| `StudyBook/.gitignore` | Ignores `local_memory/secrets/` |

Nothing under `secrets/` is committed to GitHub.

---

## E: encrypted backup

**Prerequisites:** BitLocker VHDX on `E:\EncryptedVaults\` mounted as `V:`.

**Backup root:** `V:\StudyBook_ignored_backup\`

| Subfolder | Purpose |
|-----------|---------|
| `current\` | Mirror of git-ignored files (preserves repo-relative paths) |
| `snapshots\<timestamp>\changed\` | Previous copy before overwrite |
| `snapshots\<timestamp>\removed\` | Copy before removal from mirror |
| `logs\` | Backup and verify logs |

**Run backup** (after git sync):

```powershell
C:\scripts\gitqall.ps1
```

`gitqall.ps1` calls `StudyBook\scripts\backup_gitignored_to_e.ps1` when syncing the StudyBook repo.

**Verify mirror**

```powershell
pwsh -File D:\Workarea\StudyBook\scripts\verify_gitignored_backup.ps1
```

---

## Scripts

All under `local_memory/scripts/`:

| Script | Purpose |
|--------|---------|
| `store_text_secret.ps1` | Save password/key/token to encrypted vault + registry |
| `get_text_secret.ps1` | Retrieve (masked, `-ShowPlaintext`, or `-SetEnv`) |
| `list_text_secrets.ps1` | List key IDs in vault (not values) |
| `remove_text_secret.ps1` | Remove key from vault + registry row |
| `store_secret_file.ps1` | Copy document to `secrets/files/<ID>/` + registry |
| `_vault_common.ps1` | Shared paths and encryption helpers (internal) |

---

## How to store

### Text secret (preferred — value not in chat)

```powershell
cd D:\Workarea\StudyBook\local_memory
pwsh -File scripts\store_text_secret.ps1 -Key POSTGRES_OBS_PASSWORD -Purpose "Local PostgreSQL lab"
```

Script prompts for the value. Registry updates automatically.

**With Grok:** `store secret POSTGRES_OBS_PASSWORD for local PostgreSQL lab`  
Grok runs the script; you type at the terminal prompt.

**Avoid:** pasting secret values in chat (chat logs).

### Secret file

```powershell
pwsh -File scripts\store_secret_file.ps1 -SourcePath "C:\path\document.pdf" -Id TAX_W4_2025 -Purpose "Tax form copy"
```

---

## How to retrieve

1. Open `runbooks/secret_registry.md` and find the ID.
2. **Text secret:**

```powershell
pwsh -File scripts\get_text_secret.ps1 -Key POSTGRES_OBS_PASSWORD
pwsh -File scripts\get_text_secret.ps1 -Key POSTGRES_OBS_PASSWORD -ShowPlaintext
pwsh -File scripts\get_text_secret.ps1 -Key POSTGRES_OBS_PASSWORD -SetEnv
```

3. **File secret:** open the path in the registry under `secrets/files/<ID>/`.

**List text keys**

```powershell
pwsh -File scripts\list_text_secrets.ps1
```

**Remove text secret**

```powershell
pwsh -File scripts\remove_text_secret.ps1 -Key MY_KEY
```

---

## Grok / agent rules

- **Store:** run vault scripts; never write secret values into Git-tracked markdown.
- **Retrieve:** cite `secret_registry.md`; return load command; use `-ShowPlaintext` only when Sean explicitly asks for the value.
- **Lookup:** if ID not in registry, say `I do not have this stored yet.`
- **Cloud:** never send secret values to cloud models.

Triggers: `store secret`, `save secret`, `get secret`, `load secret`.

---

## Legacy notes

Some older entries still reference secrets outside this vault (e.g. `set_env.ps1` for RAG in `runbooks/rag_foundation.md`, `obs_pass` token in `runbooks/postgres.md`). New secrets should use this vault. Migrate when convenient.

---

## Related files

| File | Role |
|------|------|
| [secret_registry.md](secret_registry.md) | Pointer table |
| [CONTROL_PROTOCOL.md](../CONTROL_PROTOCOL.md) | Agent request handling |
| [LOCAL_MEMORY_HANDOFF.md](../LOCAL_MEMORY_HANDOFF.md) | Vault architecture snapshot |
| `StudyBook/scripts/backup_gitignored_to_e.ps1` | E: mirror backup |
| `StudyBook/scripts/env/seed_status.ps1` | Encryption readiness check |

Tags: #security #secrets #encryption #backup #system-of-record