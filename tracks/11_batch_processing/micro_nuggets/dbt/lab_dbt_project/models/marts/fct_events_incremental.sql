-- fct_events_incremental.sql
-- Clickstream events fact table — incremental materialization.
--
-- Materialization: incremental
--   - First run: loads ALL rows from stg_events
--   - Subsequent runs: loads ONLY rows where event_ts > max(event_ts) in table
--   - unique_key: event_id — deduplicates on UPSERT (if same event_id arrives twice)
--   - on_schema_change: append_new_columns — if we add columns to SQL, they appear
--     in the target table with NULL for existing rows
--
-- Why incremental for events?
--   Event tables grow fast (billions of rows in production).
--   Rebuilding from scratch every run is too expensive.
--   Events are append-only → perfect for incremental pattern.

{{
    config(
        materialized='incremental',
        unique_key='event_id',
        on_schema_change='append_new_columns'
    )
}}

with source as (
    select * from {{ ref('stg_events') }}

    -- ── The is_incremental() block is THE core incremental pattern ──────────
    -- is_incremental() returns True when:
    --   (1) The target table already exists
    --   (2) We are NOT doing a --full-refresh run
    -- On first run: is_incremental() = False → load ALL rows
    -- On subsequent runs: is_incremental() = True → load only NEW rows
    --
    -- {{ this }} is a built-in dbt macro that refers to the CURRENT model's
    -- fully qualified table name (e.g., dbt_lab.fct_events_incremental)
    {% if is_incremental() %}
        where event_ts > (select max(event_ts) from {{ this }})
    {% endif %}
)

select
    event_id,
    customer_id,
    event_type,
    event_ts,
    page,
    session_id,
    -- Audit column: when this row was loaded (helps debug incremental issues)
    current_timestamp as _loaded_at

from source
