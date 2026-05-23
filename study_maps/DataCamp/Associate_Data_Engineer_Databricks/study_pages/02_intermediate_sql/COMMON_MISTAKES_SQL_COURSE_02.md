# COMMON MISTAKES - SQL COURSE 02

Status: accumulating (partial)

## 1) DISTINCT + COUNT confusion

Wrong:

```sql
SELECT DISTINCT COUNT(country)
FROM films;
```

Correct:

```sql
SELECT COUNT(DISTINCT country) AS count_distinct_countries
FROM films;
```

## 2) NULL comparison with equals

Wrong:

```sql
WHERE language = NULL
```

Correct:

```sql
WHERE language IS NULL
```

## 3) BETWEEN boundary misunderstanding

Mistake:
- Treating `BETWEEN` as exclusive.

Correction:
- `BETWEEN a AND b` includes both `a` and `b`.

## 4) Integer division surprise

Wrong expectation:

```sql
SELECT 2 / 10;
```

Safer form:

```sql
SELECT 2.0 / 10.0;
```

## 5) Alias used too early

Wrong:

```sql
SELECT gross - budget AS profit
FROM films
WHERE profit > 1000000;
```

Correct:

```sql
SELECT gross - budget AS profit
FROM films
WHERE gross - budget > 1000000;
```
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
