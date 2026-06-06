# Troubleshooting

## Relation does not exist

Run:

```sql
SET search_path TO data_manipulation_lab;
```

or qualify tables:

```sql
SELECT * FROM data_manipulation_lab.match;
```

## Duplicate rows

Check join keys and confirm that `team_api_id` is unique.

## Unexpected LEFT JOIN behavior

A condition on the right-side table in `WHERE` can remove NULL-extended rows.
Move the condition into `ON` when unmatched left rows must remain.

## Window results look unstable

Add a deterministic tie-breaker:

```sql
ORDER BY date, id
```

## NOT IN returns no rows

Check whether the subquery contains NULL. Prefer `NOT EXISTS` for anti-join logic.
