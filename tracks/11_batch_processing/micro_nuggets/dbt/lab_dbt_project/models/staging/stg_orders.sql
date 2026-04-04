-- stg_orders.sql
-- Staging layer: clean and rename raw_orders.
--
-- Preserves ALL orders (including cancelled) — no business filtering here.
-- Silver/gold layers decide what to include in metrics.

with source as (
    select * from {{ source('dbt_lab_raw', 'raw_orders') }}
),

renamed as (
    select
        cast(order_id as varchar)      as order_id,
        cast(customer_id as varchar)   as customer_id,
        cast(product_id as varchar)    as product_id,
        -- amount_cents stays as integer — conversion to dollars happens in macros
        cast(amount_cents as integer)  as amount_cents,
        status,
        cast(order_date as date)       as order_date,
        cast(updated_at as timestamp)  as updated_at
    from source
)

select * from renamed
