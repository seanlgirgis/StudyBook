# 021 - Weather Observation Station 19

## Source

HackerRank SQL - Aggregation

## Problem Summary

Given points `P1(a, c)` and `P2(b, d)`, where:
- `a = minimum LAT_N`
- `b = maximum LAT_N`
- `c = minimum LONG_W`
- `d = maximum LONG_W`

Calculate the Euclidean Distance between `P1` and `P2` and round the result to `4` decimal places.

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
    SQRT(
        POW(MAX(LAT_N)  - MIN(LAT_N), 2) +
        POW(MAX(LONG_W) - MIN(LONG_W), 2)
    ), 4)
FROM STATION;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `MIN(LAT_N)` correctly gets minimum latitude.
- `MAX(LAT_N)` correctly gets maximum latitude.
- `MIN(LONG_W)` correctly gets minimum longitude.
- `MAX(LONG_W)` correctly gets maximum longitude.
- `POW(value, 2)` squares each coordinate difference.
- `SQRT(...)` applies Euclidean distance formula.
- `ROUND(..., 4)` rounds final result to `4` decimal places.
- No `GROUP BY` is needed because this is one full-table aggregate result.

## Plain-English Explanation

Euclidean distance formula:
`sqrt((x2 - x1)^2 + (y2 - y1)^2)`

In this problem:
- `x1 = MIN(LAT_N)`
- `x2 = MAX(LAT_N)`
- `y1 = MIN(LONG_W)`
- `y2 = MAX(LONG_W)`

So compute both squared deltas, add them, take square root, then round to `4` decimals.

## Important Learning Notes

- `MIN(column)` returns smallest value.
- `MAX(column)` returns largest value.
- `POW(value, 2)` squares a value.
- `SQRT(value)` returns square root.
- `ROUND(value, 4)` rounds to `4` decimal places.
- Euclidean distance differs from Manhattan distance.
- Manhattan uses absolute additions; Euclidean uses squares + root.

## Mistakes / Reminders

- Do not use Manhattan distance for this problem.
- Do not forget `SQRT`.
- Do not forget `POW(..., 2)` for both coordinate differences.
- Do not forget `ROUND(..., 4)`.
- Do not `GROUP BY CITY` or `ID`.
- Keep this MySQL-style for HackerRank.
