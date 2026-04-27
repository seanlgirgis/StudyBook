# ============================================================
# Topic   : Apache Airflow (Docker) for Data Engineers
# File    : studybook_02_operators_sensors.py
# Covers  : BashOperator, PythonOperator, FileSensor, BranchPythonOperator
# Prereqs : Airflow Docker stack running at http://localhost:8088
# Deploy  : Place in docker/dags/ so it mounts to /opt/airflow/dags/
# Trigger : Use Airflow UI or trigger manually
# ============================================================

"""
DAG demonstrating operators and sensors in Docker Airflow.

DAG ID: studybook_02_operators_sensors

This lesson introduces:
- PythonOperator
- BashOperator
- FileSensor
- BranchPythonOperator
- TriggerRule.ALL_DONE
- Sensor mode="reschedule"

Docker reminder:
This code runs inside the Airflow container.
Use Linux container paths like /tmp/studybook/...
"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from pathlib import Path
import logging
import random
import time

OUTPUT_DIR = Path("/opt/airflow/dags/.studybook_runtime/02_operators_sensors")
TRIGGER_FILE = OUTPUT_DIR / "trigger" / "ready.txt"

log = logging.getLogger("airflow.task")


def create_trigger_file(**context) -> None:
    """
    Create a local file that the FileSensor will wait for.

    WHY this matters:
    In production, sensors often wait for files landing in S3, GCS, SFTP,
    or a mounted directory. Here we create the file ourselves so the tutorial
    is self-contained.
    """

    TRIGGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRIGGER_FILE.write_text(
        f"ready=true\n"
        f"dag_run={context['run_id']}\n"
        f"logical_date={context['ds']}\n"
    )

    log.info(f"Created trigger file: {TRIGGER_FILE}")


def inspect_environment(**context) -> None:
    """
    Show where the task is running.

    WHY:
    In Docker Airflow, your DAG file lives on the Windows host, but task code
    executes inside a Linux container.
    """

    log.info("This task is running inside the Airflow container.")
    log.info(f"Output directory: {OUTPUT_DIR}")
    log.info(f"Trigger file: {TRIGGER_FILE}")


def branch_logic(**context) -> str:
    """
    Choose one downstream task at runtime.

    BranchPythonOperator must return the task_id to follow.

    Non-selected branches become SKIPPED, not FAILED.
    """

    batch_size = random.choice(["small", "large"])
    context["ti"].xcom_push(key="batch_size", value=batch_size)

    if batch_size == "large":
        log.info("Branch selected: process_large_batch")
        return "process_large_batch"

    log.info("Branch selected: process_small_batch")
    return "process_small_batch"


def process_large_batch(**context) -> None:
    """
    Simulate a larger workload.
    """

    log.info("Processing large batch...")
    time.sleep(2)
    log.info("Large batch complete.")


def process_small_batch(**context) -> None:
    """
    Simulate a smaller workload.
    """

    log.info("Processing small batch...")
    time.sleep(1)
    log.info("Small batch complete.")


def cleanup_task(**context) -> None:
    """
    Cleanup always runs.

    WHY TriggerRule.ALL_DONE:
    Cleanup should run even if upstream work fails or one branch is skipped.
    """

    if TRIGGER_FILE.exists():
        TRIGGER_FILE.unlink()
        log.info(f"Deleted trigger file: {TRIGGER_FILE}")
    else:
        log.info("Trigger file was already missing.")

    batch_size = context["ti"].xcom_pull(
        task_ids="branch_on_batch_size",
        key="batch_size",
    )

    log.info(f"Cleanup complete. Batch size was: {batch_size}")


default_args = {
    "owner": "studybook",
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
    "email_on_failure": False,
}


with DAG(
    dag_id="studybook_02_operators_sensors",
    description="Operators and sensors in Docker Airflow",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["studybook", "docker", "operators", "sensors"],
) as dag:

    t_create_file = PythonOperator(
        task_id="create_trigger_file",
        python_callable=create_trigger_file,
    )

    t_bash_show_container = BashOperator(
        task_id="bash_show_container_context",
        bash_command="""
        echo "Running inside container:"
        hostname
        echo
        echo "Current user:"
        whoami
        echo
        echo "Airflow home:"
        echo $AIRFLOW_HOME
        echo
        echo "DAG folder contents:"
        ls -lah /opt/airflow/dags
        """,
    )

    t_inspect_environment = PythonOperator(
        task_id="inspect_environment",
        python_callable=inspect_environment,
    )

    t_wait_for_file = FileSensor(
        task_id="wait_for_trigger_file",
        filepath=str(TRIGGER_FILE),
        mode="reschedule",
        poke_interval=10,
        timeout=120,
        doc_md="""
        ## FileSensor

        This task waits until the trigger file exists.

        Important production idea:

        - `mode="poke"` keeps a worker slot busy while waiting.
        - `mode="reschedule"` releases the worker slot between checks.

        For waits longer than about a minute, `reschedule` is usually safer.
        """,
    )

    t_branch = BranchPythonOperator(
        task_id="branch_on_batch_size",
        python_callable=branch_logic,
    )

    t_large = PythonOperator(
        task_id="process_large_batch",
        python_callable=process_large_batch,
    )

    t_small = PythonOperator(
        task_id="process_small_batch",
        python_callable=process_small_batch,
    )

    t_cleanup = PythonOperator(
        task_id="cleanup",
        python_callable=cleanup_task,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    (
        t_create_file
        >> t_bash_show_container
        >> t_inspect_environment
        >> t_wait_for_file
        >> t_branch
        >> [t_large, t_small]
        >> t_cleanup
    )