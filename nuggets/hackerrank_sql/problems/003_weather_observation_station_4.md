# 003 - Weather Observation Station 4

## Source

HackerRank SQL - Basic Select

## Problem Summary

Find the difference between the total number of `CITY` entries in `STATION` and the number of distinct `CITY` entries.

## Schema

`STATION`
- `ID NUMBER`
- `CITY VARCHAR2(21)`
- `STATE VARCHAR2(2)`
- `LAT_N NUMBER`
- `LONG_W NUMBER`

## Accepted Solution

```sql
SELECT COUNT(CITY) - COUNT(DISTINCT CITY)
FROM STATION;
```

## Provided Solution Reviewed

The provided CTE solution is logically correct:

```sql
WITH CityCounts AS (
    SELECT
        COUNT(CITY) AS total_cities,
        COUNT(DISTINCT CITY) AS unique_cities
    FROM STATION
)
SELECT (total_cities - unique_cities) AS city_difference
FROM CityCounts;
```

However, the direct aggregate expression is simpler and better for HackerRank:
`COUNT(CITY) - COUNT(DISTINCT CITY)`

### What is good

- `COUNT(CITY)` counts all `CITY` entries.
- `COUNT(DISTINCT CITY)` counts unique `CITY` names.
- Subtracting the second from the first gives the duplicate count.
- No `WHERE` clause is needed because the problem asks across the whole table.

## Plain-English Explanation

If the `CITY` column has:

`New York`
`New York`
`Bengalaru`

Then:

`COUNT(CITY) = 3`

But:

`COUNT(DISTINCT CITY) = 2`

So:

`3 - 2 = 1`

That means there is `1` duplicate city entry beyond the unique city names.

## Important Learning Notes

- `COUNT(column)` counts non-null rows in that column.
- `COUNT(DISTINCT column)` counts unique non-null values.
- You can subtract aggregate results directly in `SELECT`.
- No `GROUP BY` is needed because the query returns one overall result.
- A CTE works logically, but this problem only needs one `SELECT`.

## Mistakes / Reminders

- Do not use `SELECT CITY` because the problem asks for a count difference.
- Do not `GROUP BY CITY`.
- Do not use `DISTINCT` alone; use `COUNT(DISTINCT CITY)`.
- Do not add a `WHERE` filter.
- Keep the query simple.
