"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-01 · DAG Run Lifecycle and Operational Commands                   ║
║  States, manual reruns, clear, mark success/failure, and pools               ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Understanding the Airflow UI operations and task state machine is essential
for day-to-day operations.  This nugget covers the full task/DAG run lifecycle,
and how to intervene when things go wrong.

KEY CONCEPTS
────────────
  Task States:
    queued      — waiting for a worker slot
    running     — actively executing
    success     — completed without error
    failed      — exhausted all retries
    skipped     — short-circuited or branched away from
    upstream_failed — upstream task failed; this task won't run
    up_for_retry    — waiting for retry delay
    up_for_reschedule — sensor waiting between pokes

  DAG Run States:
    running     — at least one task is running or queued
    success     — all tasks succeeded
    failed      — at least one task failed with no retry left

  Operational Commands:
    Clear task  — reset task to queued state for rerun
    Mark success/failed — manually override task state
    Trigger DAG — create a new manual DAG run

  Pools:
    Worker pool with a slot limit; assigns slots to tasks
    Use pools to limit concurrency for specific resource types

INTERVIEW RELEVANCE
───────────────────
  "What states can an Airflow task be in?"
  "How do you rerun a failed task without rerunning the whole DAG?"
  "What does clearing a task do?"
  "What is a pool and when would you use one?"
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 05-01 : DAG Run Lifecycle ------------------------")

# ── State machine illustration (no import needed) ─────────────────────────────
print()
print("  TASK STATE MACHINE")
print("  ------------------")
print()
print("  [scheduled] -> [queued] -> [running] -> [success]")
print("                                       -> [failed]   -> [up_for_retry] -> ...")
print("                                       -> [skipped]  (branch/short-circuit)")
print("                 [upstream_failed]     (upstream task failed)")
print("                 [up_for_reschedule]   (sensor between pokes)")
print()
print("  OPERATIONAL ACTIONS")
print("  --------------------")

actions = [
    ("Clear task",          "Resets task to 'queued'; reruns from that point"),
    ("Clear task + downstream", "Resets task and all dependent tasks"),
    ("Mark success",        "Force task to 'success' state (skips execution)"),
    ("Mark failed",         "Force task to 'failed' (triggers callbacks)"),
    ("Trigger DAG",         "Creates a new manual DAG run (with optional conf)"),
    ("Delete DAG run",      "Removes the run and all its task instances"),
    ("Pause DAG",           "Prevents scheduler from scheduling new runs"),
    ("Unpause DAG",         "Re-enables scheduling"),
]
for action, desc in actions:
    print(f"  {action:<30}  {desc}")

print()

# ── REST API interaction (requires live Airflow) ──────────────────────────────
POOL_DAG_CODE = '''
from airflow.decorators import dag, task
from datetime import datetime

# Pools limit how many tasks run concurrently within a resource class.
# Define pools in the Airflow UI: Admin > Pools
# Then assign tasks to a pool with pool="pool_name"

@dag(
    dag_id="lab_airflow_pools_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab", "operations"],
)
def pools_demo():
    """
    Demonstrates pool assignment for resource concurrency control.

    Scenario: Only 2 DB connection slots in "db_connections" pool.
    Even if 10 tasks are queued, only 2 run at once against the DB.
    """

    @task(pool="default_pool", pool_slots=1)
    def query_db_1() -> str:
        print("DB query 1 (uses 1 slot in default_pool)")
        return "result_1"

    @task(pool="default_pool", pool_slots=1)
    def query_db_2() -> str:
        print("DB query 2 (uses 1 slot in default_pool)")
        return "result_2"

    @task(pool="default_pool", pool_slots=2)  # heavy task, takes 2 slots
    def heavy_export() -> str:
        print("Heavy export (uses 2 slots — blocks 2 lighter tasks)")
        return "export_done"

    @task
    def aggregate(r1: str, r2: str, export: str) -> None:
        print(f"All done: {r1}, {r2}, {export}")

    r1 = query_db_1()
    r2 = query_db_2()
    exp = heavy_export()
    aggregate(r1, r2, exp)


dag_instance = pools_demo()
'''

namespace: dict = {}
try:
    exec(POOL_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] Pool demo DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks: {task_ids}")

    # Verify pool assignment
    q1 = dag_obj.get_task("query_db_1")
    q2 = dag_obj.get_task("query_db_2")
    heavy = dag_obj.get_task("heavy_export")

    assert q1.pool == "default_pool"
    assert q1.pool_slots == 1
    assert heavy.pool_slots == 2
    print("  [OK] Pool slots: query_db_1=1, heavy_export=2 (rate limiting)")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ── CLI commands reference ────────────────────────────────────────────────────
print()
print("  AIRFLOW CLI CHEAT SHEET")
print("  -----------------------")
cli_commands = [
    ("airflow dags list",                        "List all DAGs"),
    ("airflow dags trigger my_dag",              "Trigger a DAG manually"),
    ("airflow dags backfill my_dag -s 2024-01-01 -e 2024-01-31", "Backfill date range"),
    ("airflow tasks list my_dag",                "List tasks in a DAG"),
    ("airflow tasks clear my_dag -t my_task",    "Clear a specific task"),
    ("airflow tasks run my_dag my_task 2024-01-01", "Run task locally"),
    ("airflow dags pause my_dag",                "Pause scheduling"),
    ("airflow dags unpause my_dag",              "Resume scheduling"),
    ("airflow pools list",                       "List worker pools"),
    ("airflow pools set my_pool 3 'description'","Create/update pool"),
]
for cmd, desc in cli_commands:
    print(f"  $ {cmd}")
    print(f"      -> {desc}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - Clear task = requeue it for rerun (most common recovery action)")
print("  - Mark success = skip execution but mark as done (use carefully)")
print("  - Pools limit concurrent DB connections / API calls / slots")
print("  - pool_slots > 1 lets heavy tasks reserve multiple pool slots")
print("  - Backfill reruns historical intervals (needs catchup=True or CLI)")
print()
