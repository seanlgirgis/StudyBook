"""
Lab DAG: lab_airflow_capstone_pipeline

Mini capstone demonstrating all production patterns combined:
  - Fan-out parallel processing
  - Branching on data volume
  - Retries with exponential backoff
  - SLA monitoring
  - Failure simulation + safe rerun

Schedule: None (manual trigger)
"""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule


OUTPUT_DIR = Path("/tmp/airflow_lab")


def _on_failure(context: dict) -> None:
    print(
        f"[ALERT] FAILURE: {context['dag'].dag_id}.{context['task'].task_id} "
        f"| run={context['run_id']}"
    )


@dag(
    dag_id="lab_airflow_capstone_pipeline",
    description="Capstone: full orchestration demo with failure recovery",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    params={"batch_size": 500, "environment": "staging"},
    default_args={
        "retries": 3,
        "retry_delay": timedelta(seconds=30),
        "retry_exponential_backoff": True,
        "max_retry_delay": timedelta(minutes=5),
        "on_failure_callback": _on_failure,
    },
    sla_miss_callback=lambda dag, task_list, blocking_task_list, slas, blocking_tis:
        print(f"[SLA MISS] {dag.dag_id}: {task_list}"),
    tags=["lab", "capstone"],
)
def lab_capstone_pipeline():
    """
    Pipeline topology:
      ingest
        |
      quality_gate
        |
      [bronze | silver | gold]  <- parallel
        |       |       |
           aggregate
              |
            report
              |
           cleanup          <- always runs (ALL_DONE)
    """

    @task(sla=timedelta(minutes=5))
    def ingest(**context) -> dict:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        ds = context["ds"]
        batch_size = context["params"]["batch_size"]
        env = context["params"]["environment"]
        print(f"[ingest] ds={ds}, env={env}, batch_size={batch_size}")
        records = [
            {"id": i, "date": ds, "value": float(i * 1.5), "tier": ["bronze","silver","gold"][i % 3]}
            for i in range(1, batch_size + 1)
        ]
        return {"records": records, "partition": ds, "env": env}

    @task
    def quality_gate(raw: dict) -> dict:
        records = raw["records"]
        nulls = sum(1 for r in records if r.get("value") is None)
        if nulls > len(records) * 0.05:
            raise ValueError(f"Too many nulls: {nulls}")
        print(f"[quality_gate] OK: {len(records)} records")
        return raw

    @task(sla=timedelta(minutes=10))
    def process_bronze(data: dict) -> int:
        bronze = [r for r in data["records"] if r["tier"] == "bronze"]
        print(f"[bronze] Processing {len(bronze)} records")
        return len(bronze)

    @task(sla=timedelta(minutes=10))
    def process_silver(data: dict) -> int:
        silver = [r for r in data["records"] if r["tier"] == "silver"]
        print(f"[silver] Processing {len(silver)} records")
        return len(silver)

    @task(sla=timedelta(minutes=10))
    def process_gold(data: dict) -> int:
        gold = [r for r in data["records"] if r["tier"] == "gold"]
        print(f"[gold] Processing {len(gold)} records")
        return len(gold)

    @task
    def aggregate(bronze: int, silver: int, gold: int, data: dict) -> dict:
        total = bronze + silver + gold
        summary = {
            "partition": data["partition"],
            "bronze": bronze, "silver": silver, "gold": gold,
            "total": total,
        }
        print(f"[aggregate] {summary}")
        # Idempotent write
        out = OUTPUT_DIR / f"capstone_{data['partition']}.json"
        import json
        with open(out, "w") as f:
            json.dump(summary, f, indent=2)
        return {**summary, "output_path": str(out)}

    @task
    def report(result: dict) -> None:
        print(f"[report] Pipeline complete: {result['total']} records processed")
        print(f"[report] Output: {result['output_path']}")

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def cleanup() -> None:
        """Always runs — cleanup temp resources even if pipeline failed."""
        print("[cleanup] Releasing temporary resources")

    # Wire the pipeline
    raw = ingest()
    valid = quality_gate(raw)
    b = process_bronze(valid)
    s = process_silver(valid)
    g = process_gold(valid)
    result = aggregate(b, s, g, valid)
    rpt = report(result)
    rpt >> cleanup()


lab_capstone_pipeline_dag = lab_capstone_pipeline()
