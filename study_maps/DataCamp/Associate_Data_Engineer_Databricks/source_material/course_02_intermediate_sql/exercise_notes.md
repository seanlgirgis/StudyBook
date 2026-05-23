# Course 2 Exercise Notes (Checkpoint)

Status: partial checkpoint

## Captured Exercises

1. Distinct count for 90s English teen-friendly films

```sql
SELECT COUNT(DISTINCT title) AS nineties_english_films_for_teens
FROM films
WHERE release_year BETWEEN 1990 AND 1999
  AND language = ''English''
  AND certification IN (''G'', ''PG'', ''PG-13'');
```

2. Language completeness check using NULL logic

```sql
SELECT COUNT(*) AS count_language_known
FROM films
WHERE language IS NOT NULL;
```

Equivalent pattern:

```sql
SELECT COUNT(language) AS count_language_known
FROM films;
```

## Sean Notes (Important)

- COUNT(DISTINCT country) was new/important.
- BETWEEN being inclusive needed explicit attention.
- ROUND(value, negative_number) behavior was clarified and retained.
- Integer division trap (`2 / 10` -> `0` in integer context) was important.
- Alias timing in WHERE was important (`WHERE` runs before `SELECT`).

## Mistake/Trap Notes

- Trap:

```sql
SELECT DISTINCT COUNT(country)
FROM films;
```

- Why trap: counts non-NULL country values, then DISTINCT applies to one aggregate result.
- Correct unique list:

```sql
SELECT DISTINCT country
FROM films;
```

- Correct unique count:

```sql
SELECT COUNT(DISTINCT country) AS count_distinct_countries
FROM films;
```
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
