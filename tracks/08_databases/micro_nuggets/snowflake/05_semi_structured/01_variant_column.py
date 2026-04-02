"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-01 · VARIANT Column — Semi-Structured Data                        ║
║  One of Snowflake's biggest differentiators over traditional databases.      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Introduces the VARIANT type: what it is, how to insert JSON into it,
and how Snowflake stores it internally. Lays the foundation for
nuggets 05-02 (querying) and 05-03 (flattening arrays).

CONCEPTS
────────
What is VARIANT?
  A VARIANT column stores semi-structured data — JSON, XML, Avro, Parquet,
  ORC — as a single column value.  Snowflake converts the data internally
  into an optimised binary tree (called "columnar" storage even for nested
  data) so you can query deeply nested fields efficiently.

  Think of VARIANT as a column that holds an entire JSON document per row.
  Max size per value: 16 MB.

Why does this matter for Data Engineers?
  In the real world, data rarely arrives as perfectly flat rows.  APIs return
  JSON.  Kafka topics carry nested events.  Webhook payloads have optional
  fields.  A DE needs to:
    1. Land the raw document unchanged  (VARIANT column — this nugget)
    2. Query fields out of it           (nugget 05-02)
    3. Explode arrays into rows         (nugget 05-03)
    4. Promote stable fields to columns (CREATE TABLE AS SELECT with casting)

VARIANT vs dedicated JSON columns in other databases:
  PostgreSQL JSONB    — binary JSON, good querying, but no columnar pushdown
  MySQL JSON          — binary JSON, limited indexing
  Snowflake VARIANT   — native columnar storage, automatic micro-partition
                        pruning on nested paths, no separate index needed.
                        Snowflake's query engine understands the nested
                        structure and pushes predicates into the storage layer.

Inserting JSON into VARIANT:
  Method 1 — PARSE_JSON() function:
      INSERT INTO t SELECT PARSE_JSON('{"key": "value"}');
      PARSE_JSON converts a VARCHAR containing JSON into a VARIANT value.

  Method 2 — OBJECT_CONSTRUCT() function:
      INSERT INTO t SELECT OBJECT_CONSTRUCT('key', 'value', 'count', 42);
      Builds a JSON object from key-value pairs — useful for constructing
      documents from existing column values.

  Method 3 — ARRAY_CONSTRUCT():
      SELECT ARRAY_CONSTRUCT(1, 2, 3)  →  [1, 2, 3]  as VARIANT

  Method 4 — COPY INTO with FILE FORMAT = JSON:
      Covered in nugget 04_loading_data.

Snowflake's automatic schema detection:
  When you COPY INTO a VARIANT column from a JSON file, Snowflake infers
  the document structure. You can later run:
      SELECT SYSTEM$GET_SCHEMA('<stage>/<file.json>', 'json')
  to get a suggested CREATE TABLE with proper typed columns.

USAGE
─────
    python 01_variant_column.py

EXPECTED OUTPUT
───────────────
    ── VARIANT Column ───────────────────────────

      Created: NUGGET_EVENTS

      Inserted 4 event rows.

      ── All events (raw VARIANT) ──────────────────────
        ID  EVENT_TYPE        RAW_PAYLOAD (first 80 chars)
        --- ----------------- -------------------------------------------------------
          1 page_view         {"browser": "Chrome", "duration_ms": 1240, "page": "/h
          2 purchase          {"currency": "USD", "items": [{"price": 29.99, "produc
          3 error             {"code": 500, "message": "Internal Server Error", "sev
          4 page_view         {"browser": "Firefox", "duration_ms": 890, "page": "/p

      ── VARIANT type info ─────────────────────────────
        TYPEOF row 1 payload : OBJECT
        TYPEOF row 2 items   : ARRAY     ← nested array inside OBJECT
        TYPEOF row 3 code    : INTEGER

      ── OBJECT_CONSTRUCT example ──────────────────────
        Built from columns: {"event_id": 99, "event_type": "synthetic", "ts": "..."}
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── VARIANT Column ───────────────────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Create the events table
    #    Notice: one column is fully typed (event_id, event_type, created_at)
    #            one column is VARIANT (payload) — holds whatever JSON arrives.
    #    This is the "schema-on-read" approach: land everything, type later.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_EVENTS (
            event_id    NUMBER AUTOINCREMENT PRIMARY KEY,
            event_type  VARCHAR(50)   NOT NULL,
            created_at  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            payload     VARIANT       COMMENT 'Raw JSON document — shape varies per event_type'
        )
        COMMENT = 'Demo semi-structured events table — nugget 05-01'
    """)
    print("\n  Created: NUGGET_EVENTS")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Insert rows using PARSE_JSON()
    #    Each event type has a DIFFERENT document shape — that is the point.
    #    Traditional relational tables can't do this cleanly. VARIANT can.
    #
    #    Real-world analogy: a Kafka topic where each message type has its
    #    own schema (page_view vs purchase vs error vs user_signup).
    # ─────────────────────────────────────────────────────────────────────────
    events = [
        ("page_view", """{
            "page": "/home",
            "duration_ms": 1240,
            "browser": "Chrome",
            "referrer": "https://google.com",
            "user_id": 42
        }"""),
        ("purchase", """{
            "order_id": "ORD-8821",
            "currency": "USD",
            "total": 89.97,
            "items": [
                {"product_id": 10, "name": "Widget A", "price": 29.99, "qty": 1},
                {"product_id": 11, "name": "Widget B", "price": 59.98, "qty": 2}
            ],
            "user_id": 42
        }"""),
        ("error", """{
            "code": 500,
            "message": "Internal Server Error",
            "severity": "HIGH",
            "endpoint": "/api/checkout",
            "stack_trace": "NullPointerException at line 42"
        }"""),
        ("page_view", """{
            "page": "/pricing",
            "duration_ms": 890,
            "browser": "Firefox",
            "user_id": 99
        }"""),
    ]

    for event_type, json_str in events:
        cur.execute("""
            INSERT INTO NUGGET_EVENTS (event_type, payload)
            SELECT %s, PARSE_JSON(%s)
        """, (event_type, json_str))

    cur.execute("SELECT COUNT(*) FROM NUGGET_EVENTS")
    print(f"  Inserted {cur.fetchone()[0]} event rows.")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Read back — view the raw VARIANT column
    #    Snowflake serialises VARIANT back to a JSON string for display.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        SELECT event_id, event_type, payload
        FROM   NUGGET_EVENTS
        ORDER  BY event_id
    """)
    rows = cur.fetchall()

    print(f"\n  ── All events (raw VARIANT) ──────────────────────")
    print(f"    {'ID':>3}  {'EVENT_TYPE':<17} RAW_PAYLOAD (first 80 chars)")
    print(f"    {'─'*3}  {'─'*17} {'─'*55}")
    for eid, etype, payload in rows:
        snippet = str(payload).replace("\n", " ").replace("  ", " ")[:78]
        print(f"    {eid:>3}  {etype:<17} {snippet}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. TYPEOF() — inspect the data type of a VARIANT value or sub-value
    #    Types Snowflake reports: OBJECT, ARRAY, VARCHAR, INTEGER, REAL,
    #                             BOOLEAN, NULL_VALUE
    #    This is how you introspect dynamic documents at query time.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        SELECT
            TYPEOF(payload)           AS full_doc_type,
            TYPEOF(payload:items)     AS items_type,
            TYPEOF(payload:code)      AS code_type
        FROM NUGGET_EVENTS
        WHERE event_id IN (1, 2, 3)
        ORDER BY event_id
    """)
    rows = cur.fetchall()

    print(f"\n  ── TYPEOF() — type inspection ────────────────────")
    print(f"    {'EVENT':>5}  {'FULL DOC':<12}  {'payload:items':<14}  payload:code")
    for i, (doc_t, items_t, code_t) in enumerate(rows, start=1):
        print(f"    {i:>5}  {str(doc_t):<12}  {str(items_t):<14}  {code_t}")
    print("    (NULL_VALUE means the field doesn't exist in that document)")

    # ─────────────────────────────────────────────────────────────────────────
    # 5. OBJECT_CONSTRUCT() — build a VARIANT from column values
    #    Real use: after loading raw data, construct a summary document
    #    that combines multiple columns into one portable payload.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        SELECT OBJECT_CONSTRUCT(
            'event_id',   99,
            'event_type', 'synthetic',
            'ts',         CURRENT_TIMESTAMP()::VARCHAR,
            'source',     'nugget_05_01'
        ) AS constructed_doc
    """)
    doc = cur.fetchone()[0]
    print(f"\n  ── OBJECT_CONSTRUCT() example ────────────────────")
    print(f"    {str(doc)[:100]}")

conn.close()
print()
