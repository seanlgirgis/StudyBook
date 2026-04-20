---
name: StudyBook secrets system
description: How secrets (passwords/API keys) are encrypted, stored, and auto-loaded at startup via env_setter.ps1
type: project
---

Secrets are encrypted with AES-256-CBC / PBKDF2-SHA256 (150k iterations). Each secret file is a `.enc.json` committed to git.

**Passphrase resolution order** (`Get-SecretPassphrase` in env_core.ps1):
1. `$env:STUDYBOOK_SECRET_PASSPHRASE` (env var, set manually)
2. DPAPI seed file at `config/secrets/.local/studybook.secret.seed.dpapi.json` (machine+user bound, auto-unlocks)
3. Interactive `Read-Host` prompt

**Daily startup:**
```powershell
$env:STUDYBOOK_SECRET_PASSPHRASE = "<passphrase>"   # or rely on seed file
.\env_setter.ps1
```

**What gets auto-loaded** (from `config/env/base.psd1` Secrets.Files):
- `config\secrets\shared.secrets.enc.json`
- `config\secrets\{MACHINE}.secrets.enc.json`
- `config\secrets\azure.secrets.enc.json` (added 2026-04-02)

**IMPORTANT:** `config/env/base.psd1` is gitignored (matched by `ENV/` pattern in .gitignore — a Python venv pattern collision). It must be maintained locally on each machine, not through git.

**Encrypt a new secrets file:**
```powershell
. D:\StudyBook\scripts\env\env_core.ps1
$pass = Get-SecretPassphrase
Protect-StudyBookSecretFile -InputJsonPath "config\secrets\foo.secrets.json" -OutputEncryptedPath "config\secrets\foo.secrets.enc.json" -Passphrase $pass
```

**Why:** Keeps secrets off git while staying portable across machines. The seed file (DPAPI) means no passphrase prompt on the registered machine.
