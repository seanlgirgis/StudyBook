# Lab Guide: Functions for Manipulating Data in PostgreSQL

## 1. How to Use This Lab Guide

This guide grows while doing the course and lab work.

For each small lab or DataCamp exercise, capture:

- topic
- goal
- SQL file or DataCamp exercise
- SQL attempted
- corrected SQL if needed
- expected result
- mistake/pattern learned
- Field Guide reference

## 2. Current Lab Setup

Course-local lab folder:

```text
lab\
```

Current setup SQL files:

```text
lab\sql\00_create_schema.sql
lab\sql\01_create_tables.sql
lab\sql\02_insert_sample_data.sql
```

Run order:

```text
1. lab\sql\00_create_schema.sql
2. lab\sql\01_create_tables.sql
3. lab\sql\02_insert_sample_data.sql
```

## 3. Lab Progress Tracker

| Status | Topic | Source | SQL / File | Notes |
| --- | --- | --- | --- | --- |
| TODO | Lab setup SQL | local lab | 00_create_schema.sql | verify schema creation |
| TODO | Lab setup tables | local lab | 01_create_tables.sql | verify tables |
| TODO | Lab sample data | local lab | 02_insert_sample_data.sql | verify seed data |
| DONE | Expected return date | local lab | lab_rentals | added 3-day INTERVAL |
| DONE | Late-by interval | local lab | lab_rentals | compared return_date to expected_return_date |
| DONE | Return status CASE label | local lab | lab_rentals | labeled Late / Not returned / On time or early |
| DONE | Return status summary | local lab | lab_rentals | counted rentals by status |
| DONE | EXTRACT vs DATE_TRUNC | local lab | lab_rentals | compared numeric month part to month bucket |
| DONE | Monthly rental grouping | local lab | lab_rentals | counted rentals by DATE_TRUNC month bucket |
| DONE | DATE_PART vs EXTRACT | local lab | lab_rentals | both returned Q1 for sample data |
| DONE | Current date/time functions | local lab | current functions | compared CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP, NOW() |
| DONE | CURRENT_TIMESTAMP precision | local lab | current functions | tested full, 0, and 2 fractional-second precision |
| DONE | Cast timestamp to date | local lab | lab_rentals | compared ::date and CAST(... AS date) |
| DONE | Rental duration | local lab | lab_rentals | calculated return_date - rental_date |
| DONE | DATE minus DATE | local lab | lab_rentals | cast timestamps to date and calculated integer calendar days |
| DONE | DATE plus integer | local lab | lab_rentals | confirmed DATE + integer means date plus that many days |
| DONE | Clear INTERVAL version of DATE + integer | local lab | lab_rentals | compared DATE + 3 to INTERVAL '3 days' and cast-back-to-date style |
| DONE | AGE() | local lab | lab_rentals | compared AGE(return_date, rental_date) to direct timestamp subtraction |
| DONE | AGE() argument order | local lab | lab_rentals | confirmed reversed arguments produce negative intervals |
| DONE | COALESCE display label | local lab | lab_rentals | replaced NULL return_date display with Not returned yet |
| DONE | COALESCE elapsed-so-far | local lab | lab_rentals | used return_date or CURRENT_TIMESTAMP as effective end time |
| DONE | CASE + COALESCE open/closed report | local lab | lab_rentals | labeled Open/Closed and calculated elapsed time |
| DONE | Open rental overdue flag | local lab | lab_rentals | compared effective end time to expected return deadline |
| DONE | EXTRACT interval parts | local lab | lab_rentals | extracted day and hour components from rental duration |
| DONE | Total duration hours with EPOCH | local lab | lab_rentals | used EXTRACT(EPOCH) divided by 3600 for total hours |
| DONE | Rounded duration hours | local lab | lab_rentals | rounded total duration hours to 2 decimal places |
| DONE | Duration risk bands | local lab | lab_rentals | classified rentals as Normal, Long, or Very long |
| DONE | CASE order trap | local lab | lab_rentals | checked > 120 before > 72 so Very long is not swallowed by Long |
| DONE | CTE reusable duration feature | local lab | lab_rentals | calculated total_hours once and reused it for rounding and banding |
| DONE | Summary by duration band | local lab | lab_rentals | counted rentals and averaged total hours by duration band |
| DONE | Business-order sorting | local lab | lab_rentals | used CASE in ORDER BY to sort Very long, Long, Normal |
| DONE | Hidden GROUP BY helper column | local lab | lab_rentals | grouped and ordered by band_priority without displaying it |
| DONE | information_schema.columns metadata | local lab | course06_functions_lab | listed table, column, data_type, and udt_name |
| DONE | Schema-specific metadata filter | local lab | course06_functions_lab | found course lab tables outside public schema |
| DONE | Data type discovery | local lab | course06_functions_lab | identified integer, varchar, text, date, timestamp, numeric, and ARRAY columns |
| DONE | ARRAY display | local lab | lab_customers / lab_films | observed PostgreSQL arrays with curly-brace display |
| DONE | ARRAY indexing | local lab | lab_customers / lab_films | accessed array items with [1] and [2] |
| DONE | ARRAY 1-based indexing trap | local lab | lab_customers | confirmed [0] returns NULL while [1] returns first item |
| DONE | ANY() array search | local lab | lab_customers / lab_films | searched for one value inside an array |
| DONE | @> array contains one value | local lab | lab_customers | checked whether favorite_tags contains ARRAY['sql'] |
| DONE | @> array contains multiple values | local lab | lab_customers / lab_films | required multiple array values to be present |
| DONE | CARDINALITY() array count | local lab | lab_customers / lab_films | counted number of items inside arrays |
| DONE | Inspect dirty text | local lab | lab_dirty_text | reviewed raw_text, raw_code, and comparison_text |
| DONE | TRIM / LTRIM / RTRIM | local lab | lab_dirty_text | removed outside padding from text |
| DONE | UPPER / LOWER / INITCAP | local lab | lab_dirty_text | standardized text casing after trimming |
| DONE | String concatenation | local lab | lab_customers | built full_name with || and CONCAT() |
| DONE | LPAD / RPAD | local lab | lab_dirty_text | padded text codes to fixed widths |
| DONE | LENGTH and trimmed length | local lab | lab_dirty_text | compared raw length to cleaned length |
| DONE | Padding quality flag | local lab | lab_dirty_text | used LENGTH comparison to flag outside padding |
| DONE | POSITION / STRPOS | local lab | lab_dirty_text | found substring positions and observed 0 when not found |
| DONE | LEFT / RIGHT | local lab | lab_dirty_text | extracted prefixes and suffixes |
| DONE | SUBSTRING / SUBSTR | local lab | lab_dirty_text | extracted middle string pieces using 1-based positions |
| DONE | REPLACE | local lab | lab_dirty_text | replaced exact matching text |
| DONE | REVERSE | local lab | lab_dirty_text | reversed text strings |
| DONE | Clean report label | local lab | lab_dirty_text | combined LPAD, INITCAP, TRIM, and || into a report label |
| DONE | REGEXP_REPLACE whitespace collapse | inline VALUES demo | text examples | collapsed repeated internal spaces without relying on TRIM |
| DONE | LIKE starts-with wildcard | local lab | lab_dirty_text | used LIKE 'G%' to find comparison_text values starting with G |
| DONE | LIKE contains wildcard | local lab | lab_dirty_text | used LIKE '%BO%' to find comparison_text values containing BO |
| DONE | LIKE single-character wildcard | local lab | lab_dirty_text | used LIKE 'G_MBO' where _ matched exactly one character |
| DONE | LIKE case sensitivity | local lab | lab_dirty_text | proved LIKE '%CASE%' matched but LIKE '%case%' did not |
| DONE | ILIKE case-insensitive search | local lab | lab_dirty_text | used ILIKE '%case%' to match mixed CASE value |
| DONE | TRIM + ILIKE cleaned search | local lab | lab_dirty_text | searched cleaned raw_text for padded values |
| DONE | SPLIT_PART words | local lab | lab_dirty_text | split cleaned raw_text into first, second, and third words |
| DONE | SPLIT_PART generated code | local lab | lab_dirty_text | split generated code values like 7-GAMBOL into code and text parts |
| DONE | CTE parse-and-clean pipeline | local lab | lab_dirty_text | generated code, split it, padded code part, and title-cased text part |
| DONE | Chapter 3 final mini-pipeline | local lab | lab_dirty_text | combined TRIM, INITCAP, LPAD, ||, ILIKE, CASE, and CTE |
| DONE | Inspect searchable film text | local lab | lab_films | reviewed title and description as searchable text fields |
| DONE | to_tsvector searchable document | local lab | lab_films.description | converted description text into searchable English tokens |
| DONE | to_tsquery match with @@ | local lab | lab_films.description | matched searchable descriptions against full-text search queries |
| DONE | Full-text stemming | local lab | lab_films.description | searched astounded and matched Astounding through English stemming |
| DONE | ILIKE vs full-text search | local lab | lab_films.description | compared exact character matching to normalized word-token matching |
| DONE | Full-text AND operator | local lab | lab_films.description | used elf & search to require both tokens |
| DONE | Full-text OR operator | local lab | lab_films.description | used elf | sean to match either token |
| DONE | Full-text NOT operator | local lab | lab_films.description | used elf & !search to exclude search matches |
| DONE | Combined title and description search | local lab | lab_films | searched one document built from title || ' ' || description |
| DONE | plainto_tsquery user-style search | local lab | lab_films | converted plain words into a safe full-text query |
| DONE | Full-text stop-word removal | local lab | plainto_tsquery | showed a and and were removed from a postgres and database |
| DONE | Full-text normalization check | local lab | plainto_tsquery | compared elf to elves and saw different query tokens |
| DONE | Full-text prefix search | local lab | lab_films | used el:* to match tokens starting with el |
| DONE | CREATE EXTENSION fuzzystrmatch | local lab | fuzzystrmatch | enabled fuzzy text functions with IF NOT EXISTS safety |
| DONE | levenshtein edit distance | local lab | fuzzystrmatch | measured string distance as the number of edits required |
| DONE | levenshtein threshold filtering | local lab | lab_films.title | filtered likely title matches by small edit distance |
| DONE | soundex sound-alike codes | local lab | fuzzystrmatch | compared phonetic codes for similar-sounding words |
| DONE | difference sound similarity score | local lab | fuzzystrmatch | used the 0-to-4 sound similarity score |
| DONE | Combined sound and edit-distance fuzzy candidate report | local lab | lab_customers.first_name | combined difference and levenshtein to rank fuzzy name candidates |
| DONE | CREATE EXTENSION pg_trgm | local lab | pg_trgm | enabled trigram text similarity functions |
| DONE | pg_trgm extension schema check | local lab | pg_extension | verified pg_trgm lives in course06_functions_lab |
| DONE | similarity basic score | local lab | pg_trgm | compared POSTGRES HERO against typo and unrelated text |
| DONE | similarity title ranking | local lab | lab_films.title | ranked film titles by trigram similarity |
| DONE | similarity threshold filtering | local lab | lab_films.title | kept only rows with similarity >= 0.3 |
| DONE | pg_trgm CTE label | local lab | lab_films.title | calculated title similarity once and labeled match strength |
| DONE | pg_trgm percent operator | local lab | lab_films.title | used title % search_text as similar-enough shortcut |
| DONE | pg_trgm threshold inspection | local lab | SHOW pg_trgm.similarity_threshold | confirmed default threshold was 0.3 |
| DONE | show_limit() threshold check | local lab | show_limit() | confirmed active similarity threshold |
| DONE | set_limit threshold test | local lab | set_limit() | temporarily raised threshold to 0.8 and reset to 0.3 |
| DONE | word_similarity clean vs sentence input | local lab | pg_trgm | showed word_similarity stays strong when search text is buried in a longer sentence |
| DONE | word_similarity candidate report | local lab | lab_films.title | found POSTGRES HERO from a longer user-style phrase |
| DONE | trigram distance ranking | local lab | lab_films.title | used <-> distance operator to rank closest matches first |

## 4. Chapter 1 Lab Notes — Data Types and Arrays

Chapter 1 is about understanding what data types exist in the database and how PostgreSQL handles arrays. The key practical workflow is:

database metadata -> table/column discovery -> data type recognition ->
array display -> array indexing -> array search.

### 4.1 Completed lab topic: database metadata and data types

#### information_schema.columns metadata

- Goal:
  List tables, columns, SQL data types, and PostgreSQL internal type names.
- SQL:

```sql
SELECT
  table_name,
  column_name,
  data_type,
  udt_name
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

- Observed result notes:

* This returned public-schema tables like course05_sales_events, smoke_test, and students.
* It showed columns with types such as integer, text, date, numeric, and timestamp with time zone.
* It did not show lab_rentals because lab_rentals is not in the public schema.

- Pattern learned:
  information_schema.columns is a metadata table that describes database tables and columns.
- Memory line:
  information_schema.columns tells you what tables and columns exist.

#### Schema-specific metadata filter

- Goal:
  Find the actual schema for lab_rentals.
- SQL:

```sql
SELECT
  table_schema,
  table_name,
  column_name,
  data_type,
  udt_name
FROM information_schema.columns
WHERE table_name = 'lab_rentals'
ORDER BY ordinal_position;
```

- Observed result notes:

* lab_rentals lives in schema course06_functions_lab.
* Full table name is course06_functions_lab.lab_rentals.
* Columns found:
  rental_id integer / int4
  customer_id integer / int4
  film_id integer / int4
  rental_date timestamp without time zone / timestamp
  return_date timestamp without time zone / timestamp

- Pattern learned:
  A table may not live in public. Use table_schema to understand where it lives.
- Memory line:
  database -> schema -> table -> column.
- Common trap:
  Filtering only table_schema = 'public' can hide course or lab tables that live in a different schema.

#### Course lab data type discovery

- Goal:
  Inspect all course06_functions_lab tables and column types.
- SQL:

```sql
SELECT
  table_name,
  column_name,
  data_type,
  udt_name
FROM information_schema.columns
WHERE table_schema = 'course06_functions_lab'
ORDER BY table_name, ordinal_position;
```

- Observed result notes:

  Tables found:

* lab_customers
* lab_dirty_text
* lab_films
* lab_payments
* lab_rentals

  Important data types found:

* integer -> int4
* character varying -> varchar
* text -> text
* date -> date
* timestamp without time zone -> timestamp
* numeric -> numeric
* ARRAY -> _text

  Array columns found:

* lab_customers.favorite_tags ARRAY / _text
* lab_films.special_features ARRAY / _text

- Pattern learned:
  data_type is the friendly SQL type. udt_name is PostgreSQL's internal/base type name.
- Memory line:
  ARRAY with udt_name _text means text array.

### 4.2 Completed lab topic: working with ARRAYs

#### ARRAY display

- Goal:
  View text array columns in lab tables.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  last_name,
  favorite_tags
FROM lab_customers
ORDER BY customer_id;
```

- Observed result:

* Sean: {sql,analytics,postgres}
* Anna: {python,dashboard}
* Brian: {strategy,sql}
* Maya: {reporting,postgres}
* Omar: {data,quality}

- SQL:

```sql
SELECT
  film_id,
  title,
  special_features
FROM lab_films
ORDER BY film_id;
```

- Observed result notes:

* ELF ADVENTURE: {Trailers,"Deleted Scenes"}
* DATA DETECTIVE: {Commentaries,"Behind the Scenes"}
* POSTGRES HERO: {Trailers,Commentaries}
* CLEAN TEXT CLUB: {"Deleted Scenes"}
* THE FUZZY ELF: {Trailers,"Behind the Scenes"}
* ARRAY GAMES: {Commentaries}

- Pattern learned:
  PostgreSQL displays arrays with curly braces. Values with spaces are quoted.
- Memory line:
  ARRAY columns store multiple values in one column.

#### ARRAY indexing

- Goal:
  Access individual array elements.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  favorite_tags,
  favorite_tags[1] AS first_tag,
  favorite_tags[2] AS second_tag
FROM lab_customers
ORDER BY customer_id;
```

- Observed result notes:

* Sean first_tag sql, second_tag analytics
* Anna first_tag python, second_tag dashboard
* Brian first_tag strategy, second_tag sql
* Maya first_tag reporting, second_tag postgres
* Omar first_tag data, second_tag quality

- SQL:

```sql
SELECT
  film_id,
  title,
  special_features,
  special_features[1] AS first_feature
FROM lab_films
ORDER BY film_id;
```

- Observed result notes:

* ELF ADVENTURE first_feature Trailers
* DATA DETECTIVE first_feature Commentaries
* CLEAN TEXT CLUB first_feature Deleted Scenes
* ARRAY GAMES first_feature Commentaries

- Pattern learned:
  PostgreSQL array indexes start at 1.
- Memory line:
  ARRAY[1] = first item. ARRAY[2] = second item.

#### ARRAY 1-based indexing trap

- Goal:
  Prove that PostgreSQL arrays are not zero-based.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  favorite_tags,
  favorite_tags[0] AS zero_index_tag,
  favorite_tags[1] AS first_tag
FROM lab_customers
ORDER BY customer_id;
```

- Observed result notes:

* favorite_tags[0] returned NULL/blank.
* favorite_tags[1] returned the first real array item.

- Pattern learned:
  PostgreSQL arrays are 1-based, unlike Python lists.
- Common trap:
  Do not use [0] expecting the first item.
- Memory line:
  [0] = NULL / not useful in this lab. [1] = first item.

#### ANY() array search

- Goal:
  Find rows where an array contains one searched value.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  favorite_tags
FROM lab_customers
WHERE 'sql' = ANY(favorite_tags)
ORDER BY customer_id;
```

- Observed result:

* Sean: {sql,analytics,postgres}
* Brian: {strategy,sql}

- Pattern learned:
  'value' = ANY(array_column) is true when the value appears anywhere in the array.
- Memory line:
  ANY checks one searched value against array items.

#### @> contains one value

- Goal:
  Use PostgreSQL's array contains operator.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  favorite_tags
FROM lab_customers
WHERE favorite_tags @> ARRAY['sql']
ORDER BY customer_id;
```

- Observed result:

* Sean: {sql,analytics,postgres}
* Brian: {strategy,sql}

- Pattern learned:
  array_column @> ARRAY['value'] checks whether the left array contains the right array.
- Memory line:
  @> means the left array contains the requested array.

#### @> contains multiple required values

- Goal:
  Require multiple array values to be present.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  favorite_tags
FROM lab_customers
WHERE favorite_tags @> ARRAY['sql', 'postgres']
ORDER BY customer_id;
```

- Observed result:

* Sean only: {sql,analytics,postgres}

- Pattern learned:
  ARRAY['sql', 'postgres'] means both values must be present.
- Memory line:
  @> ARRAY['a', 'b'] means contains a AND b.

#### ANY() and @> on film special_features

- Goal:
  Compare one-value ANY search with multi-value @> search on films.
- SQL:

```sql
SELECT
  film_id,
  title,
  special_features
FROM lab_films
WHERE 'Trailers' = ANY(special_features)
ORDER BY film_id;
```

- Observed result:

* 101 ELF ADVENTURE
* 103 POSTGRES HERO
* 105 THE FUZZY ELF

- SQL:

```sql
SELECT
  film_id,
  title,
  special_features
FROM lab_films
WHERE special_features @> ARRAY['Trailers', 'Behind the Scenes']
ORDER BY film_id;
```

- Observed result:

* 105 THE FUZZY ELF only

- Pattern learned:
  ANY checks one searched value. @> ARRAY[...] can require all listed values.
- Memory line:
  ANY = one searched value appears in the array.
  @> ARRAY[...] = all requested values are present.

#### CARDINALITY() array count

- Goal:
  Count how many items are inside an array.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  favorite_tags,
  CARDINALITY(favorite_tags) AS tag_count
FROM lab_customers
ORDER BY customer_id;
```

- Observed result notes:

* Sean tag_count 3
* Anna tag_count 2
* Brian tag_count 2
* Maya tag_count 2
* Omar tag_count 2

- SQL:

```sql
SELECT
  film_id,
  title,
  special_features,
  CARDINALITY(special_features) AS feature_count
FROM lab_films
ORDER BY film_id;
```

- Observed result notes:

* ELF ADVENTURE feature_count 2
* CLEAN TEXT CLUB feature_count 1
* ARRAY GAMES feature_count 1

- Pattern learned:
  CARDINALITY(array_column) returns the number of items in the array.
- Memory line:
  CARDINALITY(array_column) = number of items inside the array.

## 5. Chapter 2 Lab Notes — Date/Time Functions

This is the current active area.

### Chapter 2 Quick Jumps

* [5.1 Rental return analysis](#51-completed-lab-mini-pipeline-rental-return-analysis)
* [5.2 EXTRACT vs DATE_TRUNC](#52-completed-lab-topic-extract-vs-date_trunc)
* [5.3 DATE_PART vs EXTRACT](#53-completed-lab-topic-date_part-vs-extract)
* [5.4 Current date/time functions](#54-completed-lab-topic-current-datetime-functions)
* [5.5 Casting timestamp to date](#55-completed-lab-topic-casting-timestamp-to-date)
* [5.6 Rental duration](#56-completed-lab-topic-rental-duration)
* [5.7 Concepts already covered](#57-concepts-already-covered-by-completed-labs)
* [5.8 Direct-practice topics](#58-completed-direct-practice-topics)
* [5.9 COALESCE and open-record reporting](#59-completed-lab-topic-coalesce-and-open-record-reporting)
* [5.10 Interval features and duration bands](#510-completed-lab-topic-interval-features-and-duration-bands)
* [5.11 Reusable duration-band reporting](#511-completed-lab-topic-reusable-duration-band-reporting)

### 5.1 Completed lab mini-pipeline: rental return analysis

#### Expected return date

- Goal:
  Calculate an expected return timestamp by adding a 3-day allowed rental window to `rental_date`.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  rental_date + INTERVAL '3 days' AS expected_return_date
FROM lab_rentals;
```

- Expected result:
  A calculated timestamp deadline for each rental that stays aligned to the original time of day.
- Pattern learned:
  `TIMESTAMP + INTERVAL` creates a shifted timestamp and preserves time of day.
- Common trap:
  `DATE + integer` can work for date-only math, but `TIMESTAMP + INTERVAL` is the better habit for timestamp calculations.

#### Late by interval

- Goal:
  Compare actual `return_date` to `expected_return_date`.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  rental_date + INTERVAL '3 days' AS expected_return_date,
  return_date - (rental_date + INTERVAL '3 days') AS late_by
FROM lab_rentals;
```

- Expected result:
  Positive `late_by` means late. Negative `late_by` means early. `NULL late_by` means `return_date` is missing.
  Observed examples:
  `rental_id 1002` was late by `2 days 02:45:00`
  `rental_id 1006` was late by `5 days`
  `rental_id 1005` had `NULL late_by` because `return_date` was `NULL`
- Pattern learned:
  `TIMESTAMP - TIMESTAMP` returns an `INTERVAL`.
- Common trap:
  A missing `return_date` keeps the interval result `NULL`, so unfinished rentals need explicit handling later.

#### Return status label with CASE

- Goal:
  Turn raw interval logic into a readable business label.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  rental_date + INTERVAL '3 days' AS expected_return_date,
  return_date - (rental_date + INTERVAL '3 days') AS late_by,
  CASE
    WHEN return_date IS NULL THEN 'Not returned'
    WHEN return_date > rental_date + INTERVAL '3 days' THEN 'Late'
    ELSE 'On time or early'
  END AS return_status
FROM lab_rentals;
```

- Expected result:
  Each rental gets a readable status label instead of raw timestamp logic only.
- Pattern learned:
  `CASE` turns technical timestamp logic into business-readable categories.
- Common trap:
  Check `return_date IS NULL` first. If you compare `NULL` to a timestamp, the result is unknown, not true or false.

#### Count by return status

- Goal:
  Summarize row-level status labels into a group-level count.
- SQL:

```sql
WITH rental_status AS (
  SELECT
    rental_id,
    CASE
      WHEN return_date IS NULL THEN 'Not returned'
      WHEN return_date > rental_date + INTERVAL '3 days' THEN 'Late'
      ELSE 'On time or early'
    END AS return_status
  FROM lab_rentals
)
SELECT
  return_status,
  COUNT(*) AS rental_count
FROM rental_status
GROUP BY return_status
ORDER BY rental_count DESC;
```

- Expected result:

```text
return_status     | rental_count
------------------+-------------
On time or early  | 4
Late              | 3
Not returned      | 1
```

- Pattern learned:
  Use a CTE to create row-level labels first, then aggregate those labels.
- Common trap:
  Trying to jump straight into grouped counts before naming the row-level business rule can make the query harder to debug.
- Memory line:
  Raw timestamps -> calculated deadline -> interval difference -> business label -> summary count.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.2 Completed lab topic: EXTRACT vs DATE_TRUNC

#### EXTRACT vs DATE_TRUNC

- Goal:
  Compare extracting a numeric month part with creating a monthly timestamp bucket.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  EXTRACT(month FROM rental_date) AS rental_month_number,
  DATE_TRUNC('month', rental_date) AS rental_month_bucket
FROM lab_rentals
ORDER BY rental_date;
```

- Expected result:
  January rentals returned `rental_month_number = 1`.
  February rentals returned `rental_month_number = 2`.
  March rentals returned `rental_month_number = 3`.
  `DATE_TRUNC('month', rental_date)` returned month buckets:
  `2026-01-01 00:00:00`
  `2026-02-01 00:00:00`
  `2026-03-01 00:00:00`
- Pattern learned:
  `EXTRACT()` gives a number. `DATE_TRUNC()` gives a timestamp bucket.
- Common trap:
  Do not use `EXTRACT(month FROM rental_date)` alone for cross-year monthly grouping, because January 2025 and January 2026 would both be month `1`. Use `DATE_TRUNC('month', rental_date)` for timeline grouping.

#### Monthly rental grouping

- Goal:
  Count rentals by month using a timestamp bucket.
- SQL:

```sql
SELECT
  DATE_TRUNC('month', rental_date) AS rental_month,
  COUNT(*) AS rental_count
FROM lab_rentals
GROUP BY DATE_TRUNC('month', rental_date)
ORDER BY rental_month;
```

- Expected result:

```text
rental_month         | rental_count
---------------------+-------------
2026-01-01 00:00:00  | 3
2026-02-01 00:00:00  | 3
2026-03-01 00:00:00  | 2
```

- Pattern learned:
  Raw timestamp -> monthly bucket -> `GROUP BY` bucket -> trend count.
- Common trap:
  Grouping by raw timestamps will fragment the data into individual moments instead of monthly summaries.
- Cleaner CTE pattern:

```sql
WITH rental_months AS (
  SELECT
    rental_id,
    DATE_TRUNC('month', rental_date) AS rental_month
  FROM lab_rentals
)
SELECT
  rental_month,
  COUNT(*) AS rental_count
FROM rental_months
GROUP BY rental_month
ORDER BY rental_month;
```

- Memory line:
  EXTRACT gives a number. DATE_TRUNC gives a timestamp bucket.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.3 Completed lab topic: DATE_PART vs EXTRACT

- Goal:
  Show that `DATE_PART()` and `EXTRACT()` can both pull numeric parts from a timestamp.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  EXTRACT(quarter FROM rental_date) AS quarter_extract,
  DATE_PART('quarter', rental_date) AS quarter_date_part
FROM lab_rentals
ORDER BY rental_date;
```

- Expected result:
  All current sample rentals are in Q1. Both `quarter_extract` and `quarter_date_part` returned `1` for every row.
- Pattern learned:
  `EXTRACT(part FROM timestamp)` and `DATE_PART('part', timestamp)` both pull a numeric date/time part. The syntax is different, but the purpose is similar.
- Common trap:
  Mixing up numeric-part extraction with time bucketing. These functions return values like quarter or month number, not truncated timestamps.
- Memory line:
  `EXTRACT(part FROM timestamp)` and `DATE_PART('part', timestamp)` both pull numeric date/time parts.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.4 Completed lab topic: current date/time functions

#### Current date and time functions

- Goal:
  Compare current date, current time, current timestamp, and `NOW()`.
- SQL:

```sql
SELECT
  CURRENT_DATE AS today_date,
  CURRENT_TIME AS current_clock_time,
  CURRENT_TIMESTAMP AS current_timestamp_value,
  NOW() AS now_value;
```

- Expected result:

```text
today_date | current_clock_time | current_timestamp_value      | now_value
-----------+--------------------+------------------------------+------------------------------
2026-06-04 | 00:00:14.547425+00 | 2026-06-04 00:00:14.547425+00 | 2026-06-04 00:00:14.547425+00
```

- Pattern learned:
  `CURRENT_DATE` returns date only.
  `CURRENT_TIME` returns clock time only.
  `CURRENT_TIMESTAMP` returns date plus time.
  `NOW()` returned the same timestamp value in this query.
- Common trap:
  Assuming all current-time functions return the same shape. They are related, but one returns date only and another returns time only.

#### CURRENT_TIMESTAMP precision

- Goal:
  Control fractional-second precision in current timestamp output.
- SQL:

```sql
SELECT
  CURRENT_TIMESTAMP AS full_timestamp,
  CURRENT_TIMESTAMP(0) AS timestamp_0_precision,
  CURRENT_TIMESTAMP(2) AS timestamp_2_precision;
```

- Expected result:

```text
full_timestamp               | timestamp_0_precision  | timestamp_2_precision
-----------------------------+------------------------+---------------------------
2026-06-04 00:01:23.580534+00 | 2026-06-04 00:01:24+00 | 2026-06-04 00:01:23.58+00
```

- Pattern learned:
  `CURRENT_TIMESTAMP(n)` controls fractional-second precision.
- Common trap:
  `CURRENT_TIMESTAMP(0)` rounds to whole seconds. It may round up.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.5 Completed lab topic: casting timestamp to date

- Goal:
  Remove the time part from a timestamp.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  rental_date::date AS rental_day,
  CAST(rental_date AS date) AS rental_day_cast
FROM lab_rentals
ORDER BY rental_date;
```

- Expected result:
  Both `rental_date::date` and `CAST(rental_date AS date)` returned the same date-only value.
  Example: `2026-01-02 10:15:00` became `2026-01-02`.
- Pattern learned:
  `::date` is PostgreSQL shorthand.
  `CAST(rental_date AS date)` is standard SQL style.
  Both remove the time part.
- Common trap:
  Casting to `date` removes time detail permanently in the result, so do it only when date-only output is actually what you need.
- Interview translation:
  Use PostgreSQL shorthand when working directly in PostgreSQL, but use `CAST()` when portability across SQL systems matters.
- Memory line:
  `::date` is PostgreSQL shorthand. `CAST(... AS date)` is more standard SQL style.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.6 Completed lab topic: rental duration

- Goal:
  Calculate how long each rental lasted.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  return_date - rental_date AS rental_duration
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:

  Observed examples:
  rental_id `1001` duration: `2 days 23:15:00`
  rental_id `1002` duration: `5 days 02:45:00`
  rental_id `1005` duration: `NULL` because `return_date` is missing
  rental_id `1006` duration: `8 days`
- Pattern learned:
  `TIMESTAMP - TIMESTAMP = INTERVAL`.
- Common trap:
  If `return_date` is `NULL`, duration will also be `NULL`, so open rentals need special handling in reporting.
- Memory line:
  Subtract timestamps when you want duration. Add intervals when you want a future or past timestamp.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.7 Concepts already covered by completed labs

| Concept | Covered where | Status |
| --- | --- | --- |
| TIMESTAMP + INTERVAL | expected return date | covered |
| TIMESTAMP - TIMESTAMP | late_by interval and rental duration | covered |
| INTERVAL arithmetic | expected return date and late_by interval | covered |
| CASE with date logic | return status label | covered |
| GROUP BY date bucket | monthly rental grouping | covered |
| EXTRACT() | EXTRACT vs DATE_TRUNC and DATE_PART vs EXTRACT | covered |
| DATE_PART() | DATE_PART vs EXTRACT | covered |
| DATE_TRUNC() | monthly bucket and monthly grouping | covered |
| CURRENT_DATE | current date/time functions | covered |
| CURRENT_TIME | current date/time functions | covered |
| CURRENT_TIMESTAMP | current date/time functions and precision | covered |
| NOW() | current date/time functions | covered |
| CAST and :: | casting timestamp to date | covered |
| DATE - DATE | DATE minus DATE | covered |
| DATE + integer | DATE plus integer | covered |
| DATE + INTERVAL | Clearer INTERVAL version of DATE + integer | covered |
| AGE() | AGE() and AGE() argument order | covered |
| COALESCE() | COALESCE display label and elapsed-so-far | covered |
| COALESCE with CURRENT_TIMESTAMP | elapsed-so-far and open overdue flag | covered |
| CASE with COALESCE | open/closed report and timing_status | covered |
| open-record reporting | CASE + COALESCE open/closed report | covered |
| overdue flag logic | open rental overdue flag | covered |
| EXTRACT from interval | EXTRACT interval parts | covered |
| EXTRACT(EPOCH FROM interval) | Total duration hours with EPOCH | covered |
| ROUND() | Rounded duration hours | covered |
| CASE threshold bands | Duration risk bands | covered |
| CASE order matters | CASE order trap | covered |
| CTE reusable feature | CTE reusable duration feature | covered |
| GROUP BY business band | Summary by duration band | covered |
| AVG() with grouped bands | Summary by duration band | covered |
| CASE in ORDER BY | Business-order sorting | covered |
| hidden GROUP BY column | Hidden GROUP BY helper column | covered |

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.8 Completed direct-practice topics

#### DATE minus DATE

- Goal:
  Show that subtracting one DATE from another DATE returns an integer count of calendar days.
- SQL:

```sql
SELECT
  rental_id,
  rental_date::date AS rental_day,
  return_date::date AS return_day,
  return_date::date - rental_date::date AS rental_days
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1001: 2026-01-05 - 2026-01-02 = 3
  rental_id 1002 returned 5 calendar days
  rental_id 1006 returned 8 calendar days
  rental_id 1005 returned NULL because return_date is NULL
- Pattern learned:
  DATE - DATE returns integer days.
- Common trap:
  This is different from TIMESTAMP - TIMESTAMP. Timestamp subtraction preserves hours/minutes/seconds and returns an INTERVAL.
- Memory line:
  TIMESTAMP - TIMESTAMP = INTERVAL.
  DATE - DATE = integer days.

#### DATE plus integer

- Goal:
  Show that adding an integer to a DATE adds that many calendar days.
- SQL:

```sql
SELECT
  rental_id,
  rental_date::date AS rental_day,
  rental_date::date + 3 AS expected_return_day
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1001: 2026-01-02 + 3 = 2026-01-05
  rental_id 1002: 2026-01-03 + 3 = 2026-01-06
  rental_id 1005: 2026-02-05 + 3 = 2026-02-08
  rental_id 1008: 2026-03-15 + 3 = 2026-03-18
- Pattern learned:
  In PostgreSQL, DATE + integer means add that many days.
- Common trap:
  The integer is not hours, months, or years. PostgreSQL defines DATE + integer as day arithmetic.
- Memory line:
  DATE + integer = date plus that many days.

#### Clearer INTERVAL version of DATE + integer

- Goal:
  Answer Sean's question: how does PostgreSQL know `rental_date::date + 3` means 3 days, and is there a clearer way?
- Explanation:
  PostgreSQL has a built-in operator where DATE + integer means add integer days. A clearer, more human-readable version is to use INTERVAL.
- SQL option 1 - explicit INTERVAL:

```sql
SELECT
  rental_id,
  rental_date::date AS rental_day,
  rental_date::date + INTERVAL '3 days' AS expected_return_timestamp
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  The result became timestamp-like and showed midnight:
  `2026-01-05 00:00:00`
  This happened because `rental_date::date` removed the time first.
  A DATE behaves like midnight when converted into timestamp-style interval math.
- SQL option 2 - explicit INTERVAL, then cast back to DATE:

```sql
SELECT
  rental_id,
  rental_date::date AS rental_day,
  (rental_date::date + INTERVAL '3 days')::date AS expected_return_day
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  This returned date-only results again:
  2026-01-05, 2026-01-06, 2026-01-13, etc.
- Pattern learned:
  `rental_date + INTERVAL '3 days'` keeps original timestamp time of day.
  `rental_date::date + INTERVAL '3 days'` resets the time to midnight.
  `(rental_date::date + INTERVAL '3 days')::date` gives an explicit date-only due day.
- Common trap:
  Casting to DATE first removes time-of-day detail. If exact timestamp deadlines matter, use `rental_date + INTERVAL '3 days'`, not `rental_date::date`.
- Best practical rule:

```text
For exact timestamp deadlines:
rental_date + INTERVAL '3 days'

For date-only due days:
rental_date::date + 3

For very explicit date-only due days:
(rental_date::date + INTERVAL '3 days')::date
```

#### AGE()

- Goal:
  Compare AGE() to direct timestamp subtraction.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  return_date - rental_date AS direct_duration,
  AGE(return_date, rental_date) AS age_duration
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  For this dataset, `direct_duration` and `age_duration` looked the same.
  rental_id 1001 returned `2 days 23:15:00` for both.
  rental_id 1002 returned `5 days 02:45:00` for both.
  rental_id 1005 returned NULL because return_date is NULL.
  rental_id 1006 returned `8 days` for both.
- Pattern learned:
  For simple day/hour differences, AGE() and direct subtraction may look similar.
- Conceptual difference:

```text
timestamp - timestamp = direct interval math
AGE(later, earlier)   = human-style elapsed interval
```

- Common trap:
  AGE() argument order matters.

#### AGE() argument order

- Goal:
  Show that reversing AGE() arguments produces negative intervals.
- SQL:

```sql
SELECT
  rental_id,
  AGE(return_date, rental_date) AS correct_age,
  AGE(rental_date, return_date) AS reversed_age
FROM lab_rentals
WHERE return_date IS NOT NULL
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  correct_age was positive.
  reversed_age was negative.
  rental_id 1001:
  `correct_age: 2 days 23:15:00`
  `reversed_age: -2 days -23:15:00`
  rental_id 1006:
  `correct_age: 8 days`
  `reversed_age: -8 days`
- Pattern learned:
  AGE(later, earlier) gives positive elapsed time.
  AGE(earlier, later) gives negative elapsed time.
- Memory line:
  AGE(later, earlier) = positive elapsed time.
  AGE(earlier, later) = negative elapsed time.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.9 Completed lab topic: COALESCE and open-record reporting

#### COALESCE display label

- Goal:
  Replace a NULL return_date display with a readable fallback label.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  COALESCE(return_date::text, 'Not returned yet') AS return_date_display
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  Returned rentals showed their return_date as text.
  rental_id 1005 had NULL return_date and displayed `Not returned yet`.
- Pattern learned:
  COALESCE checks values from left to right and returns the first non-NULL value.
- Common trap:
  COALESCE arguments should be compatible types. We used `return_date::text` because the fallback value `'Not returned yet'` is text.
- Memory line:
  COALESCE(value, fallback) = use value unless it is NULL.

#### COALESCE elapsed-so-far

- Goal:
  Calculate elapsed time for both closed and still-open rentals.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  COALESCE(return_date, CURRENT_TIMESTAMP) - rental_date AS elapsed_so_far
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  Returned rentals used return_date.
  Open rental 1005 used CURRENT_TIMESTAMP.
  rental_id 1005 showed an elapsed_so_far value over 118 days at the time of the run.
- Pattern learned:
  COALESCE can supply a substitute endpoint for open records.
- Memory line:
  COALESCE(return_date, CURRENT_TIMESTAMP) - rental_date
  = elapsed time for both closed and still-open records.
- Use cases:
  open tickets
  open incidents
  open rentals
  open orders
  unresolved alerts

#### CASE + COALESCE open/closed report

- Goal:
  Label each rental as Open or Closed and calculate elapsed time safely.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  CASE
    WHEN return_date IS NULL THEN 'Open'
    ELSE 'Closed'
  END AS rental_state,
  COALESCE(return_date, CURRENT_TIMESTAMP) - rental_date AS elapsed_so_far
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1005 was labeled `Open`.
  all other rentals were labeled `Closed`.
  closed rentals used actual rental duration.
  open rental 1005 used a running duration from rental_date to CURRENT_TIMESTAMP.
- Pattern learned:
  CASE labels the state. COALESCE fills the missing endpoint. Timestamp subtraction calculates elapsed time.
- Memory line:
  CASE labels the state.
  COALESCE fills the missing endpoint.
  Subtract timestamps to get elapsed time.

#### Open rental overdue flag

- Goal:
  Create a production-style timing report for both returned and open rentals.
- SQL:

```sql
SELECT
  rental_id,
  rental_date,
  return_date,
  CASE
    WHEN return_date IS NULL THEN 'Open'
    ELSE 'Closed'
  END AS rental_state,
  rental_date + INTERVAL '3 days' AS expected_return_date,
  COALESCE(return_date, CURRENT_TIMESTAMP) AS effective_end_time,
  COALESCE(return_date, CURRENT_TIMESTAMP)
    - (rental_date + INTERVAL '3 days') AS overdue_by,
  CASE
    WHEN COALESCE(return_date, CURRENT_TIMESTAMP)
           > rental_date + INTERVAL '3 days'
      THEN 'Overdue or late'
    ELSE 'On time'
  END AS timing_status
FROM lab_rentals
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1005 was Open and Overdue or late.
  rental_id 1005 used CURRENT_TIMESTAMP as effective_end_time.
  rental_id 1005 was overdue by more than 115 days at the time of the run.
  rental_ids 1002, 1006, and 1007 were Closed but Overdue or late.
  rental_ids 1001, 1003, 1004, and 1008 were On time.
  Negative overdue_by means returned before the expected deadline.
  Positive overdue_by means overdue or late.
- Pattern learned:
  Use an effective end time to handle both completed and still-open records in one query.
- Memory line:

```text
effective_end_time = COALESCE(actual_end, current_time)
deadline           = start_time + allowed_interval
overdue_by         = effective_end_time - deadline
```

- Common trap:
  If you only compare return_date to the deadline, open records with NULL return_date will not be evaluated properly. Use COALESCE when the business question requires treating open records as still running.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.10 Completed lab topic: interval features and duration bands

#### EXTRACT day/hour parts from interval

- Goal:
  Show that EXTRACT can pull individual parts from an interval.
- SQL:

```sql
SELECT
  rental_id,
  return_date - rental_date AS rental_duration,
  EXTRACT(day FROM return_date - rental_date) AS duration_days_part,
  EXTRACT(hour FROM return_date - rental_date) AS duration_hours_part
FROM lab_rentals
WHERE return_date IS NOT NULL
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1001 had rental_duration `2 days 23:15:00`,
  duration_days_part `2`, and duration_hours_part `23`.
  rental_id 1002 had rental_duration `5 days 02:45:00`,
  duration_days_part `5`, and duration_hours_part `2`.
  rental_id 1006 had rental_duration `8 days`,
  duration_days_part `8`, and duration_hours_part `0`.
- Pattern learned:
  `EXTRACT(day FROM interval)` returns the day component.
  `EXTRACT(hour FROM interval)` returns the hour component after days are separated.
- Common trap:
  `EXTRACT(hour FROM interval)` does not return total hours.
- Memory line:

```text
EXTRACT(day FROM interval)  = day piece
EXTRACT(hour FROM interval) = hour piece
```

#### Total duration hours with EPOCH

- Goal:
  Convert an interval into total hours.
- SQL:

```sql
SELECT
  rental_id,
  return_date - rental_date AS rental_duration,
  EXTRACT(EPOCH FROM return_date - rental_date) / 3600
    AS total_duration_hours
FROM lab_rentals
WHERE return_date IS NOT NULL
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1001 total_duration_hours was `71.2500000000000000`.
  rental_id 1002 total_duration_hours was `122.7500000000000000`.
  rental_id 1003 total_duration_hours was `50.8333333333333333`.
  rental_id 1006 total_duration_hours was `192.0000000000000000`.
- Pattern learned:
  `EXTRACT(EPOCH FROM interval)` returns total seconds.
  Divide by 3600 to get total hours.
- Common trap:
  For `5 days 02:45:00`, `EXTRACT(hour FROM interval)` returns `2`,
  but `EXTRACT(EPOCH FROM interval) / 3600` returns `122.75`.
- Memory line:

```text
EXTRACT(hour FROM interval) = hour component only
EXTRACT(EPOCH FROM interval) / 3600 = total hours
```

#### Rounded duration hours

- Goal:
  Make total duration hours report-friendly.
- SQL:

```sql
SELECT
  rental_id,
  return_date - rental_date AS rental_duration,
  ROUND(
    EXTRACT(EPOCH FROM return_date - rental_date) / 3600,
    2
  ) AS total_duration_hours
FROM lab_rentals
WHERE return_date IS NOT NULL
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1001 rounded to `71.25`.
  rental_id 1002 rounded to `122.75`.
  rental_id 1003 rounded to `50.83`.
  rental_id 1004 rounded to `48.50`.
  rental_id 1006 rounded to `192.00`.
  rental_id 1007 rounded to `74.25`.
  rental_id 1008 rounded to `48.83`.
- Pattern learned:
  Use `ROUND(..., 2)` to make calculated numeric duration values easier to read in reports.
- Memory line:

```text
Use EXTRACT(EPOCH) for total duration.
Use ROUND(..., 2) for report-friendly numbers.
```

#### Duration risk bands

- Goal:
  Classify rentals by total duration hours.
- SQL:

```sql
SELECT
  rental_id,
  return_date - rental_date AS rental_duration,
  ROUND(
    EXTRACT(EPOCH FROM return_date - rental_date) / 3600,
    2
  ) AS total_duration_hours,
  CASE
    WHEN EXTRACT(EPOCH FROM return_date - rental_date) / 3600 > 120
      THEN 'Very long'
    WHEN EXTRACT(EPOCH FROM return_date - rental_date) / 3600 > 72
      THEN 'Long'
    ELSE 'Normal'
  END AS duration_band
FROM lab_rentals
WHERE return_date IS NOT NULL
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  rental_id 1002 had `122.75` hours and was labeled `Very long`.
  rental_id 1006 had `192.00` hours and was labeled `Very long`.
  rental_id 1007 had `74.25` hours and was labeled `Long`.
  rental_ids 1001, 1003, 1004, and 1008 were labeled `Normal`.
- Pattern learned:
  Raw interval -> numeric feature -> rounded report value -> business band.
- Memory line:

```text
interval -> total numeric hours -> rounded report value -> business band
```

- Interview / real-world translation:

```text
raw metric -> calculated feature -> threshold/risk band -> business label
```

#### CASE order trap

- Goal:
  Explain why the order of CASE conditions matters when thresholds overlap.
- Explanation:
  The duration band query checks `> 120` before `> 72`.
- Correct order:

```sql
CASE
  WHEN hours > 120 THEN 'Very long'
  WHEN hours > 72 THEN 'Long'
  ELSE 'Normal'
END
```

- Reason:
  A value like `122.75` is greater than both 120 and 72.
  If the `> 72` condition is checked first, then `122.75` becomes `Long`
  instead of `Very long`.
- Pattern learned:
  Put the most specific or highest threshold first when CASE conditions overlap.
- Common trap:
  CASE stops at the first matching WHEN condition.
- Memory line:

```text
When thresholds overlap, order CASE from most severe/specific to least severe/general.
```

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

### 5.11 Completed lab topic: reusable duration-band reporting

#### CTE to avoid repeated duration formula

- Goal:
  Avoid repeating the same total-hours expression multiple times.
- SQL:

```sql
WITH rental_hours AS (
  SELECT
    rental_id,
    return_date - rental_date AS rental_duration,
    EXTRACT(EPOCH FROM return_date - rental_date) / 3600
      AS total_hours
  FROM lab_rentals
  WHERE return_date IS NOT NULL
)
SELECT
  rental_id,
  rental_duration,
  ROUND(total_hours, 2) AS total_duration_hours,
  CASE
    WHEN total_hours > 120 THEN 'Very long'
    WHEN total_hours > 72 THEN 'Long'
    ELSE 'Normal'
  END AS duration_band
FROM rental_hours
ORDER BY rental_id;
```

- Expected result:
  Observed result notes:
  The output matched the prior duration-band report.
  rental_id 1002 was `122.75` hours and `Very long`.
  rental_id 1006 was `192.00` hours and `Very long`.
  rental_id 1007 was `74.25` hours and `Long`.
  Other returned rentals were `Normal`.
- Pattern learned:
  Use a CTE when a calculated feature is reused.
- Memory line:
  Calculate once, then label and report many times.

#### Summarize by duration band

- Goal:
  Move from row-level duration labels to a grouped summary report.
- SQL:

```sql
WITH rental_hours AS (
  SELECT
    rental_id,
    EXTRACT(EPOCH FROM return_date - rental_date) / 3600
      AS total_hours
  FROM lab_rentals
  WHERE return_date IS NOT NULL
),
rental_bands AS (
  SELECT
    rental_id,
    total_hours,
    CASE
      WHEN total_hours > 120 THEN 'Very long'
      WHEN total_hours > 72 THEN 'Long'
      ELSE 'Normal'
    END AS duration_band
  FROM rental_hours
)
SELECT
  duration_band,
  COUNT(*) AS rental_count,
  ROUND(AVG(total_hours), 2) AS avg_duration_hours
FROM rental_bands
GROUP BY duration_band
ORDER BY avg_duration_hours DESC;
```

- Expected result:

```text
duration_band | rental_count | avg_duration_hours
--------------+--------------+-------------------
Very long     | 2            | 157.38
Long          | 1            | 74.25
Normal        | 4            | 54.85
```

- Pattern learned:
  Calculate feature -> assign band -> summarize by band.
- Interview / real-world translation:
  Raw event timestamps -> duration feature -> threshold band -> grouped operational summary.

#### Sort bands by business order

- Goal:
  Sort labels by business meaning instead of alphabetic order.
- SQL:

```sql
WITH rental_hours AS (
  SELECT
    rental_id,
    EXTRACT(EPOCH FROM return_date - rental_date) / 3600
      AS total_hours
  FROM lab_rentals
  WHERE return_date IS NOT NULL
),
rental_bands AS (
  SELECT
    rental_id,
    total_hours,
    CASE
      WHEN total_hours > 120 THEN 'Very long'
      WHEN total_hours > 72 THEN 'Long'
      ELSE 'Normal'
    END AS duration_band
  FROM rental_hours
)
SELECT
  duration_band,
  COUNT(*) AS rental_count,
  ROUND(AVG(total_hours), 2) AS avg_duration_hours
FROM rental_bands
GROUP BY duration_band
ORDER BY
  CASE duration_band
    WHEN 'Very long' THEN 1
    WHEN 'Long' THEN 2
    WHEN 'Normal' THEN 3
    ELSE 99
  END;
```

- Expected result:

```text
Very long
Long
Normal
```

- Pattern learned:
  Use CASE in ORDER BY when labels need business priority order.
- Memory line:
  Do not trust alphabetic order for business labels.

#### Hidden GROUP BY helper column

- Goal:
  Use a numeric priority column for ordering without displaying it.
- SQL:

```sql
WITH rental_hours AS (
  SELECT
    rental_id,
    EXTRACT(EPOCH FROM return_date - rental_date) / 3600
      AS total_hours
  FROM lab_rentals
  WHERE return_date IS NOT NULL
),
rental_bands AS (
  SELECT
    rental_id,
    total_hours,
    CASE
      WHEN total_hours > 120 THEN 'Very long'
      WHEN total_hours > 72 THEN 'Long'
      ELSE 'Normal'
    END AS duration_band,
    CASE
      WHEN total_hours > 120 THEN 1
      WHEN total_hours > 72 THEN 2
      ELSE 3
    END AS band_priority
  FROM rental_hours
)
SELECT
  duration_band,
  COUNT(*) AS rental_count,
  ROUND(AVG(total_hours), 2) AS avg_duration_hours
FROM rental_bands
GROUP BY
  duration_band,
  band_priority
ORDER BY band_priority;
```

- Expected result:

```text
duration_band | rental_count | avg_duration_hours
--------------+--------------+-------------------
Very long     | 2            | 157.38
Long          | 1            | 74.25
Normal        | 4            | 54.85
```

- Pattern learned:
  GROUP BY can use a helper column that is not displayed in SELECT.
- Important rule:
  GROUP BY controls how SQL forms the piles.
  SELECT controls what SQL displays from each pile.
  ORDER BY controls how SQL sorts the final result.
- Memory line:
  GROUP BY can use hidden helper columns.
  SELECT must only show grouped columns or aggregates.
- Common trap:
  A non-aggregate column shown in SELECT must be included in GROUP BY.
- Good:

```sql
SELECT
  duration_band,
  COUNT(*)
FROM rental_bands
GROUP BY duration_band;
```

- Bad:

```sql
SELECT
  duration_band,
  band_priority,
  COUNT(*)
FROM rental_bands
GROUP BY duration_band;
```

- Why bad:
  band_priority is displayed, but it is not grouped or aggregated.

[Back to Chapter 2 Quick Jumps](#chapter-2-quick-jumps)

## 6. Chapter 3 Lab Notes — Text Functions

Chapter 3 is about turning messy text into clean, searchable, report-friendly
values. The practical workflow is:

messy text -> trim -> standardize case -> inspect length -> parse pieces ->
replace or transform text -> build clean labels.

### 6.1 Completed lab topic: inspect and clean dirty text

#### Inspect dirty text

- Goal:
  View the raw practice table for Chapter 3 text functions.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text,
  raw_code,
  comparison_text
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* raw_text includes padded and mixed-case text.
* raw_code contains numeric-looking codes stored as text.
* comparison_text contains words used for string search and parsing practice.
* Example rows:

  * dirty_id 1: raw_text had padded text, raw_code 7, comparison_text GAMBOL
  * dirty_id 2: raw_text mixed CASE value, raw_code 42, comparison_text GUMBO
  * dirty_id 3: raw_text A Astounding example, raw_code 305, comparison_text ELF
  * dirty_id 4: raw_text left padded only, raw_code 9, comparison_text ELVES
  * dirty_id 5: raw_text right padded only, raw_code 1234, comparison_text POSTGRES

- Pattern learned:
  Before cleaning text, inspect the raw values and identify the kind of mess.
- Memory line:
  Inspect first, then clean.

#### TRIM / LTRIM / RTRIM

- Goal:
  Remove outside spaces from raw_text.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text,
  TRIM(raw_text) AS trim_both_sides,
  LTRIM(raw_text) AS trim_left_side,
  RTRIM(raw_text) AS trim_right_side
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* TRIM removed spaces from both sides.
* LTRIM removed spaces from the left side only.
* RTRIM removed spaces from the right side only.
* dirty_id 1 changed from padded raw text to padded text.
* dirty_id 4 showed the left-padding cleanup clearly.
* dirty_id 5 showed the right-padding cleanup clearly.

- Pattern learned:
  TRIM cleans outside padding, not spaces inside the sentence.
- Memory line:
  TRIM() removes both sides. LTRIM() removes left. RTRIM() removes right.

#### UPPER / LOWER / INITCAP

- Goal:
  Standardize text case after trimming.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text,
  TRIM(raw_text) AS cleaned_text,
  UPPER(TRIM(raw_text)) AS upper_text,
  LOWER(TRIM(raw_text)) AS lower_text,
  INITCAP(TRIM(raw_text)) AS title_case_text
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* padded text became PADDED TEXT, padded text, and Padded Text.
* mixed CASE value became MIXED CASE VALUE, mixed case value, and Mixed Case Value.
* A Astounding example became A ASTOUNDING EXAMPLE, a astounding example, and A Astounding Example.

- Pattern learned:
  Clean first, then format.
- Memory line:
  TRIM removes outside padding. UPPER, LOWER, and INITCAP standardize case.

### 6.2 Completed lab topic: concatenate and format report text

#### String concatenation with || and CONCAT()

- Goal:
  Build full customer names from first_name and last_name.
- SQL:

```sql
SELECT
  customer_id,
  first_name,
  last_name,
  first_name || ' ' || last_name AS full_name_pipe,
  CONCAT(first_name, ' ', last_name) AS full_name_concat
FROM lab_customers
ORDER BY customer_id;
```

- Observed result notes:

* Both methods produced the same readable names:

  * Sean Girgis
  * Anna Rivera
  * Brian Piccolo
  * Maya Chen
  * Omar Hassan

- Pattern learned:
  Use || or CONCAT() to build report-friendly text labels.
- Memory line:
  || is PostgreSQL string join syntax. CONCAT() is function-style string joining.
- Common trap:
  CONCAT() is often friendlier when NULLs may appear. The || operator can produce
  NULL if one joined value is NULL.

#### LPAD / RPAD

- Goal:
  Format raw codes to fixed widths.
- SQL:

```sql
SELECT
  dirty_id,
  raw_code,
  LPAD(raw_code, 4, '0') AS code_padded_left,
  RPAD(raw_code, 6, '-') AS code_padded_right
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* 7 became 0007 with LPAD.
* 42 became 0042 with LPAD.
* 305 became 0305 with LPAD.
* 9 became 0009 with LPAD.
* 1234 stayed 1234 with LPAD to length 4.
* RPAD examples included 7-----, 42----, and 1234--.

- Pattern learned:
  LPAD adds characters to the left until the target length is reached.
  RPAD adds characters to the right until the target length is reached.
- Memory line:
  LPAD(text, length, fill) pads left. RPAD(text, length, fill) pads right.

#### Clean report label

- Goal:
  Combine multiple text functions into one report-friendly label.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text,
  raw_code,
  LPAD(raw_code, 4, '0') || ' - ' || INITCAP(TRIM(raw_text))
    AS clean_report_label
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | clean_report_label
---------+-----------------------------
1        | 0007 - Padded Text
2        | 0042 - Mixed Case Value
3        | 0305 - A Astounding Example
4        | 0009 - Left Padded Only
5        | 1234 - Right Padded Only
```

- Pattern learned:
  A useful reporting label can combine code padding, text cleanup, case formatting,
  and concatenation.
- Memory line:
  dirty text + raw code -> trim -> title case -> pad code -> concatenate.

### 6.3 Completed lab topic: length and data-quality flags

#### LENGTH and trimmed length

- Goal:
  Compare raw text length to cleaned text length.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text,
  LENGTH(raw_text) AS raw_length,
  LENGTH(TRIM(raw_text)) AS trimmed_length
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* dirty_id 1 raw_length 15, trimmed_length 11.
* dirty_id 2 raw_length 16, trimmed_length 16.
* dirty_id 4 raw_length 18, trimmed_length 16.
* dirty_id 5 raw_length 19, trimmed_length 17.

- Pattern learned:
  LENGTH(raw_text) counts characters as stored, including outside spaces.
  LENGTH(TRIM(raw_text)) counts characters after outside padding is removed.
- Memory line:
  If raw_length is greater than trimmed_length, the value has outside spaces.

#### Padding quality flag

- Goal:
  Turn the length comparison into a readable data-quality flag.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text,
  LENGTH(raw_text) AS raw_length,
  LENGTH(TRIM(raw_text)) AS trimmed_length,
  CASE
    WHEN LENGTH(raw_text) > LENGTH(TRIM(raw_text))
      THEN 'Has outside padding'
    ELSE 'Clean length'
  END AS padding_status
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* dirty_id 1 was flagged Has outside padding.
* dirty_id 4 was flagged Has outside padding.
* dirty_id 5 was flagged Has outside padding.
* dirty_id 2 and dirty_id 3 were Clean length.

- Pattern learned:
  Raw value -> cleaned value -> compare lengths -> data quality flag.
- Memory line:
  LENGTH(raw_text) > LENGTH(TRIM(raw_text)) means outside padding exists.

### 6.4 Completed lab topic: find and extract text pieces

#### POSITION / STRPOS

- Goal:
  Find where a substring begins inside another string.
- SQL:

```sql
SELECT
  dirty_id,
  comparison_text,
  POSITION('ELF' IN comparison_text) AS elf_position,
  STRPOS(comparison_text, 'ELF') AS elf_strpos
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* ELF returned position 1.
* GAMBOL, GUMBO, ELVES, and POSTGRES returned 0.
* ELVES returned 0 because it starts with ELV, not ELF.

- Pattern learned:
  POSITION and STRPOS both return where a substring begins. If not found, they return 0.
- Memory line:
  POSITION('x' IN text) and STRPOS(text, 'x') find where text begins.

#### LEFT / RIGHT

- Goal:
  Extract prefixes and suffixes from comparison_text.
- SQL:

```sql
SELECT
  dirty_id,
  comparison_text,
  LEFT(comparison_text, 3) AS first_3_chars,
  RIGHT(comparison_text, 3) AS last_3_chars
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* GAMBOL -> first 3 GAM, last 3 BOL.
* GUMBO -> first 3 GUM, last 3 MBO.
* ELF -> first 3 ELF, last 3 ELF.
* ELVES -> first 3 ELV, last 3 VES.
* POSTGRES -> first 3 POS, last 3 RES.

- Pattern learned:
  LEFT(text, n) gets the first n characters.
  RIGHT(text, n) gets the last n characters.
- Memory line:
  LEFT is prefix. RIGHT is suffix.

#### SUBSTRING / SUBSTR

- Goal:
  Extract a piece from the middle of a string.
- SQL:

```sql
SELECT
  dirty_id,
  comparison_text,
  SUBSTRING(comparison_text FROM 2 FOR 3) AS middle_piece,
  SUBSTR(comparison_text, 2, 3) AS middle_piece_substr
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* GAMBOL -> AMB.
* GUMBO -> UMB.
* ELF -> LF.
* ELVES -> LVE.
* POSTGRES -> OST.

- Pattern learned:
  SUBSTRING(text FROM start FOR length) and SUBSTR(text, start, length) both pull
  a string piece. String positions are 1-based.
- Memory line:
  SUBSTRING and SUBSTR extract a piece of text using start position and length.

### 6.5 Completed lab topic: transform text

#### REPLACE

- Goal:
  Replace exact matching text.
- SQL:

```sql
SELECT
  dirty_id,
  comparison_text,
  REPLACE(comparison_text, 'ELF', 'ORC') AS replaced_text
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* ELF became ORC.
* ELVES stayed ELVES because the text contains ELV, not ELF.
* GAMBOL, GUMBO, and POSTGRES were unchanged.

- Pattern learned:
  REPLACE(text, old_text, new_text) replaces exact matching text wherever it appears.
- Memory line:
  REPLACE changes matching text, not similar-looking text.

#### REVERSE

- Goal:
  Reverse characters in a string.
- SQL:

```sql
SELECT
  dirty_id,
  comparison_text,
  REVERSE(comparison_text) AS reversed_text
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result notes:

* GAMBOL -> LOBMAG.
* GUMBO -> OBMUG.
* ELF -> FLE.
* ELVES -> SEVLE.
* POSTGRES -> SERGTSOP.

- Pattern learned:
  REVERSE(text) returns the characters in backward order.
- Memory line:
  REVERSE flips the string backward.

#### REGEXP_REPLACE: collapse repeated internal spaces

- Goal:
  Show how to collapse repeated whitespace inside text into one normal space.
- SQL:

```sql
SELECT
  sample_id,
  messy_text,
  REGEXP_REPLACE(messy_text, '\s+', ' ', 'g') AS collapsed_spaces
FROM (
  VALUES
    (1, 'padded     text'),
    (2, 'mixed      CASE      value'),
    (3, 'A     Astounding      example'),
    (4, 'left   padded   only'),
    (5, 'right       padded       only')
) AS examples(sample_id, messy_text)
ORDER BY sample_id;
```

- Observed result:

```text
sample_id | messy_text                    | collapsed_spaces
----------+-------------------------------+----------------------
1         | padded     text               | padded text
2         | mixed      CASE      value    | mixed CASE value
3         | A     Astounding      example | A Astounding example
4         | left   padded   only          | left padded only
5         | right       padded       only | right padded only
```

- Pattern learned:
  REGEXP_REPLACE can normalize repeated whitespace inside a string.
- Memory line:
  TRIM handles outside spaces.
  REGEXP_REPLACE('\s+', ' ', 'g') handles repeated internal spaces.
- Explanation:

* `\s+` means one or more whitespace characters.
* `' '` is the replacement: one normal space.
* `'g'` means global replacement, so every repeated-space run is replaced, not
  just the first one.

- Common trap:
  Do not confuse TRIM with whitespace collapsing. TRIM removes outside padding.
  It does not collapse repeated spaces inside the text.

### 6.6 Completed lab topic: pattern matching and parsing text

#### LIKE with % wildcard

- Goal:
  Find text values using wildcard pattern matching.
- SQL:

```sql
SELECT
  dirty_id,
  comparison_text
FROM lab_dirty_text
WHERE comparison_text LIKE 'G%'
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | comparison_text
---------+----------------
1        | GAMBOL
2        | GUMBO
```

- Pattern learned:
  LIKE 'G%' finds values that start with G.

- SQL:

```sql
SELECT
  dirty_id,
  comparison_text
FROM lab_dirty_text
WHERE comparison_text LIKE '%BO%'
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | comparison_text
---------+----------------
1        | GAMBOL
2        | GUMBO
```

- Pattern learned:
  LIKE '%BO%' finds values that contain BO anywhere.
- Memory line:
  % means any number of characters.

#### LIKE with _ wildcard

- Goal:
  Use the single-character wildcard.
- SQL:

```sql
SELECT
  dirty_id,
  comparison_text
FROM lab_dirty_text
WHERE comparison_text LIKE 'G_MBO'
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | comparison_text
---------+----------------
2        | GUMBO
```

- Pattern learned:
  The underscore wildcard _ means exactly one character.
- Memory line:
  % = any number of characters.
  _ = exactly one character.

#### LIKE case sensitivity and ILIKE

- Goal:
  Prove that LIKE is case-sensitive in PostgreSQL and ILIKE is case-insensitive.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text
FROM lab_dirty_text
WHERE raw_text LIKE '%CASE%'
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | raw_text
---------+------------------
2        | mixed CASE value
```

- SQL:

```sql
SELECT
  dirty_id,
  raw_text
FROM lab_dirty_text
WHERE raw_text LIKE '%case%'
ORDER BY dirty_id;
```

- Observed result:

```text
0 rows
```

- SQL:

```sql
SELECT
  dirty_id,
  raw_text
FROM lab_dirty_text
WHERE raw_text ILIKE '%case%'
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | raw_text
---------+------------------
2        | mixed CASE value
```

- Pattern learned:
  LIKE is case-sensitive. ILIKE ignores case.
- Memory line:
  LIKE = case-sensitive pattern match.
  ILIKE = case-insensitive pattern match.

#### TRIM + ILIKE cleaned search

- Goal:
  Search after cleaning outside padding.
- SQL:

```sql
SELECT
  dirty_id,
  raw_text,
  TRIM(raw_text) AS cleaned_text
FROM lab_dirty_text
WHERE TRIM(raw_text) ILIKE '%padded%'
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | raw_text              | cleaned_text
---------+-----------------------+-------------------
1        |   padded text         | padded text
4        |   left padded only    | left padded only
5        | right padded only     | right padded only
```

- Pattern learned:
  Clean first, then search.
- Memory line:
  TRIM cleans outside spaces.
  ILIKE searches without caring about case.

#### SPLIT_PART words

- Goal:
  Split cleaned text into word pieces.
- SQL:

```sql
SELECT
  dirty_id,
  TRIM(raw_text) AS cleaned_text,
  SPLIT_PART(TRIM(raw_text), ' ', 1) AS first_word,
  SPLIT_PART(TRIM(raw_text), ' ', 2) AS second_word,
  SPLIT_PART(TRIM(raw_text), ' ', 3) AS third_word
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | cleaned_text          | first_word | second_word | third_word
---------+-----------------------+------------+-------------+-----------
1        | padded text           | padded     | text        |
2        | mixed CASE value      | mixed      | CASE        | value
3        | A Astounding example  | A          | Astounding  | example
4        | left padded only      | left       | padded      | only
5        | right padded only     | right      | padded      | only
```

- Pattern learned:
  SPLIT_PART(text, delimiter, part_number) returns the requested piece.
- Memory line:
  SPLIT_PART is 1-based.
  Part 1 is the first piece.

#### SPLIT_PART generated code

- Goal:
  Generate a delimited code and split it back apart.
- SQL:

```sql
SELECT
  dirty_id,
  raw_code || '-' || comparison_text AS generated_code,
  SPLIT_PART(raw_code || '-' || comparison_text, '-', 1) AS code_part,
  SPLIT_PART(raw_code || '-' || comparison_text, '-', 2) AS text_part
FROM lab_dirty_text
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | generated_code | code_part | text_part
---------+----------------+-----------+----------
1        | 7-GAMBOL       | 7         | GAMBOL
2        | 42-GUMBO       | 42        | GUMBO
3        | 305-ELF        | 305       | ELF
4        | 9-ELVES        | 9         | ELVES
5        | 1234-POSTGRES  | 1234      | POSTGRES
```

- Pattern learned:
  SPLIT_PART can parse simple delimited strings.
- Memory line:
  Build code -> split code -> use the pieces.

#### CTE parse-and-clean pipeline

- Goal:
  Generate a code, split it, and clean each part.
- SQL:

```sql
WITH generated AS (
  SELECT
    dirty_id,
    raw_code || '-' || comparison_text AS generated_code
  FROM lab_dirty_text
)
SELECT
  dirty_id,
  generated_code,
  LPAD(SPLIT_PART(generated_code, '-', 1), 4, '0') AS padded_code_part,
  INITCAP(LOWER(SPLIT_PART(generated_code, '-', 2))) AS clean_text_part
FROM generated
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | generated_code | padded_code_part | clean_text_part
---------+----------------+------------------+----------------
1        | 7-GAMBOL       | 0007             | Gambol
2        | 42-GUMBO       | 0042             | Gumbo
3        | 305-ELF        | 0305             | Elf
4        | 9-ELVES        | 0009             | Elves
5        | 1234-POSTGRES  | 1234             | Postgres
```

- Pattern learned:
  Use a CTE to create the generated string once, then split and format it in the
  outer query.
- Memory line:
  raw combined string -> split into fields -> clean each field -> produce report columns.

### 6.7 Chapter 3 closing mini-pipeline

- Goal:
  Combine the major Chapter 3 skills into one compact report query.
- SQL:

```sql
WITH cleaned AS (
  SELECT
    dirty_id,
    raw_text,
    raw_code,
    comparison_text,
    TRIM(raw_text) AS trimmed_text,
    INITCAP(TRIM(raw_text)) AS title_text,
    LPAD(raw_code, 4, '0') AS padded_code
  FROM lab_dirty_text
)
SELECT
  dirty_id,
  padded_code || ' - ' || title_text AS report_label,
  comparison_text,
  CASE
    WHEN comparison_text ILIKE 'G%' THEN 'Starts with G'
    WHEN comparison_text ILIKE '%EL%' THEN 'Elf-like text'
    ELSE 'Other'
  END AS text_family
FROM cleaned
ORDER BY dirty_id;
```

- Observed result:

```text
dirty_id | report_label                | comparison_text | text_family
---------+-----------------------------+-----------------+--------------
1        | 0007 - Padded Text          | GAMBOL          | Starts with G
2        | 0042 - Mixed Case Value     | GUMBO           | Starts with G
3        | 0305 - A Astounding Example | ELF             | Elf-like text
4        | 0009 - Left Padded Only     | ELVES           | Elf-like text
5        | 1234 - Right Padded Only    | POSTGRES        | Other
```

- Pattern learned:
  A reusable text-cleaning report can clean once in a CTE, build a label, and
  classify text with business rules.
- Memory line:
  clean once in a CTE -> build report label -> classify text with pattern rules.

Chapter 3 closeout note:

For this lab-learning pass, Chapter 3 is complete. It covered:

* text inspection
* trimming
* case normalization
* concatenation
* code padding
* length checks
* data-quality flags
* substring position
* prefix/suffix extraction
* substring extraction
* replacement
* reversing
* regex whitespace collapse
* LIKE / ILIKE pattern matching
* SPLIT_PART parsing
* CTE-based text cleanup pipelines
* final report-label and text-family classification

## 7. Chapter 4 Lab Notes — Full-text Search and Extensions

Chapter 4 starts with PostgreSQL full-text search. This is different from
simple LIKE / ILIKE pattern matching.

Practical workflow:

normal text -> searchable document with to_tsvector()
search words -> tsquery with to_tsquery() or plainto_tsquery()
document @@ query -> matching rows

### Chapter 4 Quick Jumps

* [7.1 Inspect searchable text](#71-completed-lab-topic-inspect-searchable-text)
* [7.2 to_tsvector searchable document](#72-completed-lab-topic-to_tsvector-searchable-document)
* [7.3 to_tsquery and @@ matching](#73-completed-lab-topic-to_tsquery-and--matching)
* [7.4 ILIKE vs full-text search](#74-completed-lab-topic-ilike-vs-full-text-search)
* [7.5 Full-text boolean operators](#75-completed-lab-topic-full-text-boolean-operators)
* [7.6 Search title and description together](#76-completed-lab-topic-search-title-and-description-together)
* [7.7 plainto_tsquery user-style search](#77-completed-lab-topic-plainto_tsquery-user-style-search)
* [7.8 Stemming surprises and prefix search](#78-completed-lab-topic-stemming-surprises-and-prefix-search)
* [7.9 CREATE EXTENSION fuzzystrmatch](#79-completed-lab-topic-create-extension-fuzzystrmatch)
* [7.10 levenshtein edit distance](#710-completed-lab-topic-levenshtein-edit-distance)
* [7.11 levenshtein thresholds and fuzzy title matching](#711-completed-lab-topic-levenshtein-thresholds-and-fuzzy-title-matching)
* [7.12 soundex sound-alike codes](#712-completed-lab-topic-soundex-sound-alike-codes)
* [7.13 difference sound similarity score](#713-completed-lab-topic-difference-sound-similarity-score)
* [7.14 Combined sound and edit-distance fuzzy candidate report](#714-completed-lab-topic-combined-sound-and-edit-distance-fuzzy-candidate-report)
* [7.15 CREATE EXTENSION pg_trgm](#715-completed-lab-topic-create-extension-pg_trgm)
* [7.16 similarity() trigram score](#716-completed-lab-topic-similarity-trigram-score)
* [7.17 similarity threshold filtering](#717-completed-lab-topic-similarity-threshold-filtering)
* [7.18 pg_trgm percent operator](#718-completed-lab-topic-pg_trgm-percent-operator)
* [7.19 pg_trgm similarity threshold and set_limit()](#719-completed-lab-topic-pg_trgm-similarity-threshold-and-set_limit)
* [7.20 word_similarity()](#720-completed-lab-topic-word_similarity)
* [7.21 trigram distance operator](#721-completed-lab-topic-trigram-distance-operator)

### 7.1 Completed lab topic: inspect searchable text

- Goal:
  Identify which film text columns are useful for search.
- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
ORDER BY film_id;
```

- Observed result:

```text
film_id | title           | description
--------+-----------------+--------------------------------------------------------------
101     | ELF ADVENTURE   | A Astounding story about a helpful elf and a winter journey.
102     | DATA DETECTIVE  | A data analyst solves messy customer records with SQL.
103     | POSTGRES HERO   | A database engineer learns timestamp and interval logic.
104     | CLEAN TEXT CLUB | A team fixes padded strings, bad case, and strange codes.
105     | THE FUZZY ELF   | An elf, elven helper, and elves appear in a search story.
106     | ARRAY GAMES     | A fun look at lists, tags, and special features.
```

- Pattern learned:
  title and description are searchable text fields.
- Memory line:
  Inspect the text before building full-text search logic.

### 7.2 Completed lab topic: to_tsvector searchable document

- Goal:
  Convert normal description text into searchable full-text tokens.
- SQL:

```sql
SELECT
  film_id,
  title,
  to_tsvector('english', description) AS searchable_description
FROM lab_films
ORDER BY film_id;
```

- Observed result notes:

  For film 101, original description:

```text
A Astounding story about a helpful elf and a winter journey.
```

  became searchable tokens like:

```text
'astound':2 'elf':7 'help':6 'journey':11 'stori':3 'winter':10
```

  For film 105, original description:

```text
An elf, elven helper, and elves appear in a search story.
```

  became searchable tokens like:

```text
'appear':7 'elf':2 'elv':6 'elven':3 'helper':4 'search':10 'stori':11
```

- Pattern learned:
  to_tsvector('english', text) turns normal English text into searchable tokens.
- Important behavior:

* common words such as a, and, about may be removed
* useful words may be stemmed or normalized
* token positions are stored

- Memory line:
  to_tsvector() prepares the searchable document.

### 7.3 Completed lab topic: to_tsquery and @@ matching

- Goal:
  Match a searchable document against a full-text search query.
- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'elf')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
101     | ELF ADVENTURE
105     | THE FUZZY ELF
```

- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'astound')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
101     | ELF ADVENTURE
```

- Pattern learned:
  to_tsvector() prepares the document.
  to_tsquery() prepares the search query.
  @@ checks whether they match.
- Memory line:
  tsvector @@ tsquery means: does this searchable document match this search query?

### 7.4 Completed lab topic: ILIKE vs full-text search

- Goal:
  Compare character-pattern matching to normalized word-token matching.
- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE description ILIKE '%astounded%'
ORDER BY film_id;
```

- Observed result:

```text
0 rows
```

- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE description ILIKE '%astound%'
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
101     | ELF ADVENTURE
```

- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'astounded')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
101     | ELF ADVENTURE
```

- Pattern learned:
  ILIKE searches exact character patterns.
  Full-text search uses normalized word tokens.
- Memory line:
  ILIKE asks: do these letters appear?
  Full-text search asks: does this searchable word concept appear?

### 7.5 Completed lab topic: full-text boolean operators

- Goal:
  Use AND, OR, and NOT logic inside to_tsquery().

#### AND with &

- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'elf & search')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
105     | THE FUZZY ELF
```

- Pattern learned:
  & means AND.
  The description must match both elf and search.

#### OR with |

- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'elf | sean')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
101     | ELF ADVENTURE
105     | THE FUZZY ELF
```

- Pattern learned:
  | means OR.
  The description can match either elf or sean.

#### NOT with !

- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'elf & !search')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
101     | ELF ADVENTURE
```

- Pattern learned:
  ! means NOT.
  The description must match elf and must not match search.

- Memory line:

```text
& = AND
| = OR
! = NOT
```

### 7.6 Completed lab topic: search title and description together

- Goal:
  Build one searchable document from multiple text columns.
- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', title || ' ' || description)
      @@ to_tsquery('english', 'postgres | database')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
103     | POSTGRES HERO
```

- Pattern learned:
  title || ' ' || description combines both fields into one searchable text value.
- Memory line:
  to_tsvector('english', title || ' ' || description)
  = searchable document built from multiple columns.

Also document this alias lesson:

- SQL:

```sql
SELECT
  film_id,
  title || ' ' || description
FROM lab_films
ORDER BY film_id;
```

- Observed note:
  PostgreSQL displayed the calculated column as ?column? because no alias was given.

- Better SQL:

```sql
SELECT
  film_id,
  title || ' ' || description AS searchable_text
FROM lab_films
ORDER BY film_id;
```

- Pattern learned:
  Always alias calculated columns.

### 7.7 Completed lab topic: plainto_tsquery user-style search

- Goal:
  Use normal user-style search words instead of manual tsquery syntax.
- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', title || ' ' || description)
      @@ plainto_tsquery('english', 'postgres database')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
103     | POSTGRES HERO
```

- Pattern learned:
  plainto_tsquery('english', 'postgres database') converts plain words into a safe
  full-text search query.
- Memory line:
  plainto_tsquery() is friendlier for normal user search input.
  to_tsquery() is for manual full-text-search expressions.

Show query shape comparison:

- SQL:

```sql
SELECT
  plainto_tsquery('english', 'postgres database') AS plain_query,
  to_tsquery('english', 'postgres & database') AS manual_query;
```

- Observed result:

```text
plain_query          | manual_query
---------------------+---------------------
'postgr' & 'databas' | 'postgr' & 'databas'
```

- Pattern learned:
  Both produced the same final query shape, but plainto_tsquery accepted normal words while to_tsquery required the & operator.

#### Stop-word removal

- SQL:

```sql
SELECT
  plainto_tsquery('english', 'a postgres and database') AS plain_query;
```

- Observed result:

```text
plain_query
---------------------
'postgr' & 'databas'
```

- Pattern learned:
  English stop words such as a and and were removed.
- Memory line:
  plainto_tsquery() removes weak/common words, stems useful words, and connects
  remaining words with AND.

### 7.8 Completed lab topic: stemming surprises and prefix search

- Goal:
  Show that full-text search is smarter than ILIKE but does not always match every
  word form the way a human expects.
- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', title || ' ' || description)
      @@ plainto_tsquery('english', 'elves')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
105     | THE FUZZY ELF
```

- SQL:

```sql
SELECT
  plainto_tsquery('english', 'elf') AS elf_query,
  plainto_tsquery('english', 'elves') AS elves_query;
```

- Observed result:

```text
elf_query | elves_query
----------+-------------
'elf'     | 'elv'
```

- Pattern learned:
  PostgreSQL normalized elf and elves to different query tokens in this English dictionary.
- Memory line:
  Do not assume singular/plural always collapse together.
  Check the tsquery shape when behavior surprises you.

#### Prefix search with :*

- Goal:
  Use prefix matching when stemming does not line up exactly.
- SQL:

```sql
SELECT
  film_id,
  title,
  description
FROM lab_films
WHERE to_tsvector('english', title || ' ' || description)
      @@ to_tsquery('english', 'el:*')
ORDER BY film_id;
```

- Observed result:

```text
film_id | title
--------+---------------
101     | ELF ADVENTURE
105     | THE FUZZY ELF
```

- SQL:

```sql
SELECT
  to_tsquery('english', 'el:*') AS prefix_query,
  plainto_tsquery('english', 'elves') AS plain_elves_query;
```

- Observed result:

```text
prefix_query | plain_elves_query
-------------+-------------------
'el':*       | 'elv'
```

- Pattern learned:
  :* means prefix match in tsquery.
  'el:*' matches tokens that start with el.

- Memory line:
  plainto_tsquery() = safer user-style word search.
  to_tsquery() = manual search syntax.
  :* = prefix search.

### 7.9 Completed lab topic: CREATE EXTENSION fuzzystrmatch

- Goal:
  Enable the `fuzzystrmatch` extension so fuzzy text functions are available in the database.
- SQL:

```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
```

- Verification SQL:

```sql
SELECT
  extname
FROM pg_extension
WHERE extname = 'fuzzystrmatch';
```

- Observed result:

```text
extname
--------------
fuzzystrmatch
```

- Pattern learned:
  `CREATE EXTENSION IF NOT EXISTS` safely enables an extension without failing if it is already present.
- Memory line:
  Enable the extension first, then call the fuzzy helper functions.

### 7.10 Completed lab topic: levenshtein edit distance

- Goal:
  Measure how many edits are required to turn one string into another.
- SQL:

```sql
SELECT
  levenshtein('GUMBO', 'GAMBOL') AS edit_distance;
```

- Observed result:

```text
edit_distance
--------------
2
```

- Pattern learned:
  `levenshtein()` returns the number of insertions, deletions, or substitutions needed for a perfect match.
- Memory line:
  Smaller distance = closer spelling match.

### 7.11 Completed lab topic: levenshtein thresholds and fuzzy title matching

- Goal:
  Use a small edit-distance threshold to find likely title typo matches in `lab_films`.
- SQL:

```sql
WITH input_title AS (
  SELECT 'ELF ADVENTUR' AS raw_title
)
SELECT
  f.film_id,
  f.title,
  levenshtein(LOWER(i.raw_title), LOWER(f.title)) AS edit_distance
FROM lab_films AS f
CROSS JOIN input_title AS i
WHERE levenshtein(LOWER(i.raw_title), LOWER(f.title)) <= 2
ORDER BY edit_distance, film_id;
```

- Observed result:

```text
film_id | title           | edit_distance
--------+-----------------+---------------
101     | ELF ADVENTURE   | 1
```

- Pattern learned:
  A threshold like `<= 2` can turn raw edit distance into a practical fuzzy-match filter.
- Common trap:
  Distance thresholds are data-shape dependent. A good threshold for short titles may be too loose for long titles.
- Memory line:
  typo input -> compute distance -> keep only close candidates.

### 7.12 Completed lab topic: soundex sound-alike codes

- Goal:
  Compare words by rough pronunciation instead of exact spelling.
- SQL:

```sql
SELECT
  soundex('Hero') AS hero_code,
  soundex('Hiro') AS hiro_code,
  soundex('Array') AS array_code;
```

- Observed result:

```text
hero_code | hiro_code | array_code
----------+-----------+-----------
H600      | H600      | A600
```

- Pattern learned:
  `soundex()` maps similar-sounding words to the same coarse phonetic code.
- Memory line:
  Different spelling can still share one sound code.

### 7.13 Completed lab topic: difference sound similarity score

- Goal:
  Turn soundex comparison into a small similarity score.
- SQL:

```sql
SELECT
  difference('Hero', 'Hiro') AS close_sound_score,
  difference('Sean', 'Postgres') AS far_sound_score;
```

- Observed result:

```text
close_sound_score | far_sound_score
------------------+----------------
4                 | 0
```

- Pattern learned:
  `difference()` returns a 0-to-4 score based on how similar the two soundex codes are.
- Common trap:
  `difference()` is a coarse phonetic score, not an edit-distance score.
- Memory line:
  `4` = very close sound. `0` = very different sound.

### 7.14 Completed lab topic: Combined sound and edit-distance fuzzy candidate report

- Goal:
  Combine phonetic similarity and edit distance into one practical typo-candidate report.
- SQL:

```sql
WITH input_title AS (
  SELECT 'POSTGRES HRO' AS raw_title
)
SELECT
  f.film_id,
  f.title,
  levenshtein(LOWER(i.raw_title), LOWER(f.title)) AS edit_distance,
  difference(i.raw_title, f.title) AS sound_score
FROM lab_films AS f
CROSS JOIN input_title AS i
WHERE difference(i.raw_title, f.title) >= 2
   OR levenshtein(LOWER(i.raw_title), LOWER(f.title)) <= 3
ORDER BY edit_distance, sound_score DESC, film_id;
```

- Observed result:

```text
film_id | title           | edit_distance | sound_score
--------+-----------------+---------------+------------
103     | POSTGRES HERO   | 1             | 4
```

- Pattern learned:
  `levenshtein()` and `difference()` work well together: one checks spelling closeness and the other checks sound similarity.
- Memory line:
  spelling distance + sound score = stronger fuzzy candidate report.

### 7.15 Completed lab topic: CREATE EXTENSION pg_trgm

- Goal:
  Install PostgreSQL's trigram similarity extension.
- SQL:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

- Observed result:

```text
CREATE EXTENSION
```

- SQL:

```sql
SELECT
  extname,
  extnamespace::regnamespace AS extension_schema
FROM pg_extension
WHERE extname = 'pg_trgm';
```

- Observed result:

```text
extname | extension_schema
--------+------------------------
pg_trgm | course06_functions_lab
```

- Pattern learned:
  pg_trgm is available in the current database.
  Its extension objects live in the course06_functions_lab schema.
- Memory line:

```text
pg_trgm = PostgreSQL trigram similarity extension.
```

### 7.16 Completed lab topic: similarity() trigram score

- Goal:
  Use similarity() to compare how alike two strings are by shared trigram chunks.
- SQL:

```sql
SELECT
  similarity('POSTGRES HERO', 'POSTGRES HER0') AS hero_zero_similarity,
  similarity('POSTGRES HERO', 'POSTGRES HEROES') AS heroes_similarity,
  similarity('POSTGRES HERO', 'ELF ADVENTURE') AS elf_similarity;
```

- Observed result:

```text
hero_zero_similarity | heroes_similarity | elf_similarity
---------------------+-------------------+---------------
0.75                 | 0.8125            | 0
```

- Pattern learned:
  similarity() returns a score from 0 to 1.
  Higher is better.
  0 means no useful trigram similarity.
  1 means exact or extremely close similarity.
- Important comparison:

```text
levenshtein:
lower is better

similarity:
higher is better
```

- Memory line:

```text
similarity() = shared text chunk score.
```

### 7.17 Completed lab topic: similarity threshold filtering

- Goal:
  Rank and filter film titles by trigram similarity.
- SQL:

```sql
SELECT
  film_id,
  title,
  similarity(title, 'POSTGRES HER0') AS title_similarity
FROM lab_films
ORDER BY title_similarity DESC, film_id;
```

- Observed result:

```text
film_id | title           | title_similarity
--------+-----------------+-----------------
103     | POSTGRES HERO   | 0.75
106     | ARRAY GAMES     | 0.04
101     | ELF ADVENTURE   | 0
102     | DATA DETECTIVE  | 0
104     | CLEAN TEXT CLUB | 0
105     | THE FUZZY ELF   | 0
```

- Pattern learned:
  ORDER BY similarity(...) DESC puts the closest trigram match first.

- SQL:

```sql
SELECT
  film_id,
  title,
  similarity(title, 'POSTGRES HER0') AS title_similarity
FROM lab_films
WHERE similarity(title, 'POSTGRES HER0') >= 0.3
ORDER BY title_similarity DESC, film_id;
```

- Observed result:

```text
film_id | title         | title_similarity
--------+---------------+-----------------
103     | POSTGRES HERO | 0.75
```

- Pattern learned:
  WHERE similarity(...) >= threshold removes weak/noisy matches.

- CTE and label version:

```sql
WITH title_similarity AS (
  SELECT
    film_id,
    title,
    similarity(title, 'POSTGRES HER0') AS title_similarity
  FROM lab_films
)
SELECT
  film_id,
  title,
  title_similarity,
  CASE
    WHEN title_similarity >= 0.7 THEN 'Strong trigram match'
    WHEN title_similarity >= 0.3 THEN 'Possible trigram match'
    ELSE 'Weak / no match'
  END AS similarity_label
FROM title_similarity
ORDER BY title_similarity DESC, film_id;
```

- Observed result:

```text
film_id | title           | title_similarity | similarity_label
--------+-----------------+------------------+---------------------
103     | POSTGRES HERO   | 0.75             | Strong trigram match
106     | ARRAY GAMES     | 0.04             | Weak / no match
101     | ELF ADVENTURE   | 0                | Weak / no match
102     | DATA DETECTIVE  | 0                | Weak / no match
104     | CLEAN TEXT CLUB | 0                | Weak / no match
105     | THE FUZZY ELF   | 0                | Weak / no match
```

- Final useful candidate report:

```sql
WITH title_similarity AS (
  SELECT
    film_id,
    title,
    similarity(title, 'POSTGRES HER0') AS title_similarity
  FROM lab_films
)
SELECT
  film_id,
  title,
  title_similarity,
  CASE
    WHEN title_similarity >= 0.7 THEN 'Strong trigram match'
    WHEN title_similarity >= 0.3 THEN 'Possible trigram match'
  END AS similarity_label
FROM title_similarity
WHERE title_similarity >= 0.3
ORDER BY title_similarity DESC, film_id;
```

- Observed result:

```text
film_id | title         | title_similarity | similarity_label
--------+---------------+------------------+---------------------
103     | POSTGRES HERO | 0.75             | Strong trigram match
```

- Memory line:

```text
similarity score -> threshold filter -> business label.
```

### 7.18 Completed lab topic: pg_trgm percent operator

- Goal:
  Use the pg_trgm percent operator as a similar-enough shortcut.
- SQL:

```sql
SELECT
  film_id,
  title,
  similarity(title, 'POSTGRES HER0') AS title_similarity
FROM lab_films
WHERE title % 'POSTGRES HER0'
ORDER BY title_similarity DESC, film_id;
```

- Observed result:

```text
film_id | title         | title_similarity
--------+---------------+-----------------
103     | POSTGRES HERO | 0.75
```

- Pattern learned:
  The % operator is not percent math in this context.
  In pg_trgm, % means similar enough using the current trigram threshold.

- SQL:

```sql
SHOW pg_trgm.similarity_threshold;
```

- Observed result:

```text
pg_trgm.similarity_threshold
----------------------------
0.3
```

- SQL:

```sql
SELECT
  film_id,
  title,
  similarity(title, 'POSTGRES HER0') AS title_similarity,
  similarity(title, 'POSTGRES HER0') >= 0.3 AS passes_manual_threshold,
  title % 'POSTGRES HER0' AS passes_pg_trgm_operator
FROM lab_films
ORDER BY title_similarity DESC, film_id;
```

- Observed result:

```text
film_id | title           | title_similarity | passes_manual_threshold | passes_pg_trgm_operator
--------+-----------------+------------------+-------------------------+------------------------
103     | POSTGRES HERO   | 0.75             | t                       | t
106     | ARRAY GAMES     | 0.04             | f                       | f
101     | ELF ADVENTURE   | 0                | f                       | f
102     | DATA DETECTIVE  | 0                | f                       | f
104     | CLEAN TEXT CLUB | 0                | f                       | f
105     | THE FUZZY ELF   | 0                | f                       | f
```

- Pattern learned:
  similarity() shows the numeric score.
  % returns true/false based on the active pg_trgm threshold.

- Memory line:

```text
similarity() = score.
% = pass/fail using pg_trgm threshold.
```

### 7.19 Completed lab topic: pg_trgm similarity threshold and set_limit()

- Goal:
  Inspect and temporarily change the trigram similarity threshold.
- SQL:

```sql
SELECT
  title,
  similarity(title, 'POSTGRES HER0') AS score
FROM lab_films
WHERE title % 'POSTGRES HER0'
ORDER BY score DESC;
```

- Observed result:

```text
title         | score
--------------+------
POSTGRES HERO | 0.75
```

- SQL:

```sql
SELECT
  show_limit() AS current_similarity_threshold;
```

- Observed result:

```text
current_similarity_threshold
----------------------------
0.3
```

- SQL:

```sql
SELECT set_limit(0.8);
```

- Observed result:

```text
set_limit
---------
0.8
```

- SQL:

```sql
SELECT
  title,
  similarity(title, 'POSTGRES HER0') AS score,
  title % 'POSTGRES HER0' AS passes_pg_trgm_operator
FROM lab_films
ORDER BY score DESC;
```

- Observed result:

```text
title           | score | passes_pg_trgm_operator
----------------+-------+------------------------
POSTGRES HERO   | 0.75  | f
ARRAY GAMES     | 0.04  | f
ELF ADVENTURE   | 0     | f
DATA DETECTIVE  | 0     | f
CLEAN TEXT CLUB | 0     | f
THE FUZZY ELF   | 0     | f
```

- Pattern learned:
  The similarity score did not change.
  The pass/fail cutoff changed.
  At threshold 0.8, a score of 0.75 no longer passes.

- Reset SQL:

```sql
SELECT set_limit(0.3);

SHOW pg_trgm.similarity_threshold;
```

- Observed result after reset:

```text
pg_trgm.similarity_threshold
----------------------------
0.3
```

- Verification SQL:

```sql
SELECT
  title,
  similarity(title, 'POSTGRES HER0') AS score,
  title % 'POSTGRES HER0' AS passes_pg_trgm_operator
FROM lab_films
ORDER BY score DESC;
```

- Observed result:

```text
title           | score | passes_pg_trgm_operator
----------------+-------+------------------------
POSTGRES HERO   | 0.75  | t
ARRAY GAMES     | 0.04  | f
ELF ADVENTURE   | 0     | f
DATA DETECTIVE  | 0     | f
CLEAN TEXT CLUB | 0     | f
THE FUZZY ELF   | 0     | f
```

- Memory line:

```text
similarity() = measurement.
% = pass/fail based on threshold.
set_limit() = changes the threshold.
```

### 7.20 Completed lab topic: word_similarity()

- Goal:
  Compare whole-string similarity with word-level trigram similarity.
- SQL:

```sql
SELECT
  similarity('POSTGRES HERO', 'POSTGRES HER0') AS regular_similarity,
  word_similarity('POSTGRES HERO', 'POSTGRES HER0') AS word_similarity_score;
```

- Observed result:

```text
regular_similarity | word_similarity_score
-------------------+----------------------
0.75               | 0.85714287
```

- SQL:

```sql
SELECT
  similarity(
    'POSTGRES HERO',
    'please find POSTGRES HER0 for me'
  ) AS regular_similarity,
  word_similarity(
    'POSTGRES HERO',
    'please find POSTGRES HER0 for me'
  ) AS word_similarity_score;
```

- Observed result:

```text
regular_similarity | word_similarity_score
-------------------+----------------------
0.36363637         | 0.85714287
```

- Pattern learned:
  similarity() compares whole text to whole text.
  word_similarity() can find a strong match inside a longer text phrase.

- Table ranking SQL:

```sql
SELECT
  film_id,
  title,
  word_similarity(
    title,
    'please find POSTGRES HER0 for me'
  ) AS word_score
FROM lab_films
ORDER BY word_score DESC, film_id;
```

- Observed result:

```text
film_id | title           | word_score
--------+-----------------+------------
103     | POSTGRES HERO   | 0.85714287
106     | ARRAY GAMES     | 0.083333336
104     | CLEAN TEXT CLUB | 0.071428575
105     | THE FUZZY ELF   | 0.071428575
101     | ELF ADVENTURE   | 0
102     | DATA DETECTIVE  | 0
```

- Filtered report SQL:

```sql
SELECT
  film_id,
  title,
  word_similarity(
    title,
    'please find POSTGRES HER0 for me'
  ) AS word_score
FROM lab_films
WHERE word_similarity(
    title,
    'please find POSTGRES HER0 for me'
  ) >= 0.3
ORDER BY word_score DESC, film_id;
```

- Observed result:

```text
film_id | title         | word_score
--------+---------------+------------
103     | POSTGRES HERO | 0.85714287
```

- CTE and label version:

```sql
WITH word_scores AS (
  SELECT
    film_id,
    title,
    word_similarity(
      title,
      'please find POSTGRES HER0 for me'
    ) AS word_score
  FROM lab_films
)
SELECT
  film_id,
  title,
  word_score,
  CASE
    WHEN word_score >= 0.7 THEN 'Strong word trigram match'
    WHEN word_score >= 0.3 THEN 'Possible word trigram match'
    ELSE 'Weak / no match'
  END AS word_similarity_label
FROM word_scores
WHERE word_score >= 0.3
ORDER BY word_score DESC, film_id;
```

- Observed result:

```text
film_id | title         | word_score | word_similarity_label
--------+---------------+------------+---------------------------
103     | POSTGRES HERO | 0.85714287 | Strong word trigram match
```

- Side-by-side comparison SQL:

```sql
SELECT
  title,
  similarity(title, 'POSTGRES HER0') AS clean_input_score,
  word_similarity(
    title,
    'please find POSTGRES HER0 for me'
  ) AS sentence_input_score
FROM lab_films
ORDER BY sentence_input_score DESC, clean_input_score DESC;
```

- Observed result:

```text
title           | clean_input_score | sentence_input_score
----------------+-------------------+---------------------
POSTGRES HERO   | 0.75              | 0.85714287
ARRAY GAMES     | 0.04              | 0.083333336
CLEAN TEXT CLUB | 0                 | 0.071428575
THE FUZZY ELF   | 0                 | 0.071428575
ELF ADVENTURE   | 0                 | 0
DATA DETECTIVE  | 0                 | 0
```

- Memory line:

```text
similarity() = clean string vs clean string.
word_similarity() = stored value vs longer user sentence.
```

### 7.21 Completed lab topic: trigram distance operator

- Goal:
  Use the pg_trgm distance operator to rank closest matches.
- SQL:

```sql
SELECT
  title,
  similarity(title, 'POSTGRES HER0') AS similarity_score,
  title <-> 'POSTGRES HER0' AS trigram_distance
FROM lab_films
ORDER BY trigram_distance ASC, title;
```

- Observed result:

```text
title           | similarity_score | trigram_distance
----------------+------------------+-----------------
POSTGRES HERO   | 0.75             | 0.25
ARRAY GAMES     | 0.04             | 0.96
CLEAN TEXT CLUB | 0                | 1
DATA DETECTIVE  | 0                | 1
ELF ADVENTURE   | 0                | 1
THE FUZZY ELF   | 0                | 1
```

- Pattern learned:
  similarity high is good.
  distance low is good.

- Relationship:

```text
distance = 1 - similarity
```

- Example:

```text
POSTGRES HERO:
similarity = 0.75
distance   = 0.25
```

- Final useful distance report:

```sql
SELECT
  title,
  similarity(title, 'POSTGRES HER0') AS similarity_score,
  title <-> 'POSTGRES HER0' AS trigram_distance
FROM lab_films
WHERE title % 'POSTGRES HER0'
ORDER BY trigram_distance ASC, title;
```

- Observed result:

```text
title         | similarity_score | trigram_distance
--------------+------------------+-----------------
POSTGRES HERO | 0.75             | 0.25
```

- Pattern learned:
  Use % to filter trigram candidates.
  Use similarity() to show the score.
  Use <-> to rank closest distance first.

- Memory line:

```text
similarity high = good.
distance low = good.
```

Chapter 4 closeout note for now:

Do NOT mark all Chapter 4 complete yet.

Mark these blocks as:

Chapter 4 first full-text-search block complete.
Chapter 4 fuzzystrmatch block complete.
Chapter 4 pg_trgm block complete.

Remaining Chapter 4 topics may include:

* full-text ranking with ts_rank()
* indexes for full-text search
* indexes for pg_trgm
* performance notes

## 8. Mistakes Captured During Live Work

| Date | Topic | Mistake | Correction | Reusable pattern |
| --- | --- | --- | --- | --- |
| 2026-06-04 | COALESCE type compatibility | COALESCE(return_date, 'Not returned yet') would mix timestamp and text | Cast return_date to text before using a text fallback | COALESCE arguments should be compatible types |
| 2026-06-04 | Open records with NULL dates | return_date - rental_date returns NULL for open rentals | Use COALESCE(return_date, CURRENT_TIMESTAMP) before subtracting | Fill missing endpoint before duration math |
| 2026-06-04 | Interval part vs total duration | EXTRACT(hour FROM interval) returns only the hour component, not total hours | Use EXTRACT(EPOCH FROM interval) / 3600 for total hours | Use EPOCH when you need total duration |
| 2026-06-04 | CASE threshold order | Checking > 72 before > 120 would classify 122.75 hours as Long instead of Very long | Check > 120 first, then > 72 | Order overlapping CASE thresholds from most severe to least severe |
| 2026-06-04 | Repeated formula in SELECT and CASE | Repeating EXTRACT(EPOCH FROM interval) / 3600 makes the query noisy | Calculate total_hours once in a CTE and reuse it | Calculate once, reuse many times |
| 2026-06-04 | Business label sorting | Sorting labels alphabetically may not match business priority | Use CASE in ORDER BY or a numeric priority column | Sort business labels by priority, not alphabetically |
| 2026-06-04 | GROUP BY helper column confusion | It feels strange to GROUP BY a column not shown in SELECT | GROUP BY may use hidden helper columns; SELECT only displays chosen grouped columns and aggregates | GROUP BY forms piles; SELECT displays final columns |
| 2026-06-04 | Text cleanup order | Formatting messy text before removing padding can produce inconsistent labels | TRIM first, then apply UPPER, LOWER, or INITCAP | Clean first, then format |
| 2026-06-04 | Padding detection | Looking at text visually may hide leading or trailing spaces | Compare LENGTH(raw_text) to LENGTH(TRIM(raw_text)) | Use length difference as a data-quality flag |
| 2026-06-04 | POSITION / STRPOS not found | Expecting not-found substring searches to return NULL | POSITION and STRPOS return 0 when the substring is not found | 0 means not found |
| 2026-06-04 | String positions | Assuming string positions start at 0 like some programming languages | PostgreSQL string functions use 1-based positions | Position 1 is the first character |
| 2026-06-04 | REPLACE exact match | Expecting REPLACE(comparison_text, 'ELF', 'ORC') to change ELVES | REPLACE only changes exact matching text | Similar-looking text is not the same as matching text |
| 2026-06-04 | REGEXP_REPLACE value demonstration | Using rows with mostly outside padding made whitespace collapse hard to see | Use an inline VALUES example with repeated internal spaces | Match the demo data to the function being taught |
| 2026-06-04 | LIKE wildcard meaning | Treating % and _ as the same wildcard | % means any number of characters; _ means exactly one character | Pick wildcard based on whether length is flexible or fixed |
| 2026-06-04 | LIKE case sensitivity | Expecting LIKE '%case%' to match CASE | Use ILIKE for case-insensitive matching in PostgreSQL | LIKE is case-sensitive; ILIKE ignores case |
| 2026-06-04 | SPLIT_PART indexing | Assuming SPLIT_PART uses zero-based positions | Use part_number 1 for the first piece | SPLIT_PART is 1-based |
| 2026-06-04 | Parsing before cleaning | Building labels directly from messy raw values can produce inconsistent output | Clean and format in a CTE, then build the report label | Clean once, reuse in the final report |
| 2026-06-04 | ILIKE vs full-text search | Expecting ILIKE to match related word forms such as astounded and Astounding | Use full-text search when word normalization matters | ILIKE matches characters; full-text search matches normalized word tokens |
| 2026-06-04 | Calculated column alias | Selecting title || ' ' || description without an alias displayed ?column? | Add AS searchable_text | Always alias calculated report columns |
| 2026-06-04 | Full-text boolean syntax | Treating full-text AND/OR/NOT like normal English words | Use &, |, and ! inside to_tsquery() | to_tsquery() uses full-text query operators |
| 2026-06-04 | Stemming assumptions | Assuming elf and elves normalize to the same token | Inspect plainto_tsquery output and use prefix search when appropriate | Check query shape before assuming singular/plural behavior |
| 2026-06-04 | plainto_tsquery vs to_tsquery | Using to_tsquery when the input is normal user text | Use plainto_tsquery for normal search words and to_tsquery for manual expressions | Choose query builder based on input style |
| 2026-06-04 | CREATE EXTENSION first | Trying fuzzy functions before enabling the extension would fail | Run CREATE EXTENSION IF NOT EXISTS fuzzystrmatch before calling levenshtein, soundex, or difference | Extension functions must be enabled before use |
| 2026-06-04 | levenshtein threshold tuning | Treating edit distance 2 as universally good can overmatch longer titles or undermatch short ones | Pick thresholds based on text length and candidate quality | Fuzzy thresholds are tuning knobs, not universal truths |
| 2026-06-04 | soundex expectations | Assuming soundex is a spelling matcher | Use soundex for rough pronunciation grouping, not exact typo counting | soundex is phonetic, not letter-by-letter |
| 2026-06-04 | difference score meaning | Reading difference() like an edit count | Treat difference() as a 0-to-4 phonetic similarity score | difference() measures sound-code closeness, not character edits |
| 2026-06-04 | Combined fuzzy scoring | Relying on only sound similarity or only edit distance can miss better candidates | Use both phonetic and edit-distance checks when ranking fuzzy text candidates | Combine multiple weak signals into one stronger fuzzy match report |
| 2026-06-04 | pg_trgm operator meaning | Reading % as percent math | In pg_trgm, % means similar enough using the active trigram threshold | similarity() shows score; % gives pass/fail |
| 2026-06-04 | Threshold direction | Treating similarity like levenshtein distance | similarity is better when higher; levenshtein is better when lower | levenshtein <= cutoff; similarity >= cutoff |
| 2026-06-04 | Threshold state | Raising pg_trgm threshold to 0.8 and leaving it high | Reset with set_limit(0.3) and verify with SHOW pg_trgm.similarity_threshold | Always reset temporary threshold changes |
| 2026-06-04 | psql paste issue | Accidentally pasting explanatory output text into psql | Paste only SQL statements, or comment explanatory text with -- | Only SQL belongs at the psql prompt |
| 2026-06-04 | word_similarity use case | Expecting similarity() to stay high for long user sentences | Use word_similarity() when the match is buried inside longer text | similarity for clean values; word_similarity for longer phrases |
| 2026-06-04 | distance direction | Sorting trigram distance the wrong way would rank worse matches first | ORDER BY <-> distance ASC because lower distance is better | similarity DESC; distance ASC |

## 9. Update Cadence

After every 2–4 meaningful lab/exercise items, pause and update this Lab Guide and the Field Guide if needed.
