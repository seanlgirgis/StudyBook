# 020 - Weather Observation Station 18

## Source

HackerRank SQL - Aggregation

## Problem Summary

Given points `P1(a, b)` and `P2(c, d)`, where:
- `a = minimum LAT_N`
- `b = minimum LONG_W`
- `c = maximum LAT_N`
- `d = maximum LONG_W`

Calculate the Manhattan Distance between `P1` and `P2` and round the result to `4` decimal places.

## Schema

`STATION`
- `ID NUMBER`
- `CITY VARCHAR2(21)`
- `STATE VARCHAR2(2)`
- `LAT_N NUMBER`
- `LONG_W NUMBER`

## Accepted Solution

```sql
SELECT ROUND(
    ABS(MIN(LAT_N)  - MAX(LAT_N)) +
    ABS(MIN(LONG_W) - MAX(LONG_W)),
    4
) AS manhattan_distance
FROM STATION;
```

## Alternative Simplified Solution

```sql
SELECT ROUND(
    (MAX(LAT_N) - MIN(LAT_N)) +
    (MAX(LONG_W) - MIN(LONG_W)),
    4
)
FROM STATION;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `MIN(LAT_N)` correctly gets `a`.
- `MIN(LONG_W)` correctly gets `b`.
- `MAX(LAT_N)` correctly gets `c`.
- `MAX(LONG_W)` correctly gets `d`.
- `ABS(...)` follows Manhattan Distance formula.
- Two absolute differences are added together.
- `ROUND(..., 4)` rounds final result to `4` decimal places.

## Plain-English Explanation

Manhattan Distance formula:
`|a - c| + |b - d|`

For this problem:
- `a = MIN(LAT_N)`
- `b = MIN(LONG_W)`
- `c = MAX(LAT_N)`
- `d = MAX(LONG_W)`

So compute both absolute differences, add them, then round to `4` decimals.

## Important Learning Notes

- `MIN(column)` returns smallest value.
- `MAX(column)` returns largest value.
- `ABS(value)` returns positive magnitude.
- `ROUND(value, 4)` rounds to `4` decimal places.
- Manhattan distance adds absolute differences.
- No `GROUP BY` is needed for one full-table aggregate result.

## Mistakes / Reminders

- Do not use Euclidean distance here.
- Do not use `SQRT` or `POWER` for this problem.
- Do not subtract latitude only; include longitude too.
- Do not forget `ABS` when writing formula directly.
- Do not forget `ROUND(..., 4)`.
- Do not `GROUP BY CITY` or `ID`.
