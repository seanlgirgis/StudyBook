# PostgreSQL Functions for Manipulating Data — Course 06 Field Guide

DataCamp Associate Data Analyst in SQL

Markdown is the editable source of truth.  
HTML is the polished reading version.

## Table of Contents

1. [Course 06 Big Map](#1-course-06-big-map)
2. [Schema Inspection](#2-schema-inspection)
3. [PostgreSQL Data Types](#3-postgresql-data-types)
4. [Date and Time Arithmetic](#4-date-and-time-arithmetic)
5. [Current Date/Time and Casting](#5-current-datetime-and-casting)
6. [AGE](#6-age)
7. [EXTRACT, DATE_PART, DATE_TRUNC](#7-extract-date_part-date_trunc)
8. [Arrays](#8-arrays)
9. [Text Reformatting](#9-text-reformatting)
10. [Text Parsing](#10-text-parsing)
11. [Trimming and Padding](#11-trimming-and-padding)
12. [Full-Text Search](#12-full-text-search)
13. [Extensions and Custom Database Features](#13-extensions-and-custom-database-features)
14. [Common Traps](#14-common-traps)
15. [Interview Cheatsheet](#15-interview-cheatsheet)
16. [One-Page Quick Lookup](#16-one-page-quick-lookup)

## 1. Course 06 Big Map

Course 06 is about learning which PostgreSQL function or operator fits the
type of data sitting in front of you. The practical mental model is:

raw messy values -> inspect type -> choose function -> transform -> clean ->
extract -> format -> search

This matters because the same-looking value in query output can behave very
differently depending on whether PostgreSQL stores it as text, timestamp,
interval, array, or a user-defined type.

> Nugget: PostgreSQL rewards type awareness. Good function choice usually
> starts with understanding storage type, not just visible values.

> Sean memory line: Inspect the type first. Then pick the function.

> Interview sentence: Before I transform a column, I check its PostgreSQL data
> type so I can apply the right family of functions and avoid false
> assumptions.

## 2. Schema Inspection

When you inherit an existing database, `information_schema` gives you the
first reliable view of structure. `information_schema.tables` helps you confirm
what tables exist. `information_schema.columns` shows column names, generic
data types, and helps you see where further inspection is needed.

Before applying PostgreSQL functions, inspect the real column types. A column
can look like text in `SELECT` output, but PostgreSQL may know it as `ARRAY`,
`DATE`, `TIMESTAMP`, `DECIMAL`, or another type.

```sql
SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

```sql
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'customer';
```

This is especially useful in Sakila or DVD rental examples, where a field may
look like plain text in a simple `SELECT`, but actually be stored as an array
or a user-defined type.

> Nugget: Querying metadata is often faster than guessing from sample rows.

> Memory nugget: Before manipulating a column, inspect its data type. The
> function you choose depends on the column type.

> Common trap: Looking at displayed values alone can trick you into treating an
> `ARRAY` or `USER-DEFINED` column like plain text.

## 3. PostgreSQL Data Types

Course 06 focuses on several practical type families:

- text types: `CHAR`, `VARCHAR`, `TEXT`
- numeric types: `INT`, `DECIMAL`
- date/time types: `DATE`, `TIME`, `TIMESTAMP`, `INTERVAL`
- collection types: `ARRAY`
- extensible/custom types: `USER-DEFINED`

### Text Types

- `CHAR` stores fixed-width character data.
- `VARCHAR` stores variable-length character data with a length limit.
- `TEXT` stores variable-length text and is often the most flexible option.

### Numeric Types

- `INT` is useful for whole-number identifiers and counts.
- `DECIMAL` is useful when exact precision matters, such as currency.

### Date/Time Types

- `DATE` stores calendar dates.
- `TIME` stores clock time.
- `TIMESTAMP` stores a moment in time.
- `INTERVAL` stores a duration or time span.

### Arrays and User-Defined Types

- `ARRAY` lets one column hold multiple values.
- `USER-DEFINED` often appears with enums, domains, or custom types.

```sql
SELECT
    title,
    description,
    replacement_cost
FROM film;
```

> Common trap: `STRING` is not a PostgreSQL text type.

> Common trap: A column can look like text in `SELECT` output but actually be
> `ARRAY` or `USER-DEFINED`.

> Sean memory line: Visible shape is not storage type.

## 4. Date and Time Arithmetic

Date and time arithmetic is one of the biggest conceptual upgrades in this
course because PostgreSQL returns different result types depending on the
operands.

- `DATE - DATE` returns integer days
- `DATE + integer` treats the integer as days
- `TIMESTAMP - TIMESTAMP` returns `INTERVAL`
- `TIMESTAMP + INTERVAL` shifts a timestamp
- `INTERVAL` can be multiplied

```sql
SELECT
    rental_date,
    return_date,
    return_date - rental_date AS days_rented
FROM rental
WHERE return_date IS NOT NULL;
```

```sql
SELECT
    rental_date,
    rental_date + INTERVAL '3 days' AS expected_return_date
FROM rental;
```

```sql
SELECT
    INTERVAL '1 day' * rental_duration AS allowed_rental_period
FROM film;
```

`INTERVAL` has two common roles.

1. Fixed interval literal:
   `INTERVAL '3 days'`

This means a fixed duration written directly in SQL. Use it when the business
rule is constant.

2. Column-driven interval:
   `INTERVAL '1 day' * rental_duration`

This converts a numeric column into a duration. Use it when the number of days
comes from the data.

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

- `return_date - rental_date` calculates the actual elapsed interval.
- `rental_date + INTERVAL '3 days'` applies a fixed rule.
- `rental_date + (INTERVAL '1 day' * rental_duration)` applies the film rule.
- `INTERVAL '1 day' * rental_duration` shows the allowed duration by itself.

The key idea is that `DATE` arithmetic is often count-oriented, while
`TIMESTAMP` arithmetic is duration-oriented.

> Nugget: PostgreSQL does not treat all time math the same. Operand type
> controls result type.

> Memory nugget: `INTERVAL '3 days'` = fixed duration. `INTERVAL '1 day' *
> number` = turn a number into a duration.

> Sean memory line: Date minus date gives days. Timestamp minus timestamp gives
> duration.

> Interview sentence: For event data, I use timestamp arithmetic to calculate
> elapsed time and expected future dates. When a duration is stored as a number
> of days, I convert it into an `INTERVAL` before adding it to a timestamp.

## 5. Current Date/Time and Casting

Current-date and current-time functions are useful when building relative
filters, audit fields, or quick diagnostics.

- `NOW()`
- `CURRENT_TIMESTAMP`
- `CURRENT_TIMESTAMP(2)`
- `CURRENT_DATE`
- `CURRENT_TIME`
- `NOW()::timestamp`
- `CAST(NOW() AS timestamp)`

```sql
SELECT
    NOW() AS now_value,
    CURRENT_TIMESTAMP AS current_ts,
    CURRENT_TIMESTAMP(2) AS current_ts_2dp,
    CURRENT_DATE AS current_date_value,
    CURRENT_TIME AS current_time_value;
```

```sql
SELECT
    NOW()::timestamp AS cast_with_double_colon,
    CAST(NOW() AS timestamp) AS cast_with_cast;
```

Casting matters because some expressions produce a richer type than you need.
Explicit casts help make the output fit the intended downstream use.

> Interview sentence: I use explicit casts when I want the time value to match
> the exact type needed for grouping, comparison, or display.

## 6. AGE

`AGE(later, earlier)` returns an interval-style result representing elapsed
time between two moments.

```sql
SELECT
    rental_date,
    return_date,
    AGE(return_date, rental_date) AS rental_age
FROM rental
WHERE return_date IS NOT NULL;
```

Unlike plain subtraction, `AGE()` is often used when you want a more human-ish
elapsed-time expression rather than just a day count.

> Nugget: `AGE()` returns interval output, not just a numeric difference.

> Common trap: `AGE(later, earlier)` is the intended direction. Flipping the
> arguments flips the sign and the interpretation.

## 7. EXTRACT, DATE_PART, DATE_TRUNC

These functions support time-based grouping and reporting, but they do
different jobs:

- `EXTRACT` returns a subfield value
- `DATE_PART` is similar, with slightly different syntax
- `DATE_TRUNC` truncates to a chosen precision and returns timestamp/interval

```sql
SELECT
    EXTRACT(year FROM payment_date) AS payment_year,
    EXTRACT(quarter FROM payment_date) AS payment_quarter,
    SUM(amount) AS revenue
FROM payment
GROUP BY 1, 2
ORDER BY 1, 2;
```

```sql
SELECT
    DATE_PART('month', payment_date) AS payment_month
FROM payment;
```

```sql
SELECT
    DATE_TRUNC('month', payment_date) AS payment_month_start,
    SUM(amount) AS revenue
FROM payment
GROUP BY 1
ORDER BY 1;
```

`GROUP BY 1, 2` means “group by the first and second select-list expressions.”
It is compact, but it depends on select-list order staying stable.

> Common trap: `DATE_TRUNC` returns a timestamp/interval, not just a numeric
> field.

> Common trap: `EXTRACT` and `DATE_PART` return subfield values, not truncated
> dates.

> Interview sentence: For timestamp grouping, I use `EXTRACT` when I need a
> numeric subfield, and `DATE_TRUNC` when I need a true bucketed timestamp.

## 8. Arrays

PostgreSQL arrays are important because one column may store multiple values in
one row.

Key rules:

- PostgreSQL arrays start at `1`
- `array[1]` checks one position only
- `ANY` searches anywhere in the array
- `@>` checks whether the array contains another array

```sql
SELECT
    title,
    special_features
FROM film
WHERE special_features[1] = 'Trailers';
```

```sql
SELECT
    title,
    special_features
FROM film
WHERE 'Trailers' = ANY(special_features);
```

```sql
SELECT
    title,
    special_features
FROM film
WHERE special_features @> ARRAY['Deleted Scenes'];
```

PostgreSQL arrays are one-based. `array[1]` returns only the first item.
`value = ANY(array_column)` searches the whole array.

Important example:
Sean had `sql` as the first tag, so `first_tag = sql` and `has_sql_tag = true`.
Brian had `strategy` as the first tag, but `sql` elsewhere in the array, so
`first_tag = strategy` and `has_sql_tag = true`.

> Nugget: Position check and containment check are not the same question.

> Memory nugget: `array[1]` checks one position. `ANY(array)` searches the
> whole array.

> Common trap: `special_features[1]` only checks the first slot.

> Common trap: `ANY` searches the full array, not a fixed position.

> Sean memory line: Brackets check position. `ANY` checks anywhere.

## 9. Text Reformatting

These functions help build labels, normalize casing, and clean up presentation
text.

- concatenation with `||`
- `CONCAT()`
- combining string and non-string data
- `UPPER`
- `LOWER`
- `INITCAP`
- `REPLACE`
- `REVERSE`

```sql
SELECT
    first_name || ' ' || last_name AS full_name
FROM customer;
```

```sql
SELECT
    CONCAT(customer_id, ': ', first_name, ' ', last_name) AS customer_label
FROM customer;
```

```sql
SELECT
    UPPER(first_name) AS first_name_upper,
    LOWER(last_name) AS last_name_lower,
    INITCAP(email) AS email_title_case
FROM customer;
```

```sql
SELECT
    REPLACE(description, 'A Astounding', 'An Astounding') AS fixed_description
FROM film;
```

```sql
SELECT
    REVERSE(title) AS reversed_title
FROM film;
```

These are practical cleanup tools for reports, review pages, and before/after
transform checks.

> Interview sentence: For text cleanup, I use case conversion, replacement,
> trim, pad, and substring functions depending on whether the job is formatting
> or parsing.

## 10. Text Parsing

Parsing functions help answer “where is the piece I need?” and “how do I cut it
out safely?”

- `CHAR_LENGTH`
- `LENGTH`
- `POSITION`
- `STRPOS`
- `LEFT`
- `RIGHT`
- `SUBSTRING`
- `SUBSTR`

```sql
SELECT
    title,
    CHAR_LENGTH(title) AS title_length
FROM film;
```

```sql
SELECT
    email,
    POSITION('@' IN email) AS at_position
FROM customer;
```

```sql
SELECT
    email,
    SUBSTRING(email FROM 1 FOR POSITION('@' IN email) - 1) AS username
FROM customer;
```

```sql
SELECT
    email,
    SUBSTRING(
        email
        FROM POSITION('@' IN email) + 1
        FOR CHAR_LENGTH(email)
    ) AS domain
FROM customer;
```

You can also build equivalent logic with `STRPOS`, `LEFT`, `RIGHT`, and nested
functions. That becomes useful when field shapes are slightly different across
sources.

> Nugget: Parsing often means combining locator functions with extractor
> functions.

> Common trap: `SUBSTRING` positions are 1-based.

> Sean memory line: Find the marker, then slice the string.

## 11. Trimming and Padding

These functions are useful when imported or user-entered text contains extra
characters, or when you need fixed-width formatting for labels.

- `TRIM`
- `LTRIM`
- `RTRIM`
- `LPAD`
- `RPAD`

```sql
SELECT
    TRIM('  padded text  ') AS cleaned_text;
```

```sql
SELECT
    LPAD(customer_id::text, 5, '0') AS padded_customer_id
FROM customer;
```

```sql
SELECT
    RPAD(first_name, 12, '.') AS first_name_padded
FROM customer;
```

```sql
SELECT
    LTRIM('---value', '-') AS left_trimmed,
    RTRIM('value---', '-') AS right_trimmed;
```

> Common trap: Padding can truncate when the requested target length is shorter
> than the original string.

> Sean memory line: Trim removes noise. Pad creates alignment.

## 12. Full-Text Search

`LIKE` is useful for simple wildcard pattern checks, but it has limits.
PostgreSQL full-text search is built for smarter token-based matching.

### LIKE

- `%` means any sequence of characters
- `_` means one character
- `LIKE` is case-sensitive

```sql
SELECT
    title
FROM film
WHERE title LIKE 'ELF%';
```

### Full-Text Search

```sql
SELECT
    title
FROM film
WHERE to_tsvector(title) @@ to_tsquery('elf');
```

- `to_tsvector` converts text into searchable tokens
- `to_tsquery` converts query text into a search query
- `@@` compares the two
- `tsvector` stores normalized searchable content
- lexemes are normalized search terms

Full-text search is more useful than `LIKE` when you care about meaningful
words and search normalization rather than plain substring matching.

> Nugget: `LIKE` looks for character patterns. Full-text search looks for
> normalized search tokens.

> Common trap: Full-text search is not the same thing as `LIKE`.

> Interview sentence: `LIKE` is good for simple patterns, while full-text
> search is better for natural-language-style matching and token search.

## 13. Extensions and Custom Database Features

PostgreSQL is extensible. Course 06 introduces the idea that a database can
define its own types, functions, and extension-provided capabilities.

Key concepts:

- `CREATE TYPE`
- `ENUM`
- `pg_type`
- `information_schema.columns` with `USER-DEFINED`
- `CREATE FUNCTION`
- user-defined functions
- `CREATE EXTENSION`
- `fuzzystrmatch`
- `pg_trgm`
- `levenshtein`
- `similarity`

```sql
CREATE TYPE dayofweek AS ENUM (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
);
```

```sql
SELECT
    typname,
    typcategory
FROM pg_type
WHERE typname = 'dayofweek';
```

```sql
SELECT
    column_name,
    data_type,
    udt_name
FROM information_schema.columns
WHERE table_name = 'film';
```

```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
```

```sql
SELECT
    levenshtein('GUMBO', 'GAMBOL') AS edit_distance;
```

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

```sql
SELECT
    similarity('word', 'words') AS similarity_score;
```

You may also encounter existing custom functions in a real database or in the
Sakila examples. Those functions are often used to hide repeated logic behind
a simpler interface.

```sql
CREATE FUNCTION example_label(input_text text)
RETURNS text
LANGUAGE sql
AS $$
    SELECT UPPER(input_text);
$$;
```

> Nugget: PostgreSQL is not limited to built-in types and functions. It can be
> extended at both the schema level and the engine level.

> Common trap: `USER-DEFINED` in `information_schema.columns` means you need to
> inspect the underlying type or enum name before assuming normal text rules.

## 14. Common Traps

- `STRING` is not a PostgreSQL text type.
- PostgreSQL arrays start at `1`, not `0`.
- `special_features[1]` checks only the first array position.
- `ANY` searches anywhere in the array.
- `DATE - DATE` returns integer days.
- `TIMESTAMP - TIMESTAMP` returns `INTERVAL`.
- `DATE + integer` treats the integer as days.
- `AGE(later, earlier)`, not the other way around.
- `DATE_TRUNC` returns timestamp/interval, not just a number.
- `LIKE` is case-sensitive.
- `SUBSTRING` positions are 1-based.
- Padding can truncate if requested length is shorter than the original string.
- Full-text search is not the same as `LIKE`.

> Common trap: A query result that “looks like text” can still require array,
> interval, or user-defined type logic underneath.

## 15. Interview Cheatsheet

- “Before transforming columns, I inspect data types using
  `information_schema`.”
- “Function choice depends on the underlying data type.”
- “For event data, I distinguish `DATE`, `TIME`, `TIMESTAMP`, and `INTERVAL`.”
- “For timestamp grouping, I use `EXTRACT` or `DATE_TRUNC` depending on whether
  I need a numeric subfield or a truncated timestamp.”
- “For text cleanup, I use case, replace, trim, pad, and substring functions.”
- “For arrays, I know position checks are different from searching the full
  array.”
- “For text search, `LIKE` is useful for simple patterns, while full-text
  search is better for natural language matching.”

## 16. One-Page Quick Lookup

| Task | Function/operator | Example |
|---|---|---|
| inspect column type | `information_schema.columns` | `WHERE table_name = 'customer'` |
| add 3 days | `+ INTERVAL '3 days'` | `rental_date + INTERVAL '3 days'` |
| duration between timestamps | `AGE()` or subtraction | `AGE(return_date, rental_date)` |
| current timestamp | `NOW()`, `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP(2)` |
| extract year | `EXTRACT` | `EXTRACT(year FROM payment_date)` |
| truncate to month | `DATE_TRUNC` | `DATE_TRUNC('month', payment_date)` |
| concatenate names | `||`, `CONCAT()` | `first_name || ' ' || last_name` |
| uppercase text | `UPPER` | `UPPER(first_name)` |
| replace text | `REPLACE` | `REPLACE(description, 'A', 'An')` |
| find @ position | `POSITION`, `STRPOS` | `POSITION('@' IN email)` |
| email username | `SUBSTRING` | `SUBSTRING(email FROM 1 FOR ...)` |
| trim whitespace | `TRIM` | `TRIM('  padded text  ')` |
| pad ID | `LPAD` | `LPAD(customer_id::text, 5, '0')` |
| array contains | `ANY`, `@>` | `'Trailers' = ANY(special_features)` |
| `LIKE` pattern | `LIKE`, `%`, `_` | `title LIKE 'ELF%'` |
| full-text search | `to_tsvector`, `to_tsquery`, `@@` | `to_tsvector(title) @@ to_tsquery('elf')` |
| levenshtein distance | `levenshtein` | `levenshtein('GUMBO', 'GAMBOL')` |
| similarity score | `similarity` | `similarity('word', 'words')` |
