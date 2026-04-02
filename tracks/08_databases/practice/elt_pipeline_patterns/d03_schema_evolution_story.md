# Schema Evolution - Story Map

## 1. Story (form changes)
A store updates its order form. The old form uses `customer`, the new form uses `customer_name` and adds `currency`.

## 2. Core Concepts (street version)
- Schema evolution = fields added, removed, or renamed over time.
- Raw layer = keeps all versions for audit and replay.
- Curated layer = translates to a stable contract for consumers.

## 3. What Changes
New columns appear (currency), fields are renamed (customer -> customer_name), or types shift (amount text).

## 4. What Breaks
Downstream code that expects the old schema fails or drops rows.

## 5. How Curated Handles It
Curated maps old and new fields into a consistent schema and stamps a version for lineage.

## 6. Final Mental Model
Raw preserves change. Curated absorbs change so BI stays stable.

## 7. Run Order
1. c004_schema_evolution_demo.py
