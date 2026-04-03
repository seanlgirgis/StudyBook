# Airflow Orchestration Micro-Nuggets

Production-grade Airflow study lane for Data Engineering depth and
interview preparation.  Windows-first setup, Docker-backed, idempotent.

---

## Directory Structure

```
airflow/
  _airflow_connect.py               <- Shared connection helper
  run_all_airflow_nuggets.py        <- Master runner (PASS/FAIL per nugget)
  AIRFLOW_GLOSSARY.md               <- Plain-English definitions
  AIRFLOW_SPEEDY_STORY_AND_INTERVIEW.md  <- Story + 32 Q&A
  README.md                         <- This file

  00_setup/
    00_prereq_check.py              <- Python + package + API reachability
    01_seed_lab.py                  <- Create Variables, Connections, dirs
    99_reset_lab.py                 <- Delete all lab objects (--confirm)

  01_dag_basics/
    01_taskflow_api.py              <- @dag + @task, automatic XCom
    02_python_bash_operators.py     <- Classic operator style
    03_dag_params_and_templating.py <- Params, {{ ds }}, Jinja templates
    04_xcom_fundamentals.py         <- XCom push/pull, size limits

  02_dependencies_and_scheduling/
    01_dependency_graphs.py         <- Fan-in/fan-out, trigger rules
    02_scheduling_and_catchup.py    <- Cron, execution_date, catchup
    03_sensors.py                   <- FileSensor, ExternalTaskSensor

  03_retries_slas_and_alerting/
    01_retries_and_backoff.py       <- Retries, exponential backoff, callbacks
    02_sla_and_timeouts.py          <- SLA vs execution_timeout

  04_data_pipeline_patterns/
    01_etl_pattern.py               <- ETL with quality check + idempotent load
    02_branching_and_shortcircuit.py <- BranchPythonOperator, ShortCircuit

  05_operations_and_observability/
    01_dag_run_lifecycle.py         <- States, clear, mark, pools, CLI

  06_interview_drills/
    01_interview_drills.py          <- 12 runnable interview scenarios

  07_mini_capstone/
    01_mini_capstone.py             <- End-to-end pipeline with failure recovery

  dags/
    lab_etl_daily.py                <- Daily ETL DAG (mountable to Airflow)
    lab_capstone_pipeline.py        <- Capstone DAG with full patterns
```

---

## Prerequisites

### Python
- Python 3.8 or higher

### Packages
```powershell
pip install requests apache-airflow-client
```
For DAG parsing/testing (runs all nuggets fully):
```powershell
pip install apache-airflow
```

### Docker
The Airflow service is part of the existing StudyBook pipeline stack.
No separate install required.

---

## Setup — Step by Step

### 1. Activate virtual environment

```powershell
cd D:\StudyBook
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install dependencies

```powershell
pip install --upgrade pip
pip install requests apache-airflow-client
# Optional (for full DAG parsing):
pip install apache-airflow
```

### 3. Start the pipeline Docker stack

```powershell
pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group pipeline
```

Airflow UI: http://localhost:8082
Default credentials: `airflow` / `airflow`

### 4. Wait for Airflow to start

The first startup takes ~60 seconds.  Run the health check:
```powershell
pwsh D:\StudyBook\_infra\scripts\infra_health.ps1
```

### 5. Run the prerequisite check

```powershell
cd D:\StudyBook\tracks\12_orchestration\micro_nuggets\airflow
python 00_setup/00_prereq_check.py
```

Expected output:
```
-- Airflow Prerequisite Check ---------------------

  [OK] Python 3.12.x  (requires >= 3.8)
  [OK] requests 2.x.x

  Credentials resolved:
    Host:     localhost
    Port:     8082
    User:     airflow
    Source:   defaults

  Testing live connection...
  [OK] Connected!  Airflow 2.8.0

  All prerequisites met. Ready to run nuggets!
```

### 6. Seed the lab environment

```powershell
python 00_setup/01_seed_lab.py
```

Creates:
- Airflow Variables: `lab_airflow_*`
- Airflow Connections: `lab_airflow_postgres`, `lab_airflow_filesystem`
- Output dir variable: `lab_airflow_output_dir` (runtime/container scoped, default `/tmp/airflow_lab`)

Optional portability override for non-standard Docker host routing:
```powershell
$env:LAB_POSTGRES_HOST="host.docker.internal"
# (set to your reachable host alias/IP if needed)
```

---

## Running Nuggets

### Run a single nugget

```powershell
python 01_dag_basics/01_taskflow_api.py
python 02_dependencies_and_scheduling/02_scheduling_and_catchup.py
```

### Run all nuggets

```powershell
python run_all_airflow_nuggets.py
```

Expected output:
```
======================================================================
  Airflow Micro-Nuggets - Full Validation
======================================================================

  Running: 00_setup/00_prereq_check.py
  Running: 00_setup/01_seed_lab.py
  ...

----------------------------------------------------------------------
  Script                                               Result  Time
----------------------------------------------------------------------
  00_setup/00_prereq_check.py                          PASS    1.2s
  00_setup/01_seed_lab.py                              PASS    2.1s
  01_dag_basics/01_taskflow_api.py                     PASS    1.5s
  ...
----------------------------------------------------------------------
  Total: 16  |  Passed: 16  |  Skipped: 0  |  Failed: 0
======================================================================

  All nuggets passed! [OK]
```

### Run DAG parse test

```powershell
python -c "import sys; sys.path.insert(0,'dags'); import lab_etl_daily; print('[OK] DAG parsed')"
python -c "import sys; sys.path.insert(0,'dags'); import lab_capstone_pipeline; print('[OK] DAG parsed')"
```

---

## Reset Lab

```powershell
python 00_setup/99_reset_lab.py --confirm
```

Removes all `lab_airflow_*` Variables and Connections.

---

## Stop the Stack

```powershell
pwsh D:\StudyBook\_infra\scripts\infra_down.ps1 -Group pipeline
```

---

## Key Concepts Covered

| Topic                   | Nugget                    | Interview Relevance          |
|-------------------------|---------------------------|------------------------------|
| TaskFlow API            | 01-01                     | Airflow 2.0 authoring style  |
| XCom                    | 01-04                     | Data passing between tasks   |
| execution_date          | 02-02                     | Most common interview trap   |
| catchup + backfill      | 02-02                     | Historical reprocessing      |
| Sensors (poke/reschedule) | 02-03                   | Slot starvation prevention   |
| Retries + backoff       | 03-01                     | Transient failure handling   |
| SLA vs timeout          | 03-02                     | Production monitoring        |
| ETL idempotency         | 04-01                     | Safe rerun pattern           |
| Branching               | 04-02                     | Conditional pipelines        |
| Pools                   | 05-01                     | Concurrency control          |
| Interview scenarios     | 06-01                     | 12 runnable Q&A              |
| End-to-end pipeline     | 07-01                     | Full design walkthrough      |

---

## Common Errors and Fixes

### Airflow UI not reachable on port 8082

```
[FAIL] Cannot reach Airflow at http://localhost:8082
```

Fix:
```powershell
# Start the pipeline stack
pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group pipeline
# Wait 60 seconds for Airflow to initialize
pwsh D:\StudyBook\_infra\scripts\infra_health.ps1
```

---

### Scheduler not healthy yet

```
[WARN] Scheduler status: starting
```

Wait 60-90 seconds.  The Airflow standalone command starts the webserver,
scheduler, and triggerer in sequence.  Run:
```powershell
python 00_setup/00_prereq_check.py
```
again until scheduler shows `healthy`.

---

### DAG not showing in the UI

1. Check the DAG file is in the container's `/opt/airflow/dags` volume
2. The Airflow UI auto-refreshes every 30 seconds
3. Check for import errors: `airflow dags list-import-errors`
4. Verify the DAG is not paused (toggle in UI or `airflow dags unpause dag_id`)

---

### Broken DAG import error

```
ERROR - Failed to import: lab_etl_daily
```

Debug steps:
```bash
# Inside the container:
docker exec -it citi_airflow bash
python /opt/airflow/dags/lab_etl_daily.py
```
Fix any Python import or syntax errors, then the UI refreshes automatically.

---

### Timezone / catchup confusion

Symptom: DAG ran but processed the wrong date.
Cause: `start_date` without timezone is interpreted as UTC.
Fix: always set timezone explicitly:
```python
from datetime import datetime, timezone
start_date=datetime(2024, 1, 1, tzinfo=timezone.utc)
```

---

### Windows execution policy for venv activation

```
.\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled
```

Fix (run once per machine):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### apache-airflow not installed — nuggets show [SKIP]

Most nuggets use a try/except for the `airflow` import and print `[SKIP]`
if not installed.  This is by design — the concepts are still documented.
To run fully:
```powershell
pip install apache-airflow
python run_all_airflow_nuggets.py
```

---

## Reference Documents

- [AIRFLOW_GLOSSARY.md](AIRFLOW_GLOSSARY.md) — Plain-English definitions
- [AIRFLOW_SPEEDY_STORY_AND_INTERVIEW.md](AIRFLOW_SPEEDY_STORY_AND_INTERVIEW.md) — Story + 32 Q&A
- [Apache Airflow Docs](https://airflow.apache.org/docs/) (official)
- [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
