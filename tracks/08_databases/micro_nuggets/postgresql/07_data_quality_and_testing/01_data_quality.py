"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-01 · Data Quality Checks                                          ║
║  Testing your data for nulls, duplicates, and integrity violations.          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates data quality assertions — the kind of checks every DE pipeline
should run before loading data downstream.

CONCEPTS
────────
Data quality dimensions:
  1. Completeness: no unexpected NULLs in required columns.
  2. Uniqueness: no duplicate primary keys or business keys.
  3. Referential integrity: all FKs point to valid parent rows.
  4. Validity: values conform to expected ranges/formats.
  5. Consistency: related fields agree (e.g., line_total = qty * price).

Pattern: run checks, count violations, PASS/FAIL per check.
This is the foundation of data testing frameworks like Great Expectations,
dbt tests, and Soda Core.

USAGE
─────
    python 01_data_quality.py

EXPECTED OUTPUT
───────────────
    ── Data Quality Checks ─────────────────────────────────

      Check                              Result   Details
      ---------------------------------  ------   -------------------------
      [✓] customers: no null emails      PASS     0 violations
      [✓] orders: valid FK refs          PASS     0 orphaned orders
      [✓] order_items: line_total match  PASS     0 mismatches
      ...
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Data Quality Checks ─────────────────────────────────")

checks = []

def run_check(name, query, params=()):
    """Run a data quality check. PASS if result is 0."""
    with conn.cursor() as cur:
        cur.execute(query, params)
        violations = cur.fetchone()[0]
    status = "PASS" if violations == 0 else "FAIL"
    icon = "✓" if violations == 0 else "✗"
    checks.append((name, status, violations))
    print(f"    [{icon}] {name:<35} {status:<6} {violations} violations")

print(f"\n  {'Check':<38} {'Result':<7} {'Details'}")
print(f"  {'-'*38} {'-'*7} {'-'*25}")

# 1. Completeness — no null emails in customers
run_check("customers: no null emails",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.customers WHERE email IS NULL")

# 2. Uniqueness — no duplicate customer emails
run_check("customers: unique emails",
    f"SELECT COUNT(*) - COUNT(DISTINCT email) FROM {LAB_SCHEMA}.customers")

# 3. Referential integrity — all orders reference valid customers
run_check("orders: valid FK refs",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.orders o "
    f"LEFT JOIN {LAB_SCHEMA}.customers c ON o.customer_id = c.customer_id "
    f"WHERE c.customer_id IS NULL")

# 4. Validity — all order statuses are valid
run_check("orders: valid statuses",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.orders "
    f"WHERE status NOT IN ('pending','confirmed','shipped','delivered','cancelled')")

# 5. Consistency — line_total matches quantity * unit_price
run_check("order_items: line_total = qty*price",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.order_items "
    f"WHERE ABS(line_total - quantity * unit_price) > 0.01")

# 6. Validity — no negative prices
run_check("products: positive prices",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.products WHERE price <= 0 OR cost <= 0")

# 7. Validity — no negative quantities
run_check("order_items: positive quantities",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.order_items WHERE quantity <= 0")

# 8. Completeness — all orders have a total_amount (unless cancelled)
run_check("orders: non-null totals",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.orders "
    f"WHERE total_amount IS NULL AND status != 'cancelled'")

# 9. Referential integrity — all order_items reference valid products
run_check("order_items: valid product FKs",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.order_items oi "
    f"LEFT JOIN {LAB_SCHEMA}.products p ON oi.product_id = p.product_id "
    f"WHERE p.product_id IS NULL")

# 10. Validity — event types are known types
run_check("events: valid event types",
    f"SELECT COUNT(*) FROM {LAB_SCHEMA}.events "
    f"WHERE event_type NOT IN ('page_view','product_view','add_to_cart','checkout','purchase')")

# Summary
passed = sum(1 for _, s, _ in checks if s == "PASS")
failed = sum(1 for _, s, _ in checks if s == "FAIL")
print(f"\n  Summary: {passed} passed, {failed} failed, {len(checks)} total")

conn.close()
print()
