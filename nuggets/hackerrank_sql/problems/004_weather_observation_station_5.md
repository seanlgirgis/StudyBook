# 004 - Weather Observation Station 5

## Source

HackerRank SQL - Basic Select

## Problem Summary

Query the two cities in `STATION` with the shortest and longest `CITY` names, along with their respective name lengths. If there is more than one city with the same shortest or longest length, choose the city that comes first alphabetically.

## Schema

`STATION`
- `ID NUMBER`
- `CITY VARCHAR2(21)`
- `STATE VARCHAR2(2)`
- `LAT_N NUMBER`
- `LONG_W NUMBER`

## Accepted Solution

```sql
(SELECT CITY, LENGTH(CITY)
FROM STATION
ORDER BY LENGTH(CITY) ASC, CITY ASC
LIMIT 1)
UNION ALL
(SELECT CITY, LENGTH(CITY)
FROM STATION
ORDER BY LENGTH(CITY) DESC, CITY ASC
LIMIT 1);
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass in MySQL.

### What is good

- The first `SELECT` finds the shortest city name.
- `LENGTH(CITY)` calculates the number of characters in the city name.
- `ORDER BY LENGTH(CITY) ASC` sorts shortest names first.
- `CITY ASC` handles the alphabetical tie-breaker.
- `LIMIT 1` returns only the first matching city.
- The second `SELECT` finds the longest city name.
- `ORDER BY LENGTH(CITY) DESC` sorts longest names first.
- `UNION ALL` combines the shortest-row result and longest-row result.

## Plain-English Explanation

The problem asks for two rows:

1. The city with the shortest name and its length.
2. The city with the longest name and its length.

If there is a tie, choose the city that appears first alphabetically.

For shortest:
`ORDER BY LENGTH(CITY) ASC, CITY ASC`

For longest:
`ORDER BY LENGTH(CITY) DESC, CITY ASC`

The `ASC` or `DESC` on `LENGTH(CITY)` controls shortest versus longest.
The `CITY ASC` part handles alphabetical tie-breaking.

## Important Learning Notes

- `LENGTH(CITY)` returns the number of characters in `CITY`.
- `ORDER BY` can sort by multiple expressions.
- `ASC` means ascending order.
- `DESC` means descending order.
- `LIMIT 1` returns one row.
- `UNION ALL` combines results from two `SELECT` queries.
- `UNION ALL` keeps both rows without trying to remove duplicates.

## Sample Output Pattern

`ABC 3`
`PQRS 4`

## Mistakes / Reminders

- Do not use only `MIN(LENGTH(CITY))` or `MAX(LENGTH(CITY))` without returning the matching `CITY`.
- Do not forget the alphabetical tie-breaker.
- For longest, use `LENGTH(CITY) DESC` but still `CITY ASC`.
- Use `UNION ALL` because the problem wants two query results.
- In MySQL, `LENGTH(CITY)` is acceptable for this HackerRank problem.
- Do not use `ORDER BY` only on `CITY`, because the main requirement is shortest/longest length.
