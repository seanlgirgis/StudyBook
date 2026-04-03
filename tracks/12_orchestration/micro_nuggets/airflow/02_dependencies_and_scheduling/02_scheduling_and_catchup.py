"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-02 · Cron Scheduling, Catchup, and Backfill                       ║
║  How Airflow decides when to run your DAG                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Understanding Airflow's scheduling model is one of the most common interview
topics.  The "execution_date is the START of the interval" rule trips up
almost every new user.

KEY CONCEPTS
────────────
  schedule             — cron expression, timedelta, preset, or None
  start_date           — first eligible execution date (NOT first run time)
  execution_date       — the data interval START (past-pointing)
  data_interval_start  — alias for execution_date (Airflow 2.2+)
  data_interval_end    — the data interval END (when the run actually fires)
  catchup=True         — create runs for all missed intervals since start_date
  catchup=False        — only create the most recent run (safe default)
  backfill             — CLI command to manually fill historical runs

SCHEDULE PRESETS
────────────────
  @once          — run exactly once
  @hourly        — 0 * * * *
  @daily         — 0 0 * * *
  @weekly        — 0 0 * * 0
  @monthly       — 0 0 1 * *
  @yearly        — 0 0 1 1 *
  None           — manual trigger only

THE START_DATE TRAP
───────────────────
  If start_date=2024-01-01 and schedule=@daily, the FIRST run fires on
  2024-01-02 (it processes the 2024-01-01 interval).
  Rule: "Airflow runs AFTER the interval ends."

INTERVIEW RELEVANCE
───────────────────
  "What is execution_date vs the actual run time?"
  "I set start_date=yesterday but the DAG hasn't run — why?"
  "What does catchup=True do? Is it safe to enable?"
  "How do you backfill 30 days of historical data?"
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path
from datetime import datetime, timedelta

print("\n-- Nugget 02-02 : Scheduling and Catchup ------------------")

# Some environments elevate deprecation warnings to exceptions.
# This nugget validates scheduling concepts and should not fail on import deprecations.
warnings.filterwarnings("ignore", category=Warning)

SCHEDULE_DAG_CODE = '''
from airflow.decorators import dag, task
from airflow.timetables.base import DataInterval
from datetime import datetime, timedelta, timezone
import pendulum

@dag(
    dag_id="lab_airflow_scheduling_demo",
    start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
    schedule="0 6 * * *",   # 06:00 UTC daily
    catchup=False,           # do NOT backfill old runs on deploy
    max_active_runs=1,       # prevent overlapping runs
    tags=["lab", "scheduling"],
)
def scheduling_demo():
    """
    Illustrates execution_date semantics:
      - data_interval_start = the day being processed (execution_date)
      - data_interval_end   = the next day (when the run fires)
    """

    @task
    def show_interval(**context) -> dict:
        ds           = context["ds"]                       # YYYY-MM-DD
        ds_nodash    = context["ds_nodash"]               # YYYYMMDD
        run_id       = context["run_id"]
        data_interval_start = context["data_interval_start"]
        data_interval_end   = context["data_interval_end"]

        print(f"  Processing date:      {ds}")
        print(f"  ds_nodash:            {ds_nodash}")
        print(f"  data_interval_start:  {data_interval_start}")
        print(f"  data_interval_end:    {data_interval_end}")
        print(f"  run_id:               {run_id}")
        return {"date": ds, "run_id": run_id}

    @task
    def process_partition(info: dict) -> str:
        # Use {{ ds }} style paths for idempotent, date-partitioned storage
        partition_path = f"s3://my-bucket/events/dt={info[\'date\']}/data.parquet"
        print(f"  Would read: {partition_path}")
        return partition_path

    info = show_interval()
    process_partition(info)


dag_instance = scheduling_demo()
'''

namespace: dict = {}
try:
    exec(SCHEDULE_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    schedule_value = getattr(dag_obj, "schedule_interval", None)
    if schedule_value is None:
        schedule_value = getattr(dag_obj, "schedule", None)

    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] schedule: {schedule_value}")
    print(f"  [OK] catchup: {dag_obj.catchup}")
    print(f"  [OK] max_active_runs: {dag_obj.max_active_runs}")
    assert dag_obj.catchup is False, "catchup should be False"
    assert dag_obj.max_active_runs == 1, "max_active_runs should be 1"
    print("  [OK] Safety settings verified: catchup=False, max_active_runs=1")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ── Visual walkthrough of the scheduling model ────────────────────────────────
print()
print("  SCHEDULING MODEL WALKTHROUGH")
print("  (schedule=@daily, start_date=2024-01-01, catchup=False)")
print()
print("  start_date    execution_date    actual run time   data covers")
print("  ----------    --------------    ---------------   -----------")
examples = [
    ("2024-01-01", "2024-01-01", "2024-01-02 00:00", "Jan 1 data"),
    ("2024-01-01", "2024-01-02", "2024-01-03 00:00", "Jan 2 data"),
    ("2024-01-01", "2024-01-14", "2024-01-15 00:00", "Jan 14 data"),
]
for sd, ed, rt, covers in examples:
    print(f"  {sd}    {ed}        {rt}    {covers}")

print()
print("  CRON CHEAT SHEET")
print("  ----------------")
cron_examples = [
    ("0 * * * *",    "Every hour at :00"),
    ("0 6 * * *",    "Daily at 06:00"),
    ("0 6 * * 1",    "Every Monday at 06:00"),
    ("0 6 1 * *",    "First of each month at 06:00"),
    ("*/15 * * * *", "Every 15 minutes"),
    ("0 6,18 * * *", "Twice daily at 06:00 and 18:00"),
]
for cron, desc in cron_examples:
    print(f"  {cron:<20}  {desc}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - execution_date = start of the data interval (it's past-pointing)")
print("  - Run fires AFTER the interval ends — not at start_date")
print("  - catchup=False is safest for production; backfill explicitly")
print("  - max_active_runs=1 prevents concurrent runs of the same DAG")
print("  - Use {{ ds }} in file paths for automatic date partitioning")
print()
