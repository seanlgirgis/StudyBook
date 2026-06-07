# Functions for Manipulating Data in PostgreSQL Field Guide

## Course status

- Platform: COMPLETE
- StudyBook package: COMPLETE
- Documentation: STRONG
- Lab: DEVELOPING
- Recall: DEVELOPING
- Interview readiness: NEEDS REPETITION

## Course map

1. [Overview of Common Data Types](chapter_01_overview_of_common_data_types_field_guide.html)
2. [Working with DATE/TIME Functions and Operators](chapter_02_working_with_date_time_functions_and_operators_field_guide.html)
3. [Parsing and Manipulating Text](chapter_03_parsing_and_manipulating_text_field_guide.html)
4. [Full-text Search and PostgreSQL Extensions](chapter_04_full_text_search_and_postgresql_extensions_field_guide.html)
5. [SQL Function Quick Lookup](sql_function_quick_lookup.html)
6. [Lab Run Book](../lab/lab_run_book.md)

## Big picture

PostgreSQL function work is easiest when approached in this order:

```text
question → inspect input type → choose operation → compose expression → validate return type
```

The course covers five connected skills:

- recognize common PostgreSQL data types;
- calculate with dates, timestamps, and intervals;
- extract and bucket date/time components;
- normalize, parse, truncate, trim, pad, and combine text;
- use arrays, full-text search, user-defined types, and extensions.

## 1. Type-first query design

Before selecting a function, inspect the column type rather than relying on its name.

```sql
SELECT
    column_name,
    data_type,
    udt_name,
    character_maximum_length,
    numeric_precision,
    numeric_scale
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'film'
ORDER BY ordinal_position;
```

Useful questions:

- Is the value text, numeric, temporal, array, or user-defined?
- Is a cast required?
- What type will the expression return?
- How should null or malformed values behave?

### Arrays

```sql
SELECT title
FROM film
WHERE 'Trailers' = ANY (special_features);

SELECT title
FROM film
WHERE special_features @> ARRAY['Trailers']::text[];
```

`ANY` tests one value against array elements. `@>` tests whether the left array contains the right array.

## 2. Dates, timestamps, and intervals

```sql
SELECT DATE '2026-06-10' - DATE '2026-06-01' AS days_between;

SELECT TIMESTAMP '2026-06-10 18:00'
     - TIMESTAMP '2026-06-09 08:30' AS elapsed_time;
```

Key distinction:

- date minus date commonly returns an integer day count;
- timestamp minus timestamp returns an interval;
- adding an interval to a date or timestamp moves it forward or backward.

```sql
SELECT rental_date
     + rental_duration * INTERVAL '1 day' AS expected_return_date
FROM rental_schedule;
```

Current-time values include `CURRENT_DATE`, `CURRENT_TIME`, `CURRENT_TIMESTAMP`, `NOW()`, `LOCALTIME`, and `LOCALTIMESTAMP`.

## 3. Extracting and bucketing time

Use `EXTRACT` or `DATE_PART` when you need one scalar field. Use `DATE_TRUNC` when you need a timestamp aligned to a reporting boundary.

```sql
SELECT
    EXTRACT(YEAR FROM rental_date) AS rental_year,
    DATE_PART('month', rental_date) AS rental_month_number,
    DATE_TRUNC('month', rental_date) AS rental_month
FROM rental;
```

Memory rule:

```text
EXTRACT / DATE_PART = component
DATE_TRUNC          = boundary
```

## 4. Reformatting and combining text

```sql
SELECT
    first_name || ' ' || last_name AS full_name,
    CONCAT(first_name, ' ', last_name) AS full_name_function,
    UPPER(email) AS email_upper,
    LOWER(email) AS email_lower,
    INITCAP(first_name || ' ' || last_name) AS display_name,
    REPLACE(description, 'A Astounding', 'An Astounding') AS corrected_text,
    REVERSE(title) AS reversed_title
FROM customer;
```

`||` can propagate nulls. `CONCAT()` handles null arguments more forgivingly. Choose deliberately.

## 5. Measuring and parsing text

Locate a delimiter before extracting around it.

```sql
SELECT
    email,
    CHAR_LENGTH(email) AS email_length,
    STRPOS(email, '@') AS at_position,
    SUBSTRING(email FROM 1 FOR POSITION('@' IN email) - 1) AS username,
    SUBSTRING(email FROM POSITION('@' IN email) + 1) AS domain
FROM customer;
```

Other extraction tools:

```sql
SELECT
    LEFT(description, 50),
    RIGHT(description, 20),
    SUBSTR(description, 10, 50)
FROM film;
```

Production code should define behavior for nulls, missing delimiters, and malformed input.

## 6. Trimming, padding, and labels

```sql
SELECT
    TRIM(first_name || ' ' || last_name) AS clean_name,
    LPAD(customer_id::text, 6, '0') AS padded_id,
    RPAD(title, 30, '.') AS display_title
FROM customer;
```

A reusable label pattern:

```sql
LPAD(customer_id::text, 6, '0') || ' - ' ||
INITCAP(TRIM(first_name || ' ' || last_name))
```

## 7. Pattern matching versus full-text search

Simple pattern search:

```sql
SELECT title
FROM film
WHERE title ILIKE '%elf%';
```

Linguistic search:

```sql
SELECT title, description
FROM film
WHERE to_tsvector('english', title || ' ' || description)
      @@ to_tsquery('english', 'elf');
```

Use `LIKE` or `ILIKE` for literal patterns. Use full-text search for tokenized, normalized natural-language search.

## 8. User-defined types and extensions

```sql
CREATE TYPE dayofweek AS ENUM (
  'Monday', 'Tuesday', 'Wednesday',
  'Thursday', 'Friday', 'Saturday', 'Sunday'
);
```

Inspect types and extensions:

```sql
SELECT typname, typcategory
FROM pg_type
WHERE typname = 'dayofweek';

SELECT extname
FROM pg_extension
ORDER BY extname;
```

Optional fuzzy-search extensions:

```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

These commands may require elevated privileges.

## 9. Decision guide

| Need | Preferred tool | Key distinction |
|---|---|---|
| Inspect a column | `information_schema.columns` | Do not guess the type |
| Test one item in an array | `= ANY(array_col)` | Scalar compared with array elements |
| Test array containment | `@>` | Left array contains right array |
| Get year/month/day | `EXTRACT`, `DATE_PART` | Returns one component |
| Group by month/week/day | `DATE_TRUNC` | Returns aligned timestamp |
| Find text position | `POSITION`, `STRPOS` | Locate before extracting |
| Extract text | `SUBSTRING`, `LEFT`, `RIGHT`, `SUBSTR` | Boundaries matter |
| Normalize text | `LOWER`, `UPPER`, `INITCAP`, `TRIM` | Define desired canonical form |
| Literal text pattern | `LIKE`, `ILIKE` | Raw character matching |
| Natural-language search | full-text search | Tokenized and normalized |
| Approximate text match | `pg_trgm`, `fuzzystrmatch` | Extension availability matters |

## 10. Common mistakes

1. Guessing a data type from a column name.
2. Treating intervals and numeric day counts as interchangeable.
3. Using `DATE_TRUNC` when a scalar component is required.
4. Parsing text without checking that the delimiter exists.
5. Forgetting null behavior when concatenating with `||`.
6. Using `LIKE` as though it were linguistic full-text search.
7. Assuming an extension is installed or that the current user can install it.

## 11. Interview translation

**How do you select a PostgreSQL function?**  
Start from the input type and desired output. Inspect metadata, choose the smallest correct operation, and validate nulls, boundaries, casts, and return types.

**`EXTRACT` versus `DATE_TRUNC`?**  
`EXTRACT` returns a component. `DATE_TRUNC` returns a timestamp aligned to a period boundary.

**How do you parse a delimited value safely?**  
Locate and validate the delimiter first, then calculate extraction boundaries and define behavior for malformed rows.

**When do you use full-text search?**  
Use it for natural-language text requiring tokenization, normalization, stemming, and indexable search rather than literal substring matching.

## 12. Memory nuggets

```text
Type first. Function second.
```

```text
EXTRACT = component
DATE_TRUNC = boundary
```

```text
Locate → validate → extract → normalize
```

```text
LIKE = characters
Full-text search = words and language rules
```
