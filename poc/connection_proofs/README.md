# Connection Proofs (POC)

This folder contains small, runnable scripts to prove that a resource is reachable before doing full workflow/debug runs.

## Folder Layout

- `poc/connection_proofs/Test-TcpAccess.ps1` - one TCP reachability check
- `poc/connection_proofs/Test-HttpAccess.ps1` - one HTTP reachability check
- `poc/connection_proofs/Run-LocalInfraProofs.ps1` - bundled checks for local StudyBook infra services
- `poc/connection_proofs/lib/ProofUtils.ps1` - shared probe functions
- `poc/connection_proofs/python/mongo_connection_proof.py` - read-only MongoDB proof sample
- `poc/connection_proofs/python/gcp_connection_proof.py` - read-only GCP proof sample
- `poc/connection_proofs/python/aws_connection_proof.py` - read-only AWS STS proof sample
- `poc/connection_proofs/python/azure_connection_proof.py` - read-only Azure account/subscription proof sample
- `poc/connection_proofs/python/databricks_connection_proof.py` - read-only Databricks workspace proof sample`r`n- `poc/connection_proofs/python/snowflake_connection_proof.py` - read-only Snowflake account proof sample

## PowerShell Usage

Single TCP proof:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Test-TcpAccess.ps1 -TargetHost localhost -Port 5432 -Name postgres
```

Single HTTP proof:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Test-HttpAccess.ps1 -Url http://localhost:8082 -Name airflow
```

Bundled local infra proof run:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Run-LocalInfraProofs.ps1
```

## Python Usage

MongoDB read-only proof:

```powershell
python D:\StudyBook\poc\connection_proofs\python\mongo_connection_proof.py
```

GCP read-only proof:

```powershell
python D:\StudyBook\poc\connection_proofs\python\gcp_connection_proof.py
```

AWS read-only proof (STS GetCallerIdentity):

```powershell
python D:\StudyBook\poc\connection_proofs\python\aws_connection_proof.py --profile study
```

Azure read-only proof (CLI + SDK probes):

```powershell
python D:\StudyBook\poc\connection_proofs\python\azure_connection_proof.py --mode both
```

Databricks read-only proof (Current User API with clusters fallback):

```powershell
python D:\StudyBook\poc\connection_proofs\python\databricks_connection_proof.py
```

## Notes

- Python scripts read `_infra/env/.env.local` by default and accept CLI overrides.
- Mongo proof does `ping` and a database name sample only (no writes).
- GCP proof refreshes service-account auth token and does read-only project/storage API checks.
- AWS proof calls `aws sts get-caller-identity` (read-only) via configured CLI profile.
- Azure proof runs read-only account/subscription checks via Azure CLI and optional SDK path.
- Databricks proof calls read-only workspace APIs (`/api/2.0/current-user/me` and fallback `/api/2.0/clusters/list`).
- Databricks proof auto-falls back to seed-backed encrypted StudyBook secrets (config/secrets/shared.secrets.enc.json, config/secrets/<machine>.secrets.enc.json) for DATABRICKS_HOST/DATABRICKS_TOKEN.`r`n- Snowflake proof auto-falls back to seed-backed encrypted StudyBook secrets for SNOWFLAKE_* values and runs a read-only metadata query.
- PowerShell and Python scripts return exit code `0` on success and non-zero on failure.


