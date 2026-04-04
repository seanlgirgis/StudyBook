-- stg_payments.sql
-- Staging layer: clean and rename raw_payments.
--
-- NOTE: This intentionally includes 0-amount refund payments (PAY023, PAY024).
-- The assert_positive_amounts singular test is designed to catch these.
-- In real life you would either: (a) filter them here, or (b) fix the test
-- to exclude refund records. The lab leaves them to teach testing.

with source as (
    select * from {{ source('dbt_lab_raw', 'raw_payments') }}
),

renamed as (
    select
        cast(payment_id as varchar)     as payment_id,
        cast(order_id as varchar)       as order_id,
        cast(amount_cents as integer)   as amount_cents,
        payment_method,
        cast(paid_at as timestamp)      as paid_at,
        status
    from source
)

select * from renamed
