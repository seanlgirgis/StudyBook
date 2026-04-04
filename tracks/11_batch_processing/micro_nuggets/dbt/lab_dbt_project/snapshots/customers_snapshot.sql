{% snapshot customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['tier', 'is_active', 'email']
    )
}}

-- SCD Type 2 snapshot on customers.
--
-- dbt automatically adds these columns to the snapshot table:
--   dbt_scd_id      → unique hash for each historical row
--   dbt_updated_at  → when this row was last processed by dbt snapshot
--   dbt_valid_from  → when this version of the record became active
--   dbt_valid_to    → when this version ended (NULL = still current)
--
-- strategy='check' explanation:
--   dbt compares the check_cols values for each unique_key.
--   If ANY of (tier, is_active, email) changes:
--     1. Old row: dbt_valid_to = current_timestamp
--     2. New row: dbt_valid_to = NULL (becomes the "current" version)
--   This creates a new row for every detected change.
--
-- strategy='timestamp' alternative:
--   Reads an updated_at column instead of comparing values.
--   More performant at scale (only processes rows where updated_at > last seen).
--   Requires the source system to reliably maintain updated_at.
--
-- Query pattern for current state (Type 2 anti-pattern is forgetting this filter!):
--   SELECT * FROM customers_snapshot WHERE dbt_valid_to IS NULL
--
-- Query pattern for history at a point in time:
--   SELECT * FROM customers_snapshot
--   WHERE dbt_valid_from <= '2023-06-01' AND (dbt_valid_to > '2023-06-01' OR dbt_valid_to IS NULL)

select
    customer_id,
    customer_name,
    email,
    country,
    tier,
    is_active

-- Read from the staging model (after cleaning), not from source directly.
-- This ensures snapshot captures clean data, not raw strings.
from {{ ref('stg_customers') }}

{% endsnapshot %}
