# SCD Type 1 (Overwrite) - Story Map

## 1. Story (address book)
You keep an address book. When someone moves, you erase the old address and write the new one. The book always shows the latest info.

## 2. Core Concepts (street version)
- SCD Type 1 = overwrite in place.
- No history is kept.
- Reports always see the latest attributes.

## 3. What Happens on Change
The dimension row is updated directly. The old value is gone.

## 4. Why It Exists
Some attributes are corrections, not history. You just want the current truth.

## 5. Tradeoff
You lose the ability to report on past values.

## 6. Final Mental Model
Type 1 is "erase and replace."

## 7. Run Order
1. c004_scd_type1_demo.py
