# Dynamic SQL - Story Map

## 1. Story
You run a metrics API. The client can pick which columns to return and which filters to apply. You cannot hardcode every combination.

## 2. What dynamic SQL is
Building a SQL statement at runtime based on user or system inputs.

## 3. Why teams use it
- Flexible reporting endpoints
- Optional filters and columns
- Multi-tenant or configurable datasets

## 4. Where it is useful
- Search and filtering UIs
- Ad-hoc analytics tooling
- Admin dashboards with many options

## 5. Where it becomes dangerous
- SQL injection if you blindly concatenate strings
- Hard-to-debug query plans if everything is dynamic

## 6. Why parameterization and allowlists matter
Parameters keep values separate from the SQL text.  
Allowlists ensure only known-good column names and filters are used.

## 7. Safe vs unsafe intuition
Unsafe: "SELECT " + user_input + " FROM ..."  
Safe: pick columns from an allowlist, then bind values.

## 8. Final mental model
Dynamic SQL is a power tool: use guard rails or you will cut yourself.

## 9. Run Order
1. c104_dynamic_sql_demo.py
