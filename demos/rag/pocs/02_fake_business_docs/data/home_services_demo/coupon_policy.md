# Synthetic Demo Document

## Coupon and Offer Policy

## Standard Rules
- One coupon per paid invoice unless explicitly stated.
- Coupons cannot be combined with emergency dispatch premiums.
- Coupon eligibility must be confirmed during booking.

## Diagnostic Fee Waiver Rule
Diagnostic fee may be waived only when:
- customer approves same-visit repair above minimum spend threshold, or
- active maintenance plan benefit applies.

## Exception Handling
If customer requests special pricing exception:
- assistant should not approve directly
- escalate to pricing supervisor queue
- log outcome as `pricing_exception_requested`
