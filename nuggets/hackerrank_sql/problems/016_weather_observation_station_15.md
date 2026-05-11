# 016 - Weather Observation Station 15

## Source

HackerRank SQL - Aggregation

## Problem Summary

Query the Western Longitude `LONG_W` for the row with the largest Northern Latitude `LAT_N` that is less than `137.2345`. Round the answer to `4` decimal places.

## Schema

`STATION`
- `ID NUMBER`
- `CITY VARCHAR2(21)`
- `STATE VARCHAR2(2)`
- `LAT_N NUMBER`
- `LONG_W NUMBER`

## Accepted Solution

```sql
SELECT ROUND(LONG_W, 4)
FROM STATION
WHERE LAT_N < 137.2345
ORDER BY LAT_N DESC
LIMIT 1;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `WHERE LAT_N < 137.2345` filters to only rows below the target latitude.
- `ORDER BY LAT_N DESC` sorts remaining rows from largest `LAT_N` to smallest.
- `LIMIT 1` selects the row with the largest `LAT_N` under `137.2345`.
- `ROUND(LONG_W, 4)` returns corresponding `LONG_W` rounded to `4` decimal places.

## Plain-English Explanation

This problem is not asking for maximum `LONG_W`.

It asks for the `LONG_W` from the row where `LAT_N` is the largest value still below `137.2345`.

So:
1. Filter rows by `LAT_N < 137.2345`
2. Sort those rows by `LAT_N` descending
3. Take first row
4. Return rounded `LONG_W`

## Important Learning Notes

- `WHERE` filters rows before sorting.
- `ORDER BY LAT_N DESC` puts largest valid latitude first.
- `LIMIT 1` keeps top row only.
- `ROUND(value, 4)` rounds to four decimal places.
- This is a max-condition row lookup pattern.

## Mistakes / Reminders

- Do not use `MAX(LONG_W)`; the max criterion is on `LAT_N`.
- Do not use `LAT_N <= 137.2345`; problem requires strictly less than.
- Do not forget `ROUND(..., 4)`.
- Do not order by `LONG_W`.
- Keep this MySQL-style for HackerRank.
