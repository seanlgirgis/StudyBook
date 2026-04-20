---
name: Azure setup state
description: Azure account wired into StudyBook secrets system; one manual step pending (fill AZURE_TENANT_ID and encrypt)
type: project
---

Azure subscription linked to GitHub account (`seanlgirgis@gmail.com`):
- Subscription ID: `b3811436-61fc-4a3a-a6a9-deb05955076d`
- Resource Group: `citi-telemetry-rg`
- Location: `eastus`
- Auth method: `az login` + `DefaultAzureCredential` (no service principal)

**Why:** CLI-based auth covers all learning workloads; no client secret needed unless switching to SP auth.

**How to apply:** When helping with Azure notebooks or infra, assume `DefaultAzureCredential` picks up the CLI token. `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_LOCATION` will be in process env after `env_setter.ps1` runs (once encrypted).

### What was done (2026-04-02)
- Created `config/secrets/azure.secrets.json` (gitignored plaintext) with known values; `AZURE_TENANT_ID` is still `replace-me`
- `poc/connection_proofs/python/azure_connection_proof.py` created (committed)
- `CLOUD_ACCOUNT_REGISTRY.md` Azure row filled in (committed)

### Pending manual steps (must be done on each machine)
1. Get tenant ID: `az login` then `az account show --query tenantId -o tsv`
2. Fill `AZURE_TENANT_ID` in `D:\StudyBook\config\secrets\azure.secrets.json`
3. Encrypt: `. D:\StudyBook\scripts\env\env_core.ps1` then `Protect-StudyBookSecretFile -InputJsonPath ... -OutputEncryptedPath config\secrets\azure.secrets.enc.json -Passphrase (Get-SecretPassphrase)`
4. Add `"config\secrets\azure.secrets.enc.json"` to Files array in `D:\StudyBook\config\env\base.psd1` (file is gitignored, update locally)
5. Delete plaintext: `Remove-Item config\secrets\azure.secrets.json`
6. Commit `config/secrets/azure.secrets.enc.json`
