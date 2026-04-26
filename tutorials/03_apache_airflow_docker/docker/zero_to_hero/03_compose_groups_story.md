# 03 - Compose Files in Groups (Story Style)

Back: [00_START_HERE.md](./00_START_HERE.md)

Imagine you are building a small city.

- First you build roads and utilities.
- Then you build offices and workers.

Docker Compose grouping is the same idea.

## Group 1: Infrastructure base

File: `../compose_groups/00_infra.yml`

This contains foundation services only:
- `postgres`
- `redis`

## Group 2: Airflow application

File: `../compose_groups/10_airflow.yml`

This contains application services:
- `airflow-init`
- `airflow-webserver`
- `airflow-scheduler`
- `airflow-triggerer`
- `airflow-worker`
- `airflow-cli`

## Why groups help

- Easier to learn (infra first, app second)
- Easier to debug (start only infra if needed)
- Easier to expand (add optional groups later)

## Deploy grouped files

PowerShell example:

```powershell
docker compose --project-directory . -f compose_groups/00_infra.yml -f compose_groups/10_airflow.yml up -d
```

In this project, use helper script:

```powershell
./scripts/deploy_groups.ps1 up
```
