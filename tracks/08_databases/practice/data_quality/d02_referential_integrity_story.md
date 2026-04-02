# Referential Integrity Checks - Story Map

## 1. Story (guest list)
A club checks the guest list. If a name is not on the list, the guest cannot enter.

## 2. Core Concepts (street version)
- Parent table = customers.
- Child table = orders.
- Referential integrity = every order must reference a valid customer.

## 3. Failure Case
Orders with unknown customer_id values are orphan records and fail validation.

## 4. Passing Case
Once the missing customers are loaded, the orders pass the check.

## 5. Final Mental Model
Children cannot exist without parents. Validate references before loading curated tables.

## 6. Run Order
1. c003_referential_integrity_demo.py
