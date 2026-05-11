# 005 - Weather Observation Station 6

## Source

HackerRank SQL - Basic Select

## Problem Summary

Query the list of `CITY` names from `STATION` where the city name starts with a vowel. The result cannot contain duplicates.

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
WHERE UPPER(SUBSTRING(CITY FROM 1 FOR 1)) IN ('A', 'E', 'I', 'O', 'U');
```

## Alternative MySQL Solution

```sql
SELECT DISTINCT CITY
FROM STATION
WHERE UPPER(LEFT(CITY, 1)) IN ('A', 'E', 'I', 'O', 'U');
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `SELECT DISTINCT CITY` returns city names and removes duplicates.
- `FROM STATION` uses the correct table.
- `SUBSTRING(CITY FROM 1 FOR 1)` extracts the first character of `CITY`.
- `UPPER(...)` makes the vowel check safe for lowercase or mixed-case city names.
- `IN ('A', 'E', 'I', 'O', 'U')` checks whether the first character is a vowel.

## Plain-English Explanation

The problem asks for city names that start with a vowel.

To solve this:

1. Take the first character of `CITY`.
2. Convert it to uppercase.
3. Check whether it is `A`, `E`, `I`, `O`, or `U`.
4. Use `DISTINCT` so duplicate city names are removed.

## Important Learning Notes

- `DISTINCT` removes duplicates.
- `SUBSTRING(CITY FROM 1 FOR 1)` extracts the first letter in MySQL.
- `LEFT(CITY, 1)` is a shorter MySQL way to get the first letter.
- `UPPER()` converts text to uppercase.
- `IN (...)` checks whether a value is inside a list.
- String values must be quoted.

## Mistakes / Reminders

- Do not forget `DISTINCT`.
- Do not check the whole `CITY` value; only check the first character.
- Do not use `SELECT *` because the problem asks only for `CITY` names.
- Do not forget quotes around vowels.
- In MySQL, `LEFT(CITY, 1)` is often simpler than `SUBSTRING`.
