-- stg_customers.sql
-- Staging layer: clean and rename raw_customers.
--
-- Staging rules:
--   1. Always call source() here, never ref()
--   2. Rename columns to business-friendly names
--   3. Cast types explicitly (don't trust raw column types)
--   4. Apply minimal cleaning (lowercase email, strip spaces)
--   5. Do NOT filter rows — staging shows all raw data
--      (filtering is for silver/mart layer)
--
-- Downstream: dim_customers (mart), customers_snapshot (SCD2),
--             int_orders_with_customers (ephemeral)

with source as (
    -- source() macro: tells dbt this is a raw/external table.
    -- The first arg is the source name in schema.yml, second is the table.
    -- dbt generates: SELECT * FROM dbt_lab_raw.raw_customers
    select * from {{ source('dbt_lab_raw', 'raw_customers') }}
),

renamed as (
    select
        -- Cast to explicit types for downstream consistency
        cast(id as varchar)           as customer_id,
        name                          as customer_name,
        -- Normalize email to lowercase so joins work correctly
        lower(email)                  as email,
        country,
        -- Cast date string to actual DATE type
        cast(created_at as date)      as created_date,
        -- Cast boolean string to actual BOOLEAN
        cast(is_active as boolean)    as is_active,
        tier
    from source
)

select * from renamed
