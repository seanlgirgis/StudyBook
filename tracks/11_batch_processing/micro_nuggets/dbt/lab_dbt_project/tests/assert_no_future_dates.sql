-- assert_no_future_dates.sql
-- Singular test: assert NO order dates are in the future.
--
-- If this query returns ANY rows → TEST FAILS.
-- If this query returns 0 rows → TEST PASSES.
--
-- Detects data quality issues like:
--   - Timezone bugs (order placed in Asia but logged as tomorrow in UTC)
--   - Test data accidentally loaded to production
--   - System clock errors in source systems
--
-- The seed data should all have historical dates → this test should PASS.

select
    order_id,
    order_date,
    current_date as today
from {{ ref('stg_orders') }}
where order_date > current_date
