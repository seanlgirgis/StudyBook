"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-01 · TaskFlow API Basics                                          ║
║  Modern DAG authoring with @task decorators and automatic XCom              ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
TaskFlow API (introduced Airflow 2.0) lets you write DAGs as plain Python
functions decorated with @task.  XCom passing, task dependencies, and
return types are all inferred automatically.

KEY CONCEPTS
────────────
  @dag decorator         — marks a function as a DAG factory
  @task decorator        — marks a function as a task
  Automatic XCom         — returning a value from @task pushes it to XCom;
                           receiving it as an argument pulls it automatically
  Type hints             — help Airflow serialize/deserialize XCom values
  dag_id                 — unique identifier for the DAG in the UI

INTERVIEW RELEVANCE
───────────────────
  "What changed in Airflow 2.0 for DAG authoring?"
  "How does TaskFlow differ from the classic PythonOperator?"
  "When would you NOT use the TaskFlow API?"

WHAT THIS NUGGET DOES
─────────────────────
  Validates the TaskFlow API by importing and introspecting a sample DAG
  definition without requiring a live Airflow scheduler.  The DAG module
  is parsed and its task structure is verified.
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 01-01 : TaskFlow API Basics ----------------------")

# ── Demo: inline DAG definition (no file I/O needed) ─────────────────────────

TASKFLOW_DAG_CODE = '''
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="lab_airflow_taskflow_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,           # manual trigger only
    catchup=False,
    tags=["lab", "taskflow"],
)
def taskflow_demo():
    """
    Demonstrates TaskFlow API:
      extract -> transform -> load
    Each step passes its return value automatically via XCom.
    """

    @task
    def extract() -> dict:
        """Simulate reading raw data."""
        return {"orders": 42, "revenue": 9870.50, "date": "2024-01-15"}

    @task
    def transform(raw: dict) -> dict:
        """Apply business logic."""
        return {
            "orders": raw["orders"],
            "revenue": round(raw["revenue"], 2),
            "avg_order": round(raw["revenue"] / raw["orders"], 2),
            "date": raw["date"],
        }

    @task
    def load(metrics: dict) -> str:
        """Emit result (in prod: write to DB/S3)."""
        msg = (
            f"Loaded metrics for {metrics[\'date\']}: "
            f"{metrics[\'orders\']} orders, "
            f"avg ${metrics[\'avg_order\']}"
        )
        print(msg)
        return msg

    # Wire the pipeline — TaskFlow infers XCom passing from args
    raw = extract()
    metrics = transform(raw)
    load(metrics)


# Instantiate the DAG (required so Airflow's DagBag discovers it)
dag_instance = taskflow_demo()
'''

# ── Validate by importing the code in a sandbox namespace ────────────────────
namespace: dict = {}
try:
    exec(TASKFLOW_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace.get("dag_instance")

    if dag_obj is None:
        print("  [FAIL] dag_instance not created")
        sys.exit(1)

    # Introspect the DAG
    task_ids = list(dag_obj.task_ids)
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks found: {len(task_ids)}")
    for tid in sorted(task_ids):
        print(f"       - {tid}")

    # Verify dependency chain
    extract_task = dag_obj.get_task("extract")
    transform_task = dag_obj.get_task("transform")
    load_task = dag_obj.get_task("load")

    assert extract_task is not None, "extract task missing"
    assert transform_task is not None, "transform task missing"
    assert load_task is not None, "load task missing"

    # Check upstream/downstream wiring
    assert "extract" in [t.task_id for t in transform_task.upstream_list], \
        "transform should depend on extract"
    assert "transform" in [t.task_id for t in load_task.upstream_list], \
        "load should depend on transform"

    print("  [OK] Dependency chain: extract -> transform -> load")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    print("         This nugget requires: pip install apache-airflow")
    print("         Explanation mode only — see code above for concepts.")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ── Key takeaways ─────────────────────────────────────────────────────────────
print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - @dag + @task = minimal boilerplate, maximum readability")
print("  - Return values flow automatically via XCom — no push/pull needed")
print("  - schedule=None means manual trigger only (no automatic runs)")
print("  - catchup=False prevents backfill on first deployment")
print("  - Tags make the DAG discoverable in the UI filter bar")
print()
