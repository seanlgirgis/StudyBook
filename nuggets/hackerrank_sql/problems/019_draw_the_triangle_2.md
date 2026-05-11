# 019 - Draw The Triangle 2

## Source

HackerRank SQL - Alternative Queries

## Problem Summary

Print the pattern `P(20)`, where the first row contains `1` star, the second row contains `2` stars, and so on up to `20` stars.

## Accepted Solution

```sql
SELECT REPEAT('* ', n)
FROM (
    SELECT @rownum := @rownum + 1 AS n
    FROM information_schema.columns, (SELECT @rownum := 0) r
    LIMIT 20
) numbered;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `REPEAT('* ', n)` prints `n` stars on each row.
- `@rownum := @rownum + 1` generates row numbers.
- `(SELECT @rownum := 0)` initializes the counter.
- `information_schema.columns` is used as a convenient source of many rows.
- `LIMIT 20` makes sure exactly `20` rows are generated.
- Pattern increases from `1` star to `20` stars.

## Plain-English Explanation

SQL does not have a simple for-loop in a normal `SELECT`.

So MySQL variables are used to generate:
`1, 2, 3, ..., 20`

Then for each `n`, print stars with:
`REPEAT('* ', n)`

- `n = 1` prints `1` star
- `n = 2` prints `2` stars
- `n = 20` prints `20` stars

## Important Learning Notes

- `REPEAT(text, count)` repeats text.
- MySQL variables start with `@`.
- `:=` is assignment in MySQL.
- `@rownum := @rownum + 1` acts like a counter.
- `information_schema.columns` is only a row-generation helper.
- `LIMIT 20` restricts generated rows to `20`.
- This is a MySQL sequence-generation trick.

## Beginner-Friendly Commented Version

```sql
-- Triangle 2 prints increasing rows:
-- row 1: 1 star
-- row 2: 2 stars
-- ...
-- row 20: 20 stars

SELECT
    REPEAT('* ', n)
FROM (
    SELECT
        @rownum := @rownum + 1 AS n
    FROM
        information_schema.columns,
        (SELECT @rownum := 0) r
    LIMIT 20
) numbered;
```

## Comparison With Triangle 1

- Triangle 1 decreases stars, so it uses `21 - n`.
- Triangle 2 increases stars, so it uses `n` directly.

Triangle 1:
`REPEAT('* ', 21 - n)`

Triangle 2:
`REPEAT('* ', n)`

## Mistakes / Reminders

- Do not use `21 - n` for Triangle 2; that would print decreasing rows.
- Do not forget `LIMIT 20`.
- Do not forget the space after the star: `'* '`.
- Do not confuse `:=` assignment with `=` comparison.
- Do not worry about real contents of `information_schema.columns`; it is only used to generate rows.
- Keep this MySQL-style for HackerRank.
