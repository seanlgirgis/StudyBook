# Troubleshooting Notes

## Relation does not exist

Set the schema first:

```sql
SET search_path TO joining_data_lab;
```

## Duplicate rows after a join

Check whether:
- the key is unique on either side
- a time field such as `year` is missing from the join condition
- the relationship is legitimately one-to-many

## LEFT JOIN appears to behave like INNER JOIN

Inspect filters on right-side fields in the `WHERE` clause. Move match-eligibility filters into `ON` when unmatched left rows must remain.

## NOT IN returns no rows

Check whether the subquery returns NULL. Prefer `NOT EXISTS` or filter NULL explicitly.

## FROM subquery error

Ensure the derived table has an alias:

```sql
FROM (
    SELECT ...
) AS derived_table
```
