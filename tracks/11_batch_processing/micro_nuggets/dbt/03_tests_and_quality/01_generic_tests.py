"""
01_generic_tests.py — dbt Generic (Schema) Tests.

Teaches:
  - Four built-in generic tests: not_null, unique, relationships, accepted_values
  - How tests are defined in schema.yml (data contracts)
  - How dbt generates test SQL from schema.yml
  - Parsing test results from run_results.json
  - Why tests fail (intentional duplicates in seed data)

Key concept:
  dbt tests are just SELECT queries.
  A test FAILS if the query returns ANY rows (rows = violations).
  A test PASSES if the query returns 0 rows.

  Generic tests are defined in schema.yml and auto-compiled by dbt.
  Singular tests are raw SQL files in tests/ — more on those in nugget 02.

Run:
    python 03_tests_and_quality/01_generic_tests.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import (
    DBT_PROJECT_DIR,
    run_dbt,
    write_profiles_yml,
)


def explain_generic_tests() -> None:
    print("""
--- dbt Generic Tests ---

  Defined in schema.yml under columns: or models: blocks.
  dbt auto-generates a SELECT query for each test.

  not_null:
    SELECT count(*) FROM model WHERE column IS NULL
    → Fails if any NULLs exist in that column

  unique:
    SELECT column, count(*) FROM model GROUP BY column HAVING count(*) > 1
    → Fails if any duplicate values exist

  relationships:
    SELECT a.fk FROM child_model a
    LEFT JOIN parent_model b ON a.fk = b.pk
    WHERE b.pk IS NULL
    → Fails if any FK values don't exist in parent table

  accepted_values:
    SELECT column FROM model WHERE column NOT IN ('v1','v2',...)
    → Fails if any value outside the allowed set exists

  In schema.yml:
    columns:
      - name: tier
        tests:
          - accepted_values:
              values: ['bronze', 'silver', 'gold', 'platinum']
    """)


def parse_test_results() -> list[dict]:
    """Read run_results.json from the target/ dir and return test results."""
    results_path = DBT_PROJECT_DIR / "target" / "run_results.json"
    if not results_path.exists():
        return []
    try:
        data = json.loads(results_path.read_text(encoding="utf-8"))
        return data.get("results", [])
    except Exception:
        return []


def show_test_results(results: list[dict]) -> None:
    """Print a formatted table of test results."""
    if not results:
        print("  (No test results found in target/run_results.json)")
        return

    tests = [r for r in results if r.get("unique_id", "").startswith("test.")]
    if not tests:
        print("  (No test nodes in run_results.json — showing all results)")
        tests = results

    print(f"\n  {'STATUS':6} | {'FAILURES':8} | {'TEST NAME'}")
    print(f"  {'-'*6}-+-{'-'*8}-+-{'-'*50}")
    for r in tests:
        status = r.get("status", "?")
        failures = r.get("failures", 0) or 0
        name = r.get("unique_id", "").replace("test.dbt_lab.", "").replace("test.", "")
        # Truncate long names
        if len(name) > 60:
            name = name[:57] + "..."
        icon = "PASS" if status == "pass" else "FAIL"
        print(f"  {icon:6} | {failures:8} | {name}")


def show_test_sql(test_name_fragment: str) -> None:
    """Find and display compiled SQL for a test."""
    compiled_tests_dir = (
        DBT_PROJECT_DIR / "target" / "compiled" / "dbt_lab" / "models"
    )
    # Walk all compiled files looking for the test
    for path in compiled_tests_dir.rglob("*.sql"):
        if test_name_fragment.lower() in path.stem.lower():
            print(f"\n--- Compiled SQL for test: {path.stem} ---")
            content = path.read_text(encoding="utf-8")
            for line in content.splitlines()[:20]:
                print(f"  {line}")
            return
    print(f"\n  (Could not find compiled SQL for: {test_name_fragment})")


def main() -> int:
    print("=" * 60)
    print("  Tests & Quality — Generic Tests")
    print("=" * 60)

    explain_generic_tests()

    write_profiles_yml()

    # Ensure staging exists
    print("[Step 1] Ensuring staging layer is built...")
    run_dbt(["seed", "--full-refresh"], timeout=120)
    run_dbt(["run", "--select", "staging"], timeout=180)

    # Show schema.yml tests definition
    schema_path = DBT_PROJECT_DIR / "models" / "staging" / "schema.yml"
    if schema_path.exists():
        print("\n--- schema.yml (test definitions) ---")
        content = schema_path.read_text(encoding="utf-8")
        # Show models section only
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "models:" in line:
                for l in lines[i:i+50]:
                    print(f"  {l}")
                break

    # Step 2: Run tests on staging
    print("\n[Step 2] Running `dbt test --select staging`...")
    print("  (Expect some failures: duplicate email in raw_customers is intentional)\n")
    rc, stdout, stderr = run_dbt(["test", "--select", "staging"], timeout=180)
    output = (stdout + "\n" + stderr).strip()
    for line in output.splitlines()[-25:]:
        print(f"  {line}")

    # Step 3: Parse and display results
    print("\n[Step 3] Parsed Test Results:")
    results = parse_test_results()
    show_test_results(results)

    # Step 4: Show compiled SQL for one test
    print("\n[Step 4] Compiled SQL for a test (shows what dbt actually runs):")
    show_test_sql("unique")

    print()
    print("KEY TAKEAWAYS:")
    print("  1. Tests = SELECT queries that must return 0 rows to pass")
    print("  2. not_null, unique, relationships, accepted_values = 4 built-in generics")
    print("  3. schema.yml is your data contract — tests enforce it at run time")
    print("  4. Intentional failures: duplicate email in raw_customers is seeded")
    print("     to demonstrate that tests CATCH real data quality issues")
    print("  5. Use `dbt test --select model_name` to test one model at a time")
    print("  6. CI/CD pipeline: run `dbt test` after every `dbt run`")
    print()
    print("PASS")
    return 0  # Don't fail even if some tests fail — this is intentional teaching


if __name__ == "__main__":
    sys.exit(main())
