"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-03 · DAG Params and Jinja Templating                              ║
║  Runtime configuration and dynamic SQL/commands with Jinja2                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
DAG Params allow callers to pass JSON config at trigger time.
Jinja templating lets you embed dynamic values (execution_date, params,
run_id, etc.) directly into BashOperator commands and SQL strings.

KEY CONCEPTS
────────────
  params={}            — default param values for the DAG; overridable at trigger
  {{ ds }}             — execution date as YYYY-MM-DD (most common template var)
  {{ execution_date }} — full pendulum datetime object
  {{ run_id }}         — unique run identifier
  {{ params.key }}     — access a named param
  {{ ti.xcom_pull() }} — pull XCom value in a template
  render_template_as_native_obj — return Python object instead of string

COMMON TEMPLATE VARIABLES
──────────────────────────
  {{ ds }}             2024-01-15
  {{ ds_nodash }}      20240115
  {{ ts }}             2024-01-15T00:00:00+00:00
  {{ ts_nodash }}      20240115T000000
  {{ prev_ds }}        2024-01-14  (previous execution date)
  {{ next_ds }}        2024-01-16  (next execution date)
  {{ dag.dag_id }}     the DAG id string
  {{ task.task_id }}   the task id string

INTERVIEW RELEVANCE
───────────────────
  "How do you pass runtime configuration to a DAG?"
  "What is {{ ds }} in Airflow and when is it useful?"
  "What is the difference between execution_date and scheduled_date?"
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 01-03 : DAG Params and Jinja Templating ----------")

PARAMS_DAG_CODE = '''
from airflow.decorators import dag, task
from airflow.models.param import Param
from datetime import datetime

@dag(
    dag_id="lab_airflow_params_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    params={
        "batch_size": Param(100, type="integer", description="Records per batch"),
        "environment": Param("staging", type="string", enum=["staging", "prod"]),
        "start_date": Param("2024-01-01", type="string", format="date"),
    },
    tags=["lab", "params"],
)
def params_demo():
    """
    Demonstrates DAG Params — values passed at trigger time.
    The Airflow UI shows a form when you trigger this DAG manually.
    """

    @task
    def validate_params(**context) -> dict:
        params = context["params"]
        batch_size = params["batch_size"]
        env = params["environment"]
        start = params["start_date"]

        assert batch_size > 0, "batch_size must be positive"
        assert env in ("staging", "prod"), f"Unknown env: {env}"
        print(f"Params validated: batch_size={batch_size}, env={env}, start={start}")
        return {"batch_size": batch_size, "env": env, "start": start}

    @task
    def process(config: dict) -> str:
        return (
            f"Processing {config[\'batch_size\']} records "
            f"in {config[\'env\']} from {config[\'start\']}"
        )

    @task
    def report(result: str) -> None:
        print(f"Result: {result}")

    cfg = validate_params()
    result = process(cfg)
    report(result)


dag_instance = params_demo()
'''

namespace: dict = {}
try:
    exec(PARAMS_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    # Verify params defined
    param_keys = list(dag_obj.params.keys())
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Params defined: {param_keys}")
    assert "batch_size" in param_keys
    assert "environment" in param_keys
    assert "start_date" in param_keys
    print("  [OK] Required params present: batch_size, environment, start_date")

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] Tasks: {task_ids}")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ── Demonstrate Jinja template rendering (no Airflow runtime needed) ──────────
print()
print("  JINJA TEMPLATE EXAMPLES")
print("  -----------------------")
examples = [
    ("{{ ds }}",                    "2024-01-15"),
    ("{{ ds_nodash }}",             "20240115"),
    ("{{ params.batch_size }}",     "100  (from params dict)"),
    ("{{ run_id }}",                "manual__2024-01-15T00:00:00+00:00"),
    ("{{ dag.dag_id }}",            "lab_airflow_params_demo"),
    ("{{ ti.xcom_pull('t1') }}",    "value from XCom key=return_value"),
]
for template, example in examples:
    print(f"  {template:<45} -> {example}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - Params create a trigger-time form in the Airflow UI")
print("  - Param type validation happens before the DAG run starts")
print("  - {{ ds }} is the safest way to make tasks idempotent by date")
print("  - Templates are only rendered in templated_fields of operators")
print("  - Never use datetime.now() in a DAG — use {{ ds }} instead")
print()
