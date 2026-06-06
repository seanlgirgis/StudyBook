# Joining Data in SQL — Lab Run Book

## Lab purpose

This lab turns the DataCamp exercises into one local, repeatable PostgreSQL practice environment.

## Dataset design

The lab intentionally includes:

- countries with and without cities
- countries with and without economy rows
- an economy row without a matching country
- multiple population years
- duplicate-compatible rows for `UNION ALL`
- a `NULL` foreign-key value
- city names that are also country names
- countries with multiple languages

## Practice checkpoints

### Chapter 1
- Write a two-table INNER JOIN.
- Use aliases consistently.
- Compare `ON` and `USING`.
- Join three tables using country and year.

### Chapter 2
- Preserve unmatched countries with LEFT JOIN.
- Compare right-side filters in `ON` and `WHERE`.
- Reconcile two sources with FULL JOIN.
- Estimate CROSS JOIN row counts.
- Compare two years using a self join and conditional aggregation.

### Chapter 3
- Compare `UNION` and `UNION ALL`.
- Find common rows with `INTERSECT`.
- Find first-only rows with `EXCEPT`.

### Chapter 4
- Write semi joins and anti joins.
- Demonstrate the `NOT IN`/`NULL` trap.
- Use subqueries in `WHERE`, `SELECT`, and `FROM`.

## Completion evidence

Record:
- queries run
- row counts observed
- mistakes corrected
- patterns worth remembering
