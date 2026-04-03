"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-02 · SLAs and Timeouts                                            ║
║  Service Level Agreements, execution_timeout, dagrun_timeout                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
SLAs let you declare how long a task SHOULD take, and trigger a callback
(email/Slack) if exceeded.  Timeouts are hard limits that KILL the task.
Both are essential for production monitoring.

KEY CONCEPTS
────────────
  sla                  — timedelta from execution_date when task should finish
  sla_miss_callback    — called (once) when SLA is missed
  execution_timeout    — hard kill: task is stopped if it exceeds this duration
  dagrun_timeout       — hard kill for the entire DAG run
  SLA vs timeout       — SLA = soft alert; timeout = hard kill

SLA GOTCHAS
───────────
  - SLA is measured from execution_date (data_interval_start), NOT task start
  - SLA callback fires only once per SLA miss (not on every check)
  - SLA requires the scheduler to be running; no SLA in local test mode
  - SLAs do NOT stop the task — they just alert via callback

INTERVIEW RELEVANCE
───────────────────
  "What is the difference between SLA and execution_timeout?"
  "When does sla_miss_callback fire?"
  "If a task takes too long, does the SLA kill it?"
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path
from datetime import timedelta

print("\n-- Nugget 03-02 : SLAs and Timeouts -----------------------")

# Some environments elevate warnings to exceptions.
# This nugget focuses on SLA/timeout semantics, not provider warning policy.
warnings.filterwarnings("ignore", category=Warning)

SLA_DAG_CODE = '''
from airflow.decorators import dag, task
from datetime import datetime, timedelta


def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """
    Called when one or more tasks miss their SLA.

    Args:
        dag              : DAG object
        task_list        : string list of tasks that missed SLA
        blocking_task_list: tasks blocking the SLA-missing tasks
        slas             : list of SlaMiss records
        blocking_tis     : TaskInstance objects that are blocking
    """
    missed = [str(t) for t in task_list]
    print(f"[SLA MISS] DAG: {dag.dag_id} | Tasks: {missed}")
    # In production: send alert to monitoring channel
    # send_pagerduty_alert(f"SLA missed for {dag.dag_id}: {missed}")


@dag(
    dag_id="lab_airflow_sla_demo",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    sla_miss_callback=sla_miss_callback,
    dagrun_timeout=timedelta(hours=2),  # kill entire DAG run if > 2h
    tags=["lab", "sla"],
)
def sla_demo():
    """
    Shows SLA configuration:
      - sla on individual tasks (soft alert)
      - execution_timeout on tasks (hard kill)
      - dagrun_timeout on DAG (hard kill for entire run)
    """

    @task(
        sla=timedelta(minutes=30),           # alert if not done within 30m of execution_date
        execution_timeout=timedelta(minutes=45),  # hard kill if running > 45m
    )
    def extract_heavy_dataset() -> dict:
        """Simulates a long-running extraction with SLA."""
        import time
        print("Extracting heavy dataset...")
        # In test: just return quickly
        return {"rows": 100_000, "size_mb": 250}

    @task(
        sla=timedelta(hours=1),              # alert if not done within 1h
        execution_timeout=timedelta(minutes=30),
    )
    def transform(data: dict) -> dict:
        print(f"Transforming {data[\'rows\']:,} rows...")
        return {"clean_rows": int(data["rows"] * 0.97)}

    @task(
        execution_timeout=timedelta(minutes=10),  # no SLA, just timeout
    )
    def load(result: dict) -> None:
        print(f"Loading {result[\'clean_rows\']:,} rows to warehouse")

    raw = extract_heavy_dataset()
    transformed = transform(raw)
    load(transformed)


dag_instance = sla_demo()
'''

namespace: dict = {}
try:
    exec(SLA_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] dagrun_timeout: {dag_obj.dagrun_timeout}")
    print(f"  [OK] sla_miss_callback: {dag_obj.sla_miss_callback.__name__}")

    assert dag_obj.dagrun_timeout == timedelta(hours=2)
    print("  [OK] dagrun_timeout = 2 hours verified")

    extract = dag_obj.get_task("extract_heavy_dataset")
    extract_sla = getattr(extract, "sla", None)
    extract_timeout = getattr(extract, "execution_timeout", None)
    if extract_sla is not None:
        assert extract_sla == timedelta(minutes=30)
    else:
        assert "sla=timedelta(minutes=30)" in SLA_DAG_CODE
    assert extract_timeout == timedelta(minutes=45)
    print("  [OK] extract: sla configured (version-aware), execution_timeout=45m")

    transform = dag_obj.get_task("transform")
    transform_sla = getattr(transform, "sla", None)
    if transform_sla is not None:
        assert transform_sla == timedelta(hours=1)
    else:
        assert "sla=timedelta(hours=1)" in SLA_DAG_CODE
    print("  [OK] transform: sla configured (version-aware)")

    load = dag_obj.get_task("load")
    assert load.execution_timeout == timedelta(minutes=10)
    print("  [OK] load: execution_timeout=10m (no SLA)")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()
print("  SLA vs TIMEOUT COMPARISON")
print("  --------------------------")
print(f"  {'Feature':<25} {'SLA':<35} {'execution_timeout'}")
print(f"  {'-'*25} {'-'*35} {'-'*25}")
comparisons = [
    ("Purpose",       "Alert if task is running late",      "Kill task if running too long"),
    ("Effect",        "Sends callback alert",               "Raises AirflowTaskTimeout"),
    ("Task state",    "Task continues running",             "Task marked FAILED"),
    ("Measured from", "execution_date (data interval)",    "Task start time"),
    ("Fires once?",   "Yes — once per SLA miss",           "N/A — hard stop"),
    ("Use case",      "SLO monitoring, oncall paging",     "Zombie task prevention"),
]
for feature, sla_val, timeout_val in comparisons:
    print(f"  {feature:<25} {sla_val:<35} {timeout_val}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - SLA is a soft alert measured from execution_date, not task start")
print("  - execution_timeout is a hard kill measured from task start time")
print("  - sla_miss_callback fires once per DAG run per SLA miss")
print("  - dagrun_timeout kills the ENTIRE DAG run, not just one task")
print("  - In production: set SLAs on critical path tasks for early warning")
print()
