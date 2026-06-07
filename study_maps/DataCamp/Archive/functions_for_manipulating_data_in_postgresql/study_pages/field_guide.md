# Field Guide: Functions for Manipulating Data in PostgreSQL

## 1. How to Use This Guide

This guide collects the reusable ideas, SQL patterns, mistakes, and interview translation for the course. It is a clean reusable cheat sheet built from the completed lab work.

## 2. Course Big Picture

- PostgreSQL built-in functions help transform and prepare data.
- The course uses the Sakila / DVD Rental database.
- The course moves from data types to date/time functions, text functions, full-text search, and extensions.

## 3. Chapter 1 — Common Data Types

### Text types: CHAR, VARCHAR, TEXT

- Plain English: `CHAR` is a fixed-length-ish text type with padding behavior, `VARCHAR` stores variable-length text with an optional limit, and `TEXT` is the flexible general-purpose long-text type.
- Generic SQL pattern:
```sql
SELECT
  CAST('AB' AS CHAR(4)) AS char_value,
  CAST('Postgres' AS VARCHAR(20)) AS varchar_value,
  CAST('Longer free-form note' AS TEXT) AS text_value;
```
- Common trap: Choosing text types without thinking about constraints, cleanup rules, and how padded or long values should behave downstream.
- Interview translation: Pick the text type that matches the business rule. Use `VARCHAR(n)` when a limit matters, `TEXT` when flexibility matters, and be careful with `CHAR` when padding could confuse comparisons or presentation.

### Numeric types: INT, DECIMAL

- Plain English: `INT` is for whole numbers. `DECIMAL` or `NUMERIC` is for exact decimal values such as money, scores, or calculated amounts that should not lose precision.
- Generic SQL pattern:
```sql
SELECT
  42::INT AS quantity,
  19.95::DECIMAL(10,2) AS price,
  amount_paid::NUMERIC(12,2) AS normalized_amount
FROM some_table;
```
- Common trap: Assuming integer math will behave like decimal math. Division, rounding, and exactness assumptions can change the result.
- Interview translation: Use integers for counts and IDs. Use exact decimal types when fractional precision matters and rounding mistakes would hurt reporting or finance logic.

### Date/time types: DATE, TIME, TIMESTAMP, INTERVAL

- Plain English: `DATE` is a calendar day, `TIME` is a clock time, `TIMESTAMP` is date plus time, and `INTERVAL` is a duration or relative offset such as 3 days or 2 hours.
- Generic SQL pattern:
```sql
SELECT
  CURRENT_DATE AS today_date,
  CURRENT_TIME AS current_clock_time,
  CURRENT_TIMESTAMP AS current_ts,
  CURRENT_TIMESTAMP + INTERVAL '3 days' AS ts_plus_3_days;
```
- Common trap: Mixing date-only logic and timestamp logic as if they return the same type or level of detail.
- Interview translation: Choose the type based on the question. Use `DATE` for day-based rules, `TIMESTAMP` for event timing, and `INTERVAL` for relative time math.

### ARRAY types

- Plain English: PostgreSQL arrays hold multiple values in one column. They are useful for simple multi-value storage, but they use PostgreSQL-specific syntax and 1-based indexing.
- Generic SQL pattern:
```sql
SELECT
  tag_array,
  tag_array[1] AS first_tag,
  'sql' = ANY(tag_array) AS has_sql,
  tag_array @> ARRAY['sql', 'postgres'] AS has_both,
  CARDINALITY(tag_array) AS tag_count
FROM some_table;
```
- Common trap: Using `[0]` like Python. PostgreSQL arrays start at `[1]`, not `[0]`.
- Interview translation: Arrays are convenient for light multi-value storage and search patterns, but you need to know `ANY()`, `@>`, and `CARDINALITY()`, plus the 1-based indexing rule.

### Discovering column types with INFORMATION_SCHEMA

- Plain English: `information_schema.columns` is the metadata table that tells you what tables and columns exist and what types they use.
- Generic SQL pattern:
```sql
SELECT
  table_schema,
  table_name,
  column_name,
  data_type,
  udt_name
FROM information_schema.columns
WHERE table_schema = 'course06_functions_lab'
ORDER BY table_name, ordinal_position;
```
- Common trap: Filtering only `public` and missing course or lab schemas that hold the real practice tables.
- Interview translation: Inspect metadata first. `information_schema.columns` is often the fastest way to understand table shape before writing transformations.

### User-defined types preview

- Plain English: `CREATE TYPE` can define custom PostgreSQL types or structured reusable values, but it is a more advanced tool than the basics in this course.
- Generic SQL pattern:
```sql
CREATE TYPE mood AS ENUM ('low', 'medium', 'high');
```
- Common trap: Reaching for custom types when a simple table design or constraint would be clearer and easier to maintain.
- Interview translation: Know that PostgreSQL supports custom types, but use them deliberately. Most day-to-day analytics work still relies more on base types and good schema design.

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

#### Extracting day of week

- Plain English:

`EXTRACT(dow FROM date_or_timestamp)` returns the weekday number using PostgreSQL numbering:

```text
0 = Sunday
1 = Monday
2 = Tuesday
3 = Wednesday
4 = Thursday
5 = Friday
6 = Saturday
```

`EXTRACT(isodow FROM date_or_timestamp)` returns ISO weekday numbering:

```text
1 = Monday
2 = Tuesday
3 = Wednesday
4 = Thursday
5 = Friday
6 = Saturday
7 = Sunday
```

- Generic SQL pattern:
```sql
SELECT
  rental_date,
  EXTRACT(day FROM rental_date) AS day_of_month,
  EXTRACT(dow FROM rental_date) AS postgres_day_of_week,
  EXTRACT(isodow FROM rental_date) AS iso_day_of_week
FROM rental;
```

- Generic SQL example:
```sql
SELECT
  EXTRACT(dow FROM DATE '2026-06-07') AS postgres_dow,
  EXTRACT(isodow FROM DATE '2026-06-07') AS iso_dow;
```

- Expected idea:
```text
For a Sunday:
dow    = 0
isodow = 7
```

- Common trap:
```text
EXTRACT(day FROM some_date)
does not mean day of week.

It means day of month.
```

- Interview translation:
```text
Use dow when PostgreSQL's Sunday-zero numbering is acceptable.
Use isodow when Monday-through-Sunday numbering is clearer for business reporting.
```

- Memory nugget:
```text
day    = day of month
dow    = Sunday 0 through Saturday 6
isodow = Monday 1 through Sunday 7
```

### DATE_PART()

- Plain English: `DATE_PART()` is a close alternative to `EXTRACT()` and also returns numeric date/time parts.
- Generic SQL pattern:
```sql
SELECT DATE_PART('quarter', event_ts) AS event_quarter,
       DATE_PART('dow', event_ts) AS event_dow
FROM some_table;
```
- Matching weekday example:
```sql
SELECT
  DATE_PART('dow', rental_date) AS postgres_day_of_week,
  DATE_PART('isodow', rental_date) AS iso_day_of_week
FROM rental;
```
- Common trap: Assuming it returns a truncated date object. Like `EXTRACT()`, it returns numeric parts.
- Interview translation: Be ready to explain that `DATE_PART()` and `EXTRACT()` often solve the same problem with slightly different syntax.
- Extra note: `DATE_PART()` and `EXTRACT()` return the same weekday numbering when using the same field.

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

- Plain English: The `||` operator joins strings together and is a common way to build report labels or search documents.
- Generic SQL pattern:
```sql
SELECT first_name || ' ' || last_name AS full_name
FROM some_table;
```
- Common trap: If one side is `NULL`, the whole concatenated result can become `NULL`.
- Interview translation: `||` is the compact operator form for string concatenation and works well when you control the inputs and null behavior.

### CONCAT()

- Plain English: `CONCAT()` is the function-style way to join strings and is often friendlier around `NULL` values.
- Generic SQL pattern:
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM some_table;
```
- Common trap: Assuming `CONCAT()` behaves exactly like `||` for null handling.
- Interview translation: Use `CONCAT()` when you want readable function-style concatenation and safer default handling for missing pieces.

### UPPER(), LOWER(), INITCAP()

- Plain English: These functions normalize text case. `UPPER()` makes everything uppercase, `LOWER()` makes everything lowercase, and `INITCAP()` title-cases each word.
- Generic SQL pattern:
```sql
SELECT
  UPPER(TRIM(raw_text)) AS upper_text,
  LOWER(TRIM(raw_text)) AS lower_text,
  INITCAP(TRIM(raw_text)) AS title_text
FROM some_table;
```
- Common trap: Formatting dirty text before cleaning it first.
- Interview translation: Clean first, then format. Case functions help standardize inconsistent text for comparison, display, and downstream logic.

### REPLACE()

- Plain English: `REPLACE()` swaps exact matching text for new text.
- Generic SQL pattern:
```sql
SELECT REPLACE(comparison_text, 'ELF', 'ORC') AS replaced_text
FROM some_table;
```
- Common trap: Expecting fuzzy replacement. `ELVES` does not exactly match `ELF`.
- Interview translation: `REPLACE()` is exact text substitution, not pattern matching or fuzzy cleanup.

### REVERSE()

- Plain English: `REVERSE()` flips the character order in a string.
- Generic SQL pattern:
```sql
SELECT REVERSE(raw_code) AS reversed_code
FROM some_table;
```
- Common trap: Treating it as a normal cleanup function. It is more niche and is usually for practice or special parsing tricks.
- Interview translation: `REVERSE()` is useful when you need to inspect suffix-based patterns or demonstrate string transformation logic.

### CHAR_LENGTH() and LENGTH()

- Plain English: These functions count how long a string is. In this lab, comparing `LENGTH(raw_text)` to `LENGTH(TRIM(raw_text))` exposed outside padding.
- Generic SQL pattern:
```sql
SELECT
  LENGTH(raw_text) AS raw_len,
  LENGTH(TRIM(raw_text)) AS trimmed_len
FROM some_table;
```
- Common trap: Padding can be hard to see by eye, but length checks make it obvious.
- Interview translation: Length comparisons are a simple data-quality check for detecting hidden spaces or unexpected text growth.

### POSITION() and STRPOS()

- Plain English: `POSITION()` and `STRPOS()` find where a substring appears inside a larger string.
- Generic SQL pattern:
```sql
SELECT
  POSITION('BO' IN comparison_text) AS pos_via_position,
  STRPOS(comparison_text, 'BO') AS pos_via_strpos
FROM some_table;
```
- Common trap: They return `0` when not found, and positions are 1-based, not 0-based.
- Interview translation: Use these when you need delimiter discovery or fixed-position parsing logic.

### LEFT() and RIGHT()

- Plain English: `LEFT()` returns a fixed prefix and `RIGHT()` returns a fixed suffix.
- Generic SQL pattern:
```sql
SELECT
  LEFT(raw_code, 3) AS code_prefix,
  RIGHT(raw_code, 2) AS code_suffix
FROM some_table;
```
- Common trap: They are best for known fixed-width slices, not arbitrary free-form parsing.
- Interview translation: `LEFT()` and `RIGHT()` are simple, readable tools for extracting codes, prefixes, and suffixes.

### SUBSTRING() and SUBSTR()

- Plain English: `SUBSTRING()` and `SUBSTR()` extract part of a string from a start position for a given length.
- Generic SQL pattern:
```sql
SELECT
  SUBSTRING(raw_code FROM 2 FOR 4) AS middle_piece,
  SUBSTR(raw_code, 2, 4) AS middle_piece_alt
FROM some_table;
```
- Common trap: Positions are 1-based, so starting point assumptions from programming languages can be off by one.
- Interview translation: Use these when the text shape is known and you need to carve out specific pieces by position.

### TRIM(), LTRIM(), RTRIM()

- Plain English: `TRIM()` removes outside spaces on both sides, `LTRIM()` removes left-side padding, and `RTRIM()` removes right-side padding.
- Generic SQL pattern:
```sql
SELECT
  TRIM(raw_text) AS cleaned_text,
  LTRIM(raw_text) AS left_cleaned,
  RTRIM(raw_text) AS right_cleaned
FROM some_table;
```
- Common trap: `TRIM()` does not collapse repeated internal spaces.
- Interview translation: Trimming is outside cleanup. If internal whitespace is messy, use regex cleanup instead.

### LPAD() and RPAD()

- Plain English: `LPAD()` and `RPAD()` pad text to a target width and are useful for fixed-width display or code formatting.
- Generic SQL pattern:
```sql
SELECT
  LPAD(code_text, 4, '0') AS left_padded_code,
  RPAD(code_text, 8, '.') AS right_padded_code
FROM some_table;
```
- Common trap: If the target length is shorter than the original string, padding functions can truncate.
- Interview translation: Padding functions help standardize IDs and fixed-width labels, but always verify target length behavior.

### REGEXP_REPLACE()

- Plain English: `REGEXP_REPLACE()` does pattern-based text replacement. A key cleanup example is collapsing repeated whitespace.
- Generic SQL pattern:
```sql
SELECT REGEXP_REPLACE(text_col, '\s+', ' ', 'g') AS normalized_text
FROM some_table;
```
- Common trap: Without the `'g'` flag, only the first matching pattern is replaced.
- Interview translation: Use regex replacement when simple exact replacement is not enough and you need pattern-aware cleanup.

## 6. Chapter 4 — Full-text Search and PostgreSQL Extensions

### LIKE

- Plain English: `LIKE` does character-pattern matching.
- Generic SQL pattern:
```sql
SELECT *
FROM some_table
WHERE comparison_text LIKE 'G%';
```
- Common trap: It matches character shapes, not normalized word meaning.
- Interview translation: `LIKE` is useful for simple starts-with, contains, or shape matching, but it is not full-text search.

### LIKE wildcards: % and _

- Plain English: In `LIKE`, `%` means any number of characters and `_` means exactly one character.
- Generic SQL pattern:
```sql
SELECT *
FROM some_table
WHERE comparison_text LIKE '%BO%'
   OR comparison_text LIKE 'G_MBO';
```
- Common trap: Treating `%` and `_` as interchangeable.
- Interview translation: Use `%` when length is flexible and `_` when exactly one character should vary.

### LIKE case sensitivity

- Plain English: `LIKE` is case-sensitive in PostgreSQL. `ILIKE` is the case-insensitive version.
- Generic SQL pattern:
```sql
SELECT *
FROM some_table
WHERE comparison_text LIKE '%CASE%'
   OR comparison_text ILIKE '%case%';
```
- Common trap: Expecting `LIKE` to ignore case automatically.
- Interview translation: Reach for `ILIKE` when user-facing search should ignore case differences.

### to_tsvector()

- Plain English: `to_tsvector()` converts raw text into searchable lexemes for full-text search.
- Generic SQL pattern:
```sql
SELECT to_tsvector('english', title || ' ' || description) AS searchable_document
FROM some_table;
```
- Common trap: Expecting the original text to stay unchanged in meaning and shape. Common words may be removed and useful words may be normalized.
- Interview translation: `to_tsvector()` is the document-preparation step in PostgreSQL full-text search.

### to_tsquery()

- Plain English: `to_tsquery()` builds a full-text search query and supports operators like `&`, `|`, and `!`.
- Generic SQL pattern:
```sql
SELECT to_tsquery('english', 'postgres & database') AS search_query;
```
- Common trap: Using `to_tsquery()` for raw user text when the input is not already in full-text syntax.
- Interview translation: `to_tsquery()` is best when you want explicit search logic and control over AND, OR, NOT, and prefix search.

### plainto_tsquery()

- Plain English: `plainto_tsquery()` converts normal user-style words into a safe full-text query and removes stop words.
- Generic SQL pattern:
```sql
SELECT plainto_tsquery('english', 'postgres database') AS plain_search_query;
```
- Common trap: Forgetting that stop words can disappear and the final query may not look like the raw phrase.
- Interview translation: Use `plainto_tsquery()` when the input is ordinary search text rather than manual tsquery syntax.

### @@ match operator

- Plain English: `@@` tests whether a `tsvector` document matches a `tsquery`.
- Generic SQL pattern:
```sql
SELECT *
FROM some_table
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'elf');
```
- Common trap: Thinking `@@` is just another comparison operator. It specifically connects full-text documents and full-text queries.
- Interview translation: `@@` is the core full-text match operator in PostgreSQL.

### lexemes

- Plain English: Lexemes are normalized searchable tokens inside PostgreSQL full-text search.
- Generic SQL pattern:
```sql
SELECT to_tsvector('english', 'A story about a database') AS searchable_document;
```
- Common trap: Assuming the stored lexemes will always look exactly like the original words. For example, `story` can become `stori` and `database` can become `databas`.
- Interview translation: Lexemes are why full-text search can match normalized word forms instead of raw character strings.

### CREATE TYPE

- Plain English: `CREATE TYPE` defines a custom PostgreSQL type. It is useful to know about, but it is not the main workhorse of this course.
- Generic SQL pattern:
```sql
CREATE TYPE priority_level AS ENUM ('low', 'medium', 'high');
```
- Common trap: Using custom types where a simple constraint or reference table would be easier to evolve.
- Interview translation: Know the capability, but explain that many analytics workflows do not need custom types every day.

### CREATE FUNCTION

- Plain English: `CREATE FUNCTION` defines reusable SQL or procedural logic inside the database.
- Generic SQL pattern:
```sql
CREATE FUNCTION add_one(x INT)
RETURNS INT
LANGUAGE SQL
AS $$
  SELECT x + 1;
$$;
```
- Common trap: Overbuilding custom database functions when a one-off query expression would be simpler.
- Interview translation: Functions are useful for reusable business logic, but you should justify the maintenance cost.

### CREATE EXTENSION

- Plain English: `CREATE EXTENSION` enables extension-provided objects and functions in the current database.
- Generic SQL pattern:
```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
```
- Common trap: Assuming the feature is available before the extension is enabled.
- Interview translation: Extensions are opt-in database capabilities. Enable them first, then inspect installed metadata if needed.

### pg_available_extensions

- Plain English: `pg_available_extensions` shows which extensions are available to install.
- Generic SQL pattern:
```sql
SELECT name, default_version
FROM pg_available_extensions
ORDER BY name;
```
- Common trap: Confusing available extensions with already installed extensions.
- Interview translation: Use this catalog when you need to discover what the PostgreSQL instance can enable.

### pg_extension

- Plain English: `pg_extension` shows which extensions are installed and what schema their objects live in.
- Generic SQL pattern:
```sql
SELECT
  extname,
  extnamespace::regnamespace AS extension_schema
FROM pg_extension
ORDER BY extname;
```
- Common trap: Thinking the extension story is only "global." The extension is enabled in a database, and its objects live in a schema.
- Interview translation: `pg_extension` is the catalog table for installed extension state and schema placement.

### fuzzystrmatch

- Plain English: `fuzzystrmatch` is the extension that provides fuzzy string comparison helpers such as `levenshtein()`, `soundex()`, and `difference()`.
- Generic SQL pattern:
```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
```
- Common trap: Calling fuzzy functions before enabling the extension.
- Interview translation: This extension helps with typo tolerance and sound-alike matching when exact string comparison is too strict.

### levenshtein()

- Plain English: `levenshtein()` measures edit distance, or how many single-character edits it takes to change one string into another.
- Generic SQL pattern:
```sql
SELECT levenshtein(LOWER(input_text), LOWER(stored_text)) AS edit_distance
FROM some_table
WHERE levenshtein(LOWER(input_text), LOWER(stored_text)) <= 2;
```
- Common trap: Treating larger distance as better. Lower is better, and exact match is `0`.
- Interview translation: Use `levenshtein()` when typo tolerance should be measured by actual character edits.

### soundex()

- Plain English: `soundex()` turns strings into rough phonetic codes so similar-sounding values can land together.
- Generic SQL pattern:
```sql
SELECT soundex('Smith') AS smith_code,
       soundex('Smyth') AS smyth_code;
```
- Common trap: Assuming it is a spelling-distance function. It is phonetic, not letter-by-letter.
- Interview translation: `soundex()` is useful when pronunciation similarity matters more than exact spelling.

### difference()

- Plain English: `difference()` compares soundex codes and returns a sound-similarity score from `0` to `4`.
- Generic SQL pattern:
```sql
SELECT difference('Hero', 'Hiro') AS sound_score;
```
- Common trap: Reading it like edit distance. Higher is better here, and `4` is strongest.
- Interview translation: `difference()` is a quick phonetic similarity score, not a precise text-distance measure.

### pg_trgm

- Plain English: `pg_trgm` is PostgreSQL's trigram similarity extension. It compares shared text chunks rather than exact strings.
- Generic SQL pattern:
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```
- Common trap: Expecting it to behave like edit distance. Trigram similarity is chunk-based, not character-edit counting.
- Interview translation: `pg_trgm` is a strong choice for fuzzy candidate search when near-matches should rank by shared text similarity.

### similarity()

- Plain English: `similarity()` returns a trigram similarity score from `0` to `1`, where higher is better.
- Generic SQL pattern:
```sql
SELECT
  title,
  similarity(title, 'POSTGRES HER0') AS similarity_score
FROM some_table
WHERE similarity(title, 'POSTGRES HER0') >= 0.3
ORDER BY similarity_score DESC;
```
- Common trap: Treating similarity like distance. `similarity()` uses higher-is-better logic.
- Interview translation: Use `similarity()` when you want a numeric fuzzy-match score that can be ranked or thresholded.

### word_similarity()

- Plain English: `word_similarity()` is useful when the clean stored value may be buried inside a longer user-style sentence.
- Generic SQL pattern:
```sql
SELECT
  title,
  word_similarity(title, 'please find POSTGRES HER0 for me') AS word_score
FROM some_table
ORDER BY word_score DESC;
```
- Common trap: Expecting whole-string `similarity()` to stay high for longer noisy input phrases.
- Interview translation: Use `word_similarity()` when embedded substring-style fuzzy search matters more than whole-string equality.

### pg_trgm % operator

- Plain English: In `pg_trgm`, `%` is not percent math. It means "similar enough" using the active trigram similarity threshold.
- Generic SQL pattern:
```sql
SELECT *
FROM some_table
WHERE title % 'POSTGRES HER0';
```
- Common trap: Reading `%` as arithmetic percent instead of pass/fail fuzzy matching.
- Interview translation: `%` is the shortcut operator when you want threshold-based trigram filtering without writing the threshold comparison manually.

### pg_trgm threshold / show_limit() / set_limit()

- Plain English: `show_limit()` shows the active trigram threshold and `set_limit()` changes it for the session.
- Generic SQL pattern:
```sql
SELECT show_limit() AS current_similarity_threshold;
SELECT set_limit(0.8);
SELECT set_limit(0.3);
```
- Common trap: Raising the threshold for a test and forgetting to reset it.
- Interview translation: Threshold tuning changes pass/fail behavior, not the underlying similarity score. Reset temporary changes after testing.

### pg_trgm <-> distance operator

- Plain English: `<->` returns trigram distance, where lower is better and closer matches should sort first.
- Generic SQL pattern:
```sql
SELECT
  title,
  title <-> 'POSTGRES HER0' AS trigram_distance
FROM some_table
ORDER BY trigram_distance ASC;
```
- Common trap: Sorting distance in descending order, which pushes worse matches to the top.
- Interview translation: Use `<->` when you want distance-style ranking. It is roughly `1 - similarity`, so lower means closer.

## 7. Reusable SQL Pattern Index

| Pattern | Used for | Example topic | Practice status |
|---|---|---|---|
| Inspect metadata first | understand tables/columns/types before querying | information_schema.columns | practiced |
| Clean then transform | avoid formatting dirty text directly | TRIM + INITCAP | practiced |
| Calculate once in a CTE | reuse a derived feature safely | duration hours, fuzzy scores | practiced |
| Raw value -> feature -> label | turn technical values into business labels | duration bands, fuzzy match labels | practiced |
| Bucket timestamps | group events by month/week/day/hour | DATE_TRUNC | practiced |
| Extract numeric date parts | derive year/month/quarter features | EXTRACT / DATE_PART | practiced |
| Handle open records | use fallback endpoint for NULL end time | COALESCE(return_date, CURRENT_TIMESTAMP) | practiced |
| Pattern match text | find starts-with / contains / one-character wildcard | LIKE / ILIKE | practiced |
| Full-text match | convert text and query into searchable forms | to_tsvector @@ to_tsquery | practiced |
| Fuzzy edit-distance match | typo tolerance by edit count | levenshtein <= threshold | practiced |
| Fuzzy sound match | phonetic matching | soundex / difference | practiced |
| Trigram candidate search | similarity-based fuzzy search | pg_trgm similarity / % / <-> | practiced |

## 8. Interview Q&A Bank

### Data type questions

- Q: How do you discover column data types in PostgreSQL?
  A: Use `information_schema.columns`, filter by `table_schema` and `table_name`, and inspect `data_type` plus `udt_name`.
- Q: What is a PostgreSQL ARRAY trap?
  A: Arrays are 1-based, so `array_col[1]` is the first item and `array_col[0]` is not the first item.

### Date/time questions

- Q: What is the difference between EXTRACT and DATE_TRUNC?
  A: `EXTRACT` returns a numeric part. `DATE_TRUNC` returns a timestamp bucket.
- Q: What is the difference between DATE - DATE and TIMESTAMP - TIMESTAMP?
  A: `DATE - DATE` returns integer days. `TIMESTAMP - TIMESTAMP` returns an `INTERVAL`.

### Text manipulation questions

- Q: Why clean text before formatting it?
  A: Cleaning first removes padding or inconsistent casing so formatting functions produce stable report values.
- Q: What is the difference between TRIM and REGEXP_REPLACE whitespace collapse?
  A: `TRIM` removes outside spaces. `REGEXP_REPLACE` with `'\s+'` can collapse repeated internal whitespace.

### Full-text search questions

- Q: How does full-text search differ from LIKE?
  A: `LIKE` matches character patterns. Full-text search normalizes text into lexemes and matches search tokens.
- Q: What does @@ do?
  A: It tests whether a `tsvector` document matches a `tsquery`.

### Extension questions

- Q: What does CREATE EXTENSION do?
  A: It enables extension-provided objects and functions in the current database, usually installed into a schema.
- Q: How do levenshtein and similarity differ?
  A: `levenshtein` is edit distance where lower is better; `similarity` is trigram score where higher is better.
- Q: When would you use word_similarity?
  A: When the stored value may be embedded inside a longer user-style search phrase.

## 9. Mistakes and Corrections

| Topic | Mistake | Correction | Memory line |
|---|---|---|---|
| ARRAY indexing | Expecting [0] to return first item | Use [1] for first item in PostgreSQL arrays | PostgreSQL arrays are 1-based |
| DATE vs TIMESTAMP math | Expecting all date math to return the same type | DATE - DATE returns integer days; TIMESTAMP - TIMESTAMP returns INTERVAL | Know the return type |
| DATE_TRUNC vs EXTRACT | Treating both as bucket functions | EXTRACT returns number; DATE_TRUNC returns timestamp bucket | Number vs bucket |
| CASE order | Checking lower threshold before higher threshold | Put most severe or specific threshold first | CASE stops at first match |
| TRIM misunderstanding | Expecting TRIM to fix internal repeated spaces | Use REGEXP_REPLACE for internal whitespace collapse | TRIM outside; regex inside |
| LIKE case sensitivity | Expecting LIKE to ignore case | Use ILIKE for case-insensitive matching | LIKE case-sensitive; ILIKE ignores case |
| SPLIT_PART indexing | Expecting zero-based parts | SPLIT_PART starts at part 1 | SQL text parts are 1-based here |
| Full-text stemming | Expecting every related word to stem the same way | Inspect query and vector tokens to verify | Trust but inspect tokens |
| Extension schema | Thinking extension is only global | Check pg_extension and extnamespace::regnamespace | Extension enabled in DB, objects live in schema |
| levenshtein direction | Treating bigger distance as better | Lower edit distance is better | levenshtein lower is better |
| similarity direction | Treating similarity like distance | Higher similarity is better | similarity higher is better |
| pg_trgm % operator | Reading % as percent math | In pg_trgm, % means similar enough by threshold | % is pass/fail fuzzy match |
| pg_trgm threshold | Raising threshold and forgetting to reset | Reset with set_limit(0.3) and verify | Always reset temporary threshold |
| psql paste issue | Pasting result table text into psql | Paste only SQL, or comment text with -- | Only SQL goes at prompt |

## 10. What to Slow Down On

- INTERVAL arithmetic
- DATE_TRUNC vs EXTRACT
- SUBSTRING with POSITION
- ARRAY one-based indexing
- full-text search syntax
- extension metadata tables
- levenshtein vs similarity direction
- pg_trgm threshold behavior
- TRIM vs REGEXP_REPLACE whitespace cleanup
- full-text lexemes and stemming
- extension schema vs database enablement

## 11. Next Fill-In Pass

- Next pass should be after the DataCamp course exercises are complete. Use the completed exercises to tighten wording, remove anything beyond the course if needed, and add final examples from the DataCamp screens.
