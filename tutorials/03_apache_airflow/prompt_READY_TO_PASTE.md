# ChatGPT Prompt — Apache Airflow for Data Engineers
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: Apache Airflow for Data Engineers
SLUG: apache_airflow
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — Airflow standalone mode
NO AWS, NO DOCKER, NO CLEANUP RULES NEEDED.

SETUP (run once before generating files):
  pip install apache-airflow
  airflow db migrate
  airflow standalone   ← starts scheduler + webserver at localhost:8080

DAG FILES go in ~/airflow/dags/
All file I/O uses C:/tmp/studybook/airflow/ (Windows) or /tmp/studybook/airflow/ (Linux/Mac).

===== CODING STANDARDS =====

FILE HEADER (every file):
# ============================================================
# Topic   : Apache Airflow for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install apache-airflow | airflow standalone running
# Deploy  : cp NN_filename.py ~/airflow/dags/
# Trigger : airflow dags trigger <dag_id>  OR use the UI
# ============================================================

CRITICAL — CODE QUALITY:
- Every DAG must be importable without errors: airflow dags list must show it.
- Every function/task COMPLETE — no pass, no TODO, no placeholders.
- Generate the ENTIRE file every time.
- Comments explain WHY — Airflow concepts like XCom limits, scheduler behavior,
  task isolation, and catchup are the interview topics. Make every choice explicit.
- start_date: always use a fixed past date like datetime(2024, 1, 1) — never datetime.now().
  WHY: scheduler calculates backfill from start_date. datetime.now() moves every import
  and causes unpredictable scheduling behavior.
- catchup=False for all tutorial DAGs unless demonstrating backfill explicitly.
- All paths use pathlib.Path. Create dirs with exist_ok=True.

===== FILE 01: 01_dag_basics.py =====

"""
A simple linear DAG demonstrating Airflow fundamentals.
DAG ID: studybook_01_dag_basics
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from pathlib import Path
import logging, os, time

OUTPUT_DIR = Path("C:/tmp/studybook/airflow" if os.name == "nt"
                  else "/tmp/studybook/airflow") / "01_dag_basics"

log = logging.getLogger("airflow.task")

default_args = {
    "owner": "studybook",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    "email_on_failure": False,
}

# ── Task functions ────────────────────────────────────────────────────────────

def extract(**context) -> None:
    """
    Simulate data extraction from a source system.
    Generate 100 synthetic sensor records and write to OUTPUT_DIR/raw/extract_{date}.csv
    Log: "Extracted {n} records for {ds}"
    WHY **context: Airflow passes execution context (ds, run_id, dag, etc.) as kwargs.
    Access with context["ds"] for the logical date.
    """

def transform(**context) -> None:
    """
    Read the extract file, apply transformations:
      - Parse timestamp to datetime
      - Filter rows where value > 0
      - Add derived column: status = "NORMAL" if value < 80 else "ALERT"
    Write to OUTPUT_DIR/processed/transform_{date}.csv
    Log record count before and after filter.
    """

def load(**context) -> None:
    """
    Read the processed file, simulate load to target:
      Write to OUTPUT_DIR/loaded/load_{date}.csv (simulating DB insert)
    Log: "Loaded {n} records to target"
    """

def notify(**context) -> None:
    """
    Print a completion notification with run summary:
      "Pipeline complete for {ds}: extracted → transformed → loaded"
    In production this would call Slack, email, or SNS.
    """

# ── DAG definition ────────────────────────────────────────────────────────────

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
    WHY @daily: runs once per day at midnight UTC.
    WHY catchup=False: with start_date=2024-01-01, Airflow would try to run 400+
    backfill runs if catchup=True. Production DAGs almost always set catchup=False.
    WHY fixed start_date: avoids moving-window scheduling chaos.
    """

    t_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
        doc_md="""
        ## Extract Task
        Reads from simulated source system. Retries 2× on failure.
        Output: OUTPUT_DIR/raw/extract_{ds}.csv
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

    # Dependency chain — show both >> and set_downstream equivalents
    t_extract >> t_transform >> t_load >> t_bash_checksum >> t_notify

    # Equivalent: t_extract.set_downstream(t_transform)
    # WHY >>: syntactic sugar for set_downstream. Left = upstream, Right = downstream.

===== FILE 02: 02_operators_and_sensors.py =====

"""
DAG demonstrating core operators and sensors.
DAG ID: studybook_02_operators_sensors
"""
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from pathlib import Path
import logging, os, random

OUTPUT_DIR = Path("C:/tmp/studybook/airflow" if os.name == "nt"
                  else "/tmp/studybook/airflow") / "02_operators"

def create_trigger_file(**context) -> None:
    """
    Write a trigger file to OUTPUT_DIR/trigger/ready.txt so the FileSensor fires.
    In production this would be a file landing in S3 triggering downstream processing.
    """

def branch_logic(**context) -> str:
    """
    BranchPythonOperator function. Returns task_id of the branch to follow.
    Logic: if random.random() > 0.5 → return "process_large_batch"
           else → return "process_small_batch"
    WHY BranchPythonOperator: routes the DAG to different tasks based on runtime
    conditions (file size, API response, feature flags, etc.).
    The non-chosen branch tasks are SKIPPED, not failed.
    """

def process_large_batch(**context) -> None:
    """Simulate processing a large batch. Sleep 2s. Log 'Processing large batch...'"""

def process_small_batch(**context) -> None:
    """Simulate processing a small batch. Sleep 0.5s. Log 'Processing small batch...'"""

def cleanup_task(**context) -> None:
    """
    Always runs regardless of upstream success/failure (TriggerRule.ALL_DONE).
    Deletes the trigger file. Logs completion.
    WHY ALL_DONE: cleanup should always happen even if processing fails.
    Without this, failed runs leave temp files/locks that block future runs.
    """

with DAG(
    dag_id="studybook_02_operators_sensors",
    default_args={"owner": "studybook", "retries": 1,
                  "retry_delay": timedelta(seconds=30)},
    start_date=datetime(2024, 1, 1),
    schedule=None,   # manual trigger only for this demo
    catchup=False,
    tags=["studybook", "operators"],
) as dag:

    t_create_file = PythonOperator(
        task_id="create_trigger_file",
        python_callable=create_trigger_file,
    )

    t_wait_for_file = FileSensor(
        task_id="wait_for_trigger_file",
        filepath=str(OUTPUT_DIR / "trigger" / "ready.txt"),
        mode="reschedule",        # releases worker slot while waiting
        poke_interval=10,         # check every 10 seconds
        timeout=120,              # fail after 2 minutes
        doc_md="""
        ## FileSensor — reschedule mode
        WHY reschedule (not poke): poke mode holds a worker slot the entire time.
        reschedule mode releases the worker between checks — critical in production
        where worker slots are limited. Use reschedule for sensors > 1 minute wait.
        """,
    )

    t_branch = BranchPythonOperator(
        task_id="branch_on_batch_size",
        python_callable=branch_logic,
    )

    t_large = PythonOperator(task_id="process_large_batch",
                              python_callable=process_large_batch)
    t_small = PythonOperator(task_id="process_small_batch",
                              python_callable=process_small_batch)

    t_cleanup = PythonOperator(
        task_id="cleanup",
        python_callable=cleanup_task,
        trigger_rule=TriggerRule.ALL_DONE,  # runs even if a branch task failed
    )

    t_create_file >> t_wait_for_file >> t_branch >> [t_large, t_small] >> t_cleanup

===== FILE 03: 03_xcom_variables_connections.py =====

"""
DAG demonstrating XCom, Variables, and Connections.
DAG ID: studybook_03_xcom_variables
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.hooks.base import BaseHook
from datetime import datetime, timedelta
import logging, json

log = logging.getLogger("airflow.task")

def extract_and_push(**context) -> None:
    """
    Generate 500 synthetic records.
    Push metadata to XCom:
      context["ti"].xcom_push(key="record_count", value=500)
      context["ti"].xcom_push(key="source", value="sensor_api")
    WHY XCom for metadata, not data: XCom is stored in the Airflow metadata DB.
    Max size ≈ 48KB (SQLite) / larger with PostgreSQL backend but still limited.
    NEVER push DataFrames, large JSON, or file contents through XCom.
    Push the FILE PATH, not the file contents.
    """

def validate_counts(**context) -> None:
    """
    Pull record count from XCom:
      count = context["ti"].xcom_pull(task_ids="extract_and_push", key="record_count")
    Validate: if count < 100, raise AirflowException("Too few records: {count}")
    Log the count and source.
    WHY pull by task_ids: XCom is keyed by (dag_id, task_id, run_id, key).
    Always specify task_ids to avoid ambiguity in complex DAGs.
    """

def read_variable_config(**context) -> None:
    """
    Read Airflow Variables:
      min_records = Variable.get("studybook_min_records", default_var="100", deserialize_json=False)
      pipeline_config = Variable.get("studybook_pipeline_config", default_var="{}", deserialize_json=True)
    Log both values.
    WHY Variables: config that changes between environments (dev/staging/prod) without
    code deploy. Set via UI, CLI, or Secrets Backend (Vault/AWS SSM in production).
    WHY default_var: prevents KeyError if variable not yet created — safe for first run.
    """

def demonstrate_connection(**context) -> None:
    """
    Demonstrate how to retrieve a Connection (without actually connecting):
      try:
          conn = BaseHook.get_connection("studybook_postgres")
          log.info(f"Connection: host={conn.host} schema={conn.schema}")
      except AirflowNotFoundException:
          log.warning("Connection 'studybook_postgres' not configured — skipping demo")
          log.info("In production: airflow connections add --conn-id studybook_postgres ...")
    WHY Connections: credentials stored encrypted in Airflow metadata DB, not in code.
    Rotate passwords without touching DAG files. Integrate with Vault in production.
    """

with DAG(
    dag_id="studybook_03_xcom_variables",
    default_args={"owner": "studybook", "retries": 1},
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["studybook", "xcom"],
) as dag:

    t1 = PythonOperator(task_id="extract_and_push", python_callable=extract_and_push)
    t2 = PythonOperator(task_id="validate_counts",   python_callable=validate_counts)
    t3 = PythonOperator(task_id="read_config",       python_callable=read_variable_config)
    t4 = PythonOperator(task_id="demo_connection",   python_callable=demonstrate_connection)

    t1 >> t2 >> t3 >> t4

===== FILE 04: 04_dynamic_dags_and_taskflow.py =====

"""
Modern Airflow 2.x patterns: TaskFlow API, dynamic task mapping.
DAG ID: studybook_04_taskflow
"""
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path
import os, json, logging

OUTPUT_DIR = Path("C:/tmp/studybook/airflow" if os.name == "nt"
                  else "/tmp/studybook/airflow") / "04_taskflow"

# ── TaskFlow API DAG ──────────────────────────────────────────────────────────

@dag(
    dag_id="studybook_04_taskflow",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["studybook", "taskflow"],
)
def taskflow_pipeline():
    """
    Same extract→validate→transform→load pipeline as file 01, but using
    the modern @dag and @task decorators.
    WHY TaskFlow: @task automatically handles XCom push/pull. Return values
    from one @task are transparently passed to the next — no manual xcom_push.
    WHY not always TaskFlow: classic operators (S3Hook, PostgresOperator, etc.)
    have no @task equivalent. Mix both styles as needed.
    """

    @task
    def extract() -> dict:
        """
        Generate 200 sensor records.
        Return {"record_count": 200, "file_path": str(path), "source": "sensor_api"}
        WHY return dict: TaskFlow passes the entire return value as XCom.
        Keep it small — metadata only.
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        records = [{"id": i, "value": i * 1.5} for i in range(200)]
        path = OUTPUT_DIR / "raw_data.json"
        path.write_text(json.dumps(records))
        return {"record_count": 200, "file_path": str(path), "source": "sensor_api"}

    @task
    def validate(extract_result: dict) -> dict:
        """
        Validate extract_result["record_count"] >= 100.
        Raise ValueError if not. Return extract_result unchanged.
        Note: extract_result is automatically pulled from XCom by TaskFlow.
        """
        if extract_result["record_count"] < 100:
            raise ValueError(f"Too few records: {extract_result['record_count']}")
        logging.getLogger("airflow.task").info(
            f"Validation passed: {extract_result['record_count']} records")
        return extract_result

    @task
    def transform(validated: dict) -> dict:
        """Read file at validated["file_path"], double each value, write transformed."""
        path = Path(validated["file_path"])
        records = json.loads(path.read_text())
        transformed = [{"id": r["id"], "value": r["value"] * 2} for r in records]
        out_path = OUTPUT_DIR / "transformed_data.json"
        out_path.write_text(json.dumps(transformed))
        return {"record_count": len(transformed), "file_path": str(out_path)}

    @task
    def load(transform_result: dict) -> None:
        """Simulate load. Log completion."""
        logging.getLogger("airflow.task").info(
            f"Loaded {transform_result['record_count']} records from "
            f"{transform_result['file_path']}")

    # Wire the DAG — TaskFlow infers dependencies from return value → parameter
    raw     = extract()
    valid   = validate(raw)
    trans   = transform(valid)
    load(trans)

taskflow_dag = taskflow_pipeline()


# ── Dynamic Task Mapping DAG ──────────────────────────────────────────────────

@dag(
    dag_id="studybook_04_dynamic_mapping",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["studybook", "dynamic"],
)
def dynamic_mapping_pipeline():
    """
    Process a list of files — one task per file — using .expand().
    WHY dynamic mapping: instead of writing process_file_1, process_file_2, ...
    TaskFlow creates tasks at runtime based on the actual file list.
    Airflow 2.3+ feature.
    """

    @task
    def list_files() -> list[str]:
        """
        Generate 5 synthetic file paths to "process".
        Return list of strings: ["/tmp/file_1.csv", "/tmp/file_2.csv", ...]
        """
        return [f"/tmp/studybook/file_{i}.csv" for i in range(1, 6)]

    @task
    def process_file(file_path: str) -> dict:
        """
        Simulate processing one file. Sleep 0.5s.
        Return {"file": file_path, "rows": 1000, "status": "ok"}.
        This task runs ONCE PER FILE — 5 parallel tasks for 5 files.
        WHY: parallelism without writing 5 separate PythonOperators.
        """
        import time
        time.sleep(0.5)
        return {"file": file_path, "rows": 1000, "status": "ok"}

    @task
    def summarize(results: list[dict]) -> None:
        """Print summary of all processed files."""
        total = sum(r["rows"] for r in results)
        logging.getLogger("airflow.task").info(
            f"Processed {len(results)} files, {total} total rows")

    files   = list_files()
    results = process_file.expand(file_path=files)  # .expand() = dynamic mapping
    summarize(results)

dynamic_dag = dynamic_mapping_pipeline()

===== FILE 05: 05_error_handling_and_monitoring.py =====

"""
Production DAG patterns: callbacks, SLAs, retries, logging.
DAG ID: studybook_05_error_handling
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import logging, traceback, time, random, os
from pathlib import Path

log = logging.getLogger("airflow.task")

def on_failure_callback(context: dict) -> None:
    """
    Called by Airflow when any task fails.
    context keys: dag, dag_run, task, task_instance, exception, logical_date
    Print a formatted failure report:
      ❌ TASK FAILED
      DAG:       {context['dag'].dag_id}
      Task:      {context['task'].task_id}
      Run:       {context['dag_run'].run_id}
      Date:      {context['logical_date']}
      Exception: {str(context.get('exception', 'unknown'))}
    In production: send to Slack (SlackWebhookHook) or PagerDuty.
    WHY callback not email_on_failure: callbacks run in process, have full context,
    can include custom fields. email_on_failure just sends a fixed template.
    """

def on_success_callback(context: dict) -> None:
    """
    Called when DAG run completes successfully (dag-level callback).
    Log pipeline metrics: duration, task count, run_id.
    """

def extract_with_retry(**context) -> None:
    """
    Simulate an unreliable extract that fails on first 2 attempts.
    Use context["ti"].try_number to track attempt.
    On attempt < 3: raise ConnectionError("Upstream API timeout")
    On attempt >= 3: succeed and write output file.
    WHY: demonstrates that Airflow retries call the same Python function —
    the task function must be idempotent (safe to run multiple times).
    """

def transform_with_sla(**context) -> None:
    """
    Simulate a slow transform (sleep 3 seconds).
    Log start and end times.
    In the DAG, this task has sla=timedelta(seconds=1) — will trigger SLA miss callback.
    WHY SLA: SLA (Service Level Agreement) miss fires if a task doesn't complete
    within its SLA window from DAG start. Airflow calls sla_miss_callback.
    SLA miss does NOT fail the task — it's an alerting mechanism only.
    """

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis) -> None:
    """
    Called when any task misses its SLA.
    Log: "SLA MISS on tasks: {[t.task_id for t in task_list]}"
    In production: page the on-call engineer.
    """

def always_cleanup(**context) -> None:
    """
    Cleanup task with TriggerRule.ALL_DONE.
    Deletes temp files, logs final status.
    Checks context["ti"].xcom_pull to see if upstream succeeded or failed.
    """

with DAG(
    dag_id="studybook_05_error_handling",
    default_args={
        "owner":           "studybook",
        "retries":         3,
        "retry_delay":     timedelta(seconds=5),
        "retry_exponential_backoff": True,  # 5s, 10s, 20s delays
        "on_failure_callback": on_failure_callback,
    },
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    on_success_callback=on_success_callback,
    sla_miss_callback=sla_miss_callback,
    tags=["studybook", "error-handling"],
) as dag:

    t_extract = PythonOperator(
        task_id="extract_with_retry",
        python_callable=extract_with_retry,
    )

    t_transform = PythonOperator(
        task_id="transform_with_sla",
        python_callable=transform_with_sla,
        sla=timedelta(seconds=1),  # will miss — transform sleeps 3s
    )

    t_cleanup = PythonOperator(
        task_id="always_cleanup",
        python_callable=always_cleanup,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    t_extract >> t_transform >> t_cleanup

===== CAPSTONE PROJECT =====

Title: Daily ETL Orchestration DAG
Scenario: Orchestrates a daily data pipeline — extract → validate → transform → load → notify.
Tests cover DAG import, task behavior, and XCom flow.

Directory layout:
  capstone/
    capstone_dag.py    ← place in ~/airflow/dags/
    test_capstone.py   ← pytest using DagBag

===== CAPSTONE FILE: capstone_dag.py =====

"""
Daily ETL Orchestration DAG — Airflow Capstone.
DAG ID: studybook_capstone_etl

Pipeline:
  ExtractTask     — query source (simulated SQLite), push row count via XCom
  ValidateTask    — pull count, fail if < 100 or null rate > 5%
  TransformTask   — pandas transform: clean, enrich, aggregate; write to /tmp/
  LoadTask        — load processed file to target (simulated)
  NotifyTask      — always runs (ALL_DONE), reports pipeline status + metrics

Production features:
  - on_failure_callback: logs full context + exception traceback
  - retries=2 with retry_delay=30s on all tasks
  - SLA=10 min on transform task
  - XCom for record count, file paths, validation results
  - all temp files written to configurable OUTPUT_DIR
"""
from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import logging, json, sqlite3, pandas as pd, os
from pathlib import Path

log = logging.getLogger("airflow.task")

OUTPUT_DIR = Path(os.getenv("AIRFLOW_OUTPUT_DIR",
    "C:/tmp/studybook/airflow/capstone" if os.name == "nt"
    else "/tmp/studybook/airflow/capstone"))

def on_failure_callback(context: dict) -> None:
    """Log failure with full traceback. In prod: send to Slack/PagerDuty."""
    exc = context.get("exception")
    log.error(
        f"FAILURE | dag={context['dag'].dag_id} "
        f"task={context['task'].task_id} "
        f"run={context['dag_run'].run_id} | "
        f"exception={exc!r}"
    )

@dag(
    dag_id="studybook_capstone_etl",
    default_args={
        "owner": "studybook",
        "retries": 2,
        "retry_delay": timedelta(seconds=30),
        "on_failure_callback": on_failure_callback,
    },
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["studybook", "capstone"],
)
def etl_pipeline():

    @task
    def extract(ds: str = None) -> dict:
        """
        Simulate SQLite source query. Generate 500 sensor records.
        Write to OUTPUT_DIR/raw/extract_{ds}.csv.
        Return: {"record_count": 500, "file_path": str, "ds": ds,
                 "null_rate": 0.03, "source": "sqlite://sensors.db"}
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        import random
        records = [{"id": i, "sensor": f"s{i%20:02d}",
                    "value": random.uniform(0, 100) if i % 33 != 0 else None,
                    "ts": ds}
                   for i in range(500)]
        path = OUTPUT_DIR / f"extract_{ds}.csv"
        pd.DataFrame(records).to_csv(path, index=False)
        null_rate = sum(1 for r in records if r["value"] is None) / len(records)
        return {"record_count": len(records), "file_path": str(path),
                "ds": ds, "null_rate": round(null_rate, 3), "source": "sqlite"}

    @task
    def validate(extract_result: dict) -> dict:
        """
        Fail if record_count < 100 or null_rate > 0.05.
        Raise AirflowException with clear message on either condition.
        Return extract_result unchanged on success.
        """
        from airflow.exceptions import AirflowException
        if extract_result["record_count"] < 100:
            raise AirflowException(
                f"Too few records: {extract_result['record_count']} (min 100)")
        if extract_result["null_rate"] > 0.05:
            raise AirflowException(
                f"Null rate too high: {extract_result['null_rate']:.1%} (max 5%)")
        log.info(f"Validation passed: {extract_result['record_count']} records, "
                 f"null_rate={extract_result['null_rate']:.1%}")
        return extract_result

    @task
    def transform(validated: dict) -> dict:
        """
        Read extract file. Apply:
          1. Fill null values with median
          2. Add status column: "ALERT" if value > 80 else "NORMAL"
          3. Aggregate: avg value per sensor
        Write two outputs: cleaned CSV and aggregated CSV.
        Return: {"cleaned_path": str, "agg_path": str, "record_count": int}
        """
        df = pd.read_csv(validated["file_path"])
        df["value"] = df["value"].fillna(df["value"].median())
        df["status"] = df["value"].apply(lambda v: "ALERT" if v > 80 else "NORMAL")

        cleaned_path = OUTPUT_DIR / f"cleaned_{validated['ds']}.csv"
        agg_path     = OUTPUT_DIR / f"agg_{validated['ds']}.csv"
        df.to_csv(cleaned_path, index=False)
        df.groupby("sensor")["value"].mean().reset_index().to_csv(agg_path, index=False)

        return {"cleaned_path": str(cleaned_path), "agg_path": str(agg_path),
                "record_count": len(df)}

    @task
    def load(transform_result: dict) -> dict:
        """
        Simulate loading cleaned data to target SQLite DB.
        Write to OUTPUT_DIR/loaded_{ds}.db.
        Return {"loaded_rows": int, "target": "sqlite://loaded.db"}
        """
        df = pd.read_csv(transform_result["cleaned_path"])
        db_path = OUTPUT_DIR / "loaded_data.db"
        with sqlite3.connect(str(db_path)) as conn:
            df.to_sql("sensor_readings", conn, if_exists="replace", index=False)
        return {"loaded_rows": len(df), "target": str(db_path)}

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def notify(extract_result: dict, load_result: dict) -> None:
        """
        Always runs. Prints pipeline summary regardless of upstream success/failure.
        In production: send Slack/email with metrics.
        """
        log.info(
            f"PIPELINE COMPLETE | "
            f"extracted={extract_result.get('record_count','N/A')} | "
            f"loaded={load_result.get('loaded_rows','N/A')} | "
            f"target={load_result.get('target','N/A')}"
        )

    raw    = extract()
    valid  = validate(raw)
    trans  = transform(valid)
    loaded = load(trans)
    notify(raw, loaded)

etl_dag = etl_pipeline()

===== CAPSTONE FILE: test_capstone.py =====

"""
pytest — 5 tests validating the capstone DAG.
Run: pytest test_capstone.py -v
pip install apache-airflow pytest
"""
import pytest, sys
from pathlib import Path

def test_dag_imports_without_error():
    """DagBag must load capstone_dag.py with zero import errors."""
    from airflow.models.dagbag import DagBag
    bag = DagBag(dag_folder=str(Path(__file__).parent), include_examples=False)
    assert "studybook_capstone_etl" in bag.dags, \
        f"DAG not found. Errors: {bag.import_errors}"
    assert not bag.import_errors, f"Import errors: {bag.import_errors}"

def test_dag_has_correct_schedule():
    """DAG schedule must be @daily."""
    from airflow.models.dagbag import DagBag
    bag = DagBag(dag_folder=str(Path(__file__).parent), include_examples=False)
    dag = bag.dags["studybook_capstone_etl"]
    assert str(dag.schedule_interval) in ("@daily", "0 0 * * *")

def test_dag_has_all_expected_tasks():
    """All 5 tasks must be present."""
    from airflow.models.dagbag import DagBag
    bag = DagBag(dag_folder=str(Path(__file__).parent), include_examples=False)
    dag = bag.dags["studybook_capstone_etl"]
    task_ids = set(dag.task_ids)
    expected = {"extract", "validate", "transform", "load", "notify"}
    assert expected.issubset(task_ids), f"Missing tasks: {expected - task_ids}"

def test_notify_has_all_done_trigger():
    """notify task must have TriggerRule.ALL_DONE."""
    from airflow.models.dagbag import DagBag
    from airflow.utils.trigger_rule import TriggerRule
    bag = DagBag(dag_folder=str(Path(__file__).parent), include_examples=False)
    dag = bag.dags["studybook_capstone_etl"]
    notify_task = dag.get_task("notify")
    assert notify_task.trigger_rule == TriggerRule.ALL_DONE

def test_catchup_is_false():
    """catchup must be False to avoid backfill accumulation."""
    from airflow.models.dagbag import DagBag
    bag = DagBag(dag_folder=str(Path(__file__).parent), include_examples=False)
    dag = bag.dags["studybook_capstone_etl"]
    assert dag.catchup is False

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

  "generate file 01"    → 01_dag_basics.py
  "generate file 02"    → 02_operators_and_sensors.py
  "generate file 03"    → 03_xcom_variables_connections.py
  "generate file 04"    → 04_dynamic_dags_and_taskflow.py
  "generate file 05"    → 05_error_handling_and_monitoring.py
  "generate readme"     → README.md
  "generate capstone"   → capstone/capstone_dag.py
  "generate tests"      → capstone/test_capstone.py

Each file COMPLETE and FULLY RUNNABLE. No placeholders. No pass statements.

===
