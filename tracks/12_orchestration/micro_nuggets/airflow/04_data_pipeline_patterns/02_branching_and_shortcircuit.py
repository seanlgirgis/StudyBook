"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-02 · Branching and Short-Circuit Pattern                          ║
║  Conditional task execution and early-exit patterns                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Not every pipeline step needs to run every time.  BranchPythonOperator
chooses which downstream branch to follow; ShortCircuitOperator skips
the rest of the pipeline if a condition is False.

KEY CONCEPTS
────────────
  BranchPythonOperator  — returns task_id(s) to run; skips all others
  ShortCircuitOperator  — if callable returns False, all downstreams are skipped
  @task.branch           — TaskFlow decorator equivalent of BranchPythonOperator
  trigger_rule=NONE_FAILED — downstream task after a branch should use this
  EmptyOperator          — no-op join point after branches

COMMON USE CASES
────────────────
  - Skip load if extract returned 0 rows
  - Route to different processing based on data characteristics
  - Run expensive cleanup only on weekends
  - A/B test different transformation approaches

INTERVIEW RELEVANCE
───────────────────
  "How do you conditionally skip tasks in Airflow?"
  "What is the difference between BranchPythonOperator and ShortCircuitOperator?"
  "Why do you need trigger_rule=NONE_FAILED after a branch?"
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

print("\n-- Nugget 04-02 : Branching and Short-Circuit --------------")

# Some environments elevate deprecation warnings to exceptions.
# This nugget validates branching semantics and should not fail on import deprecations.
warnings.filterwarnings("ignore", category=Warning)

BRANCH_DAG_CODE = '''
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

@dag(
    dag_id="lab_airflow_branching",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab", "branching"],
)
def branching_demo():
    """
    Two patterns:

    Pattern 1: BranchPythonOperator
      extract -> check_data_volume -> [process_small | process_large] -> join -> report

    Pattern 2: ShortCircuitOperator
      check_weekend -> cleanup_task  (skips cleanup on weekdays)
    """

    @task
    def extract() -> dict:
        import random
        rows = random.randint(0, 10000)
        print(f"Extracted {rows} rows")
        return {"rows": rows}

    @task.branch
    def check_data_volume(data: dict) -> str:
        """Choose processing path based on row count."""
        rows = data["rows"]
        if rows == 0:
            return "no_data_skip"
        elif rows < 1000:
            return "process_small"
        else:
            return "process_large"

    @task
    def process_small() -> str:
        print("Small dataset: single-threaded processing")
        return "small_done"

    @task
    def process_large() -> str:
        print("Large dataset: parallel chunked processing")
        return "large_done"

    @task
    def no_data_skip() -> None:
        print("No data today — skipping pipeline")

    # Join point: trigger_rule=NONE_FAILED because branches are skipped (not failed)
    join = EmptyOperator(
        task_id="join",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    @task(trigger_rule=TriggerRule.NONE_FAILED)
    def report() -> None:
        print("Pipeline report generated")

    # Pattern 1 wiring
    data = extract()
    branch = check_data_volume(data)
    s = process_small()
    l = process_large()
    n = no_data_skip()
    [s, l, n] >> join >> report()

    # Pattern 2: ShortCircuitOperator
    def is_weekend(**context) -> bool:
        from datetime import datetime as dt
        day = dt.strptime(context["ds"], "%Y-%m-%d").weekday()
        is_wknd = day >= 5
        print(f"Today is {'weekend' if is_wknd else 'weekday'} — cleanup={'yes' if is_wknd else 'skipped'}")
        return is_wknd

    weekend_check = ShortCircuitOperator(
        task_id="check_weekend",
        python_callable=is_weekend,
        ignore_downstream_trigger_rules=False,
    )

    @task
    def cleanup_old_partitions() -> None:
        print("Weekend cleanup: removing partitions older than 90 days")

    weekend_check >> cleanup_old_partitions()


dag_instance = branching_demo()
'''

namespace: dict = {}
try:
    exec(BRANCH_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks: {task_ids}")

    # Verify branch task exists (type names vary across Airflow versions)
    branch = dag_obj.get_task("check_data_volume")
    assert branch is not None
    assert hasattr(branch, "downstream_task_ids")
    print(f"  [OK] Branch task present: check_data_volume (type={type(branch).__name__})")

    # Verify short-circuit task
    sc = dag_obj.get_task("check_weekend")
    assert sc is not None
    assert hasattr(sc, "python_callable")
    print(f"  [OK] Short-circuit task present: check_weekend (type={type(sc).__name__})")

    # Verify join trigger rule
    join = dag_obj.get_task("join")
    assert "none_failed" in str(join.trigger_rule).lower()
    print(f"  [OK] join trigger_rule: {join.trigger_rule} (handles skipped branches)")

    # Verify all branch paths present
    for tid in ["process_small", "process_large", "no_data_skip"]:
        assert tid in task_ids, f"Missing branch: {tid}"
    print("  [OK] All branch paths present: process_small, process_large, no_data_skip")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()
print("  BRANCHING DECISION GUIDE")
print("  -------------------------")
print("  Use BranchPythonOperator when:")
print("    - Multiple downstream paths, only one should run")
print("    - e.g., route based on data volume, environment, or day of week")
print()
print("  Use ShortCircuitOperator when:")
print("    - Binary decision: proceed or skip EVERYTHING downstream")
print("    - e.g., skip if no new data, skip if weekend, skip if feature disabled")
print()
print("  TRIGGER RULE AFTER BRANCHING")
print("  ------------------------------")
print("  - Always use trigger_rule=NONE_FAILED on join point after branch")
print("  - Without it: join fails because skipped branches look like failures")
print("  - NONE_FAILED = 'run if no upstream failed (success OR skipped)'")
print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - @task.branch returns task_id string(s) to run, skips the rest")
print("  - ShortCircuitOperator returns bool: False = skip all downstream")
print("  - Join points after branches need trigger_rule=NONE_FAILED")
print("  - Skipped tasks are colored gray/pink in the Airflow UI")
print()
