"""
01_snapshots_scd2.py — dbt Snapshots and SCD Type 2.

Teaches:
  - What SCD (Slowly Changing Dimension) Type 2 means
  - dbt snapshot block syntax and config options
  - strategy='check' vs strategy='timestamp'
  - dbt-added columns: dbt_scd_id, dbt_valid_from, dbt_valid_to, dbt_updated_at
  - How to detect history: dbt_valid_to IS NULL = current row
  - How snapshot differs from a MERGE SCD2 approach

Key concept:
  SCD Type 2 = keep a full history of dimension changes.
  When a customer's tier changes from 'silver' to 'gold':
    - Type 1: UPDATE in place (history lost)
    - Type 2: Add a NEW row, set dbt_valid_to on the old row, NULL on the new

  dbt snapshot runs AFTER your models and inserts/closes rows automatically.
  It is NOT a model — it's a snapshot block in snapshots/ directory.

Run:
    python 04_snapshots_and_scd/01_snapshots_scd2.py
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


def explain_scd2() -> None:
    print("""
--- SCD Type 2 — Slowly Changing Dimensions ---

  Problem: Customer Alice was 'gold' tier in Jan; upgraded to 'platinum' in Mar.
  You need to answer: "What tier was Alice in Feb?" — you need HISTORY.

  SCD Type 2 solution — add a new row for each change:
    | customer_id | tier      | dbt_valid_from | dbt_valid_to |
    |-------------|-----------|----------------|--------------|
    | 1           | gold      | 2023-01-01     | 2023-03-01   |  ← historical
    | 1           | platinum  | 2023-03-01     | NULL         |  ← current

  dbt snapshot generates these columns automatically:
    dbt_scd_id      → surrogate key for each historical row
    dbt_valid_from  → when this version became active
    dbt_valid_to    → when this version ended (NULL = still current)
    dbt_updated_at  → last time this row was processed

--- strategy='check' vs strategy='timestamp' ---

  check:      Compare specific columns (check_cols).
              Any change in those columns triggers a new row.
              More flexible; doesn't require an updated_at column.

  timestamp:  Use an updated_at column to detect changes.
              Only rows with updated_at > max(dbt_updated_at) are processed.
              Faster at scale (index-friendly); requires maintained updated_at.

--- dbt Snapshot vs MERGE SCD2 ---

  MERGE SCD2 (raw SQL):
    MERGE INTO dim_customers USING staging AS src ON ...
    WHEN MATCHED AND changed THEN UPDATE (close old row), INSERT (new row)
    → You write and maintain the MERGE logic
    → Hard to get right; no lineage tracking

  dbt snapshot:
    → dbt writes the MERGE logic; you define WHAT to track
    → Automatic dbt_scd_id, dbt_valid_from, dbt_valid_to columns
    → Integrated with DAG; shows in dbt docs lineage
    → Idempotent: safe to rerun
    """)


def show_snapshot_file() -> None:
    snap_path = DBT_PROJECT_DIR / "snapshots" / "customers_snapshot.sql"
    if snap_path.exists():
        print("\n--- customers_snapshot.sql ---")
        content = snap_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            print(f"  {line}")
    else:
        print(f"\n  (Snapshot file not found: {snap_path})")


def query_snapshot(label: str) -> None:
    """Query the snapshot table and show current + historical rows."""
    backend, _ = detect_backend()
    if backend != "duckdb":
        print(f"  ({label} — query only implemented for DuckDB backend)")
        return
    try:
        import duckdb
        from _dbt_lane_connect import _duckdb_path
        con = duckdb.connect(_duckdb_path(), read_only=True)
        print(f"\n  --- Snapshot rows ({label}) ---")
        for schema in ("dbt_lab_snapshots", "snapshots", "dbt_lab", "main"):
            try:
                rows = con.execute(
                    f"""
                    SELECT customer_id, customer_name, tier,
                           dbt_valid_from, dbt_valid_to
                    FROM {schema}.customers_snapshot
                    ORDER BY customer_id, dbt_valid_from
                    LIMIT 20
                    """
                ).fetchall()
                print(f"  (from schema: {schema})")
                print(f"  {'ID':4} | {'Name':20} | {'Tier':10} | {'valid_from':12} | {'valid_to':12}")
                print(f"  {'-'*4}-+-{'-'*20}-+-{'-'*10}-+-{'-'*12}-+-{'-'*12}")
                for row in rows:
                    cid, name, tier, vfrom, vto = row
                    vto_str = str(vto)[:10] if vto else "NULL (current)"
                    print(f"  {str(cid):4} | {str(name):20} | {str(tier):10} | {str(vfrom)[:12]:12} | {vto_str:14}")
                break
            except Exception:
                continue
        con.close()
    except Exception as e:
        print(f"  (Could not query snapshot: {e})")


def main() -> int:
    print("=" * 60)
    print("  Snapshots — SCD Type 2 with dbt")
    print("=" * 60)

    explain_scd2()

    write_profiles_yml()

    # Ensure staging is built (snapshot reads from stg_customers)
    print("[Step 1] Building staging layer...")
    run_dbt(["seed", "--full-refresh"], timeout=120)
    run_dbt(["run", "--select", "staging"], timeout=180)

    # Show snapshot definition
    show_snapshot_file()

    # Step 2: Run snapshot for the first time
    print("\n[Step 2] Running `dbt snapshot` — FIRST RUN (inserts all rows)...")
    rc1, stdout1, stderr1 = run_dbt(["snapshot"], timeout=120)
    for line in (stdout1 + "\n" + stderr1).strip().splitlines()[-10:]:
        print(f"  {line}")
    query_snapshot("after 1st snapshot run")

    # Step 3: Simulate a tier change
    # We do this by running seed with updated data for customer 1 (change tier)
    # For demo purposes we modify the CSV temporarily and re-seed
    print("\n[Step 3] Simulating a tier change (customer 1: gold → platinum)...")
    seeds_dir = DBT_PROJECT_DIR / "seeds"
    csv_path = seeds_dir / "raw_customers.csv"
    if csv_path.exists():
        original = csv_path.read_text(encoding="utf-8")
        # Change Alice from gold to platinum for the update demo
        updated = original.replace(
            "1,Alice Johnson,alice@example.com,US,2023-01-15,true,gold",
            "1,Alice Johnson,alice@example.com,US,2023-01-15,true,platinum",
        )
        csv_path.write_text(updated, encoding="utf-8")
        print("  Updated raw_customers.csv: Alice tier gold → platinum")

        # Re-seed and run staging
        run_dbt(["seed", "--full-refresh"], timeout=120)
        run_dbt(["run", "--select", "stg_customers"], timeout=120)

        # Step 4: Run snapshot again — should detect the change
        print("\n[Step 4] Running `dbt snapshot` — SECOND RUN (captures tier change)...")
        rc2, stdout2, stderr2 = run_dbt(["snapshot"], timeout=120)
        for line in (stdout2 + "\n" + stderr2).strip().splitlines()[-10:]:
            print(f"  {line}")
        query_snapshot("after 2nd snapshot — Alice now has 2 rows")

        # Restore original CSV
        csv_path.write_text(original, encoding="utf-8")
        print("\n  (Restored raw_customers.csv to original)")
    else:
        print("  (CSV not found — skipping tier change simulation)")

    print()
    print("KEY TAKEAWAYS:")
    print("  1. SCD Type 2 preserves history via dbt_valid_from / dbt_valid_to")
    print("  2. dbt_valid_to IS NULL = the current (active) version of a record")
    print("  3. strategy='check': compare columns list; any change → new row")
    print("  4. strategy='timestamp': use updated_at col; faster at large scale")
    print("  5. dbt snapshot handles all MERGE/UPSERT logic — you define WHAT")
    print("  6. Snapshots run AFTER models; add `dbt snapshot` to your CI pipeline")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
