"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 09-01 · Mini Capstone: Bronze → Silver → Gold Pipeline               ║
║  End-to-end DE workflow using PostgreSQL tables, views, and mat. views.      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Builds a complete data pipeline:
  1. BRONZE: raw staging tables (simulated ingestion)
  2. SILVER: cleaned, deduplicated, validated
  3. GOLD: analytics-ready materialized views

PIPELINE ARCHITECTURE
─────────────────────
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │  BRONZE      │────▶│  SILVER      │────▶│  GOLD        │
    │  (raw)       │     │  (cleaned)   │     │  (analytics) │
    └──────────────┘     └──────────────┘     └──────────────┘

USAGE
─────
    python 01_mini_capstone.py

EXPECTED OUTPUT
───────────────
    ── Mini Capstone: Bronze → Silver → Gold ───────────────

      ══ PHASE 1: BRONZE ════════════════════════════════
        Created bronze tables with raw data

      ══ PHASE 2: SILVER ════════════════════════════════
        Deduplicated and validated

      ══ PHASE 3: GOLD ══════════════════════════════════
        Created materialized views

      ══ RESULTS ════════════════════════════════════════
        Daily metrics and customer LV computed
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _pg_connect import get_connection, LAB_SCHEMA, ensure_lab_schema

conn = get_connection()
ensure_lab_schema(conn)

print("\n── Mini Capstone: Bronze → Silver → Gold ───────────────")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 1: BRONZE — Raw staging tables
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 1: BRONZE ════════════════════════════════")

with conn.cursor() as cur:
    # Create bronze tables
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {LAB_SCHEMA}.bronze_raw_orders (
            raw_id      SERIAL PRIMARY KEY,
            raw_data    JSONB NOT NULL,
            ingested_at TIMESTAMP DEFAULT NOW()
        )
    """)
    # Keep capstone rerun-safe and deterministic.
    cur.execute(f"TRUNCATE TABLE {LAB_SCHEMA}.bronze_raw_orders RESTART IDENTITY")

    # Insert raw JSON data (simulating API/file ingestion)
    cur.execute(f"""
        INSERT INTO {LAB_SCHEMA}.bronze_raw_orders (raw_data)
        SELECT jsonb_build_object(
            'customer_id', o.customer_id,
            'order_date', o.order_date::text,
            'status', o.status,
            'total', o.total_amount,
            'items', (
                SELECT jsonb_agg(jsonb_build_object(
                    'product', p.name,
                    'qty', oi.quantity,
                    'price', oi.unit_price
                ))
                FROM {LAB_SCHEMA}.order_items oi
                JOIN {LAB_SCHEMA}.products p ON oi.product_id = p.product_id
                WHERE oi.order_id = o.order_id
            )
        )
        FROM {LAB_SCHEMA}.orders o
        WHERE o.order_id <= 10
    """)
    conn.commit()

    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.bronze_raw_orders")
    bronze_count = cur.fetchone()[0]
    print(f"    Ingested {bronze_count} raw order records as JSONB")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 2: SILVER — Cleaned, validated, deduplicated
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 2: SILVER ════════════════════════════════")

with conn.cursor() as cur:
    # Create silver tables
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {LAB_SCHEMA}.silver_orders (
            order_id    SERIAL PRIMARY KEY,
            customer_id INT NOT NULL,
            order_date  DATE NOT NULL,
            status      VARCHAR(20),
            total_amount NUMERIC(12,2),
            item_count  INT,
            loaded_at   TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute(f"TRUNCATE TABLE {LAB_SCHEMA}.silver_orders RESTART IDENTITY")

    # Parse JSONB → structured, deduplicated, validated
    cur.execute(f"""
        INSERT INTO {LAB_SCHEMA}.silver_orders
            (customer_id, order_date, status, total_amount, item_count)
        SELECT DISTINCT ON (raw_data->>'customer_id', raw_data->>'order_date')
            (raw_data->>'customer_id')::INT,
            (raw_data->>'order_date')::DATE,
            raw_data->>'status',
            (raw_data->>'total')::NUMERIC(12,2),
            jsonb_array_length(raw_data->'items')
        FROM {LAB_SCHEMA}.bronze_raw_orders
        WHERE raw_data->>'status' != 'cancelled'
          AND (raw_data->>'total')::NUMERIC > 0
        ORDER BY raw_data->>'customer_id', raw_data->>'order_date', raw_id DESC
    """)
    conn.commit()

    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.silver_orders")
    silver_count = cur.fetchone()[0]
    print(f"    Cleaned: {bronze_count} raw → {silver_count} validated orders")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 3: GOLD — Analytics-ready materialized views
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 3: GOLD ══════════════════════════════════")

with conn.cursor() as cur:
    # Drop if exists as either materialized view or table.
    # Order matters: try materialized view first to avoid relation-type errors.
    cur.execute(f"DROP MATERIALIZED VIEW IF EXISTS {LAB_SCHEMA}.gold_daily_metrics CASCADE")
    cur.execute(f"DROP TABLE IF EXISTS {LAB_SCHEMA}.gold_daily_metrics CASCADE")
    cur.execute(f"DROP MATERIALIZED VIEW IF EXISTS {LAB_SCHEMA}.gold_customer_lifetime_value CASCADE")
    cur.execute(f"DROP TABLE IF EXISTS {LAB_SCHEMA}.gold_customer_lifetime_value CASCADE")
    conn.commit()

    # Daily metrics
    cur.execute(f"""
        CREATE MATERIALIZED VIEW {LAB_SCHEMA}.gold_daily_metrics AS
        SELECT
            order_date AS metric_date,
            COUNT(*) AS order_count,
            ROUND(SUM(total_amount), 2) AS revenue,
            ROUND(AVG(total_amount), 2) AS avg_order,
            COUNT(DISTINCT customer_id) AS unique_cust
        FROM {LAB_SCHEMA}.silver_orders
        GROUP BY order_date
        ORDER BY order_date
    """)

    # Customer lifetime value
    cur.execute(f"DROP MATERIALIZED VIEW IF EXISTS {LAB_SCHEMA}.gold_customer_lifetime_value")
    cur.execute(f"""
        CREATE MATERIALIZED VIEW {LAB_SCHEMA}.gold_customer_lifetime_value AS
        SELECT
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            COUNT(s.order_id) AS total_orders,
            ROUND(COALESCE(SUM(s.total_amount), 0), 2) AS total_spent,
            ROUND(COALESCE(AVG(s.total_amount), 0), 2) AS avg_order,
            MIN(s.order_date) AS first_order,
            MAX(s.order_date) AS last_order
        FROM {LAB_SCHEMA}.customers c
        LEFT JOIN {LAB_SCHEMA}.silver_orders s ON c.customer_id = s.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY total_spent DESC
    """)
    conn.commit()

    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.gold_daily_metrics")
    daily_count = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM {LAB_SCHEMA}.gold_customer_lifetime_value")
    clv_count = cur.fetchone()[0]
    print(f"    Daily metrics: {daily_count} rows")
    print(f"    Customer LTV: {clv_count} rows")

# ═════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ RESULTS ════════════════════════════════════════")

print("\n  ── Daily Metrics ──────────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT metric_date, order_count, revenue, avg_order, unique_cust
        FROM {LAB_SCHEMA}.gold_daily_metrics
        ORDER BY metric_date
        LIMIT 10
    """)
    rows = cur.fetchall()

print(f"    {'Date':<12} {'Orders':<7} {'Revenue':<11} {'Avg':<9} {'Customers'}")
print(f"    {'-'*12} {'-'*7} {'-'*11} {'-'*9} {'-'*9}")
for date, orders, rev, avg, custs in rows:
    print(f"    {str(date):<12} {orders:<7} ${rev:>9,.2f} ${avg:>8,.2f} {custs}")

print("\n  ── Customer Lifetime Value ────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT customer_name, total_orders, total_spent, avg_order
        FROM {LAB_SCHEMA}.gold_customer_lifetime_value
        ORDER BY total_spent DESC
        LIMIT 10
    """)
    rows = cur.fetchall()

print(f"    {'Customer':<20} {'Orders':<7} {'Spent':<11} {'Avg'}")
print(f"    {'-'*20} {'-'*7} {'-'*11} {'-'*9}")
for name, orders, spent, avg in rows:
    print(f"    {name:<20} {orders:<7} ${spent:>9,.2f} ${avg:>8,.2f}")

conn.close()
print("\n  Pipeline complete!")
print()
