# ============================================================
# Topic   : Apache Airflow (Docker) for Data Engineers
# File    : studybook_05_error_handling_monitoring.py
# Covers  : Retries, callbacks, trigger rules, failure handling
# Prereqs : Airflow Docker stack running at http://localhost:8088
# Deploy  : Place in docker/dags/ so it mounts to /opt/airflow/dags/
# Trigger : Use Airflow UI or trigger manually
# ============================================================

"""
Production-style error handling and monitoring patterns.

DAG ID: studybook_05_error_handling_monitoring

This lesson demonstrates:
- task retries
- retry_delay
- retry_exponential_backoff
- task-level failure callbacks
- DAG-level success callback
- TriggerRule.ALL_DONE for cleanup
- idempotent task design
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from pathlib import Path
import logging
import traceback

OUTPUT_DIR = Path("/opt/airflow/dags/.studybook_runtime/05_error_handling_monitoring")

log = logging.getLogger("airflow.task")


def on_failure_callback(context: dict) -> None:
    """
    Called automatically when a task fails.

    WHY this matters:
    In production, this is where teams notify Slack, email, PagerDuty,
    Teams, incident tooling, or observability systems.
    """

    exc = context.get("exception")

    log.error("TASK FAILURE CALLBACK FIRED")
    log.error(f"DAG:        {context['dag'].dag_id}")
    log.error(f"Task:       {context['task'].task_id}")
    log.error(f"Run ID:     {context['dag_run'].run_id}")
    log.error(f"Date:       {context['logical_date']}")
    log.error(f"Exception:  {exc!r}")

    if exc:
        log.error("Traceback:")
        log.error("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))


def on_success_callback(context: dict) -> None:
    """
    Called when the DAG run succeeds.

    DAG-level callbacks are useful for final pipeline reporting.
    """

    log.info("DAG SUCCESS CALLBACK FIRED")
    log.info(f"DAG:    {context['dag'].dag_id}")
    log.info(f"Run ID: {context['dag_run'].run_id}")


def unreliable_extract(**context) -> None:
    """
    Simulate a flaky upstream system.

    This intentionally fails on the first attempt, then succeeds on retry.

    WHY:
    Airflow retries rerun the exact same task function.
    Therefore, task code must be idempotent:
    safe to execute more than once.
    """

    attempt = context["ti"].try_number

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    marker = OUTPUT_DIR / f"extract_attempt_{context['run_id'].replace(':', '_')}.txt"

    log.info(f"Extract attempt number: {attempt}")

    if attempt < 2:
        marker.write_text("first attempt failed intentionally\n")
        raise ConnectionError("Simulated upstream API timeout on first attempt")

    marker.write_text("retry succeeded\n")
    log.info("Extract succeeded on retry.")


def transform_with_possible_warning(**context) -> None:
    """
    Simulate a transform step.

    This task succeeds, but logs warnings that would matter in production.
    """

    output_file = OUTPUT_DIR / "transform_output.txt"
    output_file.write_text(
        "transform complete\n"
        "warning_count=2\n"
        "bad_rows=3\n"
    )

    log.warning("Transform completed with warning_count=2")
    log.warning("Bad rows were quarantined instead of failing the whole pipeline.")
    log.info(f"Wrote transform output: {output_file}")


def load_data(**context) -> None:
    """
    Simulate load step.

    WHY separate load:
    In real systems this could write to Postgres, Snowflake, S3, BigQuery, etc.
    """

    input_file = OUTPUT_DIR / "transform_output.txt"

    if not input_file.exists():
        raise FileNotFoundError(f"Missing transform output: {input_file}")

    load_file = OUTPUT_DIR / "load_complete.txt"
    load_file.write_text("load complete\n")

    log.info(f"Load succeeded. Marker: {load_file}")


def always_cleanup(**context) -> None:
    """
    Cleanup runs even when upstream tasks fail.

    WHY TriggerRule.ALL_DONE:
    Cleanup should release locks, remove temp files, and write final status
    whether the pipeline succeeded or failed.
    """

    dag_run = context["dag_run"]
    cleanup_file = OUTPUT_DIR / f"cleanup_{dag_run.run_id.replace(':', '_')}.txt"

    cleanup_file.write_text(
        f"cleanup ran\n"
        f"dag_run_state={dag_run.state}\n"
        f"logical_date={context['logical_date']}\n"
    )

    log.info("Cleanup ran because trigger_rule=ALL_DONE.")
    log.info(f"Cleanup marker: {cleanup_file}")


default_args = {
    "owner": "studybook",
    "retries": 2,
    "retry_delay": timedelta(seconds=15),
    "retry_exponential_backoff": True,
    "email_on_failure": False,
    "on_failure_callback": on_failure_callback,
}


with DAG(
    dag_id="studybook_05_error_handling_monitoring",
    description="Retries, callbacks, and cleanup patterns in Docker Airflow",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    on_success_callback=on_success_callback,
    tags=["studybook", "docker", "errors", "monitoring"],
) as dag:

    t_extract = PythonOperator(
        task_id="unreliable_extract",
        python_callable=unreliable_extract,
    )

    t_transform = PythonOperator(
        task_id="transform_with_possible_warning",
        python_callable=transform_with_possible_warning,
    )

    t_load = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    t_cleanup = PythonOperator(
        task_id="always_cleanup",
        python_callable=always_cleanup,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    t_extract >> t_transform >> t_load >> t_cleanup