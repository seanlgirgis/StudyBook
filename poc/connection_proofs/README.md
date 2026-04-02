# Connection Proofs (POC)

This folder contains small, runnable scripts to prove that a resource is reachable before doing full workflow/debug runs.

## Folder Layout

- `poc/connection_proofs/Test-TcpAccess.ps1` - one TCP reachability check
- `poc/connection_proofs/Test-HttpAccess.ps1` - one HTTP reachability check
- `poc/connection_proofs/Run-LocalInfraProofs.ps1` - bundled checks for local StudyBook infra services
- `poc/connection_proofs/Run-CoreDockerProofs.ps1` - core stack Docker connect + simple operation checks
- `poc/connection_proofs/Run-StreamingDockerProofs.ps1` - streaming stack Docker connect + simple operation checks
- `poc/connection_proofs/Run-PipelineDockerProofs.ps1` - pipeline stack Docker connect + simple operation checks
- `poc/connection_proofs/Run-ObservabilityDockerProofs.ps1` - observability stack Docker connect + simple operation checks
- `poc/connection_proofs/Run-AllDockerProofs.ps1` - run all Docker group proofs in one command
- `poc/connection_proofs/lib/ProofUtils.ps1` - shared TCP/HTTP probe functions
- `poc/connection_proofs/DockerProofUtils.ps1` - shared Docker group proof helpers
- `poc/connection_proofs/python/mongo_connection_proof.py` - read-only MongoDB proof sample
- `poc/connection_proofs/python/gcp_connection_proof.py` - read-only GCP proof sample
- `poc/connection_proofs/python/aws_connection_proof.py` - read-only AWS STS proof sample
- `poc/connection_proofs/python/azure_connection_proof.py` - read-only Azure account/subscription proof sample
- `poc/connection_proofs/python/databricks_connection_proof.py` - read-only Databricks workspace proof sample
- `poc/connection_proofs/python/snowflake_connection_proof.py` - read-only Snowflake account proof sample
- `poc/connection_proofs/python/_docker_service_common.py` - shared Python Docker proof logic for per-service wrappers

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
- Databricks proof auto-falls back to seed-backed encrypted StudyBook secrets (config/secrets/shared.secrets.enc.json, config/secrets/<machine>.secrets.enc.json) for DATABRICKS_HOST/DATABRICKS_TOKEN.
- Snowflake proof auto-falls back to seed-backed encrypted StudyBook secrets for SNOWFLAKE_* values and runs a read-only metadata query.
- PowerShell and Python scripts return exit code `0` on success and non-zero on failure.





## Docker Service Groups

- Core: `postgres`, `redis`, `cassandra`, `neo4j`, `influxdb`
- Streaming: `zookeeper`, `kafka`, `kafka_ui`
- Pipeline: `spark`, `spark_worker`, `airflow`, `mlflow`, `jupyterlab`
- Observability: `elasticsearch`, `kibana`, `splunk`

## Docker Group Usage

Core group:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Run-CoreDockerProofs.ps1
```

Streaming group:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Run-StreamingDockerProofs.ps1
```

Pipeline group:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Run-PipelineDockerProofs.ps1
```

Observability group:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Run-ObservabilityDockerProofs.ps1
```

All groups:

```powershell
pwsh D:\StudyBook\poc\connection_proofs\Run-AllDockerProofs.ps1
```




## Python Docker Service Scripts

Core:
- `python D:\StudyBook\poc\connection_proofs\python\postgres_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\redis_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\cassandra_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\neo4j_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\influxdb_docker_proof.py`

Streaming:
- `python D:\StudyBook\poc\connection_proofs\python\zookeeper_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\kafka_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\kafka_ui_docker_proof.py`

Pipeline:
- `python D:\StudyBook\poc\connection_proofs\python\spark_master_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\spark_worker_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\airflow_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\mlflow_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\jupyterlab_docker_proof.py`

Observability:
- `python D:\StudyBook\poc\connection_proofs\python\elasticsearch_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\kibana_docker_proof.py`
- `python D:\StudyBook\poc\connection_proofs\python\splunk_docker_proof.py`



Run all Python proofs with one-line status output:

```powershell
python D:\StudyBook\poc\connection_proofs\python\run_all_connection_proofs.py
```
