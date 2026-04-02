# SCD Type 2 (History Rows) - Story Map

## 1. Story (passport renewals)
When you renew a passport, the old one is not erased. You get a new one, and the old one becomes inactive. History is preserved.

## 2. Core Concepts (street version)
- SCD Type 2 = create a new row on change.
- Old row is expired, new row is current.
- Facts join to the version that was current at the time.

## 3. What Happens on Change
The old dimension row is closed (effective_end or current_flag = false).
The new row starts (effective_start or current_flag = true).

## 4. Why It Exists
You can report on history: "what the customer was back then."

## 5. Tradeoff
More rows and more complex joins, but accurate history.

## 6. Final Mental Model
Type 2 is "add a new version, keep the old."

## 7. Run Order
1. c005_scd_type2_demo.py
