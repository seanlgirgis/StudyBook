-- stg_events.sql
-- Staging layer: clean and rename raw_events.
--
-- Events are high-volume append-only records.
-- Downstream: fct_events_incremental (incremental materialization)

with source as (
    select * from {{ source('dbt_lab_raw', 'raw_events') }}
),

renamed as (
    select
        cast(event_id as varchar)       as event_id,
        cast(customer_id as varchar)    as customer_id,
        event_type,
        -- Cast timestamp string to proper TIMESTAMP type
        cast(event_ts as timestamp)     as event_ts,
        page,
        cast(session_id as varchar)     as session_id
    from source
)

select * from renamed
