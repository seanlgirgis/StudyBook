"""
NUGGET 07-01 (Bridge) -- Data Quality Checks
=============================================
Covers: null checks, duplicate checks, referential integrity,
        range validation, assertion-style test outputs,
        data quality results table.

Why data quality checks in DE:
  Bad data flows downstream and corrupts reports, ML features, and
  business decisions. Quality gates catch issues at ingestion time.
  This is the foundation of the "Silver layer" validation step.

PostgreSQL comparison:
  - Same SQL patterns (COUNT, IS NULL, GROUP BY HAVING)
  - PostgreSQL CHECK constraints enforce quality at write time
  - Delta: no CHECK constraints -- enforce via pipeline logic or
    Delta Constraints (Runtime 9.0+)

Usage:
    python 01_data_quality_checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

C = LAB_CATALOG
S = LAB_SCHEMA
DIVIDER = "-" * 64
results = []
quality_results = []


def check(label: str, condition: bool, detail: str = "") -> None:
    results.append((label, condition))
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status}  {label}{suffix}")


def dq_check(label: str, passed: bool, detail: str, table: str = "sales_orders") -> None:
    """Record a data quality check result."""
    quality_results.append({
        "check_name": label,
        "table": table,
        "passed": passed,
        "detail": detail,
    })
    status = "PASS" if passed else "FAIL"
    print(f"  DQ [{status}]  {label}  -- {detail}")


print()
print("=" * 64)
print("  Nugget 07-01: Data Quality Checks")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Null checks ────────────────────────────────────────────────────
    # Critical columns must not be NULL.
    # NULLs in join keys cause silent data loss (rows don't match).
    print()
    print("  [1] Null checks: critical columns in sales_orders")
    null_checks = [
        ("order_id",    "NOT NULL primary key"),
        ("customer_id", "NOT NULL FK to customers"),
        ("product_id",  "NOT NULL FK to products"),
        ("order_date",  "NOT NULL required for time partitioning"),
        ("total_amount","NOT NULL required for revenue metrics"),
    ]
    for col, reason in null_checks:
        cur.execute(f"""
            SELECT COUNT(*) FROM {C}.{S}.sales_orders WHERE {col} IS NULL
        """)
        null_count = cur.fetchone()[0]
        passed = null_count == 0
        dq_check(f"no_nulls_{col}", passed,
                 f"null_count={null_count}  ({reason})")

    # ── 2. Duplicate primary key check ───────────────────────────────────
    print()
    print("  [2] Duplicate check: order_id uniqueness")
    cur.execute(f"""
        SELECT COUNT(*) AS dup_count FROM (
            SELECT order_id
            FROM {C}.{S}.sales_orders
            GROUP BY order_id
            HAVING COUNT(*) > 1
        )
    """)
    dup_count = cur.fetchone()[0]
    dq_check("no_duplicate_order_ids",
             dup_count == 0,
             f"duplicate groups={dup_count}")

    # ── 3. Referential integrity: FK checks ───────────────────────────────
    # Every customer_id in sales_orders must exist in customers.
    # Delta has no FK constraints -- enforce via pipeline checks.
    print()
    print("  [3] Referential integrity: FK checks")
    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.sales_orders o
        LEFT JOIN {C}.{S}.customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)
    orphan_orders = cur.fetchone()[0]
    dq_check("fk_customer_id_valid",
             orphan_orders == 0,
             f"orphan orders={orphan_orders}")

    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.sales_orders o
        LEFT JOIN {C}.{S}.products p ON o.product_id = p.product_id
        WHERE p.product_id IS NULL
    """)
    orphan_products = cur.fetchone()[0]
    dq_check("fk_product_id_valid",
             orphan_products == 0,
             f"orphan orders={orphan_products}")

    # ── 4. Range validation: business rules ───────────────────────────────
    print()
    print("  [4] Range checks: business rule validation")

    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.sales_orders
        WHERE total_amount <= 0
    """)
    neg_amounts = cur.fetchone()[0]
    dq_check("total_amount_positive",
             neg_amounts == 0,
             f"non-positive amounts={neg_amounts}")

    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.sales_orders
        WHERE quantity <= 0
    """)
    neg_qty = cur.fetchone()[0]
    dq_check("quantity_positive",
             neg_qty == 0,
             f"non-positive quantities={neg_qty}")

    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.sales_orders
        WHERE order_date > CURRENT_DATE()
    """)
    future_orders = cur.fetchone()[0]
    dq_check("order_date_not_future",
             future_orders == 0,
             f"future-dated orders={future_orders}")

    # ── 5. Value set validation: status column ────────────────────────────
    print()
    print("  [5] Value set check: status must be in allowed set")
    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.sales_orders
        WHERE status NOT IN ('Shipped', 'Pending', 'Cancelled', 'Returned')
    """)
    invalid_status = cur.fetchone()[0]
    dq_check("status_valid_values",
             invalid_status == 0,
             f"invalid status rows={invalid_status}")

    # ── 6. Completeness check: expected row count ─────────────────────────
    print()
    print("  [6] Completeness: minimum expected row counts")
    for tbl, min_rows in [("customers", 15), ("products", 10), ("sales_orders", 40)]:
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.{tbl}")
        actual = cur.fetchone()[0]
        dq_check(f"row_count_minimum_{tbl}",
                 actual >= min_rows,
                 f"actual={actual}, min={min_rows}",
                 table=tbl)

    # ── 7. Cross-column consistency ───────────────────────────────────────
    print()
    print("  [7] Cross-column: total_amount = quantity * unit_price")
    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.sales_orders
        WHERE ABS(total_amount - (quantity * unit_price)) > 0.01
    """)
    inconsistent = cur.fetchone()[0]
    dq_check("total_amount_consistent_with_qty_price",
             inconsistent == 0,
             f"inconsistent rows={inconsistent}")

    # ── 8. Write quality results to Delta table ───────────────────────────
    print()
    print("  [8] Persist quality results to data_quality_results table")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.data_quality_results")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.data_quality_results (
                run_ts      TIMESTAMP,
                table_name  STRING,
                check_name  STRING,
                passed      BOOLEAN,
                detail      STRING
            )
            USING DELTA
            COMMENT 'Data quality check results log -- bridge lab'
        """)
        for qr in quality_results:
            passed_str = "true" if qr["passed"] else "false"
            detail_safe = qr["detail"].replace("'", "''")
            cur.execute(f"""
                INSERT INTO {C}.{S}.data_quality_results VALUES
                (CURRENT_TIMESTAMP(), '{qr["table"]}', '{qr["check_name"]}',
                 {passed_str}, '{detail_safe}')
            """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.data_quality_results")
        stored = cur.fetchone()[0]
        check("Quality results persisted", stored == len(quality_results),
              f"{stored}/{len(quality_results)} checks stored")
    except Exception as exc:
        check("Persist quality results", False, str(exc)[:60])

    # ── 9. Quality summary ────────────────────────────────────────────────
    print()
    print("  [9] Quality summary")
    dq_passed = sum(1 for qr in quality_results if qr["passed"])
    dq_failed = len(quality_results) - dq_passed
    check("All DQ checks passed",
          dq_failed == 0,
          f"passed={dq_passed}, failed={dq_failed}")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
dq_pass = sum(1 for qr in quality_results if qr["passed"])
print(f"  Nugget 07-01: {passed}/{total} framework checks passed")
print(f"  Data quality: {dq_pass}/{len(quality_results)} DQ assertions passed")
print(DIVIDER)
print()
if passed < total or dq_pass < len(quality_results):
    sys.exit(1)
