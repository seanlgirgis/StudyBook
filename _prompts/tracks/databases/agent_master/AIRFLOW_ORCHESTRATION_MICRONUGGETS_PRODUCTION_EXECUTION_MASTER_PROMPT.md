# Airflow Orchestration Micro-Nuggets Production Execution Master Prompt

Use this prompt with external code agents to build a complete, tested Airflow micro-nuggets lane for Data Engineering orchestration and interview preparation.

```text
You are a senior code agent working in this repo: D:\StudyBook

MISSION
Build a production-grade Airflow micro-nuggets system for Data Engineering orchestration depth, operational reliability, and interview readiness.
This must be runnable by a beginner on Windows PowerShell.

PRIMARY TARGET LOCATION
Create everything under:
D:\StudyBook\tracks\12_orchestration\micro_nuggets\airflow

MANDATORY CONTEXT (READ FIRST)
- Existing pipeline Docker stack is already defined in:
  - D:\StudyBook\_infra\docker\pipeline.yml
- Existing infra scripts:
  - D:\StudyBook\_infra\scripts\infra_up.ps1
  - D:\StudyBook\_infra\scripts\infra_down.ps1
  - D:\StudyBook\_infra\scripts\infra_health.ps1
- Airflow service from repo stack:
  - container name: citi_airflow
  - web UI: http://localhost:8082
- Do not create a parallel Airflow stack unless explicitly required.

MANDATORY PRE-WORK (DO THIS FIRST)
1) Discover and reuse repository conventions from existing micro-nugget lanes:
   - run-all runner style
   - prereq checks
   - idempotent setup/reset behavior
2) Validate Airflow service can start with existing repo scripts.
3) Build preparatory setup for Airflow variables/connections and any required local data/tables.
4) Build deterministic run-all validation and execute it before claiming completion.

NON-NEGOTIABLE REQUIREMENTS
- Production-grade code quality and error handling.
- Every nugget runnable with clear PASS/FAIL output.
- Windows-first execution docs.
- Idempotent setup/reset.
- No hardcoded secrets.
- No fake success claims.
- Real validation evidence required before delivery.

PYTHON ENVIRONMENT REQUIREMENTS (MANDATORY)
Use this exact beginner-safe setup flow in README and prereq check:

1) Create/activate venv:
   powershell
   cd D:\StudyBook
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2) Install dependencies:
   powershell
   pip install --upgrade pip
   pip install apache-airflow-client requests

3) For DAG parsing/testing helpers (if needed), include exact package list and why each is required.

DOCKER STARTUP REQUIREMENTS (MANDATORY)
Use repo infra scripts only:

- Start pipeline group:
  powershell
  pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group pipeline

- Health check:
  powershell
  pwsh D:\StudyBook\_infra\scripts\infra_health.ps1

- Open Airflow UI:
  http://localhost:8082

- Stop pipeline group:
  powershell
  pwsh D:\StudyBook\_infra\scripts\infra_down.ps1 -Group pipeline

SCOPE TO IMPLEMENT

A) Folder structure
D:\StudyBook\tracks\12_orchestration\micro_nuggets\airflow\
  00_setup\
  01_dag_basics\
  02_dependencies_and_scheduling\
  03_retries_slas_and_alerting\
  04_data_pipeline_patterns\
  05_operations_and_observability\
  06_interview_drills\
  07_mini_capstone\
  dags\
  _airflow_connect.py
  run_all_airflow_nuggets.py
  AIRFLOW_SPEEDY_STORY_AND_INTERVIEW.md
  AIRFLOW_GLOSSARY.md
  README.md

B) Setup stage (must be implemented and tested)
Create in 00_setup:
1) 00_prereq_check.py
   - Python version and dependency checks
   - Airflow web/API reachability check
   - optional CLI health probe via docker exec (if available)
2) 01_seed_lab.py
   - create required Airflow Variables and (non-secret) Connections for nuggets
   - create required local folders/files for DAG outputs
   - idempotent behavior
3) 99_reset_lab.py
   - cleanup only lab-created variables/connections/dag artifacts
   - requires explicit confirmation flag

C) Required concept coverage

01_dag_basics
- TaskFlow API basics
- PythonOperator/BashOperator examples
- DAG params and templating basics
- XCom fundamentals

02_dependencies_and_scheduling
- task dependency graphs (fan-in/fan-out)
- cron scheduling, catchup, backfill behavior
- start_date pitfalls and timezone basics
- sensors (time/file/external task style)

03_retries_slas_and_alerting
- retries, retry delay, exponential backoff
- SLA concept and timeout handling
- on_failure_callback pattern
- dead-letter/recovery pattern for failed tasks

04_data_pipeline_patterns
- extract -> transform -> load DAG pattern
- idempotent task design
- incremental watermark pattern
- branching and short-circuit pattern

05_operations_and_observability
- DAG run state lifecycle
- task instance logs and troubleshooting
- manual rerun, clear task, mark success/failure semantics
- queue/concurrency pools and parallelism basics

06_interview_drills
- 10+ runnable interview scenarios with concise model answers
- include scheduling, retries, idempotency, backfill, sensors, XCom, failure recovery

07_mini_capstone
- end-to-end orchestration example DAG:
  - ingest small dataset
  - transform with quality checks
  - load result artifact/table
  - simulate one task failure and demonstrate safe rerun recovery

DAG FILE REQUIREMENTS
- Place runnable DAGs under:
  D:\StudyBook\tracks\12_orchestration\micro_nuggets\airflow\dags
- Include clear naming convention and schedule metadata.
- Keep DAGs deterministic and safe for repeated local runs.

RUNNER + VALIDATION (MANDATORY)
Implement:
D:\StudyBook\tracks\12_orchestration\micro_nuggets\airflow\run_all_airflow_nuggets.py

Runner requirements:
- deterministic order
- one-line PASS/FAIL per script
- per-script timeout
- robust subprocess handling
- Windows-safe output encoding
- summary totals and failed list

Mandatory validation before delivery:
1) prereq check
2) setup/seed
3) run all nuggets
4) DAG parse/import checks
5) reset check (optional but preferred)

BEGINNER README (MANDATORY)
Must include exact copy/paste command blocks for:
1) activate venv
2) install dependencies
3) start pipeline Docker stack
4) run prereq check
5) run setup/seed
6) run single nugget
7) run all nuggets
8) run DAG parse test
9) reset lab
10) stop stack

Required error-fix entries:
- Airflow UI not reachable on 8082
- Scheduler/webserver not healthy yet
- DAG not showing in UI
- broken DAG import error
- timezone/catchup confusion
- Windows execution policy issues for venv activation

GLOSSARY + STORY (MANDATORY)
Create:
- AIRFLOW_GLOSSARY.md
  - plain-English definitions
  - include: DAG, task, operator, scheduler, executor, XCom, sensor, SLA, catchup, backfill, pool, concurrency, trigger rule
- AIRFLOW_SPEEDY_STORY_AND_INTERVIEW.md
  - narrative from beginner to DE-ready orchestration
  - 30+ interview Q&A
  - link answers to runnable nuggets and DAGs

QUALITY BAR
- No TODO placeholders.
- No hardcoded secrets.
- No machine-specific absolute paths in runtime logic unless project-root derived.
- Keep files ASCII unless unavoidable.
- Ensure setup + runner are idempotent.

DELIVERY FORMAT
At completion, provide:
1) full file tree created
2) module-by-module implementation summary
3) validation commands executed
4) pass/fail table with totals
5) known constraints/blockers (if any)
6) next recommended phase after Airflow lane

WORK STYLE
- Make reasonable assumptions and proceed.
- Do not pause for optional clarifications.
- Finish end-to-end with tested artifacts.
```
