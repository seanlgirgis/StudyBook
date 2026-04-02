# Staging ? Raw ? Curated - Story Map

## 1. Story (warehouse receiving)
A retailer receives daily order files. The loading dock drops boxes in staging, the storeroom keeps a clean copy of everything in raw, and the showroom only displays validated products in curated.

## 2. Core Concepts (street version)
- Staging = the landing zone for inbound files.
- Raw = standardized schema with full history preserved.
- Curated = business-ready tables with quality rules applied.

## 3. Staging (what it does)
Staging keeps file boundaries and raw rows. No transformations yet. The goal is safe landing and easy replay.

## 4. Raw (what it does)
Raw standardizes column names and basic types but keeps every row. This is the audit trail and recovery layer.

## 5. Curated (what it does)
Curated applies business rules: valid customers, paid status, positive amounts, and deduplication. This is what BI and dashboards read.

## 6. Failure Mode (why layers matter)
If curated logic changes, you can re-run from raw. If a file arrives late, you can reprocess from staging.

## 7. Final Mental Model
Staging catches the delivery, raw preserves history, curated publishes the trusted view.

## 8. Run Order
1. c001_staging_raw_curated_demo.py
