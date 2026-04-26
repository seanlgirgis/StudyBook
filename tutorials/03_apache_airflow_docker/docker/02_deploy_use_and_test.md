# Deploy, Use, and Test

Back to [README.md](./README.md)

## Start/Stop commands

- Start services:
  `./scripts/manage.ps1 up`
- Stop services:
  `./scripts/manage.ps1 down`
- View status:
  `./scripts/manage.ps1 ps`
- Stream logs:
  `./scripts/manage.ps1 logs`

## Use the stack

1. Place DAGs in `./dags` (a sample DAG is already included).
2. Open [http://localhost:8088](http://localhost:8088).
3. Enable DAG `studybook_docker_hello`.
4. Trigger a run from the UI.

## CLI examples

- List DAGs:
  `./scripts/manage.ps1 dags`
- Trigger sample DAG:
  `docker compose run --rm airflow-cli airflow dags trigger studybook_docker_hello`

## Smoke testing

Run:
`./tests/smoke_test.ps1`

This validates:
- required containers are up
- Airflow health endpoint responds
- sample DAG is discoverable via CLI