# 006 - Weather Observation Station 7

## Source

HackerRank SQL - Basic Select

## Problem Summary

Query the list of `CITY` names from `STATION` where the city name ends with a vowel. The result cannot contain duplicates.

## Schema

`STATION`
- `ID NUMBER`
- `CITY VARCHAR2(21)`
- `STATE VARCHAR2(2)`
- `LAT_N NUMBER`
- `LONG_W NUMBER`

## Accepted Solution

```sql
SELECT DISTINCT CITY
FROM STATION
WHERE LOWER(RIGHT(CITY, 1)) IN ('a', 'e', 'i', 'o', 'u');
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `SELECT DISTINCT CITY` returns city names and removes duplicates.
- `FROM STATION` uses the correct table.
- `RIGHT(CITY, 1)` extracts the last character of `CITY`.
- `LOWER(...)` makes the vowel check case-insensitive.
- `IN ('a', 'e', 'i', 'o', 'u')` checks whether the last character is a vowel.

## Plain-English Explanation

The problem asks for city names that end with a vowel.

To solve this:

1. Take the last character of `CITY`.
2. Convert it to lowercase.
3. Check whether it is `a`, `e`, `i`, `o`, or `u`.
4. Use `DISTINCT` so duplicate city names are removed.

## Important Learning Notes

- `DISTINCT` removes duplicates.
- `RIGHT(CITY, 1)` extracts the last character in MySQL.
- `LOWER()` converts text to lowercase.
- `IN (...)` checks whether a value is inside a list.
- String values must be quoted.
- This is MySQL-style SQL.

## Mistakes / Reminders

- Do not forget `DISTINCT`.
- Do not check the first character for this problem; this one asks for names ending with vowels.
- Do not use `LIKE '%[AEIOUaeiou]'` in MySQL because MySQL `LIKE` does not support bracket character groups.
- Do not use `SELECT *` because the problem asks only for `CITY` names.
- Keep `CITY` and `STATION` spelled exactly as the schema shows.
