# Null and Type Checks - Story Map

## 1. Story (airport security)
Passengers with missing IDs or wrong documents are stopped before boarding.

## 2. Core Concepts (street version)
- Null checks = required fields must not be empty.
- Type checks = values must be the expected type.
- Failing rows = blocked or quarantined.

## 3. Passing Case
Rows with complete fields and correct types proceed to curated tables.

## 4. Failing Case
Rows with missing values or wrong types are flagged.

## 5. Final Mental Model
Nulls and type mismatches are basic quality gates that prevent bad data downstream.

## 6. Run Order
1. c002_null_type_checks_demo.py
