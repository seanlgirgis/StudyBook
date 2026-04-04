"""
02_selectors_state_artifacts.py — Node selectors, graph operators, and state.

Teaches:
  - Node selector syntax: model names, tags, sources, paths
  - Graph operators: + (upstream/downstream), @ (node + all children + parents)
  - state:modified — only run models changed since last CI run
  - defer: use prod catalog for unchanged models during dev
  - Why selectors are critical for CI/CD cost control

Key concept:
  Without selectors: dbt run rebuilds EVERYTHING every CI run → expensive.
  With selectors: dbt build --select state:modified+ → only changed + downstream.

  state:modified compares the current manifest.json to a "previous" one
  (typically downloaded from the last prod CI run artifact).

Run:
    python 05_operations_and_deploy/02_selectors_state_artifacts.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import (
    run_dbt,
    write_profiles_yml,
)


def explain_selectors() -> None:
    print("""
--- Node Selectors & Graph Operators ---

  Model name:
    dbt run --select stg_customers          → run one model
    dbt run --select staging                → run all models in staging/ folder
    dbt run --select marts.dim_customers    → dot-path notation

  Tags (defined in dbt_project.yml or model config):
    dbt run --select tag:daily              → all models tagged 'daily'
    dbt run --select tag:mart               → all mart-layer models

  Sources:
    dbt run --select source:dbt_lab_raw+    → all models downstream of raw sources
    dbt run --select source:dbt_lab_raw.raw_customers+  → specific table + downstream

  Graph operators (prepend/append to model name):
    +stg_customers       → stg_customers AND all its ancestors (upstream)
    stg_customers+       → stg_customers AND all its descendants (downstream)
    +stg_customers+      → full lineage: ancestors + model + descendants
    @stg_customers       → stg_customers + all downstream + their OTHER parents

  State-based selectors (CI/CD power feature):
    state:modified       → models whose SQL/config changed vs state manifest
    state:modified+      → changed models + all their downstream dependents
    state:new            → models that didn't exist in the previous manifest
    state:modified.body  → only SQL body changed (not config/tests)

--- defer ---
  dbt run --select my_model --defer --state ./path/to/prod_manifest/
    → For unchanged upstream deps: use PROD relations instead of rebuilding
    → Saves dev compute: you only rebuild the model you're working on
    → Requires state manifest from prod run
    """)


def run_selector_demo(args: list[str], description: str) -> None:
    """Run a dbt ls command and print results."""
    print(f"\n  > dbt {' '.join(args)}")
    print(f"    [{description}]")
    rc, stdout, stderr = run_dbt(args, timeout=60)
    output = (stdout + "\n" + stderr).strip()
    lines = [l for l in output.splitlines() if l.strip()]
    # Filter to just the model names (skip dbt preamble lines)
    model_lines = [l for l in lines if "." in l and l.strip().startswith("dbt_lab")]
    if model_lines:
        for line in model_lines[:15]:
            print(f"    {line.strip()}")
    else:
        for line in lines[-8:]:
            print(f"    {line.strip()}")


def main() -> int:
    print("=" * 60)
    print("  Operations — Selectors, State & Artifacts")
    print("=" * 60)

    explain_selectors()

    write_profiles_yml()

    # Ensure models are built first
    print("[Step 1] Ensuring models are built for selector demos...")
    run_dbt(["build"], timeout=300)

    # Step 2: Selector demonstrations
    print("\n[Step 2] Selector Demonstrations with `dbt ls`:")

    run_selector_demo(
        ["ls", "--select", "tag:daily"],
        "Models tagged 'daily' (dim_customers, fct_orders)"
    )
    run_selector_demo(
        ["ls", "--select", "+dim_customers"],
        "dim_customers and all UPSTREAM ancestors"
    )
    run_selector_demo(
        ["ls", "--select", "fct_orders+"],
        "fct_orders and all DOWNSTREAM dependents"
    )
    run_selector_demo(
        ["ls", "--select", "source:dbt_lab_raw+"],
        "Everything downstream of raw sources"
    )
    run_selector_demo(
        ["ls", "--select", "staging"],
        "All models in the staging/ folder"
    )
    run_selector_demo(
        ["ls", "--select", "tag:mart"],
        "All mart-layer models"
    )

    # Step 3: Explain state:modified workflow
    print("\n[Step 3] state:modified — CI/CD cost optimization")
    print("""
  Typical CI/CD pipeline with state:
    Step 1: Download manifest.json from last successful prod run
            (stored as artifact in GitHub Actions / dbt Cloud)

    Step 2: Run only changed models + downstream:
            dbt build --select state:modified+ --state ./prod_manifest/

    Step 3: Upload new manifest.json as artifact for next run

  This means: if you change only stg_orders.sql, dbt will:
    ✓ Rebuild stg_orders
    ✓ Rebuild int_orders_with_customers (depends on stg_orders)
    ✓ Rebuild fct_orders (depends on int_)
    ✗ Skip stg_customers, stg_events, stg_payments, stg_products
    ✗ Skip dim_customers (no dependency on stg_orders)

  Huge cost saving on large projects with hundreds of models.
    """)

    # Step 4: Explain defer
    print("\n[Step 4] defer — dev efficiency")
    print("""
  dbt run --select fct_orders --defer --state ./prod_manifest/

  Without --defer:
    dbt runs ALL upstream models (stg_customers, stg_orders, int_orders...)
    even if you only changed fct_orders.sql

  With --defer:
    dbt sees that stg_customers etc. are UNCHANGED vs prod manifest
    → Uses the PROD schemas for unchanged models instead of rebuilding
    → You only build fct_orders in dev

  Requires: prod manifest.json in ./prod_manifest/
  Requires: dev has READ access to prod schemas (or use --favor-state)
    """)

    print()
    print("KEY TAKEAWAYS:")
    print("  1. Selectors: model name, tag:name, source:name+, path/to/folder")
    print("  2. + prefix = upstream ancestors; + suffix = downstream descendants")
    print("  3. state:modified+ = only changed models + their downstream (CI gold standard)")
    print("  4. defer = use prod schemas for unchanged deps in dev (cost saving)")
    print("  5. Always store manifest.json as CI artifact for next run's state compare")
    print("  6. `dbt ls` is dry-run selector testing — always check before `dbt run`")
    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
