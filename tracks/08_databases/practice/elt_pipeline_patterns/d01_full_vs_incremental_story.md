# Full Load vs Incremental Load - Story Map

## 1. Story (daily inventory reset)
A store receives a daily customer snapshot. One team replaces the entire table nightly. Another team keeps the table warm and only applies the change list.

## 2. Core Concepts (street version)
- Full load = replace the target with a complete snapshot.
- Incremental load = apply inserts, updates, and deletes since the last run.
- Deltas = the change list between snapshots.

## 3. Full Load (what it does)
Full load truncates the target and reloads all rows from the newest snapshot. It is simple but can be heavy.

## 4. Incremental Load (what it does)
Incremental load keeps yesterday's target and applies only the delta rows. It is efficient but depends on accurate change capture.

## 5. Failure Mode (drift)
If a delta is missing, incremental results drift from the source. Periodic full loads can reset the truth.

## 6. Final Mental Model
Full load is a full rebuild. Incremental load is a surgical update. Both should end at the same state when deltas are correct.

## 7. Run Order
1. c002_full_vs_incremental_demo.py
