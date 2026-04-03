"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-04 · XCom Fundamentals                                            ║
║  Cross-task communication: pushing and pulling small values                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
XCom (Cross-Communication) is Airflow's mechanism for tasks to share small
data values.  Values are stored in the Airflow metadata database and retrieved
by key.

KEY CONCEPTS
────────────
  xcom_push(key, value) — store a value in the metadata DB
  xcom_pull(task_ids, key) — retrieve a value pushed by another task
  return value          — @task / PythonOperator auto-push return as "return_value"
  XCom size limit       — keep values small (< 48KB); use S3/GCS for large data
  do_xcom_push=False    — opt out of auto-push for BashOperator

IMPORTANT LIMITATIONS
─────────────────────
  - XCom is NOT for large datasets (DataFrames, files, ML models)
  - Use XCom for: file paths, record counts, status flags, small dicts
  - Use object storage (S3/GCS) for: large arrays, DataFrames, model artifacts
  - XCom values are serialized with JSON (or pickle if enabled — avoid pickle)

INTERVIEW RELEVANCE
───────────────────
  "What is XCom and when should you NOT use it?"
  "How do you pass a file path between tasks?"
  "What is the XCom size limit and how do you handle large data?"
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 01-04 : XCom Fundamentals ------------------------")

XCOM_DAG_CODE = '''
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="lab_airflow_xcom_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab", "xcom"],
)
def xcom_demo():
    """
    Shows three XCom patterns:
      1. Automatic XCom via @task return value
      2. Explicit xcom_push / xcom_pull
      3. Multiple return values (dict unpacking)
    """

    # Pattern 1: Automatic XCom — return value is auto-pushed
    @task
    def produce_count() -> int:
        count = 42
        print(f"Produced count: {count}")
        return count  # auto-pushed as key="return_value"

    @task
    def consume_count(count: int) -> str:
        # count is pulled automatically from the upstream task
        msg = f"Consumed count: {count}"
        print(msg)
        return msg

    # Pattern 2: Explicit push/pull for named keys
    @task
    def push_multiple(**context) -> None:
        ti = context["ti"]
        ti.xcom_push(key="file_path", value="/tmp/airflow_lab/output.csv")
        ti.xcom_push(key="row_count", value=1000)
        ti.xcom_push(key="status", value="success")
        print("Pushed 3 named XCom values")

    @task
    def pull_named(**context) -> dict:
        ti = context["ti"]
        file_path = ti.xcom_pull(task_ids="push_multiple", key="file_path")
        row_count  = ti.xcom_pull(task_ids="push_multiple", key="row_count")
        status     = ti.xcom_pull(task_ids="push_multiple", key="status")
        print(f"Pulled: file={file_path}, rows={row_count}, status={status}")
        return {"file_path": file_path, "row_count": row_count, "status": status}

    # Pattern 3: Dict return for structured output
    @task
    def produce_metrics() -> dict:
        return {"orders": 500, "revenue": 25000.0, "errors": 0}

    @task
    def use_metrics(metrics: dict) -> None:
        print(f"Orders: {metrics[\'orders\']}, Revenue: ${metrics[\'revenue\']:,.2f}")
        assert metrics["errors"] == 0, "Errors found in metrics!"

    # Wire all patterns
    count = produce_count()
    consume_count(count)

    push_multiple() >> pull_named()

    m = produce_metrics()
    use_metrics(m)


dag_instance = xcom_demo()
'''

namespace: dict = {}
try:
    exec(XCOM_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks: {len(task_ids)}")
    for tid in task_ids:
        print(f"       - {tid}")

    # Verify XCom-related tasks exist
    required = {"produce_count", "consume_count", "push_multiple",
                "pull_named", "produce_metrics", "use_metrics"}
    found = set(task_ids)
    assert required == found, f"Missing tasks: {required - found}"
    print("  [OK] All 6 XCom pattern tasks present")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ── Best-practice summary ─────────────────────────────────────────────────────
print()
print("  XCOM BEST PRACTICES")
print("  -------------------")
guidelines = [
    ("Use XCom for",      "file paths, row counts, status flags, small dicts"),
    ("Avoid XCom for",    "DataFrames, arrays, binary blobs, ML models"),
    ("Size limit",        "< 48 KB per value (metadata DB backed)"),
    ("Large data",        "Write to S3/GCS; pass the URI via XCom instead"),
    ("Serialization",     "JSON only (never enable xcom_pickling in production)"),
    ("Naming",            "Use explicit keys for multi-value push (not return_value)"),
]
for label, value in guidelines:
    print(f"  {label:<20}  {value}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - @task return value -> auto XCom push as key='return_value'")
print("  - TaskFlow pulls XCom automatically when you pass task output as arg")
print("  - Classic operators: ti.xcom_push(key=...) / ti.xcom_pull(task_ids=...)")
print("  - Never XCom a DataFrame — write to storage and pass the path")
print()
