-- gld_order_summary.sql
-- GOLD layer: pre-aggregated order metrics by country and tier.
--
-- Gold philosophy:
--   - Business-ready: what goes into dashboards and reports
--   - Pre-aggregated to make BI queries fast
--   - Denormalized (country, tier already there — no joins needed in BI)
--   - Materialized as TABLE (gold is always table — BI tools need speed)
--
-- Consumers: business intelligence tools, Tableau, Power BI, Looker, etc.

with silver as (
    -- Gold reads from silver — the cleaned, filtered, enriched layer.
    -- Never skip layers: gold reads silver, silver reads bronze, bronze reads staging.
    select * from {{ ref('slv_orders_cleaned') }}
)

select
    -- Dimension attributes (group-by keys for slicing/dicing in BI)
    country,
    tier,
    -- Time dimension (monthly grain for trend analysis)
    cast(strftime('%Y-%m', order_date) as varchar)  as order_month,

    -- Metrics
    count(distinct order_id)                         as order_count,
    count(distinct customer_id)                      as unique_customers,
    sum(amount_dollars)                              as total_revenue_dollars,
    avg(amount_dollars)                              as avg_order_value_dollars,
    min(amount_dollars)                              as min_order_value_dollars,
    max(amount_dollars)                              as max_order_value_dollars,

    -- Audit
    current_timestamp                               as _aggregated_at

from silver
group by
    country,
    tier,
    cast(strftime('%Y-%m', order_date) as varchar)

order by
    order_month,
    total_revenue_dollars desc
