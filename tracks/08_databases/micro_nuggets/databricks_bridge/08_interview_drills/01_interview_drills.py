"""
NUGGET 08-01 (Bridge) -- Interview Drills (Runnable)
=====================================================
Scenario-based interview questions with runnable model answers.
Each scenario prints the question, then executes the SQL answer.

Format:
  Q: <interview question>
  A: <model answer>
  [SQL execution + output]

Usage:
    python 01_interview_drills.py
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


def scenario(num: int, question: str, answer: str) -> None:
    print()
    print(f"  ── Scenario {num} " + "-" * (50 - len(str(num))))
    print(f"  Q: {question}")
    print(f"  A: {answer}")


def check(label: str, condition: bool, detail: str = "") -> None:
    results.append((label, condition))
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status}  {label}{suffix}")


print()
print("=" * 64)
print("  Nugget 08-01: Interview Drills")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── Scenario 1: Find the top customer per region ───────────────────
    scenario(1,
        "Find the customer with the highest total spend in each region.",
        "Use ROW_NUMBER() OVER (PARTITION BY region ORDER BY spend DESC) in a CTE, then WHERE rn=1.")
    cur.execute(f"""
        WITH customer_spend AS (
            SELECT
                c.customer_id,
                c.customer_name,
                o.region,
                SUM(o.total_amount) AS total_spend
            FROM {C}.{S}.sales_orders o
            JOIN {C}.{S}.customers c ON o.customer_id = c.customer_id
            WHERE o.status = 'Shipped'
            GROUP BY c.customer_id, c.customer_name, o.region
        ),
        ranked AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY region ORDER BY total_spend DESC) AS rn
            FROM customer_spend
        )
        SELECT region, customer_name, total_spend
        FROM ranked WHERE rn = 1
        ORDER BY region
    """)
    rows = cur.fetchall()
    check("S1: top customer per region", len(rows) >= 4, f"{len(rows)} regions")
    for r in rows:
        print(f"         {r}")

    # ── Scenario 2: Detect duplicate orders ────────────────────────────
    scenario(2,
        "How do you find duplicate orders where same customer bought same product on same day?",
        "GROUP BY (customer_id, product_id, order_date) HAVING COUNT(*) > 1")
    cur.execute(f"""
        SELECT customer_id, product_id, order_date, COUNT(*) AS occurrences
        FROM {C}.{S}.sales_orders
        GROUP BY customer_id, product_id, order_date
        HAVING COUNT(*) > 1
        ORDER BY occurrences DESC
    """)
    rows = cur.fetchall()
    results.append(("S2: duplicate detection query", True))
    print(f"  PASS  S2: duplicate detection  ({len(rows)} duplicates found -- 0 is valid)")

    # ── Scenario 3: Month-over-month growth ────────────────────────────
    scenario(3,
        "Calculate month-over-month revenue growth using window functions.",
        "Use LAG(revenue, 1) OVER (ORDER BY month) and compute growth pct.")
    cur.execute(f"""
        WITH monthly AS (
            SELECT
                DATE_TRUNC('MONTH', order_date) AS month,
                SUM(total_amount) AS revenue
            FROM {C}.{S}.sales_orders
            WHERE status = 'Shipped'
            GROUP BY DATE_TRUNC('MONTH', order_date)
        )
        SELECT
            month,
            revenue,
            LAG(revenue) OVER (ORDER BY month) AS prev_month_rev,
            ROUND((revenue - LAG(revenue) OVER (ORDER BY month))
                  / LAG(revenue) OVER (ORDER BY month) * 100, 1) AS mom_growth_pct
        FROM monthly
        ORDER BY month
    """)
    rows = cur.fetchall()
    check("S3: MoM growth calculation", len(rows) >= 2, f"{len(rows)} months")
    for r in rows:
        print(f"         {r}")

    # ── Scenario 4: Running total with reset ───────────────────────────
    scenario(4,
        "What is each customer's cumulative spend, and flag when it crosses $500?",
        "Use SUM() OVER (PARTITION BY customer_id ORDER BY order_date ROWS UNBOUNDED PRECEDING).")
    cur.execute(f"""
        SELECT
            customer_id,
            order_date,
            total_amount,
            SUM(total_amount) OVER (
                PARTITION BY customer_id
                ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cumulative_spend,
            CASE WHEN SUM(total_amount) OVER (
                PARTITION BY customer_id
                ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) >= 500 THEN 'HIGH VALUE' ELSE 'STANDARD' END AS tier
        FROM {C}.{S}.sales_orders
        WHERE status = 'Shipped'
        ORDER BY customer_id, order_date
        LIMIT 8
    """)
    rows = cur.fetchall()
    check("S4: running total with tier flag", len(rows) > 0)
    for r in rows:
        print(f"         {r}")

    # ── Scenario 5: Products never ordered ─────────────────────────────
    scenario(5,
        "Find products that have never been ordered (use both LEFT JOIN and NOT EXISTS).",
        "LEFT JOIN: WHERE order_id IS NULL.  NOT EXISTS: WHERE NOT EXISTS (SELECT 1 FROM orders WHERE product_id = p.product_id).")
    cur.execute(f"""
        SELECT p.product_id, p.product_name
        FROM {C}.{S}.products p
        LEFT JOIN {C}.{S}.sales_orders o ON p.product_id = o.product_id
        WHERE o.product_id IS NULL
        ORDER BY p.product_id
    """)
    rows = cur.fetchall()
    results.append(("S5: unordered products (LEFT JOIN)", True))
    print(f"  PASS  S5: unordered products via LEFT JOIN  ({len(rows)} products -- 0 is valid)")

    # ── Scenario 6: Time Travel recovery ───────────────────────────────
    scenario(6,
        "You accidentally deleted rows. How do you recover in Databricks?",
        "Use RESTORE TABLE table TO VERSION AS OF N, where N is the version before the delete (from DESCRIBE HISTORY).")
    cur.execute(f"DESCRIBE HISTORY {C}.{S}.customers LIMIT 3")
    hist = cur.fetchall()
    check("S6: DESCRIBE HISTORY to find restore point",
          len(hist) > 0,
          f"{len(hist)} versions in history")
    print("         RESTORE TABLE nugget_lab.bridge_lab.customers TO VERSION AS OF <N>")
    for r in hist[:2]:
        print(f"         version={r[0]}  op={r[4]}  ts={str(r[1])[:19]}")

    # ── Scenario 7: MERGE upsert vs INSERT ON CONFLICT ─────────────────
    scenario(7,
        "What is the difference between MERGE in Databricks and INSERT ... ON CONFLICT in PostgreSQL?",
        "Both are upsert patterns. MERGE supports INSERT/UPDATE/DELETE in one atomic statement. PostgreSQL ON CONFLICT only handles INSERT + UPDATE. MERGE is more expressive and supported by SQL standard (SQL:2003).")
    # Demonstrate MERGE syntax
    cur.execute(f"""
        SELECT COUNT(*) AS customers_in_lab FROM {C}.{S}.customers
    """)
    row = cur.fetchone()
    check("S7: MERGE vs ON CONFLICT (conceptual)", True,
          f"lab has {row[0]} customers")
    print("         MERGE: INSERT + UPDATE + DELETE in one atomic statement")
    print("         PG ON CONFLICT: INSERT + UPDATE only (no DELETE)")

    # ── Scenario 8: Explain a slow query ────────────────────────────────
    scenario(8,
        "A query joining 3 large tables is slow. What do you check first?",
        "1) EXPLAIN to find Exchange nodes (shuffles). 2) Check if partition keys are used in WHERE. 3) Add BROADCAST hint for small tables. 4) Run OPTIMIZE + ZORDER on join key columns. 5) ANALYZE TABLE to update statistics.")
    cur.execute(f"""
        EXPLAIN SELECT /*+ BROADCAST(p) */
            c.region, p.category, SUM(o.total_amount)
        FROM {C}.{S}.sales_orders o
        JOIN {C}.{S}.customers c ON o.customer_id = c.customer_id
        JOIN {C}.{S}.products  p ON o.product_id  = p.product_id
        GROUP BY c.region, p.category
    """)
    explain_rows = cur.fetchall()
    check("S8: EXPLAIN slow join query", len(explain_rows) > 0)

    # ── Scenario 9: Write idempotent pipeline ───────────────────────────
    scenario(9,
        "How do you ensure a pipeline can be rerun safely without creating duplicates?",
        "1) Use a watermark control table (update only on success). 2) Use MERGE for upserts (not INSERT). 3) For full refresh: DROP + CTAS or INSERT OVERWRITE. 4) Use ROW_NUMBER dedup in Silver layer.")
    check("S9: idempotency pattern (conceptual)", True,
          "covered in 04_de_patterns/04_incremental_and_late_events.py")

    # ── Scenario 10: Delta vs Parquet ──────────────────────────────────
    scenario(10,
        "What does Delta Lake add on top of plain Parquet files?",
        "Delta adds: 1) Transaction log (_delta_log/) for ACID. 2) Schema enforcement. 3) Time Travel (version history). 4) OPTIMIZE/ZORDER for compaction and clustering. 5) MERGE support. 6) CDF (Change Data Feed).")
    cur.execute(f"""
        DESCRIBE DETAIL {C}.{S}.sales_orders
    """)
    detail = cur.fetchone()
    check("S10: Delta vs Parquet (inspect table format)",
          detail is not None and "delta" in str(detail[0]).lower(),
          f"format={detail[0] if detail else 'unknown'}")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 08-01: {passed}/{total} scenarios passed")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
