# 017 - Weather Observation Station 16

## Source

HackerRank SQL - Aggregation

## Problem Summary

Query the Western Longitude `LONG_W` for the row with the smallest Northern Latitude `LAT_N` that is greater than `38.7780`. Round the answer to `4` decimal places.

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
WHERE LAT_N > 38.7780
ORDER BY LAT_N ASC
LIMIT 1;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `WHERE LAT_N > 38.7780` filters to only rows above the target latitude.
- `ORDER BY LAT_N ASC` sorts remaining rows from smallest `LAT_N` to largest.
- `LIMIT 1` selects the row with the smallest `LAT_N` greater than `38.7780`.
- `ROUND(LONG_W, 4)` returns corresponding `LONG_W` rounded to `4` decimal places.

## Plain-English Explanation

This problem is not asking for the smallest `LONG_W`.

It asks for the `LONG_W` from the row where `LAT_N` is the smallest value still above `38.7780`.

So:
1. Filter rows by `LAT_N > 38.7780`
2. Sort those rows by `LAT_N` ascending
3. Take first row
4. Return rounded `LONG_W`

## Important Learning Notes

- `WHERE` filters rows before sorting.
- `ORDER BY LAT_N ASC` puts smallest valid latitude first.
- `LIMIT 1` keeps top row only.
- `ROUND(value, 4)` rounds to four decimal places.
- This is a min-condition row lookup pattern.

## Mistakes / Reminders

- Do not use `MIN(LONG_W)`; the min criterion is on `LAT_N`.
- Do not use `LAT_N >= 38.7780`; problem requires strictly greater than.
- Do not forget `ROUND(..., 4)`.
- Do not order by `LONG_W`.
- Keep this MySQL-style for HackerRank.
