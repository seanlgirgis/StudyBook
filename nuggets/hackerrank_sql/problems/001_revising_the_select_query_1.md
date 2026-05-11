# 001 - Revising the Select Query I

## Source

HackerRank SQL - Basic Select

## Problem Summary

Query the `NAME` field for all American cities in the `CITY` table where `POPULATION` is greater than `120000`. The `COUNTRYCODE` for America is `USA`.

## Schema

`CITY`
- `ID NUMBER`
- `NAME VARCHAR2(17)`
- `COUNTRYCODE VARCHAR2(3)`
- `DISTRICT VARCHAR2(20)`
- `POPULATION NUMBER`

## Accepted Solution

```sql
SELECT NAME
FROM CITY
WHERE COUNTRYCODE = 'USA'
  AND POPULATION > 120000;
```

## Review

The provided SQL solution is correct and should pass.

### What is good

- `SELECT NAME` returns only the requested column.
- `FROM CITY` uses the correct table.
- `WHERE` filters the rows.
- `COUNTRYCODE = 'USA'` limits results to American cities.
- `POPULATION > 120000` limits results to cities above the required population.
- `AND` means both conditions must be true.

## Plain-English Explanation

The query asks for city names only.

The `WHERE` clause applies two filters:

1. The city must be in the USA.
2. The city population must be larger than 120000.

Both filters must be true because they are connected with `AND`.

## Important Learning Notes

- `SELECT` chooses columns.
- `FROM` chooses the table.
- `WHERE` filters rows.
- String values use quotes: `'USA'`.
- Numeric comparisons do not use quotes: `POPULATION > 120000`.
- `AND` means both conditions are required.
- SQL statements commonly end with a semicolon.

## Mistakes / Reminders

- Do not use `SELECT *` because the problem asks only for `NAME`.
- Do not write `COUNTRYCODE = USA` without quotes.
- Do not use `>=` because the problem says larger than `120000`, which means `>` `120000`.
- Do not forget the `AND` between conditions.
