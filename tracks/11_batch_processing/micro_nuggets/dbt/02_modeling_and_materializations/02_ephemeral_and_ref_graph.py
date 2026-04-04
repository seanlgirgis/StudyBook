"""
02_ephemeral_and_ref_graph.py — Ephemeral models and the ref() DAG.

Teaches:
  - Ephemeral materialization: model exists only as a CTE, never in DB
  - ref() creates directed edges in the DAG (Directed Acyclic Graph)
  - dbt resolves execution ORDER from the DAG automatically
  - `dbt ls` with graph operators to explore lineage
  - Why the DAG is dbt's superpower: no manual orchestration of SQL order

Key concept:
  ref('model_name') does TWO things:
    1. Generates the correct schema-qualified table name at runtime
    2. Registers a dependency edge in the DAG → enforces execution order

  Ephemeral model = CTE injected into the calling model's SQL.
  The ephemeral model never creates a table/view in the database.
  Use ephemeral for intermediate logic that has only ONE downstream consumer.

Run:
    python 02_modeling_and_materializations/02_ephemeral_and_ref_graph.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import (
    DBT_PROJECT_DIR,
    run_dbt,
    write_profiles_yml,
)


def explain_dag() -> None:
    print("""
--- The dbt DAG (Directed Acyclic Graph) ---

  Every ref() call creates a directed edge:
    stg_customers ──► int_orders_with_customers (ephemeral)
    stg_orders    ──► int_orders_with_customers (ephemeral)
                                  │
                                  ▼
                             fct_orders (table)

  dbt runs nodes in topological order:
    1. stg_customers and stg_orders (no dependencies on other models)
    2. int_orders_with_customers (depends on 1)
    3. fct_orders (depends on 2)

  This means you NEVER need to manually ORDER your SQL scripts.
  dbt figures it out from the ref() graph.

  Ephemeral models are "inlined" — they become CTEs inside downstream models.
  The final compiled SQL for fct_orders will contain the int_ CTE inside it.

--- Graph Operators ---
  +model_name      → model AND all its ancestors (upstream)
  model_name+      → model AND all its descendants (downstream)
  +model_name+     → full lineage: ancestors + model + descendants
  @model_name      → model + all children (downstream) + their parents
  source:name+     → all models downstream of a source
  tag:tagname      → all models with a specific tag
    """)


def show_ephemeral_model() -> None:
    model_path = DBT_PROJECT_DIR / "models" / "intermediate" / "int_orders_with_customers.sql"
    if model_path.exists():
        print("\n--- int_orders_with_customers.sql (ephemeral) ---")
        content = model_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            print(f"  {line}")
    else:
        print("\n  (int_orders_with_customers.sql not found)")


def show_compiled_fct_orders() -> None:
    """Show the compiled SQL for fct_orders which inlines the ephemeral CTE."""
    compiled = (
        DBT_PROJECT_DIR / "target" / "compiled" / "dbt_lab"
        / "models" / "marts" / "fct_orders.sql"
    )
    if compiled.exists():
        print("\n--- Compiled fct_orders.sql (note: int_ CTE is inlined) ---")
        content = compiled.read_text(encoding="utf-8")
        lines = content.splitlines()
        for line in lines[:50]:
            print(f"  {line}")
        if len(lines) > 50:
            print(f"  ... ({len(lines) - 50} more lines)")
    else:
        print("\n  (Compiled fct_orders.sql not found — run dbt compile first)")


def main() -> int:
    print("=" * 60)
    print("  Modeling — Ephemeral Models & ref() DAG")
    print("=" * 60)

    explain_dag()

    write_profiles_yml()

    # Ensure staging is present
    run_dbt(["seed", "--full-refresh"], timeout=120)
    run_dbt(["run", "--select", "staging"], timeout=180)

    # Show ephemeral model source
    show_ephemeral_model()

    # Step 1: Run fct_orders (triggers int_ ephemeral → fct_orders)
    print("\n[Step 1] Running fct_orders (depends on ephemeral int_orders_with_customers)...")
    rc, stdout, stderr = run_dbt(
        ["run", "--select", "fct_orders"], timeout=120
    )
    for line in (stdout + "\n" + stderr).strip().splitlines()[-10:]:
        print(f"  {line}")

    # Step 2: Compile to show inlined CTE
    print("\n[Step 2] Compiling to show ephemeral inlining...")
    run_dbt(["compile", "--select", "fct_orders"], timeout=120)
    show_compiled_fct_orders()

    # Step 3: Explore lineage with dbt ls
    print("\n[Step 3] Exploring lineage with `dbt ls`...")

    selectors = [
        (["ls", "--select", "+fct_orders"], "Ancestors of fct_orders (upstream)"),
        (["ls", "--select", "fct_orders+"], "Descendants of fct_orders (downstream)"),
        (["ls", "--select", "source:dbt_lab_raw+"], "Everything downstream of raw sources"),
        (["ls", "--select", "tag:daily"],   "Models tagged 'daily'"),
    ]
    for args, description in selectors:
        print(f"\n  > dbt {' '.join(args)}")
        print(f"    [{description}]")
        rc_ls, stdout_ls, stderr_ls = run_dbt(args, timeout=60)
        output = (stdout_ls + "\n" + stderr_ls).strip()
        for line in output.splitlines()[-10:]:
            if line.strip():
                print(f"    {line}")

    print()
    print("KEY TAKEAWAYS:")
    print("  1. ref() = dependency declaration + schema resolution in one macro")
    print("  2. Ephemeral = CTE; no DB object; use for single-consumer intermediates")
    print("  3. dbt resolves execution order from ref() graph — no scripting needed")
    print("  4. `dbt ls --select +model` explores the graph like a filesystem")
    print("  5. Graph operators: +upstream, downstream+, tag:name, source:name+")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
