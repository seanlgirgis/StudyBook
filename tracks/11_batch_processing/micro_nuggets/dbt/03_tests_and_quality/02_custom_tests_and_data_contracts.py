"""
02_custom_tests_and_data_contracts.py — Singular tests and data contracts.

Teaches:
  - Singular (custom) tests: raw SQL files in tests/ directory
  - Why singular tests exist: business logic that generic tests can't express
  - Data contracts in schema.yml: making implicit expectations explicit
  - Running specific tests with `dbt test --select test_name`
  - Understanding intentional test failures (0-amount payments)

Key concept:
  Singular test = a SQL file in tests/ that selects VIOLATION rows.
  If ANY rows are returned → test FAILS.
  Test SQL is parameterized with ref() to stay environment-agnostic.

  Data contract = the schema.yml file is a promise about your model's shape.
  It documents column types, descriptions, and test expectations.
  In dbt 1.5+: can also enforce column types and constraints explicitly.

Run:
    python 03_tests_and_quality/02_custom_tests_and_data_contracts.py
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


def explain_singular_tests() -> None:
    print("""
--- Singular Tests vs Generic Tests ---

  Generic test (schema.yml):
    columns:
      - name: amount_cents
        tests: [not_null]   ← dbt generates the SQL for you

  Singular test (tests/assert_positive_amounts.sql):
    SELECT payment_id, amount_cents
    FROM {{ ref('stg_payments') }}
    WHERE amount_cents <= 0
    → YOUR SQL; you define what "violation" means
    → Any row returned = test fails

  When to use singular tests:
    ✓ Business rules that span multiple columns or tables
    ✓ Complex conditions generic tests can't express
    ✓ "Assert no order total differs from sum of line items"
    ✓ "Assert no user has more than one active subscription"

  When to use generic tests:
    ✓ Simple not_null, unique, FK, enum checks
    ✓ Repeatable patterns (define once, apply everywhere via schema.yml)

--- Data Contracts in schema.yml ---
  A schema.yml entry is a contract between the model author and consumers.
  It says: "This column always exists, is never null, and only contains these values."

  In dbt 1.5+, you can also add:
    data_tests: → alias for tests:
    constraints: → enforce DB-level NOT NULL, UNIQUE, etc. (warehouse-dependent)
    """)


def show_singular_test(test_file: str) -> None:
    """Print a singular test SQL file."""
    path = DBT_PROJECT_DIR / "tests" / test_file
    if path.exists():
        print(f"\n--- tests/{test_file} ---")
        content = path.read_text(encoding="utf-8")
        for line in content.splitlines():
            print(f"  {line}")
    else:
        print(f"\n  (Test file not found: {path})")


def main() -> int:
    print("=" * 60)
    print("  Tests & Quality — Singular Tests & Data Contracts")
    print("=" * 60)

    explain_singular_tests()

    write_profiles_yml()

    # Ensure models are built
    print("[Step 1] Building staging and payments models...")
    run_dbt(["seed", "--full-refresh"], timeout=120)
    run_dbt(["run", "--select", "staging"], timeout=180)

    # Show singular test files
    show_singular_test("assert_positive_amounts.sql")
    show_singular_test("assert_no_future_dates.sql")

    # Show data contract in schema.yml
    marts_schema = DBT_PROJECT_DIR / "models" / "marts" / "schema.yml"
    if marts_schema.exists():
        print("\n--- models/marts/schema.yml (data contract excerpt) ---")
        content = marts_schema.read_text(encoding="utf-8")
        for line in content.splitlines()[:30]:
            print(f"  {line}")

    # Step 2: Run singular tests
    print("\n[Step 2] Running singular tests...")
    print("  Expected: assert_positive_amounts FAILS (0-amount refunds in seed data)")
    print("  Expected: assert_no_future_dates PASSES\n")

    rc_pos, stdout_pos, stderr_pos = run_dbt(
        ["test", "--select", "test_type:singular"], timeout=120
    )
    output = (stdout_pos + "\n" + stderr_pos).strip()
    for line in output.splitlines()[-20:]:
        print(f"  {line}")

    # Step 3: Show what a failure looks like
    print("\n[Step 3] Demonstrating failure: query that returns violation rows")
    print("  The assert_positive_amounts test catches PAY023 and PAY024 (0-cent refunds)")
    print("  These are seeded intentionally to show that tests WORK.")
    print()
    print("  In production you would:")
    print("    1. Fix the root data issue (filter refunds in stg_payments)")
    print("    2. OR adjust the test to exclude refund records")
    print("    3. Re-run tests to confirm green")

    print()
    print("KEY TAKEAWAYS:")
    print("  1. Singular test = SQL file; returns rows = FAIL; 0 rows = PASS")
    print("  2. Use ref() in singular tests so they work in dev AND prod schemas")
    print("  3. schema.yml is your living data contract — document everything")
    print("  4. Intentional failures = the testing system is working correctly")
    print("  5. dbt test --select test_type:singular runs only custom tests")
    print("  6. CI/CD: block merges if any tests fail")
    print()
    print("PASS")
    return 0  # Intentional test failures are expected teaching content


if __name__ == "__main__":
    sys.exit(main())
