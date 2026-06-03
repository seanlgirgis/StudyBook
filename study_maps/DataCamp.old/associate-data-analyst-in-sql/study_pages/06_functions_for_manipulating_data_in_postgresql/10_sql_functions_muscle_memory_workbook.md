# Course 06 SQL Functions Muscle-Memory Workbook

## Purpose

Hands-on rehearsal log for PostgreSQL data manipulation functions.

## Training Mode Rules

- Type the SQL by hand before checking older notes.
- Keep each exercise small and repeatable.
- Record mistakes exactly as they happened.
- Convert each correction into a reusable pattern.
- End each exercise with one memory nugget and one interview translation.

## How To Use This Workbook

1. Read the prompt.
2. Write your own SQL in the `Sean SQL` section.
3. Note what the result means in plain English.
4. Capture mistakes, discoveries, and fixes immediately.
5. Distill the exercise into a compact memory nugget.
6. Translate the exercise into interview-ready language.

---

## Exercise 01 - Schema Inspection and Arrays

### Prompt

Inspect the Course 06 lab schema, list its tables, inspect the
`lab_customers` column types, then compare array position access with
array-wide search.

### Sean SQL

```sql
SET search_path TO course06_functions_lab;

SELECT
  table_name
FROM information_schema.tables
WHERE table_schema = 'course06_functions_lab'
ORDER BY table_name;

SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_schema = 'course06_functions_lab'
  AND table_name = 'lab_customers'
ORDER BY ordinal_position;

SELECT
  customer_id,
  first_name,
  last_name,
  email,
  favorite_tags
FROM lab_customers
ORDER BY customer_id;

SELECT
  customer_id,
  favorite_tags[1] AS first_tag,
  'sql' = ANY(favorite_tags) AS has_sql_tag
FROM lab_customers
ORDER BY customer_id;
```

### Result Meaning

`information_schema.tables` lists tables in the lab schema.
`information_schema.columns` shows column names and data types.
`favorite_tags` is an ARRAY, not plain text.
`favorite_tags[1]` returns only the first array item.
`'sql' = ANY(favorite_tags)` searches the whole array.

Important result:
Sean had `sql` as the first tag, so `first_tag = sql` and `has_sql_tag = true`.
Brian had `strategy` as the first tag, but `sql` elsewhere in the array,
so `first_tag = strategy` and `has_sql_tag = true`.

### Mistake / Discovery

A column can look like text when displayed, but PostgreSQL knows its
real data type.
Array position access and array searching are different.

### Corrected Pattern

Use `array[1]` when you need a specific position.
Use `value = ANY(array_column)` when you need to search the whole array.

### Memory Nugget

`array[1]` checks one position.
`ANY(array)` searches the whole array.

### Interview Translation

Before transforming data, I inspect the schema so I know the real column
types. For PostgreSQL arrays, I know that position access like `array[1]`
is different from searching the whole array with `ANY`.

---

## Exercise 02 — Date/Time Arithmetic and INTERVAL

### Prompt

Compare actual rental time, fixed expected return time, film-rule expected
return time, and allowed rental period.

### Sean SQL

```sql
SELECT
  r.rental_id,
  f.title,
  f.rental_duration,
  r.rental_date,
  r.return_date,

  r.return_date - r.rental_date AS actual_rental_period,

  r.rental_date + INTERVAL '3 days'
    AS fixed_3_day_expected_return,

  r.rental_date + (INTERVAL '1 day' * f.rental_duration)
    AS film_rule_expected_return,

  INTERVAL '1 day' * f.rental_duration
    AS allowed_rental_period

FROM lab_rentals AS r
INNER JOIN lab_films AS f
  ON r.film_id = f.film_id
WHERE r.return_date IS NOT NULL
ORDER BY r.rental_id;
```

### Result Meaning

The query compares actual rental duration against two expected-return ideas.
One expected date uses a fixed three-day rule.
The other expected date uses each film's `rental_duration` column.
The `allowed_rental_period` column shows the numeric `rental_duration`
converted into a PostgreSQL `INTERVAL`.

### Mistake / Discovery

`INTERVAL` is not used only one way.
`INTERVAL '3 days'` is a fixed literal duration.
`INTERVAL '1 day' * rental_duration` converts a number into a duration.

### Corrected Pattern

Use a fixed `INTERVAL` when the rule is constant.
Use `INTERVAL '1 day' * numeric_column` when the duration comes from the data.

### Memory Nugget

`INTERVAL '3 days'` = fixed duration.
`INTERVAL '1 day' * number` = turn a number into a duration.
`TIMESTAMP - TIMESTAMP` = `INTERVAL`.
`TIMESTAMP + INTERVAL` = shifted `TIMESTAMP`.

### Interview Translation

For event data, I use timestamp arithmetic to calculate elapsed time and
expected dates. If a duration is stored as a numeric day count, I convert it
to an `INTERVAL` before adding it to a timestamp.
