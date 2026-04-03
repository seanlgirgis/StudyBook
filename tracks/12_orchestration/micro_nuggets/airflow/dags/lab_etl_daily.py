"""
Lab DAG: lab_airflow_etl_daily

Daily ETL pipeline demonstrating:
  - TaskFlow API
  - Date-partitioned extraction
  - Idempotent load (DELETE + INSERT)
  - Retry with exponential backoff
  - Audit metadata

Schedule: @daily
"""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task


def _on_failure(context: dict) -> None:
    dag_id  = context["dag"].dag_id
    task_id = context["task"].task_id
    run_id  = context["run_id"]
    exc     = context.get("exception", "unknown")
    print(f"[ALERT] {dag_id}.{task_id} FAILED | run={run_id} | err={exc}")


@dag(
    dag_id="lab_airflow_etl_daily",
    description="Daily ETL: ingest -> quality -> transform -> load -> audit",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "retry_exponential_backoff": True,
        "max_retry_delay": timedelta(minutes=30),
        "on_failure_callback": _on_failure,
    },
    tags=["lab", "etl", "daily"],
)
def lab_etl_daily():
    """Daily ETL pipeline with production patterns."""

    @task
    def extract(**context) -> dict:
        ds = context["ds"]
        print(f"[extract] Fetching records for partition: {ds}")
        # Simulate extraction — in prod: query API or source DB
        rows = [
            {"id": i, "date": ds, "amount": float(i * 10), "category": "A" if i % 2 == 0 else "B"}
            for i in range(1, 101)
        ]
        return {"partition": ds, "records": rows, "count": len(rows)}

    @task
    def quality_check(raw: dict) -> dict:
        records = raw["records"]
        nulls = [r for r in records if r.get("amount") is None]
        if nulls:
            raise ValueError(f"Data quality fail: {len(nulls)} null amounts")
        if len(records) == 0:
            raise ValueError("No records extracted — possible source issue")
        print(f"[quality_check] OK: {len(records)} records, 0 nulls")
        return raw

    @task
    def transform(validated: dict) -> dict:
        records = validated["records"]
        partition = validated["partition"]
        by_cat: dict = {}
        for r in records:
            cat = r["category"]
            if cat not in by_cat:
                by_cat[cat] = {"count": 0, "total": 0.0}
            by_cat[cat]["count"] += 1
            by_cat[cat]["total"] += r["amount"]

        result = [
            {
                "partition_date": partition,
                "category": cat,
                "record_count": d["count"],
                "total_amount": round(d["total"], 2),
                "avg_amount": round(d["total"] / d["count"], 2),
            }
            for cat, d in by_cat.items()
        ]
        print(f"[transform] {len(records)} records -> {len(result)} summary rows")
        return {"partition": partition, "rows": result, "source_count": len(records)}

    @task
    def load(transformed: dict) -> dict:
        partition = transformed["partition"]
        rows = transformed["rows"]
        # Idempotent: DELETE then INSERT
        print(f"[load] DELETE FROM daily_metrics WHERE partition_date = '{partition}'")
        for row in rows:
            print(f"[load] INSERT: {row}")
        return {
            "partition": partition,
            "rows_loaded": len(rows),
            "source_count": transformed["source_count"],
        }

    @task
    def audit(load_result: dict, **context) -> None:
        from datetime import datetime as dt
        record = {
            "dag_id": "lab_airflow_etl_daily",
            "partition": load_result["partition"],
            "rows_loaded": load_result["rows_loaded"],
            "source_count": load_result["source_count"],
            "run_id": context["run_id"],
            "loaded_at": dt.utcnow().isoformat(),
            "status": "success",
        }
        print(f"[audit] {record}")

    raw = extract()
    validated = quality_check(raw)
    transformed = transform(validated)
    load_result = load(transformed)
    audit(load_result)


# Instantiate DAG
lab_etl_daily_dag = lab_etl_daily()
