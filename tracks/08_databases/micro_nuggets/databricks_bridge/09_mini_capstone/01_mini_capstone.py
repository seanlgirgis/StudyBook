"""
NUGGET 09-01 (Bridge) -- Mini Capstone: Bronze -> Silver -> Gold
================================================================
End-to-end DE pipeline demonstrating:
  Bronze  : raw event ingestion (as-is, with duplicates and bad data)
  Silver  : deduplication, type casting, validation, enrichment
  Gold    : analytics-ready aggregations (daily summary + customer LTV)
  Recovery: simulate a bad batch, detect it, restore from Time Travel

This capstone combines all prior concepts:
  - Delta tables (03_delta_core)
  - Deduplication pattern (04_de_patterns/01)
  - MERGE upsert (04_de_patterns/02)
  - Data quality checks (07_data_quality_and_testing/01)
  - Time Travel recovery (03_delta_core/03)

Usage:
    python 01_mini_capstone.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

C = LAB_CATALOG
S = LAB_SCHEMA
DIVIDER = "=" * 64
results = []


def check(label: str, condition: bool, detail: str = "") -> None:
    results.append((label, condition))
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status}  {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 64)
    print(f"  {title}")
    print("-" * 64)


print()
print(DIVIDER)
print("  Nugget 09-01: Mini Capstone -- Bronze -> Silver -> Gold")
print(DIVIDER)

conn = get_connection()
with conn.cursor() as cur:

    # ════════════════════════════════════════════════════════════════
    # PHASE 1: BRONZE LAYER
    # Raw data as-is. No transformations. Accept duplicates and errors.
    # Goal: never lose raw data, always have full history.
    # ════════════════════════════════════════════════════════════════
    section("Phase 1: Bronze Layer (raw ingestion)")

    print("  [1a] Create bronze_events (raw, no cleanup)")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.bronze_events")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.bronze_events (
                event_id    STRING,
                event_type  STRING,
                user_id     INT,
                event_ts    TIMESTAMP,
                payload     STRING,
                source      STRING,
                _ingest_ts  TIMESTAMP,
                _batch_id   STRING   COMMENT 'Pipeline run identifier'
            )
            USING DELTA
            COMMENT 'Bronze: raw events, no transformations -- capstone'
        """)
        check("Bronze table created", True)
    except Exception as exc:
        check("Create bronze table", False, str(exc)[:60])
        conn.close()
        sys.exit(1)

    print("  [1b] Load bronze: seed data + intentional duplicates + nulls")
    try:
        # Load clean events
        cur.execute(f"""
            INSERT INTO {C}.{S}.bronze_events
            SELECT
                event_id, event_type, user_id, event_ts, payload, source, _ingest_ts,
                'batch_001' AS _batch_id
            FROM {C}.{S}.events_stream
        """)
        # Add intentional duplicates (as would happen with retry delivery)
        cur.execute(f"""
            INSERT INTO {C}.{S}.bronze_events
            SELECT
                event_id, event_type, user_id, event_ts, payload, source,
                CURRENT_TIMESTAMP() AS _ingest_ts,
                'batch_001_retry' AS _batch_id
            FROM {C}.{S}.events_stream
            WHERE event_id IN ('evt-001', 'evt-002', 'evt-005')
        """)
        # Add a row with a null event_type (bad data from upstream)
        cur.execute(f"""
            INSERT INTO {C}.{S}.bronze_events VALUES
            ('evt-BAD', NULL, 99, CURRENT_TIMESTAMP(), '{{}}', 'broken', CURRENT_TIMESTAMP(), 'batch_001')
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.bronze_events")
        bronze_count = cur.fetchone()[0]
        check("Bronze loaded with raw + duplicates + nulls",
              bronze_count == 30 + 3 + 1,
              f"total rows={bronze_count}")
    except Exception as exc:
        check("Load bronze", False, str(exc)[:60])

    # ════════════════════════════════════════════════════════════════
    # PHASE 2: SILVER LAYER
    # Deduplicated, typed, validated. Ready for analysis.
    # ════════════════════════════════════════════════════════════════
    section("Phase 2: Silver Layer (clean and deduplicate)")

    print("  [2a] Create silver_events")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.silver_events")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.silver_events (
                event_id    STRING  NOT NULL,
                event_type  STRING  NOT NULL,
                user_id     INT,
                event_ts    TIMESTAMP,
                event_date  DATE    COMMENT 'Derived from event_ts for partitioning',
                source      STRING,
                _processed_ts TIMESTAMP COMMENT 'When this row was written to Silver'
            )
            USING DELTA
            PARTITIONED BY (event_date)
            COMMENT 'Silver: clean, deduped events -- capstone'
        """)
        check("Silver table created", True)
    except Exception as exc:
        check("Create silver table", False, str(exc)[:60])

    print("  [2b] Load silver: dedup + filter nulls + enrich")
    try:
        cur.execute(f"""
            INSERT INTO {C}.{S}.silver_events
            WITH ranked AS (
                SELECT
                    event_id,
                    event_type,
                    user_id,
                    event_ts,
                    DATE(event_ts)        AS event_date,
                    source,
                    CURRENT_TIMESTAMP()   AS _processed_ts,
                    ROW_NUMBER() OVER (
                        PARTITION BY event_id
                        ORDER BY _ingest_ts
                    ) AS rn
                FROM {C}.{S}.bronze_events
                WHERE event_type IS NOT NULL
                  AND user_id IS NOT NULL
            )
            SELECT event_id, event_type, user_id, event_ts, event_date, source, _processed_ts
            FROM ranked
            WHERE rn = 1
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.silver_events")
        silver_count = cur.fetchone()[0]
        check("Silver: 30 clean deduped rows",
              silver_count == 30,
              f"rows={silver_count}")
    except Exception as exc:
        check("Load silver", False, str(exc)[:60])

    print("  [2c] Silver quality gate: no nulls, no dups")
    cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.silver_events WHERE event_type IS NULL")
    null_types = cur.fetchone()[0]
    check("Silver: no null event_type", null_types == 0, f"nulls={null_types}")

    cur.execute(f"""
        SELECT COUNT(*) FROM (
            SELECT event_id FROM {C}.{S}.silver_events
            GROUP BY event_id HAVING COUNT(*) > 1
        )
    """)
    dups = cur.fetchone()[0]
    check("Silver: no duplicate event_ids", dups == 0, f"dup groups={dups}")

    # ════════════════════════════════════════════════════════════════
    # PHASE 3: GOLD LAYER
    # Analytics-ready aggregations for BI and dashboards.
    # ════════════════════════════════════════════════════════════════
    section("Phase 3: Gold Layer (analytics aggregations)")

    print("  [3a] Create gold_daily_summary")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.gold_daily_summary")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.gold_daily_summary
            USING DELTA
            COMMENT 'Gold: daily event summary -- capstone'
            AS
            SELECT
                event_date,
                event_type,
                source,
                COUNT(*)                    AS event_count,
                COUNT(DISTINCT user_id)     AS unique_users,
                CURRENT_TIMESTAMP()         AS computed_at
            FROM {C}.{S}.silver_events
            GROUP BY event_date, event_type, source
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.gold_daily_summary")
        gold_count = cur.fetchone()[0]
        check("Gold daily summary created",
              gold_count > 0,
              f"aggregation rows={gold_count}")
        cur.execute(f"""
            SELECT event_date, event_type, event_count, unique_users
            FROM {C}.{S}.gold_daily_summary
            ORDER BY event_date, event_type
            LIMIT 5
        """)
        sample = cur.fetchall()
        for r in sample:
            print(f"         {r}")
    except Exception as exc:
        check("Create gold summary", False, str(exc)[:60])

    # ════════════════════════════════════════════════════════════════
    # PHASE 4: FAILURE SIMULATION + TIME TRAVEL RECOVERY
    # ════════════════════════════════════════════════════════════════
    section("Phase 4: Failure Simulation and Time Travel Recovery")

    print("  [4a] Record pre-failure silver row count")
    cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.silver_events")
    pre_failure_count = cur.fetchone()[0]
    cur.execute(f"DESCRIBE HISTORY {C}.{S}.silver_events LIMIT 1")
    good_version_row = cur.fetchone()
    good_version = int(good_version_row[0]) if good_version_row else 0
    print(f"         Pre-failure count: {pre_failure_count}, good version: {good_version}")
    check("Pre-failure baseline recorded", pre_failure_count > 0)

    print("  [4b] Simulate bad batch: insert corrupt rows")
    try:
        cur.execute(f"""
            INSERT INTO {C}.{S}.silver_events VALUES
            ('CORRUPT-1', 'BAD_EVENT', -1, CURRENT_TIMESTAMP(), CURRENT_DATE(), 'bad_source', CURRENT_TIMESTAMP()),
            ('CORRUPT-2', 'BAD_EVENT', -1, CURRENT_TIMESTAMP(), CURRENT_DATE(), 'bad_source', CURRENT_TIMESTAMP()),
            ('CORRUPT-3', 'BAD_EVENT', -1, CURRENT_TIMESTAMP(), CURRENT_DATE(), 'bad_source', CURRENT_TIMESTAMP())
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.silver_events")
        post_corrupt = cur.fetchone()[0]
        check("Corrupt batch inserted (simulated failure)",
              post_corrupt == pre_failure_count + 3,
              f"rows after corruption={post_corrupt}")
    except Exception as exc:
        check("Corrupt batch insert", False, str(exc)[:60])
        post_corrupt = pre_failure_count

    print("  [4c] Detect corruption via data quality check")
    cur.execute(f"""
        SELECT COUNT(*) FROM {C}.{S}.silver_events
        WHERE user_id < 0 OR event_type = 'BAD_EVENT'
    """)
    bad_rows = cur.fetchone()[0]
    check("Corruption detected by DQ check",
          bad_rows == 3,
          f"bad rows detected={bad_rows}")

    print("  [4d] Recover via Time Travel RESTORE")
    try:
        cur.execute(f"""
            RESTORE TABLE {C}.{S}.silver_events TO VERSION AS OF {good_version}
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.silver_events")
        post_restore = cur.fetchone()[0]
        check("RESTORE to good version succeeded",
              post_restore == pre_failure_count,
              f"restored count={post_restore}")

        # Verify corrupt rows are gone
        cur.execute(f"""
            SELECT COUNT(*) FROM {C}.{S}.silver_events
            WHERE event_id LIKE 'CORRUPT%'
        """)
        still_corrupt = cur.fetchone()[0]
        check("Corrupt rows removed after RESTORE",
              still_corrupt == 0,
              f"corrupt rows remaining={still_corrupt}")
    except Exception as exc:
        check("RESTORE TIME TRAVEL", False, str(exc)[:60])

    # ════════════════════════════════════════════════════════════════
    # FINAL SUMMARY
    # ════════════════════════════════════════════════════════════════
    section("Capstone Summary")

    for layer, tbl in [("Bronze", "bronze_events"), ("Silver", "silver_events"),
                       ("Gold", "gold_daily_summary")]:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.{tbl}")
            cnt = cur.fetchone()[0]
            print(f"  Layer {layer:<8} table={tbl:<25} rows={cnt}")
        except Exception:
            print(f"  Layer {layer:<8} table={tbl:<25} rows=ERR")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 09-01 (Capstone): {passed}/{total} checks passed")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
