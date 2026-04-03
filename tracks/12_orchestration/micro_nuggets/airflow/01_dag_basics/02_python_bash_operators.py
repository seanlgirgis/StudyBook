"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-02 · PythonOperator and BashOperator                              ║
║  Classic operator-based DAG authoring for comparison and legacy contexts     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Before TaskFlow API, DAGs were built by instantiating operator objects.
Understanding the classic style is essential for reading legacy code and
understanding Airflow internals.

KEY CONCEPTS
────────────
  PythonOperator     — runs a Python callable; python_callable=my_func
  BashOperator       — runs a shell command; bash_command="echo hello"
  op_kwargs          — pass static keyword args into python_callable
  task_id            — unique identifier within the DAG
  provide_context    — (Airflow 1.x) passed **context to callable; 2.x auto
  dag=dag            — assign task to DAG object

COMPARISON: TaskFlow vs Classic
────────────────────────────────
  TaskFlow   : @task def my_func(): ...  — concise, automatic XCom
  Classic    : PythonOperator(task_id=..., python_callable=my_func, dag=dag)
  Both compile to the same task graph; TaskFlow is preferred for new DAGs.

INTERVIEW RELEVANCE
───────────────────
  "What is a PythonOperator and when would you use it over TaskFlow?"
  "How does BashOperator work? What are its risks?"
  "Why might BashOperator cause issues in containerized environments?"
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 01-02 : PythonOperator and BashOperator ----------")

CLASSIC_DAG_CODE = '''
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

def extract_data(**context):
    """Classic python_callable — receives execution context via **context."""
    run_id = context["run_id"]
    print(f"Extracting data for run: {run_id}")
    # In classic style, XCom push is explicit
    context["ti"].xcom_push(key="record_count", value=150)
    return 150  # return value also auto-pushed to XCom as "return_value"

def transform_data(multiplier: int, **context):
    """op_kwargs lets you pass static params to the callable."""
    ti = context["ti"]
    count = ti.xcom_pull(task_ids="extract_data_task", key="record_count")
    result = count * multiplier
    print(f"Transformed {count} records with multiplier {multiplier} -> {result}")
    return result

default_args = {
    "owner": "lab",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="lab_airflow_classic_operators",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["lab", "classic"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data_task",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data_task",
        python_callable=transform_data,
        op_kwargs={"multiplier": 2},
    )

    report_task = BashOperator(
        task_id="report_task",
        bash_command="echo 'Pipeline complete at $(date)' && echo 'Result: {{ ti.xcom_pull(task_ids=\\'transform_data_task\\') }}'",
    )

    # Classic dependency syntax
    extract_task >> transform_task >> report_task
'''

namespace: dict = {}
try:
    exec(CLASSIC_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace.get("dag")

    if dag_obj is None:
        print("  [FAIL] dag object not found in namespace")
        sys.exit(1)

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks: {task_ids}")

    # Verify dependency chain
    t_transform = dag_obj.get_task("transform_data_task")
    t_report = dag_obj.get_task("report_task")

    assert "extract_data_task" in [t.task_id for t in t_transform.upstream_list]
    assert "transform_data_task" in [t.task_id for t in t_report.upstream_list]
    print("  [OK] Dependency chain: extract -> transform -> report")

    # Check operator types
    t_extract = dag_obj.get_task("extract_data_task")
    assert "PythonOperator" in type(t_extract).__name__
    assert "PythonOperator" in type(t_transform).__name__
    assert "BashOperator" in type(t_report).__name__
    print("  [OK] Operator types verified: PythonOperator x2, BashOperator x1")

    # Verify default_args propagation
    assert dag_obj.default_args["retries"] == 1
    print("  [OK] default_args applied (retries=1)")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    print("         Explanation mode only — concepts documented above.")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - PythonOperator: runs any Python callable; use op_kwargs for params")
print("  - BashOperator: runs shell; avoid for complex logic (prefer Python)")
print("  - Classic >> syntax sets downstream dependencies explicitly")
print("  - default_args: propagate retries/retry_delay/owner to all tasks")
print("  - XCom pull in classic: ti.xcom_pull(task_ids='task_name')")
print()
