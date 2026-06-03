# CODE SNIPPETS - SQL COURSE 02

Status: accumulating (partial)

## Counting

```sql
SELECT COUNT(*) AS row_count
FROM people;
```

```sql
SELECT COUNT(birthdate) AS count_birthdate
FROM people;
```

```sql
SELECT COUNT(DISTINCT country) AS count_distinct_countries
FROM films;
```

## Filtering and Ranges

```sql
SELECT title, release_year
FROM films
WHERE release_year BETWEEN 1990 AND 2000;
```

```sql
SELECT COUNT(DISTINCT title) AS nineties_english_films_for_teens
FROM films
WHERE release_year BETWEEN 1990 AND 1999
  AND language = ''English''
  AND certification IN (''G'', ''PG'', ''PG-13'');
```

## NULL Checks

```sql
SELECT COUNT(*) AS count_language_known
FROM films
WHERE language IS NOT NULL;
```

## Aggregates and Rounding

```sql
SELECT AVG(budget) AS avg_budget
FROM films
WHERE release_year >= 2010;
```

```sql
SELECT ROUND(AVG(facebook_likes), -2) AS avg_likes_rounded
FROM films;
```

## Arithmetic and Alias Timing

```sql
SELECT gross - budget AS profit
FROM films
WHERE gross - budget > 1000000;
```

```sql
SELECT 2.0 / 10.0 AS decimal_result;
```
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
