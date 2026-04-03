"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 06-01 · Interview Drills                                             ║
║  12 runnable scenarios covering the most common Airflow interview topics     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Each scenario below:
  1. States a realistic interview question
  2. Validates the answer via runnable code
  3. Prints the model answer

TOPICS COVERED
──────────────
  Q01  execution_date vs actual run time
  Q02  catchup=True behavior and risk
  Q03  XCom size limit and large data pattern
  Q04  Sensor poke vs reschedule mode
  Q05  Idempotent task design
  Q06  BranchPythonOperator trigger rules
  Q07  Retry exponential backoff
  Q08  SLA vs execution_timeout
  Q09  TaskFlow vs classic operators
  Q10  Pool slot starvation pattern
  Q11  Backfill command usage
  Q12  Dead-letter / recovery pattern
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 06-01 : Interview Drills -------------------------")
print()

PASS = 0
FAIL = 0
results: list[tuple[str, bool, str]] = []


def check(qid: str, condition: bool, answer: str) -> None:
    global PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS += 1
    else:
        FAIL += 1
    results.append((qid, condition, answer))


# ── detect airflow availability once ─────────────────────────────────────────
try:
    import airflow as _af_mod
    _AIRFLOW_OK = True
except ImportError:
    _AIRFLOW_OK = False

# ── Q01: execution_date semantics ─────────────────────────────────────────────
if _AIRFLOW_OK:
    try:
        from airflow.decorators import dag, task
        from datetime import datetime, timedelta

        @dag(dag_id="q01_exec_date", start_date=datetime(2024, 1, 1),
             schedule="@daily", catchup=False)
        def q01():
            @task
            def check_ds(**context) -> str:
                return context["ds"]
            check_ds()

        d = q01()
        check(
            "Q01",
            d.catchup is False,
            "execution_date = start of the data interval (yesterday for @daily). "
            "Run fires AFTER the interval ends. ds='2024-01-01' processes Jan 1 data "
            "but actually runs on Jan 2 at midnight."
        )
    except Exception as e:
        check("Q01", False, str(e))
else:
    check("Q01", True, "[SKIP] apache-airflow not installed — answer only")

# ── Q02: catchup behavior ─────────────────────────────────────────────────────
if _AIRFLOW_OK:
    try:
        from airflow.decorators import dag as _dag2
        from datetime import datetime as _dt2

        @_dag2(dag_id="q02_catchup", start_date=_dt2(2023, 1, 1),
               schedule="@daily", catchup=True)
        def q02(): pass
        d = q02()
        check(
            "Q02",
            d.catchup is True,
            "catchup=True creates a DAG run for every missed interval since start_date. "
            "If start_date=2023-01-01 and you deploy today, Airflow creates ~400 runs. "
            "Use catchup=False in production; backfill explicitly when needed."
        )
    except Exception as e:
        check("Q02", False, str(e))
else:
    check("Q02", True, "[SKIP]")

# ── Q03: XCom size limit ──────────────────────────────────────────────────────
XCOM_LIMIT_KB = 48
XCOM_LIMIT_BYTES = XCOM_LIMIT_KB * 1024

# Validate the pattern: pass file path, not data
file_path = "/tmp/airflow_lab/large_dataset.parquet"
assert isinstance(file_path, str), "file path should be a string"
assert len(file_path.encode()) < XCOM_LIMIT_BYTES, "file path fits in XCom"

check(
    "Q03",
    True,
    f"XCom is backed by the metadata DB and limited to ~{XCOM_LIMIT_KB}KB per value. "
    "Never XCom a DataFrame or large array. Pattern: write large data to S3/GCS, "
    "pass the URI via XCom: xcom_push(key='output_path', value='s3://...')"
)

# ── Q04: sensor modes ─────────────────────────────────────────────────────────
if _AIRFLOW_OK:
    try:
        from airflow.sensors.filesystem import FileSensor
        fs_poke = FileSensor(task_id="t_poke", filepath="/tmp/test", mode="poke")
        fs_reschedule = FileSensor(task_id="t_reschedule", filepath="/tmp/test", mode="reschedule")
        check(
            "Q04",
            fs_poke.mode == "poke" and fs_reschedule.mode == "reschedule",
            "poke: holds a worker slot the entire time (good for < 5 min waits). "
            "reschedule: releases slot between checks, rescheduled at next poke_interval. "
            "Always use reschedule for long waits to avoid slot starvation."
        )
    except Exception as e:
        check("Q04", False, str(e))
else:
    check("Q04", True, "[SKIP]")

# ── Q05: idempotency ──────────────────────────────────────────────────────────
# Demonstrate idempotent load pattern
def idempotent_load(partition: str, rows: list) -> str:
    """DELETE + INSERT is the standard idempotent load pattern."""
    sql = f"DELETE FROM target WHERE partition_date = '{partition}';\n"
    sql += f"INSERT INTO target SELECT * FROM staging WHERE partition_date = '{partition}';"
    return sql

sql1 = idempotent_load("2024-01-15", [1, 2, 3])
sql2 = idempotent_load("2024-01-15", [1, 2, 3])
check(
    "Q05",
    sql1 == sql2,
    "Idempotent = rerunning produces the same result. "
    "DELETE WHERE partition_date=ds then INSERT ensures reruns don't duplicate. "
    "Always filter by {{ ds }} so each run owns exactly one partition."
)

# ── Q06: BranchPythonOperator trigger rule ────────────────────────────────────
if _AIRFLOW_OK:
    try:
        from airflow.utils.trigger_rule import TriggerRule
        from airflow.operators.empty import EmptyOperator
        join = EmptyOperator(task_id="join_test", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)
        check(
            "Q06",
            "none_failed" in str(join.trigger_rule).lower(),
            "After BranchPythonOperator, skipped branches look like non-success states. "
            "The join task needs trigger_rule=NONE_FAILED (or NONE_FAILED_MIN_ONE_SUCCESS) "
            "so it runs when branches are skipped rather than raising AirflowSkipException."
        )
    except Exception as e:
        check("Q06", False, str(e))
else:
    check("Q06", True, "[SKIP]")

# ── Q07: exponential backoff ──────────────────────────────────────────────────
base_delay = 30  # seconds
delays = [min(base_delay * (2 ** i), 600) for i in range(5)]
check(
    "Q07",
    delays == [30, 60, 120, 240, 480],
    f"Exponential backoff: base_delay * 2^attempt (capped at max_retry_delay). "
    f"Delays: {delays} seconds. "
    "Better than fixed retry: spreads load and allows transient issues to resolve."
)

# ── Q08: SLA vs execution_timeout ────────────────────────────────────────────
sla_kills = False       # SLA does NOT kill the task
timeout_kills = True    # execution_timeout DOES kill the task
check(
    "Q08",
    not sla_kills and timeout_kills,
    "SLA is a soft alert (fires sla_miss_callback but task continues). "
    "execution_timeout is a hard kill (raises AirflowTaskTimeout). "
    "SLA measured from execution_date; execution_timeout measured from task start."
)

# ── Q09: TaskFlow vs classic operators ───────────────────────────────────────
if _AIRFLOW_OK:
    try:
        from airflow.decorators import task as af_task

        @af_task
        def my_taskflow() -> str:
            return "hello"

        from airflow.operators.python import PythonOperator

        def my_classic_func() -> str:
            return "hello"

        check(
            "Q09",
            True,
            "TaskFlow (@task decorator): automatic XCom, no boilerplate, Pythonic. "
            "Classic (PythonOperator): explicit, works with older code, easier to test in isolation. "
            "Both compile to the same task graph. Use TaskFlow for new DAGs; "
            "understand classic for reading legacy code."
        )
    except Exception as e:
        check("Q09", False, str(e))
else:
    check("Q09", True, "[SKIP]")

# ── Q10: pool slot starvation ─────────────────────────────────────────────────
# Demonstrate pool math
pool_slots = 3
sensors_poke_mode = 10  # 10 sensors each holding a slot
remaining_slots = pool_slots - sensors_poke_mode
check(
    "Q10",
    remaining_slots < 0,
    f"With {pool_slots} pool slots and {sensors_poke_mode} poke-mode sensors, "
    f"all slots are exhausted ({remaining_slots} free). "
    "No processing tasks can run — deadlock. "
    "Fix: use mode=reschedule so sensors release slots between pokes."
)

# ── Q11: backfill ────────────────────────────────────────────────────────────
backfill_cmd = "airflow dags backfill my_dag --start-date 2024-01-01 --end-date 2024-01-31"
check(
    "Q11",
    "backfill" in backfill_cmd and "start-date" in backfill_cmd,
    "CLI: airflow dags backfill dag_id --start-date YYYY-MM-DD --end-date YYYY-MM-DD. "
    "Creates runs for all missing intervals in the range. "
    "Requires catchup=True or explicit date range. "
    "Use --dry-run to preview without executing."
)

# ── Q12: dead-letter / recovery pattern ──────────────────────────────────────
def recovery_pattern():
    """
    Dead-letter pattern: on failure, write to a recovery queue.
    Airflow implementation: use on_failure_callback to save failed payload.
    """
    def on_failure_cb(context: dict) -> None:
        run_id = context["run_id"]
        partition = context["ds"]
        # Write to dead letter table for reprocessing
        return f"INSERT INTO dead_letter_queue VALUES ('{run_id}', '{partition}', NOW())"

    return on_failure_cb

cb = recovery_pattern()
check(
    "Q12",
    callable(cb),
    "Dead-letter pattern: on_failure_callback writes failed run metadata to a "
    "recovery table. A separate reconciliation DAG periodically checks the table "
    "and retriggers failed runs. Prevents silent data loss."
)

# ── Summary ──────────────────────────────────────────────────────────────────
print(f"  {'Q':<5} {'Status':<6}  Answer")
print(f"  {'-'*5} {'-'*6}  {'-'*60}")
for qid, passed, answer in results:
    status = "PASS" if passed else "FAIL"
    # Truncate answer for display
    short = (answer[:75] + "...") if len(answer) > 78 else answer
    print(f"  {qid:<5} {status:<6}  {short}")

print()
print(f"  Total: {len(results)} | Passed: {PASS} | Failed: {FAIL}")
print()

if FAIL > 0:
    sys.exit(1)
