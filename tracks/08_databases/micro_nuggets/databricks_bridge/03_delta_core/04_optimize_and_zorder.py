"""
NUGGET 03-04 (Bridge) -- OPTIMIZE and Z-ORDER
==============================================
Covers: small files problem, OPTIMIZE, Z-ORDER, DESCRIBE DETAIL,
        partitioning vs Z-ORDER decision.

Why OPTIMIZE matters:
  Incremental writes (streaming or small batches) create many tiny Parquet
  files (e.g., 1000 x 1 MB files). Queries must open each file separately,
  causing high task overhead. OPTIMIZE rewrites them into 128 MB targets.

OPTIMIZE vs Z-ORDER:
  OPTIMIZE alone = compaction (fewer, larger files)
  OPTIMIZE + ZORDER BY = compaction + data clustering by column(s)

Z-ORDER vs Partitioning:
  PARTITION BY  = physical directory split (low cardinality: date, country)
                  Good for: order_date, region (few distinct values)
  Z-ORDER BY    = within-partition clustering (high cardinality: user_id)
                  Good for: customer_id, product_id (many distinct values)
                  Rule: never Z-ORDER a column you already PARTITION BY

PostgreSQL comparison:
  - CLUSTER TABLE = closest equivalent (one-time physical sort)
  - PostgreSQL has no equivalent of Delta's OPTIMIZE (small-file compaction)
  - BRIN indexes serve similar data-skipping purposes as Z-ORDER

Snowflake comparison:
  - CLUSTER BY = similar to Z-ORDER (automatic micro-partition clustering)
  - Snowflake manages this automatically; Databricks requires manual OPTIMIZE

Usage:
    python 04_optimize_and_zorder.py
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


def check(label: str, condition: bool, detail: str = "") -> None:
    results.append((label, condition))
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status}  {label}{suffix}")


print()
print("=" * 64)
print("  Nugget 03-04: OPTIMIZE and Z-ORDER")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. DESCRIBE DETAIL: baseline file count ───────────────────────────
    # numFiles shows how many Parquet files exist.
    # After many small inserts this number grows; OPTIMIZE reduces it.
    print()
    print("  [1] DESCRIBE DETAIL: sales_orders file count before OPTIMIZE")
    try:
        cur.execute(f"DESCRIBE DETAIL {C}.{S}.sales_orders")
        detail = cur.fetchone()
        if detail:
            # Typical result cols: format, id, name, description, location,
            #   createdAt, lastModified, partitionColumns, numFiles, sizeInBytes, ...
            check("DESCRIBE DETAIL returned", True, f"format={detail[0]}")
            # Try to find numFiles -- column index varies by runtime version
            print(f"         Full detail row (first 8 cols): {list(detail)[:8]}")
        else:
            check("DESCRIBE DETAIL", False, "no row returned")
    except Exception as exc:
        check("DESCRIBE DETAIL baseline", False, str(exc)[:60])

    # ── 2. Simulate many small inserts to create small files ──────────────
    # Each INSERT in a Delta table creates one new Parquet file.
    # In a real pipeline with streaming micro-batches, you get thousands.
    print()
    print("  [2] Simulate small file accumulation (10 single-row INSERTs)")
    insert_ok = 0
    for i in range(10):
        try:
            order_id = 9800 + i
            cur.execute(f"""
                INSERT INTO {C}.{S}.sales_orders VALUES
                ({order_id}, 1, 101, '2024-07-{i+1:02d}', 1, 9.99, 9.99, 'Pending', 'North')
            """)
            insert_ok += 1
        except Exception:
            break
    check("10 single-row INSERTs succeeded", insert_ok == 10,
          f"{insert_ok}/10 inserted")

    # ── 3. OPTIMIZE: compact small files ──────────────────────────────────
    # OPTIMIZE rewrites all files in the table (or partition) into
    # 128 MB target files. This is a background operation in production
    # (often scheduled as a daily job or via OPTIMIZE AUTO on Databricks).
    #
    # PostgreSQL analogy: VACUUM + CLUSTER (but VACUUM is automatic in PG)
    print()
    print("  [3] OPTIMIZE: compact files in sales_orders")
    try:
        cur.execute(f"OPTIMIZE {C}.{S}.sales_orders")
        optimize_result = cur.fetchone()
        check("OPTIMIZE completed", True,
              f"result={list(optimize_result)[:3] if optimize_result else 'no result'}")
    except Exception as exc:
        check("OPTIMIZE", False, str(exc)[:60])

    # ── 4. DESCRIBE DETAIL: file count after OPTIMIZE ─────────────────────
    print()
    print("  [4] DESCRIBE DETAIL: file count after OPTIMIZE")
    try:
        cur.execute(f"DESCRIBE DETAIL {C}.{S}.sales_orders")
        detail_after = cur.fetchone()
        check("DESCRIBE DETAIL after OPTIMIZE", detail_after is not None)
        if detail_after:
            print(f"         After OPTIMIZE: {list(detail_after)[:8]}")
    except Exception as exc:
        check("DESCRIBE DETAIL after", False, str(exc)[:60])

    # ── 5. OPTIMIZE with Z-ORDER ──────────────────────────────────────────
    # Z-ORDER sorts data within each file by the specified columns,
    # enabling data skipping: if a query filters WHERE customer_id = 5,
    # Delta reads only files where customer_id 5 might appear.
    #
    # Z-ORDER is useful for HIGH-cardinality columns (many distinct values).
    # Do NOT Z-ORDER a partition column (already separated into files).
    print()
    print("  [5] OPTIMIZE with ZORDER BY customer_id, product_id")
    try:
        cur.execute(f"""
            OPTIMIZE {C}.{S}.sales_orders
            ZORDER BY (customer_id, product_id)
        """)
        zorder_result = cur.fetchone()
        check("OPTIMIZE ZORDER BY completed", True,
              f"result={list(zorder_result)[:3] if zorder_result else 'no result'}")
    except Exception as exc:
        check("OPTIMIZE ZORDER BY", False, str(exc)[:60])

    # ── 6. Verify OPTIMIZE appears in history ────────────────────────────
    print()
    print("  [6] OPTIMIZE operations visible in DESCRIBE HISTORY")
    cur.execute(f"DESCRIBE HISTORY {C}.{S}.sales_orders LIMIT 5")
    hist = cur.fetchall()
    ops = [r[4] for r in hist] if hist else []
    optimize_in_history = any("OPTIMIZE" in str(op).upper() for op in ops)
    check("OPTIMIZE in DESCRIBE HISTORY", optimize_in_history,
          f"recent ops: {ops[:3]}")

    # ── 7. Cleanup test rows ──────────────────────────────────────────────
    print()
    print("  [7] Cleanup test rows (order_ids 9800-9809)")
    try:
        cur.execute(f"""
            DELETE FROM {C}.{S}.sales_orders
            WHERE order_id BETWEEN 9800 AND 9809
        """)
        check("Cleanup test rows", True)
    except Exception as exc:
        check("Cleanup test rows", False, str(exc)[:60])

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 03-04: {passed}/{total} checks passed")
print()
print("  OPTIMIZE decision guide:")
print("    PARTITION BY  -- low cardinality (date, country, status)")
print("    ZORDER BY     -- high cardinality (customer_id, product_id)")
print("    OPTIMIZE alone -- compaction only (no Z-ORDER)")
print("    Schedule OPTIMIZE daily on active tables")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
