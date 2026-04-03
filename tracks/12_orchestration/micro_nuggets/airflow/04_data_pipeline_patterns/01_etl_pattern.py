"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-01 · ETL Pipeline Pattern                                         ║
║  Extract -> Transform -> Load with idempotency and quality checks            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
A canonical ETL DAG pattern: extract raw data, transform it with business
logic and quality checks, then load to a target.  The key engineering
requirement is idempotency — rerunning must produce the same result.

KEY CONCEPTS
────────────
  Idempotency          — rerunning a task produces the same result every time
  DELETE + INSERT      — classic pattern for idempotent loads
  MERGE / UPSERT       — database-native idempotent write
  Watermark            — high-water mark for incremental extraction
  audit metadata       — row_count, load_time, run_id stored alongside data

INTERVIEW RELEVANCE
───────────────────
  "How do you make an ETL pipeline idempotent?"
  "What is the difference between full load and incremental load?"
  "How do you handle duplicate records in a pipeline?"
  "What does idempotent mean in the context of Airflow tasks?"
"""
from __future__ import annotations

import sys
from pathlib import Path

print("\n-- Nugget 04-01 : ETL Pipeline Pattern --------------------")

ETL_DAG_CODE = '''
from airflow.decorators import dag, task
from datetime import datetime, timedelta

@dag(
    dag_id="lab_airflow_etl_pattern",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=3),
    },
    tags=["lab", "etl", "patterns"],
)
def etl_pattern():
    """
    Production-grade ETL pattern:
      extract  -> data_quality_check -> transform -> load -> audit

    Idempotency strategy:
      - extract: partition by {{ ds }} (date-based, re-runnable)
      - load: DELETE WHERE date={{ ds }} then INSERT (idempotent write)
      - audit: record run metadata for lineage
    """

    @task
    def extract(**context) -> dict:
        """
        Extract records for the execution date partition.
        Pattern: always filter by {{ ds }} so reruns overwrite the same data.
        """
        ds = context["ds"]
        run_id = context["run_id"]
        print(f"Extracting records for partition: {ds}")

        # Simulated extraction result
        records = [
            {"id": 1, "date": ds, "value": 100.0, "category": "A"},
            {"id": 2, "date": ds, "value": 200.0, "category": "B"},
            {"id": 3, "date": ds, "value": None,  "category": "A"},  # null to catch
            {"id": 4, "date": ds, "value": 150.0, "category": "B"},
        ]
        print(f"Extracted {len(records)} raw records for {ds}")
        return {"records": records, "partition": ds, "run_id": run_id}

    @task
    def data_quality_check(raw: dict) -> dict:
        """
        Fail fast: catch data issues before wasting transform compute.
        """
        records = raw["records"]
        partition = raw["partition"]

        errors = []
        if not records:
            errors.append("No records extracted")

        null_values = [r for r in records if r.get("value") is None]
        if null_values:
            print(f"  WARNING: {len(null_values)} records with null value")
            # Non-fatal: log but continue (could also fail here in strict mode)

        # Remove nulls
        clean = [r for r in records if r.get("value") is not None]

        if errors:
            raise ValueError(f"Data quality failed: {errors}")

        print(f"  Quality check: {len(records)} in -> {len(clean)} clean")
        return {**raw, "records": clean, "dropped": len(records) - len(clean)}

    @task
    def transform(validated: dict) -> dict:
        """Apply business logic: normalize, aggregate, enrich."""
        records = validated["records"]
        partition = validated["partition"]

        # Normalize + aggregate by category
        by_cat: dict = {}
        for r in records:
            cat = r["category"]
            if cat not in by_cat:
                by_cat[cat] = {"count": 0, "total": 0.0}
            by_cat[cat]["count"] += 1
            by_cat[cat]["total"] += r["value"]

        result_rows = [
            {
                "partition_date": partition,
                "category": cat,
                "record_count": data["count"],
                "total_value": round(data["total"], 2),
                "avg_value": round(data["total"] / data["count"], 2),
            }
            for cat, data in by_cat.items()
        ]
        print(f"  Transform: {len(records)} records -> {len(result_rows)} summary rows")
        return {**validated, "transformed": result_rows}

    @task
    def load(transformed: dict) -> dict:
        """
        Idempotent load: DELETE existing partition, then INSERT.
        This pattern works for any database (PostgreSQL, BigQuery, Redshift).
        """
        rows = transformed["transformed"]
        partition = transformed["partition"]

        # Pseudo-SQL (would use actual DB connection in production)
        print(f"  DELETE FROM daily_metrics WHERE partition_date = '{partition}'")
        print(f"  INSERT INTO daily_metrics ({len(rows)} rows)")

        for row in rows:
            print(f"    {row}")

        return {
            "partition": partition,
            "rows_loaded": len(rows),
            "run_id": transformed["run_id"],
        }

    @task
    def audit(load_result: dict) -> None:
        """Record audit metadata for lineage and monitoring."""
        from datetime import datetime as dt
        record = {
            "dag_id": "lab_airflow_etl_pattern",
            "partition": load_result["partition"],
            "rows_loaded": load_result["rows_loaded"],
            "run_id": load_result["run_id"],
            "loaded_at": dt.utcnow().isoformat(),
            "status": "success",
        }
        print(f"  Audit: {record}")
        # In production: INSERT INTO pipeline_audit_log

    raw = extract()
    validated = data_quality_check(raw)
    transformed = transform(validated)
    load_result = load(transformed)
    audit(load_result)


dag_instance = etl_pattern()
'''

namespace: dict = {}
try:
    exec(ETL_DAG_CODE, namespace)  # noqa: S102
    dag_obj = namespace["dag_instance"]

    task_ids = sorted(dag_obj.task_ids)
    print(f"  [OK] DAG parsed: {dag_obj.dag_id}")
    print(f"  [OK] Tasks: {task_ids}")

    # Verify full ETL chain
    required = {"extract", "data_quality_check", "transform", "load", "audit"}
    assert required == set(task_ids), f"Missing: {required - set(task_ids)}"
    print("  [OK] Full ETL chain: extract -> dq_check -> transform -> load -> audit")

    # Verify dependency chain
    dq = dag_obj.get_task("data_quality_check")
    assert "extract" in [t.task_id for t in dq.upstream_list]

    audit = dag_obj.get_task("audit")
    assert "load" in [t.task_id for t in audit.upstream_list]
    print("  [OK] Dependency chain correct")

    # Verify retries
    assert dag_obj.default_args["retries"] == 2
    print("  [OK] default_args retries=2")

except ImportError as e:
    print(f"  [SKIP] apache-airflow not installed: {e}")
    sys.exit(0)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()
print("  IDEMPOTENCY PATTERNS")
print("  --------------------")
patterns = [
    ("DELETE + INSERT",  "Delete partition then insert — safe for all DBs"),
    ("MERGE / UPSERT",   "ON CONFLICT DO UPDATE — efficient for keyed data"),
    ("TRUNCATE + INSERT","For full-table loads; risky if partial failure"),
    ("Write-once S3",    "s3://bucket/dt=YYYY-MM-DD/file.parquet — immutable"),
    ("Overwrite mode",   "spark.write.mode('overwrite') — always safe"),
]
for pattern, desc in patterns:
    print(f"  {pattern:<20}  {desc}")

print()
print("  KEY TAKEAWAYS")
print("  -------------")
print("  - Always filter extractions by {{ ds }} for idempotent reruns")
print("  - Fail fast with a data_quality_check task before expensive transforms")
print("  - Use DELETE+INSERT pattern for idempotent DB loads")
print("  - Record audit metadata (run_id, loaded_at, rows) for lineage")
print("  - Never use datetime.now() for partitioning — use execution_date")
print()
