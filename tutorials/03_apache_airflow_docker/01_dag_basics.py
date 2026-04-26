# ============================================================
# Topic   : Apache Airflow for Data Engineers
# File    : 01_dag_basics.py
# Covers  : Linear ETL DAG fundamentals: extract, transform, load, notify
# Prereqs : pip install apache-airflow | airflow standalone running
# Deploy  : cp 01_dag_basics.py ~/airflow/dags/
# Trigger : airflow dags trigger studybook_01_dag_basics  OR use the UI
# ============================================================

"""
A simple linear DAG demonstrating Airflow fundamentals.
DAG ID: studybook_01_dag_basics
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta
from pathlib import Path
import csv
import logging
import os
import random
import time


OUTPUT_DIR = Path(
    "C:/tmp/studybook/airflow" if os.name == "nt"
    else "/tmp/studybook/airflow"
) / "01_dag_basics"

log = logging.getLogger("airflow.task")

default_args = {
    "owner": "studybook",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    "email_on_failure": False,
}


def extract(**context) -> None:
    """
    Simulate data extraction from a source system.

    WHY **context:
    Airflow injects runtime metadata into task callables. The most common interview
    fields are ds, run_id, dag, task, and ti. Here we use ds as the logical date.
    """
    ds = context["ds"]

    raw_dir = OUTPUT_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    output_path = raw_dir / f"extract_{ds}.csv"

    random.seed(ds)

    rows = []
    for i in range(100):
        rows.append({
            "id": i + 1,
            "timestamp": f"{ds}T{i % 24:02d}:00:00",
            "sensor": f"sensor_{i % 10:02d}",
            "value": round(random.uniform(-10, 120), 2),
        })

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "timestamp", "sensor", "value"],
        )
        writer.writeheader()
        writer.writerows(rows)

    log.info("Extracted %s records for %s", len(rows), ds)


def transform(**context) -> None:
    """
    Read extracted data, filter invalid values, and enrich with a status column.

    WHY write files instead of returning large objects:
    Airflow tasks may run in separate processes or workers. Durable intermediate
    storage is safer than relying on in-memory objects between tasks.
    """
    ds = context["ds"]

    input_path = OUTPUT_DIR / "raw" / f"extract_{ds}.csv"
    processed_dir = OUTPUT_DIR / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_path = processed_dir / f"transform_{ds}.csv"

    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        input_rows = list(reader)

    transformed_rows = []
    for row in input_rows:
        value = float(row["value"])

        if value <= 0:
            continue

        parsed_timestamp = datetime.fromisoformat(row["timestamp"])
        status = "NORMAL" if value < 80 else "ALERT"

        transformed_rows.append({
            "id": int(row["id"]),
            "timestamp": parsed_timestamp.isoformat(),
            "sensor": row["sensor"],
            "value": value,
            "status": status,
        })

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "timestamp", "sensor", "value", "status"],
        )
        writer.writeheader()
        writer.writerows(transformed_rows)

    log.info(
        "Transformed records for %s: before=%s after=%s",
        ds,
        len(input_rows),
        len(transformed_rows),
    )


def load(**context) -> None:
    """
    Simulate loading transformed data into a target system.

    WHY this writes another file:
    In production this might insert into Postgres, Snowflake, or BigQuery. For a
    local tutorial DAG, copying to a loaded directory keeps the example runnable.
    """
    ds = context["ds"]

    input_path = OUTPUT_DIR / "processed" / f"transform_{ds}.csv"
    loaded_dir = OUTPUT_DIR / "loaded"
    loaded_dir.mkdir(parents=True, exist_ok=True)

    output_path = loaded_dir / f"load_{ds}.csv"

    with input_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "timestamp", "sensor", "value", "status"],
        )
        writer.writeheader()
        writer.writerows(rows)

    log.info("Loaded %s records to target", len(rows))


def notify(**context) -> None:
    """
    Print a completion notification.

    WHY notification is its own task:
    It makes pipeline completion visible in the DAG graph and allows independent
    retry/alert behavior for the notification step.
    """
    ds = context["ds"]

    message = f"Pipeline complete for {ds}: extracted → transformed → loaded"
    log.info(message)
    print(message)


with DAG(
    dag_id="studybook_01_dag_basics",
    description="Linear ETL: extract → transform → load → notify",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["studybook", "basics"],
) as dag:
    """
    WHY @daily:
    Runs once per day at midnight UTC.

    WHY catchup=False:
    With start_date=2024-01-01, Airflow would try to create many historical
    backfill runs if catchup=True. Tutorial DAGs should usually avoid that.

    WHY fixed start_date:
    datetime.now() changes every DAG parse, causing unstable scheduler behavior.
    """

    t_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
        doc_md="""
        ## Extract Task
        Reads from a simulated source system.

        Output:
        `OUTPUT_DIR/raw/extract_{ds}.csv`
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

    t_bash_checksum = BashOperator(
        task_id="checksum_output",
        bash_command=f"find {OUTPUT_DIR}/loaded -name '*.csv' | head -5",
        doc_md="Verify output files exist using bash.",
    )

    t_notify = PythonOperator(
        task_id="notify",
        python_callable=notify,
    )

    t_extract >> t_transform >> t_load >> t_bash_checksum >> t_notify

    # Equivalent:
    # t_extract.set_downstream(t_transform)
    #
    # WHY >>:
    # It is syntactic sugar for set_downstream.
    # Left side = upstream task.
    # Right side = downstream task.