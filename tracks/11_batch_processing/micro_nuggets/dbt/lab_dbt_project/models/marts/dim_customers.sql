-- dim_customers.sql
-- Customer dimension: one row per customer, materialized as a TABLE.
--
-- Materialization: table
--   - Rebuilt from scratch on every dbt run
--   - Fast to query (no view-over-view stack)
--   - Appropriate because customers table is small (< 1M rows)
--
-- Uses ref() NOT source() — we consume stg_customers, not raw_customers.
-- This ensures the staging cleaning (lowercase email, type casts) is applied.

{{
    config(
        materialized='table',
        tags=['daily', 'mart']
    )
}}

with customers as (
    -- ref() creates a DAG dependency on stg_customers.
    -- dbt will always run stg_customers before this model.
    select * from {{ ref('stg_customers') }}
)

select
    customer_id,
    customer_name,
    email,
    country,
    created_date,
    is_active,
    tier,
    -- Derived columns — computed once at build time
    case
        when tier = 'platinum' then 4
        when tier = 'gold'     then 3
        when tier = 'silver'   then 2
        else 1
    end as tier_rank,
    current_timestamp as _dbt_loaded_at

from customers
