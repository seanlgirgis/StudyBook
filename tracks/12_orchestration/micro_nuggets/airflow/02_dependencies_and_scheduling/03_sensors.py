"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-03 · Sensors — Waiting for External Conditions                    ║
║  TimeDeltaSensor, FileSensor, ExternalTaskSensor patterns                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Sensors are special operators that poll a condition and block until it is met
(or until a timeout).  They're the standard way to wait for:
  - Another DAG to finish
  - A file to appear
  - An API to become ready
  - A database row to exist

KEY CONCEPTS
────────────
  poke_interval       — how often (seconds) to check the condition
  timeout             — how long (seconds) before raising AirflowSensorTimeout
  mode="poke"         — keeps a worker slot occupied while waiting
  mode="reschedule"   — releases the slot between checks (preferred in prod)
  soft_fail=True      — mark task as SKIPPED instead of FAILED on timeout
  ExternalTaskSensor  — waits for a task in another DAG to reach a state

SENSOR MODES: POKE vs RESCHEDULE
──────────────────────────────────
  poke (default)      — holds worker slot the entire time
                        Good for short waits (< 5 min), bad for long waits
  reschedule          — releases slot, rescheduled at next poke_interval
                        Always use for long waits (files, external systems)

INTERVIEW RELEVANCE
───────────────────
  "What is a sensor and when would you use one?"
  "What is the difference between poke and reschedule mode?"
  "How do you avoid slot starvation with long-running sensors?"
  "How do you wait for an upstream DAG to finish?"
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 02-03 : Sensors ----------------------------------")

SENSOR_DAG_CODE = '''
from airflow.decorators import dag, task
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

@dag(
    dag_id="lab_airflow_sensor_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab", "sensors"],
)
def sensor_demo():
    """
    Demonstrates three sensor patterns:
      1. TimeDeltaSensor — wait a fixed duration
      2. FileSensor      — wait for a file to appear
      3. ExternalTaskSensor — wait for another DAG task
    """

    # 1. TimeDeltaSensor: wait 5 seconds from DAG start
    wait_for_offset = TimeDeltaSensor(
        task_id="wait_5_seconds",
        delta=timedelta(seconds=5),
    )

    # 2. FileSensor: wait for a file to appear on a filesystem
    wait_for_file = FileSensor(
        task_id="wait_for_input_file",
        filepath="/tmp/airflow_lab/trigger.txt",
        fs_conn_id="lab_airflow_filesystem",
        poke_interval=10,
        timeout=300,
        mode="reschedule",   # production best practice
        soft_fail=True,      # skip instead of fail if file never appears
    )

    # 3. ExternalTaskSensor: wait for upstream DAG to complete
    wait_for_upstream = ExternalTaskSensor(
        task_id="wait_for_upstream_dag",
        external_dag_id="lab_airflow_scheduling_demo",
        external_task_id=None,   # None = wait for the whole DAG
        timeout=600,
        poke_interval=30,
        mode="reschedule",
        soft_fail=True,
        allowed_states=["success"],
        check_existence=True,
    )

    proceed = EmptyOperator(task_id="proceed_with_pipeline")

    # After any sensor is done (or skipped), proceed
    [wait_for_offset, wait_for_file, wait_for_upstream] >> proceed


dag_instance = sensor_demo()
'''

namespace: dict = {}
try:
    exec(SENSOR_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks: {task_ids}")

    # Verify sensor tasks
    file_sensor = dag_obj.get_task("wait_for_input_file")
    ext_sensor = dag_obj.get_task("wait_for_upstream_dag")
    time_sensor = dag_obj.get_task("wait_5_seconds")

    assert file_sensor is not None
    assert ext_sensor is not None
    assert time_sensor is not None
    print("  [OK] All 3 sensor tasks present")

    # Verify reschedule mode on FileSensor
    assert str(file_sensor.mode) == "reschedule"
    assert str(ext_sensor.mode) == "reschedule"
    print("  [OK] FileSensor and ExternalTaskSensor use mode=reschedule")

    # Verify soft_fail on FileSensor
    assert file_sensor.soft_fail is True
    print("  [OK] FileSensor soft_fail=True (skips instead of fails)")

    # Verify proceed depends on all sensors
    proceed = dag_obj.get_task("proceed_with_pipeline")
    upstream_ids = {t.task_id for t in proceed.upstream_list}
    assert "wait_for_input_file" in upstream_ids
    assert "wait_for_upstream_dag" in upstream_ids
    assert "wait_5_seconds" in upstream_ids
    print("  [OK] proceed waits for all 3 sensors (fan-in)")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()
print("  SENSOR CONFIGURATION GUIDE")
print("  --------------------------")
settings = [
    ("mode",           "poke", "reschedule",   "Use reschedule for waits > 5 min"),
    ("poke_interval",  "60s",  "10-60s",       "Balance freshness vs DB load"),
    ("timeout",        "7 days","300-3600s",   "Set explicitly; never leave unlimited"),
    ("soft_fail",      "False", "True",        "Use True if absence is acceptable"),
]
print(f"  {'Setting':<16} {'Default':<10} {'Recommended':<14} {'Notes'}")
print(f"  {'-'*16} {'-'*10} {'-'*14} {'-'*35}")
for s, d, r, n in settings:
    print(f"  {s:<16} {d:<10} {r:<14} {n}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - mode=reschedule releases worker slots between checks (prod default)")
print("  - mode=poke is fine for short waits (< 5 min), bad for long waits")
print("  - Always set timeout — unbound sensors starve your worker pool")
print("  - soft_fail=True turns timeout into a SKIP (pipeline continues)")
print("  - ExternalTaskSensor: external_task_id=None waits for entire DAG")
print()
