# Tutorials Project on ChatGPT

## Purpose
This file is a context handoff for ChatGPT so tutorial work can move faster with fewer Codex tokens.

## Who Is Codex (Important)
Codex runs on the live development machine (`D:\Workarea\StudyBook`) with full local filesystem access and Docker access.

Codex can:
- read/edit/create files directly in the repository,
- run scripts and validations,
- bring Docker stacks up/down,
- inspect logs and runtime state,
- verify outputs with real commands.

Use ChatGPT for planning, ideation, outlines, teaching narratives, and content design.
Use Codex for execution, file changes, and real environment validation.

## Sessions to Keep in Context
Relevant sessions for this tutorial workflow:
- `019dcb22-f172-75a2-bc85-eaa204234111`
- `019dcaf1-7f8d-7503-9ecc-431b03412b7b`
- `019dcab5-4000-77f3-b147-a26eee867019`

## What Was Completed in This Workstream
Inside `tutorials/03_apache_airflow_docker/docker`, Codex built a full from-scratch Airflow Docker learning pack and validated it.

### Delivered
- Full compose-based Airflow stack with:
  - Airflow webserver, scheduler, worker, triggerer, init, cli
  - Postgres metadata DB
  - Redis broker
- Environment templates (`.env.example`) and helper scripts
- Smoke test script for stack readiness
- Beginner DAG sample (`studybook_docker_hello`)
- Beginner tutorial path (`zero_to_hero`)
- Grouped compose examples (`compose_groups`)
- Tool handoff card (`TOOL_INFO_CARD.yaml`)
- Safe destroy option in grouped deploy script

### Naming + Cleanup
- Project name standardized to `docker_airflow`
- Legacy `citi_airflow` container/volumes removed

## Current Docker Access and Running Containers
Codex currently sees active containers including:
- `docker_airflow-airflow-webserver-1`
- `docker_airflow-airflow-scheduler-1`
- `docker_airflow-airflow-worker-1`
- `docker_airflow-airflow-triggerer-1`
- `docker_airflow-postgres-1`
- `docker_airflow-redis-1`
- `citi_spark`, `citi_spark_worker`, `citi_jupyterlab`
- `studybook_index_ui`

This confirms Docker is available and tutorial stacks are runnable.

## Tutorial Scope We Are Working On
Primary active lane:
- `tutorials/03_apache_airflow_docker`

Broader tutorials catalog is under:
- `D:\Workarea\StudyBook\tutorials\01_*` through `47_*`
- includes lanes like PySpark, AWS services, SQL, testing, FastAPI, Terraform, Redis, etc.

## How ChatGPT Should Collaborate with Codex (Token-Saving Protocol)
1. ChatGPT proposes structure, lesson goals, and acceptance criteria.
2. ChatGPT asks Codex to implement directly in files with exact paths.
3. Codex runs local validation and returns factual results.
4. ChatGPT iterates only on deltas (not full rewrites).
5. Keep prompts scoped by file and outcome.

### Recommended Prompt Pattern for ChatGPT
"Codex, in `D:\Workarea\StudyBook`, edit `<exact files>` to implement `<exact outcome>`. Then run `<exact commands>` and report pass/fail with key logs."

## Working Commands (Airflow Docker Tutorial)
From:
`D:\Workarea\StudyBook\tutorials\03_apache_airflow_docker\docker`

- Start grouped stack:
  - `./scripts/deploy_groups.ps1 up`
- Init only:
  - `./scripts/deploy_groups.ps1 init`
- Status:
  - `./scripts/deploy_groups.ps1 ps`
- Stop:
  - `./scripts/deploy_groups.ps1 down`
- Safe destroy (with confirmation):
  - `./scripts/deploy_groups.ps1 destroy`
- Force destroy (automation):
  - `./scripts/deploy_groups.ps1 destroy -Force`
- Smoke test:
  - `./tests/smoke_test.ps1`
- Open UI:
  - `http://localhost:8088` (admin/admin)

## Key Files to Reuse
- `tutorials/03_apache_airflow_docker/docker/README.md`
- `tutorials/03_apache_airflow_docker/docker/zero_to_hero/00_START_HERE.md`
- `tutorials/03_apache_airflow_docker/docker/TOOL_INFO_CARD.yaml`
- `tutorials/03_apache_airflow_docker/docker/scripts/manage.ps1`
- `tutorials/03_apache_airflow_docker/docker/scripts/deploy_groups.ps1`
- `tutorials/03_apache_airflow_docker/docker/scripts/newbie_dag.ps1`

## Notes
- `.env.example` is a template; local `.env` is machine-specific runtime config.
- Compose files are common patterns developers adapt, not typically memorized line-by-line.
- For production-grade tutorials, keep secrets out of DAG code and use Airflow Variables/Connections.