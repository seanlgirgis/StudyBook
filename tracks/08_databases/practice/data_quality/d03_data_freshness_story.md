# Data Freshness - Story Map

## 1. Story (daily newspaper)
The newspaper should arrive by morning. If it arrives at lunch, it is stale.

## 2. Core Concepts (street version)
- Freshness window = the expected arrival time.
- Fresh data = arrived within the window.
- Stale data = arrived late.

## 3. Passing Case
The batch arrives before the cutoff time and passes validation.

## 4. Failure Case
The batch arrives after the cutoff and is flagged as stale.

## 5. Final Mental Model
Freshness checks ensure downstream reports are not built on late data.

## 6. Run Order
1. c004_data_freshness_demo.py
