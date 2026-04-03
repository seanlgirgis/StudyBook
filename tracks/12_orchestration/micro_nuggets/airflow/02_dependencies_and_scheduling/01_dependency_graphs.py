"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-01 · Task Dependency Graphs (Fan-In / Fan-Out)                    ║
║  Parallel branches, merge points, and trigger rules                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Real pipelines are not always linear.  Fan-out runs tasks in parallel;
fan-in waits for multiple upstreams before proceeding.  Trigger rules
control what "all upstream done" actually means.

KEY CONCEPTS
────────────
  >>  operator         — set_downstream: A >> B means B runs after A
  <<  operator         — set_upstream:   B << A is equivalent
  list syntax          — [A, B] >> C means C waits for both A and B
  trigger_rule         — when does a task run relative to its upstreams?
    ALL_SUCCESS (default) — all upstreams succeeded
    ALL_DONE              — all upstreams finished (any state)
    ONE_SUCCESS           — at least one upstream succeeded
    ONE_FAILED            — at least one upstream failed
    NONE_FAILED           — no upstream failed (success OR skipped)
    NONE_SKIPPED          — no upstream skipped

INTERVIEW RELEVANCE
───────────────────
  "How do you run tasks in parallel in Airflow?"
  "What is fan-in and fan-out?"
  "Explain trigger_rule and when you would use ALL_DONE."
  "How do you implement a cleanup task that always runs even if upstream fails?"
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 02-01 : Task Dependency Graphs ------------------")

FAN_DAG_CODE = '''
from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

@dag(
    dag_id="lab_airflow_fan_in_fan_out",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab", "dependencies"],
)
def fan_in_fan_out():
    """
    Graph topology:
                 ingest
               /   |   \\
         bronze  silver  gold   <- fan-out (parallel)
               \\   |   /
                validate       <- fan-in  (waits for all 3)
                    |
                 cleanup       <- always runs (trigger_rule=ALL_DONE)
    """

    @task
    def ingest() -> dict:
        print("Ingesting raw data...")
        return {"rows": 5000, "source": "api"}

    @task
    def process_bronze(data: dict) -> int:
        print(f"Bronze: raw copy of {data[\'rows\']} rows")
        return data["rows"]

    @task
    def process_silver(data: dict) -> int:
        cleaned = int(data["rows"] * 0.95)
        print(f"Silver: cleaned {cleaned} rows")
        return cleaned

    @task
    def process_gold(data: dict) -> int:
        agg = int(data["rows"] * 0.10)
        print(f"Gold: aggregated {agg} rows")
        return agg

    @task
    def validate(bronze: int, silver: int, gold: int) -> str:
        # Fan-in: receives outputs from all 3 parallel tasks
        assert silver <= bronze, "Silver count exceeds bronze"
        assert gold <= silver, "Gold count exceeds silver"
        summary = f"Validation OK: bronze={bronze}, silver={silver}, gold={gold}"
        print(summary)
        return summary

    @task(trigger_rule=TriggerRule.ALL_DONE)  # runs even if upstream fails
    def cleanup() -> None:
        print("Cleanup: releasing temp resources (always runs)")

    raw = ingest()
    b = process_bronze(raw)
    s = process_silver(raw)
    g = process_gold(raw)
    v = validate(b, s, g)
    v >> cleanup()


dag_instance = fan_in_fan_out()
'''

namespace: dict = {}
try:
    exec(FAN_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks: {task_ids}")

    # Verify fan-out: ingest has 3 downstream tasks
    ingest = dag_obj.get_task("ingest")
    downstream_ids = {t.task_id for t in ingest.downstream_list}
    expected_fan_out = {"process_bronze", "process_silver", "process_gold"}
    assert expected_fan_out == downstream_ids, f"Fan-out mismatch: {downstream_ids}"
    print(f"  [OK] Fan-out: ingest -> {sorted(downstream_ids)}")

    # Verify fan-in: validate has 3 upstream tasks
    validate = dag_obj.get_task("validate")
    upstream_ids = {t.task_id for t in validate.upstream_list}
    expected_fan_in = {"process_bronze", "process_silver", "process_gold"}
    assert expected_fan_in == upstream_ids, f"Fan-in mismatch: {upstream_ids}"
    print(f"  [OK] Fan-in:  {sorted(upstream_ids)} -> validate")

    # Verify cleanup trigger rule
    cleanup = dag_obj.get_task("cleanup")
    assert str(cleanup.trigger_rule) in ("all_done", "TriggerRule.ALL_DONE")
    print("  [OK] cleanup trigger_rule = ALL_DONE (runs even on failure)")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()
print("  TRIGGER RULE CHEAT SHEET")
print("  -------------------------")
rules = [
    ("ALL_SUCCESS (default)", "All upstreams succeeded"),
    ("ALL_DONE",              "All upstreams finished (any state) — use for cleanup"),
    ("ALL_FAILED",            "All upstreams failed"),
    ("ONE_SUCCESS",           "At least one upstream succeeded — early exit pattern"),
    ("ONE_FAILED",            "At least one upstream failed — alerting"),
    ("NONE_FAILED",           "None failed (success or skipped) — after branching"),
    ("NONE_SKIPPED",          "No upstream was skipped"),
]
for rule, desc in rules:
    print(f"  {rule:<28}  {desc}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - Fan-out: one task feeds multiple parallel tasks (list syntax or multi-arrow)")
print("  - Fan-in: @task receives multiple positional args — waits for all upstreams")
print("  - Use trigger_rule=ALL_DONE for cleanup/notification that must always run")
print("  - NONE_FAILED is the right rule after a BranchPythonOperator branch")
print()
