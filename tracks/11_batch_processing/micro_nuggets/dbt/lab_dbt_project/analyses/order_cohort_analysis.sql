-- order_cohort_analysis.sql
-- Analysis: Monthly cohort revenue analysis.
--
-- This file lives in analyses/ — it is compiled by dbt but NOT materialized.
-- Use `dbt compile` to render the Jinja → SQL, then run it manually.
-- Useful for ad-hoc exploration that benefits from ref() but doesn't need
-- to be part of the production DAG.
--
-- Run compiled version:
--   dbt compile --select order_cohort_analysis
--   cat target/compiled/dbt_lab/analyses/order_cohort_analysis.sql
--   (then paste into your SQL client or DuckDB)

with cohort_base as (
    select
        customer_id,
        -- Cohort month = first order month for each customer
        min(cast(strftime('%Y-%m', order_date) as varchar)) as cohort_month
    from {{ ref('stg_orders') }}
    where status = 'completed'
    group by customer_id
),

monthly_revenue as (
    select
        o.customer_id,
        cast(strftime('%Y-%m', o.order_date) as varchar) as order_month,
        sum({{ cents_to_dollars('o.amount_cents') }})    as revenue_dollars
    from {{ ref('stg_orders') }} o
    where o.status = 'completed'
    group by o.customer_id, cast(strftime('%Y-%m', o.order_date) as varchar)
)

select
    c.cohort_month,
    m.order_month,
    count(distinct m.customer_id)   as active_customers,
    sum(m.revenue_dollars)          as total_revenue,
    avg(m.revenue_dollars)          as avg_revenue_per_customer

from cohort_base c
join monthly_revenue m
    on c.customer_id = m.customer_id

group by
    c.cohort_month,
    m.order_month

order by
    c.cohort_month,
    m.order_month
