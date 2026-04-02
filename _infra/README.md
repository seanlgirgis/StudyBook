# StudyBook Infra

Reproducible local infrastructure for DE/AI learning in `D:\StudyBook`.

## Layout
- `_infra/docker/core.yml` - Postgres, Redis, Cassandra, Neo4j, InfluxDB
- `_infra/docker/streaming.yml` - Zookeeper, Kafka, Kafka UI
- `_infra/docker/pipeline.yml` - Spark master/worker, Airflow, MLflow, JupyterLab
- `_infra/docker/observability.yml` - Elasticsearch, Kibana, Splunk
- `_infra/docker/docker-compose.yml` - full stack (all services)
- `_infra/env/.env.example` - placeholder environment template
- `_infra/scripts/infra_up.ps1` - start infra group (`all|core|streaming|pipeline|observability`)
- `_infra/scripts/infra_down.ps1` - stop infra group (`all|core|streaming|pipeline|observability`)
- `_infra/scripts/infra_seed.ps1` - run idempotent seed scripts (`all|core|tech`)
- `_infra/scripts/infra_health.ps1` - machine-readable infra health report
- `_infra/seeds/seed_core.py` - seeds `telemetry.*`
- `_infra/seeds/seed_tech_telemetry.py` - seeds simplified `public.*`

## Quick Start (Reproducible)
1. Create runtime env file from template:
```powershell
Copy-Item D:\StudyBook\_infra\env\.env.example D:\StudyBook\_infra\env\.env.local
```

2. Start full stack:
```powershell
pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group all
```

3. Run seeds:
```powershell
pwsh D:\StudyBook\_infra\scripts\infra_seed.ps1 -Target all
```

4. Run health checks:
```powershell
pwsh D:\StudyBook\_infra\scripts\infra_health.ps1
pwsh D:\StudyBook\_infra\scripts\infra_health.ps1 -AsJson
```

5. Open JupyterLab (pipeline/all groups):
```powershell
Start-Process http://localhost:8888/lab
```

6. Validate compose rendering:
```powershell
docker compose -f D:\StudyBook\_infra\docker\docker-compose.yml --env-file D:\StudyBook\_infra\env\.env.local config
```

## Service Port Contract
- Postgres `5432`
- Redis `6380`
- Cassandra `9042`
- Neo4j `7474`, `7687`
- InfluxDB `8086`
- Zookeeper `2181`
- Kafka `9092`, `29092`
- Kafka UI `8080`
- Spark master `7077`, `8081`
- Spark worker UI `8085`
- Airflow `8082`
- MLflow `5000`
- JupyterLab `8888`
- Elasticsearch `9200`
- Kibana `5601`
- Splunk `8000`, `8088`, `8089`

## Cloud Account Metadata
- Track non-secret cloud account details in:
  - `docs/programs/zero_to_hero/CLOUD_ACCOUNT_REGISTRY.md`
- Keep secrets only in encrypted secret flow (`config/secrets/*.enc.json`) and local env overlays.

## Service Dictionary
- docs/operations/docker_service_dictionary.md - quick function reference for each Docker service

## Reproducibility Rules
- Keep real credentials in `.env.local`; never commit secret values.
- Keep seed scripts idempotent and deterministic.
- Keep service names and exposed ports stable unless change is documented.
- Use `docker compose ... config` before runtime changes.
