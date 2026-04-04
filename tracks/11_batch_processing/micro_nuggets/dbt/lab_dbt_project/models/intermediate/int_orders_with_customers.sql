-- int_orders_with_customers.sql
-- Intermediate model: joins orders with customer attributes.
--
-- Materialization: ephemeral (set in dbt_project.yml for intermediate/ folder)
--   - This model is NEVER materialized as a table or view in the database.
--   - dbt inlines its SQL as a CTE inside the calling model (fct_orders).
--   - You can still ref() it from other models — dbt handles the inlining.
--
-- When to use ephemeral:
--   ✓ Intermediate logic used by only ONE downstream model
--   ✓ You want to break up a complex SELECT into readable steps
--   ✓ The intermediate result doesn't need to be queryable by analysts
--
-- When NOT to use ephemeral:
--   ✗ Multiple downstream models need it → use view or table instead
--   ✗ The intermediate query is slow → materializing saves re-computation
--   ✗ You need to test this model directly → ephemeral models can't be tested

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select
        customer_id,
        customer_name,
        country,
        tier
    from {{ ref('stg_customers') }}
)

select
    o.order_id,
    o.customer_id,
    o.product_id,
    o.amount_cents,
    o.status,
    o.order_date,
    o.updated_at,
    -- Enriched from customers
    c.customer_name,
    c.country,
    c.tier

from orders o
left join customers c
    on o.customer_id = c.customer_id
