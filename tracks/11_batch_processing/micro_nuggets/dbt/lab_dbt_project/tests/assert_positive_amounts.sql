-- assert_positive_amounts.sql
-- Singular test: assert ALL payment amounts are positive (> 0).
--
-- If this query returns ANY rows → TEST FAILS.
-- If this query returns 0 rows → TEST PASSES.
--
-- Teaching moment:
--   The seed data intentionally includes PAY023 and PAY024 with amount_cents=0
--   (they represent refunds). This test WILL fail on the seeded data.
--
--   In production you would fix this by either:
--     (a) Filtering refunds in stg_payments: WHERE status != 'refunded'
--     (b) Changing the test: WHERE amount_cents <= 0 AND status != 'refunded'
--     (c) Modeling refunds as a separate table (best practice)
--
-- Violation rows returned by this test:

select
    payment_id,
    order_id,
    amount_cents,
    status
from {{ ref('stg_payments') }}
where amount_cents <= 0
