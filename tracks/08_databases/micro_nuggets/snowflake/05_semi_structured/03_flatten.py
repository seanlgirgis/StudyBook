"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-03 · LATERAL FLATTEN — Explode Arrays into Rows                   ║
║  Turn one JSON document with an array into multiple relational rows.         ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Shows FLATTEN() — Snowflake's table function that "explodes" a VARIANT array
into one row per element. Essential for analysing line items, tags, events
within events, or any repeated nested structure.

CONCEPTS
────────
The problem FLATTEN solves:
  You have a purchase event whose payload contains an array of line items.
  In relational SQL you can't GROUP BY or JOIN on array elements directly.
  FLATTEN unpacks the array so each item becomes its own row.

  Before FLATTEN:
    order_id=ORD-8821  items=[{Widget A, 29.99}, {Widget B, 59.98}]

  After FLATTEN on items:
    order_id=ORD-8821  item=Widget A  price=29.99
    order_id=ORD-8821  item=Widget B  price=59.98

Syntax:
    SELECT ...
    FROM   my_table,
           LATERAL FLATTEN(INPUT => my_table.col:array_field) f

  LATERAL means "run FLATTEN once per row of my_table using that row's data".
  f (or any alias) is the output table of FLATTEN.

FLATTEN output columns (always available as f.<col>):
  f.VALUE   — the array element as VARIANT (the whole item)
  f.INDEX   — 0-based position in the array
  f.KEY     — for OBJECT flattening: the key name
  f.PATH    — full dot-notation path to this element
  f.THIS    — the input array/object that was flattened
  f.SEQ     — sequence number for ordering (useful with nested FLATTEN)

FLATTEN modes (RECURSIVE and OUTER):
  Default (RECURSIVE => FALSE):
    Flattens one level deep only.
  RECURSIVE => TRUE:
    Descends into nested arrays/objects automatically.
    Use carefully — can produce huge result sets on deeply nested data.
  OUTER => TRUE:
    Like LEFT JOIN — rows with NULL or empty arrays are preserved.
    Without OUTER, rows whose array is empty or NULL are silently dropped.

Real DE use cases:
  - Line items from e-commerce orders
  - Tags/labels arrays on infrastructure resources
  - Skills lists on job profiles
  - Sensor readings bundled in one event (IoT)
  - Nested log entries from distributed tracing

FLATTEN on OBJECT (not just arrays):
  FLATTEN can also expand a JSON OBJECT into key-value rows:
    FLATTEN(INPUT => col:metadata)  →  one row per key in the object
  Useful for wide semi-structured objects with unknown keys.

USAGE
─────
    python 03_flatten.py

EXPECTED OUTPUT
───────────────
    ── LATERAL FLATTEN ───────────────────────────

      ── 1. Explode purchase line items ────────────────
        ORDER_ID       IDX  PRODUCT       QTY   PRICE
        -------------- ---- ------------- ----  ------
        ORD-8821         0  Widget A         1   29.99
        ORD-8821         1  Widget B         2   59.98

      ── 2. Aggregate after FLATTEN ────────────────────
        ORDER_ID       TOTAL_ITEMS  LINE_REVENUE
        -------------- ----------- ------------
        ORD-8821                 2        89.97

      ── 3. FLATTEN an OBJECT (key-value pairs) ────────
        KEY                VALUE
        ------------------ -----------
        browser            Chrome
        duration_ms        1240
        page               /home
        referrer           https://google.com
        user_id            42

      ── 4. OUTER => TRUE (keep rows with no array) ────
        EVENT_TYPE   ITEM_NAME
        ------------ ---------------------
        page_view    (no items — OUTER kept this row)
        purchase     Widget A
        purchase     Widget B
        error        (no items — OUTER kept this row)
        page_view    (no items — OUTER kept this row)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── LATERAL FLATTEN ───────────────────────────")

with conn.cursor() as cur:

    # Guard: ensure events table exists
    cur.execute("SHOW TABLES LIKE 'NUGGET_EVENTS'")
    if not cur.fetchone():
        print("\n  ERROR: NUGGET_EVENTS not found.")
        print("  Run 05_semi_structured/01_variant_column.py first.\n")
        conn.close()
        sys.exit(1)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. FLATTEN an array — explode purchase line items
    #
    #    The comma before LATERAL FLATTEN is a cross-join.
    #    LATERAL allows the FLATTEN to reference e.payload from the same row.
    #    f.VALUE is the entire array element as VARIANT.
    #    f.INDEX is 0-based position.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 1. Explode purchase line items ────────────────")
    cur.execute("""
        SELECT
            e.payload:order_id::VARCHAR   AS order_id,
            f.index                       AS idx,
            f.value:name::VARCHAR         AS product,
            f.value:qty::NUMBER           AS qty,
            f.value:price::FLOAT          AS price
        FROM   NUGGET_EVENTS e,
               LATERAL FLATTEN(INPUT => e.payload:items) f
        WHERE  e.event_type = 'purchase'
        ORDER  BY order_id, f.index
    """)
    rows = cur.fetchall()
    print(f"    {'ORDER_ID':<14}  {'IDX':>3}  {'PRODUCT':<15}  {'QTY':>4}  {'PRICE':>6}")
    print(f"    {'─'*14}  {'─'*3}  {'─'*15}  {'─'*4}  {'─'*6}")
    for order_id, idx, product, qty, price in rows:
        print(f"    {str(order_id):<14}  {idx:>3}  {str(product):<15}  {qty:>4}  {price:>6.2f}")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Aggregate AFTER FLATTEN
    #    Once exploded into rows, use normal GROUP BY / SUM / COUNT.
    #    This pattern — FLATTEN then aggregate — is the standard recipe
    #    for analysing nested arrays in Snowflake.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 2. Aggregate after FLATTEN ────────────────────")
    cur.execute("""
        SELECT
            e.payload:order_id::VARCHAR          AS order_id,
            COUNT(*)                             AS total_items,
            ROUND(SUM(f.value:price::FLOAT
                      * f.value:qty::NUMBER), 2) AS line_revenue
        FROM   NUGGET_EVENTS e,
               LATERAL FLATTEN(INPUT => e.payload:items) f
        WHERE  e.event_type = 'purchase'
        GROUP  BY order_id
    """)
    rows = cur.fetchall()
    print(f"    {'ORDER_ID':<14}  {'TOTAL_ITEMS':>11}  LINE_REVENUE")
    print(f"    {'─'*14}  {'─'*11}  {'─'*12}")
    for order_id, cnt, rev in rows:
        print(f"    {str(order_id):<14}  {cnt:>11}  {rev:>12.2f}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. FLATTEN an OBJECT — produces key/value rows
    #    When you FLATTEN an OBJECT (not an array), each top-level key
    #    becomes a row.  f.KEY = the key name, f.VALUE = the value.
    #    Use case: wide JSON objects with unknown or varying keys.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 3. FLATTEN an OBJECT (key-value pairs) ────────")
    cur.execute("""
        SELECT
            f.key                      AS key,
            f.value::VARCHAR           AS value
        FROM   NUGGET_EVENTS e,
               LATERAL FLATTEN(INPUT => e.payload) f
        WHERE  e.event_id = 1          -- the first page_view event
        ORDER  BY f.key
    """)
    rows = cur.fetchall()
    print(f"    {'KEY':<20}  VALUE")
    print(f"    {'─'*20}  {'─'*20}")
    for key, value in rows:
        # Strip surrounding quotes Snowflake adds on VARCHAR VARIANT values
        clean_val = str(value).strip('"')
        print(f"    {key:<20}  {clean_val}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. OUTER => TRUE — keep rows even when the array is NULL or empty
    #    Default FLATTEN drops rows with no matching array (inner join behaviour).
    #    OUTER => TRUE preserves them (left join behaviour).
    #    Crucial when you want ALL events in your result, not just purchases.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 4. OUTER => TRUE (keep rows with no array) ────")
    cur.execute("""
        SELECT
            e.event_type,
            COALESCE(
                f.value:name::VARCHAR,
                '(no items — OUTER kept this row)'
            ) AS item_name
        FROM   NUGGET_EVENTS e,
               LATERAL FLATTEN(INPUT => e.payload:items, OUTER => TRUE) f
        ORDER  BY e.event_id, f.index
    """)
    rows = cur.fetchall()
    print(f"    {'EVENT_TYPE':<12}  ITEM_NAME")
    print(f"    {'─'*12}  {'─'*36}")
    for etype, item_name in rows:
        print(f"    {etype:<12}  {item_name}")

conn.close()
print()
