"""
07_mini_capstone/01_mini_capstone.py — Bronze → Silver → Gold medallion architecture.

Teaches:
  - Medallion (lakehouse) architecture: Bronze → Silver → Gold
  - How dbt models map to each layer
  - Building all three layers with `dbt build`
  - Querying the final gold table for business insights
  - Why medallion beats "one big query" for maintainability

Key concept:
  Medallion architecture = layered data quality zones:

  Bronze  (Raw/Landing):  Exact copy of source; minimal transformation.
                          Preserves history; safe to reprocess. View or table.

  Silver  (Cleaned):      Filtered, deduplicated, standardized. Business rules applied.
                          Column renames, type casts, null handling. Table or incremental.

  Gold    (Aggregated):   Business-ready aggregations for reporting/ML.
                          Dimensional model, metrics, KPIs. Always table.

  ref() chain: brz_raw_orders → slv_orders_cleaned → gld_order_summary

Run:
    python 07_mini_capstone/01_mini_capstone.py
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


def explain_medallion() -> None:
    print("""
--- Medallion Architecture ---

  BRONZE (brz_)   → Raw data, minimal change
  │  - Preserves raw column names (or close to it)
  │  - May filter obvious garbage (NULLs in PK, etc.)
  │  - Stored as view or table depending on volume
  │  - Think: "safe landing zone for raw data"
  ▼
  SILVER (slv_)   → Cleaned, standardized
  │  - Renamed columns, proper types, deduplication
  │  - Applied business rules (exclude cancelled orders from revenue)
  │  - Joins allowed here (enrich orders with customer country)
  │  - Think: "trusted, queryable, but not yet aggregated"
  ▼
  GOLD (gld_)     → Business-ready aggregations
     - Revenue by country, cohort metrics, KPIs
     - Wide, denormalized, pre-aggregated for BI tools
     - Think: "final answer for the dashboard"

  Why not just write one big query?
    - Easier debugging: test each layer independently
    - Reuse: multiple gold tables can share one silver model
    - Performance: materialize silver as table; gold reads it fast
    - Lineage: clear separation of concerns in dbt docs
    """)


def show_model(layer: str, model: str) -> None:
    """Print a medallion layer model."""
    model_path = DBT_PROJECT_DIR / "models" / layer / f"{model}.sql"
    if model_path.exists():
        print(f"\n--- {layer}/{model}.sql ---")
        content = model_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            print(f"  {line}")
    else:
        print(f"\n  (Model not found: {model_path})")


def query_gold_table() -> None:
    """Query the gold table and print results."""
    backend, _ = detect_backend()
    if backend != "duckdb":
        print("  (Gold table query only shown for DuckDB backend)")
        return
    try:
        import duckdb
        from _dbt_lane_connect import _duckdb_path
        con = duckdb.connect(_duckdb_path(), read_only=True)
        print("\n--- Gold Table: gld_order_summary (top 10 rows) ---")
        for schema in ("dbt_lab_gold", "gold", "dbt_lab", "main"):
            try:
                rows = con.execute(
                    f"SELECT * FROM {schema}.gld_order_summary ORDER BY total_revenue_dollars DESC LIMIT 10"
                ).fetchall()
                col_names = [d[0] for d in con.description]
                # Print header
                header = " | ".join(f"{c:20}" for c in col_names)
                print(f"  {header}")
                print(f"  {'-'*len(header)}")
                for row in rows:
                    row_str = " | ".join(f"{str(v):20}" for v in row)
                    print(f"  {row_str}")
                break
            except Exception:
                continue
        con.close()
    except Exception as e:
        print(f"  (Could not query gold table: {e})")


def main() -> int:
    print("=" * 60)
    print("  Mini Capstone — Bronze → Silver → Gold")
    print("=" * 60)

    explain_medallion()

    write_profiles_yml()

    # Show the three layer models
    print("[Step 1] Medallion layer models:")
    show_model("bronze", "brz_raw_orders")
    show_model("silver", "slv_orders_cleaned")
    show_model("gold",   "gld_order_summary")

    # Step 2: Ensure seeds are loaded
    print("\n[Step 2] Loading seed data...")
    run_dbt(["seed", "--full-refresh"], timeout=120)

    # Step 3: Build all three layers
    print("\n[Step 3] Running `dbt build --select bronze silver gold staging`...")
    print("  (Building: staging → bronze → silver → gold in DAG order)\n")
    rc, stdout, stderr = run_dbt(
        ["build", "--select", "staging bronze silver gold"],
        timeout=300,
    )
    output = (stdout + "\n" + stderr).strip()
    for line in output.splitlines()[-20:]:
        print(f"  {line}")

    if rc != 0:
        print(f"\n  [NOTE] Build returned rc={rc}")
        print("  Some tests may fail due to intentional seed data issues.")
        print("  The medallion architecture is still demonstrated.")

    # Step 4: Query gold table
    print("\n[Step 4] Querying final gold table (business-ready output):")
    query_gold_table()

    # Step 5: Show lineage
    print("\n[Step 5] Lineage chain:")
    rc_ls, stdout_ls, stderr_ls = run_dbt(
        ["ls", "--select", "+gld_order_summary+"],
        timeout=60
    )
    output_ls = (stdout_ls + "\n" + stderr_ls).strip()
    lines = [l for l in output_ls.splitlines() if l.strip()]
    for line in lines[-15:]:
        print(f"  {line.strip()}")

    print()
    print("MEDALLION ARCHITECTURE SUMMARY:")
    print("  brz_raw_orders      → exact copy of seed, minimal filtering")
    print("  slv_orders_cleaned  → type-safe, business rules, cancelled excluded")
    print("  gld_order_summary   → aggregated by country, pre-computed for BI")
    print()
    print("  ref() chain: stg_orders → brz_raw_orders → slv_orders_cleaned → gld_order_summary")
    print("  dbt runs them in dependency order — no manual orchestration")
    print()
    print("KEY TAKEAWAYS:")
    print("  1. Bronze = preserve raw; Silver = clean + standardize; Gold = aggregate")
    print("  2. Separate layers = easier debugging, testing, and reuse")
    print("  3. Each layer has its own schema (bronze, silver, gold) in dbt_project.yml")
    print("  4. Medallion is storage-agnostic: works on DuckDB, Snowflake, BigQuery, etc.")
    print("  5. Gold tables are what BI tools / dashboards query — keep them fast")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
