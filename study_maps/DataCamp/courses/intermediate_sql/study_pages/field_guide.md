# Intermediate SQL — Field Guide

## Course Status

- **Platform status:** PASSED
- **Documentation coverage:** COMPLETE
- **Lab coverage:** STRONG
- **Recall confidence:** STRONG
- **Interview readiness:** NEEDS REPETITION

## Purpose

This field guide is the whole-course memory map for the DataCamp **Intermediate SQL** course.

Use it to:

- review the major SQL patterns from all four chapters
- jump to the detailed chapter guides
- remember common traps
- translate course concepts into interview-safe language
- reconnect concepts to the local PostgreSQL lab

---

## Course Navigation

### Detailed chapter guides

1. [Chapter 1 — Selecting Data](chapter_01_selecting_data_field_guide.html)
2. [Chapter 2 — Filtering Records](chapter_02_filtering_records_field_guide.html)
3. [Chapter 3 — Aggregate Functions](chapter_03_aggregate_functions_field_guide.html)
4. [Chapter 4 — Sorting and Grouping](chapter_04_sorting_and_grouping_field_guide.html)

### Supporting resources

- [SQL Quick Lookup](sql_quick_lookup.html)
- [Course Home](../index.html)
- [Lab Run Book](../lab/lab_run_book.md)
- [How to Run the Lab](../lab/00_how_to_run.md)

---

# 1. Selecting Data

## Core query pattern

```sql
SELECT column_name
FROM table_name;
```

- `SELECT` chooses the output columns or expressions.
- `FROM` identifies the source table.

Example:

```sql
SELECT title,
       release_year,
       country
FROM films;
```

## Selecting all columns

```sql
SELECT *
FROM films;
```

Use `SELECT *` for quick exploration. Prefer named columns for reusable or production SQL.

## DISTINCT

`DISTINCT` removes duplicate rows from the result.

```sql
SELECT DISTINCT country
FROM films;
```

With multiple columns, it returns unique combinations:

```sql
SELECT DISTINCT country,
                language
FROM films;
```

## COUNT forms

### Count all rows

```sql
SELECT COUNT(*)
FROM films;
```

### Count non-NULL values

```sql
SELECT COUNT(budget)
FROM films;
```

### Count unique non-NULL values

```sql
SELECT COUNT(DISTINCT country)
FROM films;
```

### Count a non-NULL expression

```sql
SELECT COUNT(budget + gross)
FROM films;
```

The expression is counted only when its result is not `NULL`.

### Conditional count with CASE

```sql
SELECT COUNT(
         CASE
           WHEN country = 'Canada' THEN 1
         END
       ) AS canadian_films
FROM films;
```

### Conditional count with PostgreSQL FILTER

```sql
SELECT COUNT(*) FILTER (
         WHERE country = 'Canada'
       ) AS canadian_films
FROM films;
```

### Count distinct combinations in PostgreSQL

```sql
SELECT COUNT(DISTINCT (country, language))
FROM films;
```

## Chapter 1 lab evidence

```text
COUNT(*)                 = 16
COUNT(budget)            = 15
COUNT(DISTINCT country)  = 10
```

This proves:

- `COUNT(*)` counts rows.
- `COUNT(column)` ignores `NULL`.
- `COUNT(DISTINCT column)` ignores `NULL` and duplicates.

---

# 2. Filtering Records

## WHERE

`WHERE` filters rows before they reach the final result.

```sql
SELECT title,
       release_year
FROM films
WHERE release_year = 2020;
```

## Comparison operators

| Operator | Meaning |
|---|---|
| `=` | Equal to |
| `<>` or `!=` | Not equal to |
| `>` | Greater than |
| `>=` | Greater than or equal to |
| `<` | Less than |
| `<=` | Less than or equal to |

Example:

```sql
SELECT title,
       imdb_score
FROM films
WHERE imdb_score >= 7.5;
```

## Text filtering

Text values use single quotes.

```sql
SELECT title,
       country
FROM films
WHERE country = 'Canada';
```

PostgreSQL uses double quotes for quoted identifiers, not text values.

## AND

All conditions must be true.

```sql
SELECT title,
       country,
       imdb_score
FROM films
WHERE country = 'Canada'
  AND imdb_score >= 7.0;
```

## OR

At least one condition must be true.

```sql
SELECT title,
       country
FROM films
WHERE country = 'Canada'
   OR country = 'Germany';
```

## Parentheses with AND and OR

```sql
SELECT title,
       country,
       release_year
FROM films
WHERE (country = 'Canada' OR country = 'Germany')
  AND release_year >= 2019;
```

Memory rule:

```text
AND narrows.
OR broadens.
Parentheses make the intended logic explicit.
```

## BETWEEN

`BETWEEN` is inclusive of both boundaries.

```sql
SELECT title,
       release_year
FROM films
WHERE release_year BETWEEN 2018 AND 2021;
```

Equivalent form:

```sql
WHERE release_year >= 2018
  AND release_year <= 2021
```

## LIKE

Pattern matching with `%` and `_`.

```sql
SELECT title
FROM films
WHERE title LIKE 'B%';
```

- `%` matches zero or more characters.
- `_` matches exactly one character.

Contains pattern:

```sql
SELECT title
FROM films
WHERE title LIKE '%Market%';
```

## NOT LIKE

```sql
SELECT title
FROM films
WHERE title NOT LIKE '%Film%';
```

## ILIKE

PostgreSQL-specific case-insensitive pattern matching:

```sql
SELECT title
FROM films
WHERE title ILIKE '%market%';
```

## IN

```sql
SELECT title,
       country
FROM films
WHERE country IN ('Canada', 'Germany', 'France');
```

## NOT IN

```sql
SELECT title,
       certification
FROM films
WHERE certification NOT IN ('R', 'PG-13');
```

Be careful when a `NOT IN` list or subquery contains `NULL`.

## NULL handling

`NULL` means missing, unknown, or not applicable.

Find missing values:

```sql
SELECT title,
       budget
FROM films
WHERE budget IS NULL;
```

Find known values:

```sql
SELECT title,
       imdb_score
FROM films
WHERE imdb_score IS NOT NULL;
```

Do not write:

```sql
WHERE budget = NULL
```

Use:

```sql
WHERE budget IS NULL
```

## Chapter 2 lab evidence

```text
BETWEEN 2018 AND 2021                    = 8 rows
country IN ('Canada', 'Germany')         = 5 rows
imdb_score >= 7.5                        = 5 rows
title LIKE 'B%'                          = Blue Orchard
budget IS NULL                           = No Budget Film
Canada/Germany and release_year >= 2019  = 3 rows
```

---

# 3. Aggregate Functions

Aggregate functions summarize many rows into one result.

## COUNT

```sql
SELECT COUNT(*)
FROM films;
```

## SUM

```sql
SELECT SUM(gross)
FROM films;
```

## AVG

```sql
SELECT AVG(duration)
FROM films;
```

## MIN

```sql
SELECT MIN(release_year)
FROM films;
```

## MAX

```sql
SELECT MAX(imdb_score)
FROM films;
```

## Multiple aggregates together

```sql
SELECT AVG(duration) AS average_duration,
       MIN(duration) AS shortest_duration,
       MAX(duration) AS longest_duration
FROM films;
```

## Filtering before aggregation

`WHERE` filters rows before the aggregate is calculated.

```sql
SELECT AVG(imdb_score) AS average_canadian_score
FROM films
WHERE country = 'Canada';
```

Logical idea:

```text
FROM
WHERE
AGGREGATE
SELECT result
```

## ROUND

Round to two decimal places:

```sql
SELECT ROUND(AVG(imdb_score), 2)
FROM films;
```

Round to the nearest whole number:

```sql
SELECT ROUND(AVG(duration))
FROM films;
```

## Negative ROUND precision

Negative values round to positions left of the decimal point.

```sql
SELECT ROUND(AVG(budget), -3)
       AS avg_budget_rounded_to_thousands
FROM films;
```

Memory map:

```text
ROUND(value,  2)  nearest hundredth
ROUND(value,  1)  nearest tenth
ROUND(value,  0)  nearest whole number
ROUND(value, -1)  nearest ten
ROUND(value, -2)  nearest hundred
ROUND(value, -3)  nearest thousand
ROUND(value, -6)  nearest million
```

## Arithmetic expressions

### Profit

```sql
SELECT title,
       gross - budget AS profit
FROM films;
```

### Ratio or percentage

```sql
SELECT title,
       ROUND((gross / NULLIF(budget, 0)) * 100, 2)
         AS gross_as_percent_of_budget
FROM films;
```

## Integer division

```sql
SELECT 5 / 2;          -- 2
SELECT 5.0 / 2;        -- 2.5
SELECT 5::numeric / 2; -- 2.5
```

Cast or use a decimal literal when the fractional part matters.

## Division by zero

Use `NULLIF` to protect the denominator:

```sql
gross / NULLIF(budget, 0)
```

## Aggregate behavior with NULL

Most aggregate functions ignore `NULL`.

```sql
SELECT COUNT(*) AS total_films,
       COUNT(budget) AS known_budgets,
       AVG(budget) AS average_known_budget
FROM films;
```

Observed result:

```text
total_films       = 16
known_budgets     = 15
average_budget    = 21033333.333333333333
```

The average used only the 15 known budget values.

## Casting text before numeric aggregation

When numeric data is stored as text, cast it before numeric comparison or aggregation.

PostgreSQL shorthand:

```sql
SELECT MIN(year_text::integer) AS earliest_year,
       MAX(year_text::integer) AS latest_year
FROM your_table;
```

Standard SQL form:

```sql
SELECT MIN(CAST(year_text AS integer)) AS earliest_year,
       MAX(CAST(year_text AS integer)) AS latest_year
FROM your_table;
```

Do not cast dirty text blindly. Validate first:

```sql
SELECT MAX(
         CASE
           WHEN year_text ~ '^\d{4}$'
           THEN year_text::integer
         END
       ) AS latest_valid_year
FROM your_table;
```

Memory rule:

```text
Text MIN/MAX uses lexical ordering.
Numeric MIN/MAX uses numeric ordering.
```

## Chapter 3 lab evidence

```text
AVG(duration)                         = 112.4375000000000000
ROUND(AVG(duration), 2)               = 112.44
ROUND(AVG(budget), -3)                = 21033000
SUM(gross) for release_year >= 2020   = 686900000.00
MAX Canadian imdb_score               = 7.3
COUNT(*)                              = 16
COUNT(budget)                         = 15
AVG(budget)                           = 21033333.333333333333
5 / 2                                 = 2
5.0 / 2                               = 2.5
```

---

# 4. Sorting and Grouping

## ORDER BY

Ascending order:

```sql
SELECT title,
       release_year
FROM films
ORDER BY release_year ASC;
```

Descending order:

```sql
SELECT title,
       imdb_score
FROM films
ORDER BY imdb_score DESC;
```

Without `ORDER BY`, row order is not guaranteed.

## Multiple-column sorting

```sql
SELECT title,
       release_year,
       imdb_score
FROM films
ORDER BY release_year ASC,
         imdb_score DESC;
```

SQL sorts by the first expression, then uses the next expression as the tie-breaker.

## GROUP BY

```sql
SELECT country,
       COUNT(*) AS film_count
FROM films
GROUP BY country;
```

## Grouped averages

```sql
SELECT genre,
       ROUND(AVG(imdb_score), 2) AS average_score
FROM films
WHERE imdb_score IS NOT NULL
GROUP BY genre;
```

## Grouping by multiple columns

```sql
SELECT country,
       language,
       COUNT(*) AS film_count
FROM films
GROUP BY country,
         language;
```

Each unique combination becomes a separate group.

## GROUP BY rule

Every selected expression must either:

- be aggregated, or
- appear in the `GROUP BY` clause

Invalid:

```sql
SELECT country,
       title,
       COUNT(*)
FROM films
GROUP BY country;
```

SQL cannot choose one title to represent an entire country group.

## WHERE versus HAVING

### WHERE filters rows before grouping

```sql
SELECT country,
       COUNT(*) AS recent_film_count
FROM films
WHERE release_year >= 2019
GROUP BY country;
```

### HAVING filters groups after aggregation

```sql
SELECT country,
       COUNT(*) AS film_count
FROM films
GROUP BY country
HAVING COUNT(*) >= 2;
```

### Using both

```sql
SELECT country,
       COUNT(*) AS recent_film_count
FROM films
WHERE release_year >= 2019
GROUP BY country
HAVING COUNT(*) >= 2
ORDER BY recent_film_count DESC,
         country;
```

## Alias use in ORDER BY

PostgreSQL allows selected aliases in `ORDER BY`.

```sql
SELECT country,
       COUNT(*) AS film_count
FROM films
GROUP BY country
ORDER BY film_count DESC;
```

## Chapter 4 lab evidence

```text
Multi-column ORDER BY passed.

Country grouping returned 10 groups.

Canada          = 3 films
United States   = 3 films
Germany         = 2 films
United Kingdom  = 2 films

Highest average genre score:
Animation = 8.00

HAVING COUNT(*) >= 2 returned 4 countries.

WHERE release_year >= 2019
+ GROUP BY country
+ HAVING COUNT(*) >= 2
returned:

Canada          = 2
United Kingdom  = 2
United States   = 2
```

---

# 5. Logical Query Execution Order

SQL is written in one order but logically evaluated in another.

```text
1. FROM
2. WHERE
3. GROUP BY
4. HAVING
5. SELECT
6. DISTINCT
7. ORDER BY
8. LIMIT
```

## Why this matters

- `FROM` identifies the source.
- `WHERE` filters rows before grouping.
- `GROUP BY` creates groups.
- `HAVING` filters completed groups.
- `SELECT` produces output expressions and aliases.
- `DISTINCT` removes duplicate output rows.
- `ORDER BY` sorts the final result.
- `LIMIT` restricts how many rows are returned.

Example:

```sql
SELECT country,
       COUNT(*) AS film_count
FROM films
WHERE release_year >= 2019
GROUP BY country
HAVING COUNT(*) >= 2
ORDER BY film_count DESC
LIMIT 5;
```

---

# 6. Common Mistakes and Corrections

## Mistake: using `COUNT(column)` as a row count

```sql
COUNT(budget)
```

This counts only non-NULL budgets.

Use:

```sql
COUNT(*)
```

for total rows.

## Mistake: assuming `DISTINCT` acts independently on each column

```sql
SELECT DISTINCT country, language
```

This returns unique country-language combinations.

## Mistake: using `= NULL`

Wrong:

```sql
WHERE budget = NULL
```

Correct:

```sql
WHERE budget IS NULL
```

## Mistake: mixing AND and OR without parentheses

Use parentheses when the intended grouping is not obvious.

## Mistake: forgetting BETWEEN is inclusive

```sql
BETWEEN 2018 AND 2021
```

includes both 2018 and 2021.

## Mistake: using `WHERE` with an aggregate condition

Wrong pattern:

```sql
WHERE COUNT(*) >= 2
```

Correct:

```sql
HAVING COUNT(*) >= 2
```

## Mistake: selecting non-grouped, non-aggregated columns

Every selected non-aggregate column must appear in `GROUP BY`.

## Mistake: assuming rows have a natural order

Use `ORDER BY` whenever order matters.

## Mistake: unexpected integer division

```sql
5 / 2
```

returns `2` in PostgreSQL.

Use a decimal or cast:

```sql
5.0 / 2
```

## Mistake: blindly casting dirty text

Validate text before converting it to a numeric type.

---

# 7. Interview Translation

## What is the difference between COUNT(*) and COUNT(column)?

`COUNT(*)` counts rows. `COUNT(column)` counts only non-NULL values in that column.

## What does DISTINCT do?

It removes duplicate result rows based on the complete selected column set.

## What is the difference between WHERE and HAVING?

`WHERE` filters rows before grouping. `HAVING` filters grouped aggregate results.

## What is the difference between ORDER BY and GROUP BY?

`ORDER BY` changes result order. `GROUP BY` changes result granularity by combining rows into categories.

## Why must non-aggregate selected columns appear in GROUP BY?

Each output row represents one group, so SQL needs one defined value for every selected non-aggregate expression.

## How do aggregate functions handle NULL?

Most aggregate functions ignore NULL values. `COUNT(*)` is the main exception because it counts rows.

## How do you avoid integer division?

Cast one operand to a decimal type or use a decimal literal before division.

## Why is logical execution order important?

It explains when rows are filtered, when groups are formed, when aliases become available, and why aggregate filters belong in `HAVING`.

## How do you safely divide when the denominator might be zero?

Use `NULLIF(denominator, 0)` to convert zero to NULL and prevent a division-by-zero error.

---

# 8. Quick Memory Nuggets

```text
SELECT chooses columns.
WHERE chooses rows.
GROUP BY creates categories.
HAVING filters categories.
ORDER BY sorts the final output.
LIMIT restricts final rows.
```

```text
COUNT(*) counts rows.
COUNT(column) counts known values.
COUNT(DISTINCT column) counts unique known values.
```

```text
AND narrows.
OR broadens.
BETWEEN is inclusive.
LIKE uses % and _.
```

```text
WHERE happens before GROUP BY.
HAVING happens after GROUP BY.
```

```text
Positive ROUND precision moves right.
Negative ROUND precision moves left.
```

```text
More GROUP BY columns = more detailed groups.
More ORDER BY columns = more tie-breakers.
```

---

# 9. Course Completion Summary

The course covered:

- selecting columns
- counting rows and values
- duplicate removal
- filtering numbers and text
- compound conditions
- pattern matching
- NULL handling
- aggregate functions
- rounding
- arithmetic
- aliases
- sorting
- grouping
- HAVING
- logical execution order

Local PostgreSQL practice was completed successfully against the `intermediate_sql` schema and the `films` dataset.

## Final status

```text
Platform status: PASSED
Documentation coverage: COMPLETE
Lab coverage: STRONG
Recall confidence: STRONG
Interview readiness: NEEDS REPETITION
```
