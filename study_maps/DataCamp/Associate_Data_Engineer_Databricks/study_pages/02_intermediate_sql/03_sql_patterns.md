# Course 2: Intermediate SQL - SQL Patterns

Status: partial checkpoint

## Counting Patterns

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

## Filtering Patterns

```sql
SELECT title
FROM films
WHERE release_year > 1960;
```

```sql
SELECT title
FROM films
WHERE country = ''Japan'';
```

```sql
WHERE release_year BETWEEN 1990 AND 2000
  AND budget > 100000000
  AND language IN (''Spanish'', ''French'')
```

## Pattern Matching

```sql
WHERE name LIKE ''A%''
WHERE name LIKE ''%r''
WHERE name LIKE ''%an%''
WHERE name LIKE ''Ev_''
WHERE name NOT LIKE ''A%''
```

## NULL Completeness Patterns

```sql
SELECT name
FROM people
WHERE birthdate IS NULL;
```

```sql
SELECT COUNT(*) AS count_language_known
FROM films
WHERE language IS NOT NULL;
```

## Aggregation + Filter-First Pattern

```sql
SELECT AVG(budget) AS avg_budget
FROM films
WHERE release_year >= 2010;
```

## ROUND and Arithmetic

```sql
SELECT ROUND(AVG(facebook_likes), -2) AS avg_likes_rounded
FROM films;
```

```sql
SELECT gross - budget AS profit
FROM films;
```

```sql
SELECT 2.0 / 10.0 AS decimal_result;
```

## Alias Timing Safe Pattern

```sql
SELECT gross - budget AS profit
FROM films
WHERE gross - budget > 1000000;
```
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
