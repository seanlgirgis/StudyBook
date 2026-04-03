# System Build Baseline

Purpose: single operational snapshot of machine prerequisites, cloud access posture, Docker stack, and setup methods for StudyBook.

Last updated: 2026-04-03

## Scope

- What this machine/project expects for local developer runtime.
- Which cloud platforms are configured/verified (non-secret view).
- Which Docker services are part of StudyBook infra and how to start them.
- What software is required vs optional.

## Source-Of-Truth Links

- Cloud account status: `docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md`
- Docker service roles: `docs/operations/docker_service_dictionary.md`
- Environment bootstrap: `docs/PORTABLE_ENV.md`
- Secrets flow: `docs/operations/secrets_workflow.md`
- Connection proofs: `poc/connection_proofs/README.md`
- Infra startup scripts: `_infra/scripts/infra_up.ps1`, `_infra/scripts/infra_down.ps1`, `_infra/scripts/infra_health.ps1`

## Cloud Access (Non-Secret)

Use this as summary only; full details live in the cloud registry.

- AWS: local profiles available; proof verified with `study` profile.
- Azure: proof verified local.
- GCP: key present local; proof workflow available.
- Databricks: proof verified local (fallback endpoint pattern used).
- Snowflake: proof verified local.
- Redshift: not yet verified.
- MongoDB Atlas: provided, test status tracked in registry.

## Docker Stack

StudyBook Docker services are defined in:

- `_infra/docker/core.yml`
- `_infra/docker/streaming.yml`
- `_infra/docker/pipeline.yml`
- `_infra/docker/observability.yml`
- `_infra/docker/docker-compose.yml`

Run methods:

```powershell
cd D:\StudyBook
pwsh .\_infra\scripts\infra_up.ps1 -Group core
pwsh .\_infra\scripts\infra_up.ps1 -Group full
pwsh .\_infra\scripts\infra_health.ps1 -AsJson
pwsh .\_infra\scripts\infra_down.ps1 -Group full
```

Service meanings are documented in:

- `docs/operations/docker_service_dictionary.md`

## Software Baseline

### Required

- PowerShell 7 (`pwsh`)
- Python + project venv (`C:\py_venv\proj_educate`)
- Docker Desktop
- Git
- AWS CLI v2
- Java JDK 17 (for Spark/Apache ecosystem tooling)

### Recommended

- Maven
- SBT + Scala
- VS Code / Cursor

### Optional (per workload)

- Gradle
- Local Spark CLI (`spark-submit`, `pyspark`) if running Spark outside Docker

## Java Baseline (Added 2026-04-03)

Issue observed:

- `java` resolved to legacy Oracle Java 8 alias.
- `javac` and `JAVA_HOME` pointed to JDK 17, creating mismatch.

Actions taken:

- Set user `JAVA_HOME` to:
  - `C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot`
- Added Java 17 preference block in:
  - `C:\Users\shareuser\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`
- Result: new PowerShell sessions resolve `java` to JDK 17 first.

Verification commands (new shell):

```powershell
java -version
javac -version
$env:JAVA_HOME
where.exe java
```

Expected:

- `java -version` shows 17.x
- `javac -version` shows 17.x
- first `where.exe java` result is JDK 17 bin path

Note:

- Machine-level PATH may still contain old Oracle alias entries in some contexts.
- StudyBook PowerShell sessions are corrected via profile precedence.

## How To Rebuild This Machine Quickly

```powershell
cd D:\StudyBook
.\scripts\env\bootstrap_all.ps1
.\env_setter.ps1
pwsh .\_infra\scripts\infra_up.ps1 -Group core
pwsh .\_infra\scripts\infra_health.ps1 -AsJson
```

Then validate key external connectivity with:

```powershell
cd D:\StudyBook\poc\connection_proofs\python
python .\aws_connection_proof.py
python .\gcp_connection_proof.py
python .\azure_connection_proof.py
python .\databricks_connection_proof.py
python .\snowflake_connection_proof.py
```

## Maintenance Rule

- Keep this file updated whenever:
  - a core prerequisite changes,
  - a cloud provider status changes materially,
  - infra service topology changes,
  - local machine bootstrap behavior changes.
