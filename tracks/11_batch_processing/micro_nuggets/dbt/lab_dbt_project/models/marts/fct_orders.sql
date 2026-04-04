-- fct_orders.sql
-- Order fact table: one row per order, enriched with customer info.
--
-- Materialization: table
-- Dependencies:
--   stg_orders ──────────────────────────────► fct_orders
--   stg_customers ──► int_orders_with_customers ──► fct_orders (via ephemeral)
--   dim_customers ───────────────────────────────► fct_orders
--
-- Note: int_orders_with_customers is ephemeral — it becomes a CTE
-- inside THIS model's compiled SQL. No separate DB object is created.

{{
    config(
        materialized='table',
        tags=['daily', 'mart']
    )
}}

-- The ephemeral model's SQL is inlined here as a CTE by dbt compiler.
-- In the compiled SQL you'll see int_orders_with_customers's SELECT inside.
with orders_enriched as (
    select * from {{ ref('int_orders_with_customers') }}
),

payments_agg as (
    -- Aggregate completed payments per order
    select
        order_id,
        sum(amount_cents)     as total_paid_cents,
        count(*)              as payment_count,
        max(paid_at)          as last_paid_at
    from {{ ref('stg_payments') }}
    where status = 'completed'
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.customer_name,
    o.country,
    o.tier,
    o.product_id,
    o.amount_cents                               as order_amount_cents,
    -- Use the macro to convert cents → dollars (see macros/cents_to_dollars.sql)
    {{ cents_to_dollars('o.amount_cents') }}      as order_amount_dollars,
    o.status,
    o.order_date,
    o.updated_at,
    coalesce(p.total_paid_cents, 0)              as total_paid_cents,
    coalesce(p.payment_count, 0)                 as payment_count,
    p.last_paid_at,
    current_timestamp                            as _dbt_loaded_at

from orders_enriched o
left join payments_agg p
    on o.order_id = p.order_id
