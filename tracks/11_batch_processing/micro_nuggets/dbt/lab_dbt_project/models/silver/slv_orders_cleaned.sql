-- slv_orders_cleaned.sql
-- SILVER layer: cleaned, filtered, enriched orders.
--
-- Silver philosophy:
--   - Filter out invalid / cancelled records for business reporting
--   - Enrich with related dimension attributes (customer country, tier)
--   - Convert monetary values to proper units (cents → dollars)
--   - Apply deduplication if needed
--   - Materialized as TABLE (silver is frequently queried by gold layer)
--
-- Downstream: gld_order_summary (gold layer)

with bronze_orders as (
    -- Always read from the bronze layer, not from staging/source directly.
    -- This enforces the medallion lineage: raw → bronze → silver → gold
    select * from {{ ref('brz_raw_orders') }}
),

customers as (
    select customer_id, country, tier
    from {{ ref('stg_customers') }}
)

select
    o.order_id,
    o.customer_id,
    o.product_id,
    o.amount_cents,
    -- Convert cents to dollars using the cents_to_dollars macro
    -- Macro lives in macros/cents_to_dollars.sql
    {{ cents_to_dollars('o.amount_cents') }} as amount_dollars,
    o.order_date,
    o.updated_at,
    -- Enriched attributes from dimension
    c.country,
    c.tier,
    -- Silver audit column
    current_timestamp as _cleaned_at

from bronze_orders o
left join customers c
    on o.customer_id = c.customer_id

-- Silver business rule: only include revenue-generating orders
where o.status = 'completed'
