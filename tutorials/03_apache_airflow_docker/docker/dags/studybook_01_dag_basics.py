# ============================================================
# Topic   : Apache Airflow (Docker) for Data Engineers
# File    : studybook_01_dag_basics.py
# Covers  : Basic DAG structure, PythonOperator, BashOperator, scheduling
# Prereqs : Airflow Docker stack running (http://localhost:8088)
# Deploy  : Place in docker/dags/ (auto-mounted into container)
# Trigger : Use Airflow UI or trigger manually
# ============================================================

"""
A simple linear DAG demonstrating Airflow fundamentals in Docker.

DAG ID: studybook_01_dag_basics

KEY DOCKER CONCEPT:
This DAG runs INSIDE the Airflow container, not your Windows host.

- Host path:
  D:\Workarea\StudyBook\tutorials\03_apache_airflow_docker\docker\dags

- Container path:
  /opt/airflow/dags

All file writes must use container-safe paths like /tmp/, not Windows paths.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from pathlib import Path
import logging, os, random, time, csv

# IMPORTANT: inside container — NOT Windows path
OUTPUT_DIR = Path("/tmp/studybook/01_dag_basics")

log = logging.getLogger("airflow.task")

default_args = {
    "owner": "studybook",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    "email_on_failure": False,
}

# ── Task functions ───────────────────────────────────────────

def extract(**context) -> None:
    """
    Simulate data extraction.

    Writes:
      /tmp/studybook/01_dag_basics/raw/extract_{ds}.csv

    WHY /tmp:
    - Always exists inside Linux containers
    - Safe write location
    - Avoids Windows path issues

    WHY context["ds"]:
    - Logical execution date (NOT current time)
    - Makes DAG deterministic and reproducible
    """

    ds = context["ds"]

    raw_dir = OUTPUT_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    file_path = raw_dir / f"extract_{ds}.csv"

    records = []
    for i in range(100):
        records.append({
            "id": i,
            "value": random.uniform(-10, 100),
            "ts": ds
        })

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "value", "ts"])
        writer.writeheader()
        writer.writerows(records)

    log.info(f"Extracted {len(records)} records for {ds}")
    log.info(f"File written to: {file_path}")


def transform(**context) -> None:
    """
    Transform step:
    - Filter value > 0
    - Add status column

    WHY separate task:
    Airflow enforces task isolation — each step runs independently.
    """

    ds = context["ds"]

    raw_file = OUTPUT_DIR / "raw" / f"extract_{ds}.csv"
    processed_dir = OUTPUT_DIR / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_file = processed_dir / f"transform_{ds}.csv"

    with open(raw_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    before = len(rows)

    filtered = []
    for r in rows:
        value = float(r["value"])
        if value > 0:
            r["status"] = "NORMAL" if value < 80 else "ALERT"
            filtered.append(r)

    after = len(filtered)

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "value", "ts", "status"])
        writer.writeheader()
        writer.writerows(filtered)

    log.info(f"Transform: before={before}, after={after}")
    log.info(f"Output: {output_file}")


def load(**context) -> None:
    """
    Simulate loading data.

    WHY separate load:
    In real pipelines:
    - Extract → API
    - Transform → compute
    - Load → database
    """

    ds = context["ds"]

    processed_file = OUTPUT_DIR / "processed" / f"transform_{ds}.csv"
    loaded_dir = OUTPUT_DIR / "loaded"
    loaded_dir.mkdir(parents=True, exist_ok=True)

    output_file = loaded_dir / f"load_{ds}.csv"

    with open(processed_file, "r") as f:
        data = f.read()

    with open(output_file, "w") as f:
        f.write(data)

    log.info(f"Loaded data for {ds}")
    log.info(f"Target file: {output_file}")


def notify(**context) -> None:
    """
    Final notification step.

    WHY explicit notify task:
    - Central place for alerts
    - Easy to replace with Slack/email later
    """

    ds = context["ds"]
    log.info(f"Pipeline complete for {ds}: extract → transform → load")


# ── DAG definition ───────────────────────────────────────────

with DAG(
    dag_id="studybook_01_dag_basics",
    description="Linear ETL in Docker: extract → transform → load → notify",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["studybook", "docker", "basics"],
) as dag:

    """
    CRITICAL INTERVIEW POINTS:

    start_date:
      Fixed date → required for stable scheduling
      NEVER use datetime.now()

    schedule="@daily":
      Runs once per day (UTC)

    catchup=False:
      Prevents hundreds of backfill runs
    """

    t_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
        doc_md="""
        ## Extract Task
        Generates synthetic data.
        Output: /tmp/studybook/01_dag_basics/raw/
        """,
    )

    t_transform = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    t_load = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    t_bash_check = BashOperator(
        task_id="check_output_files",
        bash_command="ls -lah /tmp/studybook/01_dag_basics/loaded || true",
        doc_md="""
        ## BashOperator Example
        Shows how to run shell commands inside the container.
        """,
    )

    t_notify = PythonOperator(
        task_id="notify",
        python_callable=notify,
    )

    # DAG dependencies
    t_extract >> t_transform >> t_load >> t_bash_check >> t_notify