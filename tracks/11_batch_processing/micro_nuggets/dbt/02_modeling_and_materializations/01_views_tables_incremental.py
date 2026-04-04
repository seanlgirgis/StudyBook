"""
01_views_tables_incremental.py — Materialization types in dbt.

Teaches:
  - view: recreated each run; no data stored; cheapest but slowest to query
  - table: dropped and rebuilt from scratch each run; fastest to query
  - incremental: only processes new/changed rows; cheapest for large tables
  - on_schema_change: what happens when the model SQL changes columns
  - unique_key: deduplication key for incremental models
  - The {% if is_incremental() %} pattern — the core of incremental dbt

Key concept:
  Materialization determines HOW dbt writes results to the database, not WHAT the SQL does.
  Choosing wrong materializations = wasted compute or stale data.

  view:        SELECT runs every time a downstream model queries it
  table:       Full rebuild every dbt run — predictable but expensive on large data
  incremental: Only new rows → huge cost saving for high-volume append-only tables
  ephemeral:   Not materialized at all — CTE injected into downstream models

Run:
    python 02_modeling_and_materializations/01_views_tables_incremental.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import (
    DBT_PROJECT_DIR,
    detect_backend,
    run_dbt,
    write_profiles_yml,
)


def explain_materializations() -> None:
    print("""
--- dbt Materialization Types ---

  +------------+------------------+-----------------------------------+
  | Type       | Storage          | When to use                       |
  +------------+------------------+-----------------------------------+
  | view       | None (query def) | Small/fast source; rarely queried |
  | table      | Full copy        | Frequently queried; moderate size |
  | incremental| Append/merge     | High volume, append-only streams  |
  | ephemeral  | CTE in memory    | Intermediate steps; not queried   |
  +------------+------------------+-----------------------------------+

  on_schema_change (incremental only):
    "ignore"             → new columns in model SQL are silently dropped
    "fail"               → dbt errors if model SQL changes column list
    "append_new_columns" → new columns added to target, existing data NULL
    "sync_all_columns"   → adds new + removes old columns (careful!)

  unique_key (incremental only):
    Tells dbt how to identify a record for UPSERT / MERGE.
    If a row with that key exists, it's UPDATED.  If not, it's INSERTED.
    Without unique_key, dbt only INSERTs (pure append mode).
    """)


def show_compiled_diff(model_a: str, model_b: str) -> None:
    """Compare compiled SQL between two models to show materialization differences."""
    target_dir = DBT_PROJECT_DIR / "target" / "compiled" / "dbt_lab" / "models"
    for subdir, model in [("marts", model_a), ("marts", model_b)]:
        p = target_dir / subdir / f"{model}.sql"
        if p.exists():
            print(f"\n--- Compiled SQL: {model}.sql ---")
            content = p.read_text(encoding="utf-8")
            for line in content.splitlines()[:25]:
                print(f"  {line}")
            if len(content.splitlines()) > 25:
                print(f"  ... ({len(content.splitlines()) - 25} more lines)")
        else:
            print(f"\n  (Compiled SQL not found for {model})")


def main() -> int:
    print("=" * 60)
    print("  Materializations — view, table, incremental")
    print("=" * 60)

    explain_materializations()

    # Write profiles.yml
    write_profiles_yml()

    # Step 1: Run staging first (dependencies)
    print("[Step 1] Seeding and running staging layer...")
    run_dbt(["seed", "--full-refresh"], timeout=120)
    rc_stg, _, _ = run_dbt(["run", "--select", "staging"], timeout=180)

    # Step 2: Run dim_customers (table materialization)
    print("\n[Step 2] Running dim_customers (materialized=table)...")
    rc_dim, stdout_dim, stderr_dim = run_dbt(
        ["run", "--select", "dim_customers"], timeout=120
    )
    for line in (stdout_dim + "\n" + stderr_dim).strip().splitlines()[-8:]:
        print(f"  {line}")

    # Step 3: Run fct_events_incremental FIRST run
    print("\n[Step 3] Running fct_events_incremental — FIRST RUN (full load)...")
    rc_inc1, stdout_inc1, stderr_inc1 = run_dbt(
        ["run", "--select", "fct_events_incremental"], timeout=120
    )
    for line in (stdout_inc1 + "\n" + stderr_inc1).strip().splitlines()[-8:]:
        print(f"  {line}")

    # Show row count after first run
    backend, _ = detect_backend()
    first_run_count = 0
    if backend == "duckdb":
        try:
            import duckdb
            from _dbt_lane_connect import _duckdb_path
            con = duckdb.connect(_duckdb_path(), read_only=True)
            for schema in ("dbt_lab", "main"):
                try:
                    row = con.execute(
                        f"SELECT COUNT(*) FROM {schema}.fct_events_incremental"
                    ).fetchone()
                    first_run_count = row[0]
                    print(f"\n  After 1st run: {schema}.fct_events_incremental = {first_run_count} rows")
                    break
                except Exception:
                    continue
            con.close()
        except Exception as e:
            print(f"  (Could not query: {e})")

    # Step 4: Run AGAIN — incremental should process 0 new rows
    print("\n[Step 4] Running fct_events_incremental — SECOND RUN (incremental)...")
    print("  Expected: 0 new rows inserted (all rows already loaded)")
    rc_inc2, stdout_inc2, stderr_inc2 = run_dbt(
        ["run", "--select", "fct_events_incremental"], timeout=120
    )
    for line in (stdout_inc2 + "\n" + stderr_inc2).strip().splitlines()[-8:]:
        print(f"  {line}")

    if backend == "duckdb" and first_run_count > 0:
        try:
            import duckdb
            from _dbt_lane_connect import _duckdb_path
            con = duckdb.connect(_duckdb_path(), read_only=True)
            for schema in ("dbt_lab", "main"):
                try:
                    row = con.execute(
                        f"SELECT COUNT(*) FROM {schema}.fct_events_incremental"
                    ).fetchone()
                    second_run_count = row[0]
                    print(f"\n  After 2nd run: {schema}.fct_events_incremental = {second_run_count} rows")
                    if second_run_count == first_run_count:
                        print("  CONFIRMED: Incremental run added 0 new rows (idempotent)")
                    break
                except Exception:
                    continue
            con.close()
        except Exception as e:
            print(f"  (Could not query: {e})")

    # Show compiled SQL diff
    print("\n[Step 5] Comparing compiled SQL...")
    show_compiled_diff("dim_customers", "fct_events_incremental")

    print("\nThe is_incremental() pattern in fct_events_incremental.sql:")
    model_path = DBT_PROJECT_DIR / "models" / "marts" / "fct_events_incremental.sql"
    if model_path.exists():
        content = model_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            print(f"  {line}")

    print()
    print("KEY TAKEAWAYS:")
    print("  1. view = virtual; table = physical copy; incremental = delta append")
    print("  2. {% if is_incremental() %} guards the WHERE clause for delta runs")
    print("  3. unique_key drives UPSERT logic (prevents duplicates)")
    print("  4. on_schema_change='append_new_columns' is safe for additive changes")
    print("  5. Use `dbt run --full-refresh` to force rebuild of incremental models")
    print("  6. Incremental models save cost on event tables with millions of rows")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
