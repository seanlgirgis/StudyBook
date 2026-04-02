"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-02 · Querying JSON with Colon Notation                            ║
║  Navigate into nested documents like a path — no joins, no pivots.          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Shows every way to extract values from a VARIANT column:
colon notation, dot notation, bracket notation, casting, and IS NULL checks.
Depends on NUGGET_EVENTS created in nugget 05-01.

CONCEPTS
────────
Colon path notation  (Snowflake-specific, most common)
  col:key             — top-level key
  col:key:nested      — nested key (chain colons)
  col:array[0]        — first element of a JSON array
  col:array[0]:name   — field inside the first array element

  Example:
    payload:user_id                    → 42
    payload:items[0]:price             → 29.99
    payload:items[0]:name              → "Widget A"  (quoted — still VARCHAR)

Dot notation  (SQL-standard style, same result)
  col["key"]          — equivalent to col:key
  col["key"]["sub"]   — equivalent to col:key:sub

Why results come back quoted:
  By default, a path expression returns a VARIANT sub-value.
  Numbers:  returned as a VARIANT INTEGER
  Strings:  returned as a VARIANT VARCHAR — displayed with surrounding quotes
  Cast to a SQL type to strip the quotes and get a proper typed value:
    payload:user_id::NUMBER          → 42    (NUMBER)
    payload:items[0]:name::VARCHAR   → Widget A  (no quotes)

Casting VARIANT to SQL types:
  ::VARCHAR     — text
  ::NUMBER      — integer or decimal
  ::FLOAT       — floating point
  ::BOOLEAN     — true/false
  ::DATE        — date
  ::TIMESTAMP_NTZ — datetime
  ::ARRAY       — array sub-type (use with FLATTEN — nugget 05-03)
  ::OBJECT      — sub-document

NULL vs missing key:
  If a key doesn't exist in a document, the path expression returns NULL.
  This lets you write one query across documents with different shapes.
  Use IS NULL to detect missing fields:
    WHERE payload:severity IS NOT NULL   ← only error events

TRY_CAST():
  Like ::cast but returns NULL on failure instead of raising an error.
  Useful when a field sometimes contains a number, sometimes a string:
    TRY_CAST(payload:price AS FLOAT)

GET() and GET_PATH():
  GET(col, 'key')              — same as col:key
  GET_PATH(col, 'a.b.c')      — dot-delimited path string
  Useful in dynamic SQL where the path is a variable.

USAGE
─────
    python 02_query_json.py

EXPECTED OUTPUT
───────────────
    ── Querying JSON with Colon Notation ────────

      ── 1. Simple field extraction ────────────────────
        ID  TYPE        USER_ID  PAGE / ENDPOINT
        --- ----------- -------- ------------------
          1 page_view        42  /home
          2 purchase         42  (null — no page field)
          3 error          null  /api/checkout
          4 page_view        99  /pricing

      ── 2. Typed extraction (:: cast) ─────────────────
        ORDER_ID      TOTAL   ITEM_COUNT
        ------------- ------- ----------
        ORD-8821       89.97           2

      ── 3. Nested array element access ────────────────
        FIRST_ITEM_NAME   FIRST_ITEM_PRICE
        ----------------- ----------------
        Widget A                     29.99

      ── 4. Cross-event query (mixed schemas) ──────────
        TYPE        SEVERITY   ERROR_CODE   DURATION_MS
        ----------- ---------- ------------ -----------
        page_view   null       null                1240
        purchase    null       null                null
        error       HIGH            500            null
        page_view   null       null                 890

      ── 5. Filter by nested field ─────────────────────
        High-severity events: 1 row(s)
          ID=3  code=500  message=Internal Server Error
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── Querying JSON with Colon Notation ────────")

with conn.cursor() as cur:

    # Guard: ensure events table exists from nugget 05-01
    cur.execute("SHOW TABLES LIKE 'NUGGET_EVENTS'")
    if not cur.fetchone():
        print("\n  ERROR: NUGGET_EVENTS not found.")
        print("  Run 05_semi_structured/01_variant_column.py first.\n")
        conn.close()
        sys.exit(1)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Simple field extraction with colon notation
    #    payload:user_id   — returns VARIANT (displayed without quotes for ints)
    #    payload:page      — returns VARIANT VARCHAR (shown with quotes)
    #    COALESCE handles missing fields: page_view has :page, error has :endpoint
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 1. Simple field extraction ────────────────────")
    cur.execute("""
        SELECT
            event_id,
            event_type,
            payload:user_id                                    AS user_id_variant,
            COALESCE(payload:page::VARCHAR, payload:endpoint::VARCHAR)
                                                               AS page_or_endpoint
        FROM NUGGET_EVENTS
        ORDER BY event_id
    """)
    rows = cur.fetchall()
    print(f"    {'ID':>3}  {'TYPE':<11}  {'USER_ID':>7}  PAGE / ENDPOINT")
    print(f"    {'─'*3}  {'─'*11}  {'─'*7}  {'─'*18}")
    for eid, etype, uid, page in rows:
        print(f"    {eid:>3}  {etype:<11}  {str(uid or 'null'):>7}  {page or '(null)'}")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Cast to proper SQL types with ::
    #    Without cast: payload:total returns VARIANT "89.97" — a VARIANT REAL
    #    With ::FLOAT : returns 89.97  — a true SQL FLOAT you can SUM/AVG
    #
    #    ARRAY_SIZE() counts elements in a JSON array field.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 2. Typed extraction (:: cast) ─────────────────")
    cur.execute("""
        SELECT
            payload:order_id::VARCHAR    AS order_id,
            payload:total::FLOAT         AS total,
            ARRAY_SIZE(payload:items)    AS item_count
        FROM NUGGET_EVENTS
        WHERE event_type = 'purchase'
    """)
    rows = cur.fetchall()
    print(f"    {'ORDER_ID':<15}  {'TOTAL':>7}  ITEM_COUNT")
    print(f"    {'─'*15}  {'─'*7}  {'─'*10}")
    for order_id, total, item_count in rows:
        print(f"    {str(order_id):<15}  {total:>7.2f}  {item_count}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Access elements inside a nested array
    #    payload:items[0]           — first element (VARIANT OBJECT)
    #    payload:items[0]:name      — field inside first element
    #    payload:items[0]:price     — numeric field inside first element
    #    Arrays are 0-indexed.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 3. Nested array element access ────────────────")
    cur.execute("""
        SELECT
            payload:items[0]:name::VARCHAR    AS first_item_name,
            payload:items[0]:price::FLOAT     AS first_item_price,
            payload:items[1]:name::VARCHAR    AS second_item_name,
            payload:items[1]:price::FLOAT     AS second_item_price
        FROM NUGGET_EVENTS
        WHERE event_type = 'purchase'
    """)
    rows = cur.fetchall()
    print(f"    {'FIRST_ITEM':<18}  {'PRICE':>6}  {'SECOND_ITEM':<18}  PRICE")
    print(f"    {'─'*18}  {'─'*6}  {'─'*18}  {'─'*6}")
    for n1, p1, n2, p2 in rows:
        print(f"    {str(n1):<18}  {p1:>6.2f}  {str(n2):<18}  {p2:>6.2f}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Cross-event query — one SELECT spans all event types
    #    Fields that don't exist in a given document return NULL automatically.
    #    This is the power of VARIANT: no UNION, no CASE, no schema changes.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 4. Cross-event query (all shapes in one SELECT) ─")
    cur.execute("""
        SELECT
            event_type,
            payload:severity::VARCHAR    AS severity,
            payload:code::NUMBER         AS error_code,
            payload:duration_ms::NUMBER  AS duration_ms
        FROM NUGGET_EVENTS
        ORDER BY event_id
    """)
    rows = cur.fetchall()
    print(f"    {'TYPE':<11}  {'SEVERITY':<10}  {'ERROR_CODE':<12}  DURATION_MS")
    print(f"    {'─'*11}  {'─'*10}  {'─'*12}  {'─'*11}")
    for etype, sev, code, dur in rows:
        print(
            f"    {etype:<11}  {str(sev or 'null'):<10}  "
            f"{str(code or 'null'):<12}  {dur or 'null'}"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # 5. Filter by a nested field — WHERE on a VARIANT path
    #    This is how you query "only error events with HIGH severity".
    #    Snowflake's micro-partition pruning applies to VARIANT paths too
    #    when the path is used frequently (see nugget 09_performance).
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── 5. Filter by nested field ─────────────────────")
    cur.execute("""
        SELECT
            event_id,
            payload:code::NUMBER       AS error_code,
            payload:message::VARCHAR   AS message
        FROM NUGGET_EVENTS
        WHERE payload:severity::VARCHAR = 'HIGH'
    """)
    rows = cur.fetchall()
    print(f"  High-severity events: {len(rows)} row(s)")
    for eid, code, msg in rows:
        print(f"    ID={eid}  code={code}  message={msg}")

conn.close()
print()
