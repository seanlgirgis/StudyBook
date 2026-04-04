-- stg_products.sql
-- Staging layer: clean and rename raw_products.

with source as (
    select * from {{ source('dbt_lab_raw', 'raw_products') }}
),

renamed as (
    select
        cast(product_id as varchar)     as product_id,
        name                            as product_name,
        category,
        cast(price_cents as integer)    as price_cents,
        cast(is_active as boolean)      as is_active
    from source
)

select * from renamed
