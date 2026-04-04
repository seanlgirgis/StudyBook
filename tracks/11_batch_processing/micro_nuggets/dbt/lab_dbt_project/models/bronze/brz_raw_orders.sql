-- brz_raw_orders.sql
-- BRONZE layer: raw order data with minimal transformation.
--
-- Bronze philosophy:
--   - Preserve ALL records, including cancelled, duplicates, outliers
--   - Apply ONLY basic type casts and column renames
--   - Never filter rows — bronze is the "source of truth" for reprocessing
--   - Materialized as VIEW (volume is small in lab; use TABLE in production)
--
-- Downstream: slv_orders_cleaned (silver layer)

-- Bronze models read from the staging layer, not directly from source().
-- Staging provides type safety; bronze adds the lineage anchor.
with staging as (
    select * from {{ ref('stg_orders') }}
)

select
    order_id,
    customer_id,
    product_id,
    amount_cents,
    status,
    order_date,
    updated_at,
    -- Bronze audit column: when was this row ingested into the lakehouse
    current_timestamp as _ingested_at

from staging
