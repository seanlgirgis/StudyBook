# 018 - Draw The Triangle 1

## Source

HackerRank SQL - Alternative Queries

## Problem Summary

Print the pattern `P(20)`, where the first row contains `20` stars, the second row contains `19` stars, and so on down to `1` star.

## Accepted Solution

```sql
SELECT REPEAT('* ', 21 - n)
FROM (
    SELECT @rownum := @rownum + 1 AS n
    FROM information_schema.columns,
         (SELECT @rownum := 0) init
    LIMIT 20
) numbers;
```

## Provided Solution Reviewed

The provided solution is valid MySQL-style SQL and should pass.

Provided solution:

```sql
SET @rows = 20;

SELECT REPEAT('* ', @rows - n + 1)
FROM (
    SELECT @rownum := @rownum + 1 AS n
    FROM information_schema.columns,
         (SELECT @rownum := 0) r
    LIMIT 20
) numbered;
```

### What is good

- `@rows` stores the desired number of rows.
- `@rownum := @rownum + 1` generates row numbers.
- `LIMIT 20` limits output to exactly `20` rows.
- `REPEAT('* ', @rows - n + 1)` prints decreasing star counts.
- First row prints `20` stars.
- Last row prints `1` star.

## Plain-English Explanation

SQL does not have a simple loop like Python, so the query uses a MySQL variable to generate numbers.

`@rownum := @rownum + 1` creates:
`1, 2, 3, ..., 20`

Then:
`REPEAT('* ', 21 - n)`

- `n = 1` gives `20` stars
- `n = 2` gives `19` stars
- `n = 20` gives `1` star

## Important Learning Notes

- `REPEAT(text, count)` repeats text.
- MySQL variables start with `@`.
- `:=` assigns a value to a MySQL variable.
- `information_schema.columns` is used only as a convenient source of many rows.
- `LIMIT 20` ensures only `20` generated rows are used.
- This is a sequence-generation workaround in MySQL.

## Beginner-Friendly Expanded Version

```sql
SET @total_rows = 20;
SET @row_number = 0;

SELECT
    REPEAT('* ', @total_rows - @row_number + 1)
FROM
    information_schema.columns
WHERE
    (@row_number := @row_number + 1) <= @total_rows;
```

## Mistakes / Reminders

- Do not print increasing stars for Triangle 1; this one requires decreasing rows.
- Do not forget the space after the star: `'* '`.
- Do not forget `LIMIT 20` when using `information_schema.columns` in this pattern.
- Do not confuse `:=` assignment with `=` comparison.
- `information_schema.columns` is not challenge data; it is only used to generate rows.
- Keep this MySQL-style for HackerRank.
