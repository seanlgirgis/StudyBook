# Data Contracts - Story Map

## 1. Story (restaurant menu)
A kitchen publishes a menu (the contract). Servers and guests depend on that menu staying consistent.

## 2. Core Concepts (street version)
- Data contract = shared agreement on fields, types, and allowed values.
- Producer = publishes data that must honor the contract.
- Consumer = builds logic that assumes the contract is true.

## 3. What It Includes
Required columns, allowed values, and meaning of each field.

## 4. What Breaks
If the producer changes fields or values, consumers can fail or compute wrong results.

## 5. How Pipelines Handle It
Validate incoming batches against the contract before loading curated tables.

## 6. Final Mental Model
Contracts are promises between teams. Validation enforces trust.

## 7. Run Order
1. c005_data_contracts_demo.py
