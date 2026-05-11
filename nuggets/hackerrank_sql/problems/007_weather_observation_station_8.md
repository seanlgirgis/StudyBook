# 007 - Weather Observation Station 8

## Source

HackerRank SQL - Basic Select

## Problem Summary

Query the list of `CITY` names from `STATION` where the city name starts with a vowel and ends with a vowel. The result cannot contain duplicates.

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
WHERE LOWER(LEFT(CITY, 1)) IN ('a', 'e', 'i', 'o', 'u')
  AND LOWER(RIGHT(CITY, 1)) IN ('a', 'e', 'i', 'o', 'u');
```

## Provided Solution Reviewed

The provided SQL idea is correct but had a small syntax issue.

The original query correctly checked the last character using:
`LOWER(RIGHT(CITY, 1)) IN ('a', 'e', 'i', 'o', 'u')`

But the first-character condition was missing the `IN` keyword:
`LOWER(LEFT(CITY, 1)) ('a', 'e', 'i', 'o', 'u')`

The corrected condition is:
`LOWER(LEFT(CITY, 1)) IN ('a', 'e', 'i', 'o', 'u')`

### What is good

- `SELECT DISTINCT CITY` removes duplicate city names.
- `LEFT(CITY, 1)` checks the first character.
- `RIGHT(CITY, 1)` checks the last character.
- `LOWER(...)` makes the check case-insensitive.
- `IN (...)` checks whether the character is one of the vowels.
- `AND` requires both the first and last character to be vowels.

## Plain-English Explanation

This problem asks for city names that start and end with a vowel.

The first vowel check is:
`LOWER(LEFT(CITY, 1)) IN ('a', 'e', 'i', 'o', 'u')`

The last vowel check is:
`LOWER(RIGHT(CITY, 1)) IN ('a', 'e', 'i', 'o', 'u')`

Because both conditions must be true, we connect them with `AND`.

## Important Learning Notes

- `LEFT(CITY, 1)` gets the first character.
- `RIGHT(CITY, 1)` gets the last character.
- `LOWER()` handles uppercase/lowercase safely.
- `IN (...)` is required before the vowel list.
- `AND` means both conditions must be true.
- `DISTINCT` removes duplicates.

## Mistakes / Reminders

- Do not forget the second `IN`.
- Do not use `OR` because the problem requires both first and last characters to be vowels.
- Do not use `SELECT *` because the problem asks only for `CITY`.
- Do not forget `DISTINCT`.
- Keep this MySQL-style for HackerRank.
