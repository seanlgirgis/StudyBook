# Setup and Configuration

Back to [README.md](./README.md)

## What this stack includes

- `postgres`: Airflow metadata database
- `redis`: queue backend for CeleryExecutor
- `airflow-init`: one-time setup (DB migrate + admin user)
- `airflow-webserver`: UI/API
- `airflow-scheduler`: scheduling and task state transitions
- `airflow-triggerer`: deferred task trigger engine
- `airflow-worker`: Celery worker to execute tasks

## Files

- `docker-compose.yml`: service orchestration
- `.env.example`: local defaults (copy to `.env`)
- `dags/`: DAG files mounted into containers
- `scripts/manage.ps1`: helper commands
- `tests/smoke_test.ps1`: basic runtime checks

## First-time setup

1. Open PowerShell in this folder.
2. Create env file:
   `Copy-Item .env.example .env`
3. Run initialization:
   `./scripts/manage.ps1 init`
4. Bring stack up:
   `./scripts/manage.ps1 up`

Continue with [02_deploy_use_and_test.md](./02_deploy_use_and_test.md).