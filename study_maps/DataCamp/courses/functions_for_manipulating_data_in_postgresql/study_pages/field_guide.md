# Field Guide: Functions for Manipulating Data in PostgreSQL

## 1. How to Use This Guide

This guide collects the reusable ideas, SQL patterns, mistakes, and interview translation for the course. It is a working field guide scaffold, not the final expanded reference.

## 2. Course Big Picture

- PostgreSQL built-in functions help transform and prepare data.
- The course uses the Sakila / DVD Rental database.
- The course moves from data types to date/time functions, text functions, full-text search, and extensions.

## 3. Chapter 1 — Common Data Types

### Text types: CHAR, VARCHAR, TEXT

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### Numeric types: INT, DECIMAL

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### Date/time types: DATE, TIME, TIMESTAMP, INTERVAL

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### ARRAY types

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### Discovering column types with INFORMATION_SCHEMA

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### User-defined types preview

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

## 4. Chapter 2 — DATE/TIME Functions and Operators

### Date subtraction

- Plain English: Subtracting one `DATE` from another returns an integer count of days between them.
- Generic SQL pattern:
```sql
SELECT end_date - start_date AS day_gap
FROM some_table;
```
- Common trap: Expecting an `INTERVAL` here. `DATE - DATE` returns a whole-number day difference, not hours/minutes/seconds detail.
- Interview translation: Know which date/time math returns scalars versus intervals; `DATE - DATE` is often used for SLA days, retention windows, or gap counts.

### Date plus integer

- Plain English: Adding an integer to a `DATE` moves the date forward by that many days.
- Generic SQL pattern:
```sql
SELECT start_date + 7 AS next_week_date
FROM some_table;
```
- Common trap: Forgetting that PostgreSQL treats the integer as days when the left side is a `DATE`.
- Interview translation: This is a compact way to compute due dates, renewal dates, or fixed-day offsets from a baseline date.

### Timestamp arithmetic

- Plain English: Subtracting one `TIMESTAMP` from another returns an `INTERVAL`.
- Generic SQL pattern:
```sql
SELECT finished_at - started_at AS elapsed_interval
FROM some_table;
```
- Common trap: Assuming the result is a number. `TIMESTAMP - TIMESTAMP` preserves time-unit detail as an interval.
- Interview translation: Use timestamp arithmetic when you need duration precision rather than just day counts.

### INTERVAL arithmetic

- Plain English: `INTERVAL` values are best for relative time calculations like "plus 3 days" or "plus 2 hours."
- Generic SQL pattern:
```sql
SELECT event_ts + INTERVAL '3 days' AS shifted_ts,
       event_ts + 7 * INTERVAL '1 day' AS shifted_ts_alt
FROM some_table;
```
- Common trap: Mixing integers and timestamps directly; use `INTERVAL` when you need timestamp-safe relative offsets.
- Interview translation: `INTERVAL` arithmetic is the portable mental model for scheduling, expiry logic, and time-window transformations.

### AGE()

- Plain English: `AGE()` returns the difference between two timestamps as an `INTERVAL`.
- Generic SQL pattern:
```sql
SELECT AGE(later_ts, earlier_ts) AS age_interval
FROM some_table;
```
- Common trap: Treating `AGE()` as just another numeric diff. It returns an interval-like elapsed time expression.
- Interview translation: `AGE()` is useful when you want a readable time gap between two timestamp values.

### NOW()

- Plain English: `NOW()` returns the current timestamp value, typically with timezone and high precision.
- Generic SQL pattern:
```sql
SELECT NOW() AS current_ts;
```
- Common trap: Forgetting that you may want to cast away timezone or precision depending on the downstream use.
- Interview translation: `NOW()` is a standard PostgreSQL way to anchor queries to "current system time."

### CURRENT_TIMESTAMP

- Plain English: `CURRENT_TIMESTAMP` also returns the current timestamp value and can accept a precision parameter.
- Generic SQL pattern:
```sql
SELECT CURRENT_TIMESTAMP AS current_ts,
       CURRENT_TIMESTAMP(0) AS rounded_current_ts;
```
- Common trap: Missing that `CURRENT_TIMESTAMP(precision)` can round fractional seconds.
- Interview translation: Use this when you want standard-style SQL syntax or when precision control matters.

### CURRENT_DATE

- Plain English: `CURRENT_DATE` returns the current date only, without a time component.
- Generic SQL pattern:
```sql
SELECT CURRENT_DATE AS today_date;
```
- Common trap: Expecting timestamp precision from a date-only function.
- Interview translation: This is ideal for day-based filters, reporting dates, and comparisons that do not need time-of-day detail.

### CURRENT_TIME

- Plain English: `CURRENT_TIME` returns the current time only, without the date portion.
- Generic SQL pattern:
```sql
SELECT CURRENT_TIME AS current_clock_time;
```
- Common trap: Forgetting that this is time-only output, so it is not enough by itself for full event ordering across dates.
- Interview translation: Use `CURRENT_TIME` when the business question is about clock time rather than calendar date.

### CAST and ::

- Plain English: Both `CAST()` and `::` convert a value from one data type to another; `::` is PostgreSQL-specific and `CAST()` is more standard SQL style.
- Generic SQL pattern:
```sql
SELECT NOW()::timestamp AS ts_no_tz,
       CAST(NOW() AS timestamp) AS ts_no_tz_standard;
```
- Common trap: Using `::` in contexts where cross-database SQL portability matters.
- Interview translation: Explain both forms and when you would prefer standard SQL syntax over PostgreSQL shorthand.

### EXTRACT()

- Plain English: `EXTRACT()` pulls a numeric date/time part such as year, month, quarter, or dow from a timestamp, time, or interval.
- Generic SQL pattern:
```sql
SELECT EXTRACT(YEAR FROM event_ts) AS event_year,
       EXTRACT(MONTH FROM event_ts) AS event_month
FROM some_table;
```
- Common trap: Confusing extracted numeric parts with truncated timestamps; `EXTRACT()` gives numbers, not time buckets.
- Interview translation: This is how you derive grouping keys or model features from raw temporal data.

### DATE_PART()

- Plain English: `DATE_PART()` is a close alternative to `EXTRACT()` and also returns numeric date/time parts.
- Generic SQL pattern:
```sql
SELECT DATE_PART('quarter', event_ts) AS event_quarter,
       DATE_PART('dow', event_ts) AS event_dow
FROM some_table;
```
- Common trap: Assuming it returns a truncated date object. Like `EXTRACT()`, it returns numeric parts.
- Interview translation: Be ready to explain that `DATE_PART()` and `EXTRACT()` often solve the same problem with slightly different syntax.

### DATE_TRUNC()

- Plain English: `DATE_TRUNC()` rounds a timestamp or interval down to a named bucket such as month, year, week, day, or hour.
- Generic SQL pattern:
```sql
SELECT DATE_TRUNC('month', event_ts) AS event_month_bucket,
       DATE_TRUNC('week', event_ts) AS event_week_bucket
FROM some_table;
```
- Common trap: Thinking it returns only a number. `DATE_TRUNC()` returns a bucketed timestamp or interval value.
- Interview translation: `DATE_TRUNC()` is the go-to function for time-based grouping in dashboards, reporting, and trend analysis.

## 5. Chapter 3 — Parsing and Manipulating Text

### Concatenation with ||

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### CONCAT()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### UPPER(), LOWER(), INITCAP()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### REPLACE()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### REVERSE()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### CHAR_LENGTH() and LENGTH()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### POSITION() and STRPOS()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### LEFT() and RIGHT()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### SUBSTRING() and SUBSTR()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### TRIM(), LTRIM(), RTRIM()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### LPAD() and RPAD()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

## 6. Chapter 4 — Full-text Search and PostgreSQL Extensions

### LIKE

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### LIKE wildcards: % and _

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### LIKE case sensitivity

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### to_tsvector()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### to_tsquery()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### @@ match operator

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### lexemes

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### CREATE TYPE

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### CREATE FUNCTION

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### CREATE EXTENSION

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### pg_available_extensions

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### pg_extension

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### fuzzystrmatch

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### levenshtein()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### pg_trgm

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

### similarity()

- Plain English:
- Generic SQL pattern:
- Common trap:
- Interview translation:

## 7. Reusable SQL Pattern Index

| Pattern | Used for | Example topic | Practice status |
|---|---|---|---|
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |

## 8. Interview Q&A Bank

### Data type questions

- Placeholder:

### Date/time questions

- Placeholder:

### Text manipulation questions

- Placeholder:

### Full-text search questions

- Placeholder:

### Extension questions

- Placeholder:

## 9. Mistakes and Corrections

- Placeholder for mistakes discovered during the live DataCamp pass.

## 10. What to Slow Down On

- INTERVAL arithmetic
- DATE_TRUNC vs EXTRACT
- SUBSTRING with POSITION
- ARRAY one-based indexing
- full-text search syntax
- extension metadata tables

## 11. Next Fill-In Pass

- Next pass should expand Chapter 2 first because that is the current live DataCamp study area.
