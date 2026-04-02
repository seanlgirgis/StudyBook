# Delivery Semantics - Story Map

## 1. Story (mailroom retries)
The mailroom sometimes drops a package, so it resends it. The receiver might get duplicates, but it is better than missing the package.

## 2. Core Concepts (street version)
- At-least-once = may deliver duplicates, but should not lose messages.
- Exactly-once (effect) = no duplicate impact; final result is correct.
- Idempotency = processing the same message twice has no extra effect.

## 3. At-Least-Once (what happens)
A crash happens after processing but before acknowledging. On retry, the same event is delivered again.

## 4. Exactly-Once (what it means here)
The system prevents duplicate impact by deduping or using idempotent writes.

## 5. Why It Matters
Duplicates can overcharge customers or double-count metrics if you do not guard against them.

## 6. Failure Mode (double apply)
If you do not dedupe, retries corrupt downstream state.

## 7. Final Mental Model
At-least-once is safe for data loss but risky for duplicates. Exactly-once effect is achieved by idempotency or dedup.

## 8. Run Order
1. c005_delivery_semantics_demo.py
