# Course 2: Intermediate SQL - Exercise Mistakes

Status: partial checkpoint

## Mistake: DISTINCT around COUNT instead of inside COUNT

Wrong:

```sql
SELECT DISTINCT COUNT(country)
FROM films;
```

Correction:

```sql
SELECT COUNT(DISTINCT country) AS count_distinct_countries
FROM films;
```

## Mistake: Treating BETWEEN as exclusive

Wrong assumption:
- `BETWEEN 1990 AND 2000` excludes endpoints.

Correction:
- `BETWEEN` is inclusive of both ends.

## Mistake: Using `= NULL`

Wrong:

```sql
WHERE birthdate = NULL
```

Correction:

```sql
WHERE birthdate IS NULL
```

## Mistake: Integer division surprise

Trap:

```sql
SELECT 2 / 10;
```

Correction:

```sql
SELECT 2.0 / 10.0;
```

## Mistake: Using alias in WHERE

Wrong:

```sql
SELECT gross - budget AS profit
FROM films
WHERE profit > 1000000;
```

Correction:

```sql
SELECT gross - budget AS profit
FROM films
WHERE gross - budget > 1000000;
```
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
