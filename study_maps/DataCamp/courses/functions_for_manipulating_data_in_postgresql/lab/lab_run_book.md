# Lab Run Book: Functions for Manipulating Data in PostgreSQL

## 1. Purpose

This lab run book will later guide hands-on PostgreSQL practice for:

* data types
* date/time functions
* arrays
* text functions
* full-text search
* PostgreSQL extensions

This is a planning document only. Do not create runnable labs yet.

## 2. Lab Dataset Plan

Use a simple DVD-rental-inspired mini-dataset.

Planned tables:

### customers

Likely columns:

* customer_id
* first_name
* last_name
* email
* create_date
* active

### films

Likely columns:

* film_id
* title
* description
* rating
* special_features
* replacement_cost

### rentals

Likely columns:

* rental_id
* rental_date
* inventory_id
* customer_id
* return_date

### payments

Likely columns:

* payment_id
* customer_id
* rental_id
* amount
* payment_date

### inventory

Likely columns:

* inventory_id
* film_id
* store_id

### support_notes

Likely columns:

* note_id
* customer_id
* note_text
* created_at

## 3. Lab Environment Plan

Placeholders only:

* local PostgreSQL
* optional Docker PostgreSQL
* Sakila/DVD rental compatibility notes
* seed data script
* reset script
* expected output folder

Do not create these files yet.

## 4. Chapter 1 Lab Plan — Data Types and Arrays

### Discovering column data types

* goal: inspect a table and confirm what PostgreSQL data types each column actually uses
* SQL concept practiced: schema inspection and type awareness
* expected skill: read a schema before writing transformations

### Querying INFORMATION_SCHEMA.COLUMNS

* goal: retrieve column names and data types from metadata tables
* SQL concept practiced: `INFORMATION_SCHEMA.COLUMNS`
* expected skill: use system metadata to audit unfamiliar tables

### Comparing VARCHAR, TEXT, INT, DECIMAL

* goal: see how PostgreSQL stores text and numeric values with different purposes
* SQL concept practiced: core scalar data types
* expected skill: choose reasonable types for string and numeric fields

### DATE, TIME, TIMESTAMP, INTERVAL examples

* goal: compare date-only, time-only, timestamp, and duration-style values
* SQL concept practiced: temporal type differences
* expected skill: recognize when each date/time type fits a use case

### ARRAY access with one-based indexing

* goal: query specific positions inside an array column
* SQL concept practiced: PostgreSQL array indexing
* expected skill: remember arrays start at index `1`, not `0`

### ANY()

* goal: search an array for a matching value
* SQL concept practiced: `ANY()`
* expected skill: filter rows using membership tests against arrays

### @> contains operator

* goal: test whether one array contains another value or sub-array
* SQL concept practiced: `@>` containment operator
* expected skill: distinguish direct indexing from containment searches

## 5. Chapter 2 Lab Plan — Date/Time Functions

### Expected return date

* goal: calculate a due date from a rental timestamp plus a relative duration
* SQL concept practiced: timestamp plus `INTERVAL`
* expected skill: build practical return/deadline calculations

### DATE minus DATE

* goal: compute elapsed whole days between two dates
* SQL concept practiced: `DATE - DATE`
* expected skill: recognize that date subtraction returns an integer day count

### DATE plus integer

* goal: shift a date forward by a fixed number of days
* SQL concept practiced: `DATE + integer`
* expected skill: use day-based offsets without converting to interval first

### TIMESTAMP minus TIMESTAMP

* goal: measure elapsed time between two events with time-of-day precision
* SQL concept practiced: timestamp subtraction
* expected skill: interpret an `INTERVAL` result instead of expecting a plain number

### INTERVAL arithmetic

* goal: add relative time windows to timestamps and dates
* SQL concept practiced: `INTERVAL` addition, multiplication, and relative offsets
* expected skill: choose interval math for reusable scheduling logic

### AGE()

* goal: compare two timestamps and return a readable elapsed interval
* SQL concept practiced: `AGE()`
* expected skill: contrast `AGE()` with plain subtraction

### NOW()

* goal: anchor a query to the current timestamp
* SQL concept practiced: `NOW()`
* expected skill: stamp or compare records against current runtime time

### CURRENT_TIMESTAMP

* goal: retrieve the current timestamp using standard-style SQL syntax
* SQL concept practiced: `CURRENT_TIMESTAMP` and precision parameter use
* expected skill: control timestamp precision in query output

### CURRENT_DATE

* goal: capture the current date without a time value
* SQL concept practiced: `CURRENT_DATE`
* expected skill: use day-level comparisons cleanly

### CURRENT_TIME

* goal: capture the current time without a date value
* SQL concept practiced: `CURRENT_TIME`
* expected skill: separate clock-time logic from calendar-date logic

### CAST and ::

* goal: convert timestamp outputs between related types
* SQL concept practiced: `CAST()` and PostgreSQL `::`
* expected skill: pick between standard and PostgreSQL-specific casting syntax

### EXTRACT()

* goal: pull date parts like year, month, quarter, and dow from timestamps
* SQL concept practiced: `EXTRACT()`
* expected skill: derive numeric time features for grouping and analysis

### DATE_PART()

* goal: extract date/time parts using the alternative PostgreSQL syntax
* SQL concept practiced: `DATE_PART()`
* expected skill: treat `DATE_PART()` as a peer to `EXTRACT()`

### DATE_TRUNC()

* goal: bucket timestamps into months, weeks, days, or years
* SQL concept practiced: `DATE_TRUNC()`
* expected skill: prepare timestamps for grouped reporting windows

### Monthly/quarterly payment grouping

* goal: aggregate payments by reusable calendar buckets
* SQL concept practiced: `DATE_TRUNC()`, `EXTRACT()`, or `DATE_PART()` with aggregation
* expected skill: build reporting queries from transactional timestamp columns

## 6. Chapter 3 Lab Plan — Text Functions

### Full customer name with ||

* goal: combine first and last name into one output field
* SQL concept practiced: string concatenation with `||`
* expected skill: build readable text outputs from multiple columns

### Full customer name with CONCAT()

* goal: produce the same combined name using function syntax
* SQL concept practiced: `CONCAT()`
* expected skill: compare operator-style and function-style concatenation

### UPPER(), LOWER(), INITCAP()

* goal: normalize inconsistent text casing
* SQL concept practiced: case transformation functions
* expected skill: standardize text for display or matching

### REPLACE()

* goal: swap out unwanted characters or tokens inside text
* SQL concept practiced: `REPLACE()`
* expected skill: perform simple inline text cleanup

### REVERSE()

* goal: reverse text values to inspect output behavior
* SQL concept practiced: `REVERSE()`
* expected skill: understand character-order transformations

### CHAR_LENGTH() and LENGTH()

* goal: count characters in text fields
* SQL concept practiced: string length functions
* expected skill: validate or filter text by length

### POSITION() and STRPOS()

* goal: locate a character or token inside a string
* SQL concept practiced: position lookup functions
* expected skill: find delimiter boundaries before parsing

### LEFT() and RIGHT()

* goal: extract a fixed number of characters from either side of a string
* SQL concept practiced: `LEFT()` and `RIGHT()`
* expected skill: trim text to useful prefixes or suffixes

### SUBSTRING() and SUBSTR()

* goal: extract text segments from the middle of a string
* SQL concept practiced: substring functions
* expected skill: carve reusable slices from larger text values

### Extracting email username/domain

* goal: split emails into left and right components around `@`
* SQL concept practiced: `SUBSTRING()` with `POSITION()` or `CHAR_LENGTH()`
* expected skill: parse identifier strings into component fields

### TRIM(), LTRIM(), RTRIM()

* goal: remove padding or unwanted edge characters
* SQL concept practiced: trimming functions
* expected skill: clean imported text before downstream use

### LPAD() and RPAD()

* goal: pad or truncate strings to fixed display lengths
* SQL concept practiced: padding functions
* expected skill: shape text fields to standard output widths

## 7. Chapter 4 Lab Plan — Full-text Search and Extensions

### LIKE with %

* goal: search for variable-length patterns in text
* SQL concept practiced: `LIKE` with `%`
* expected skill: write basic wildcard text filters

### LIKE with _

* goal: match exactly one unknown character in a pattern
* SQL concept practiced: `LIKE` with `_`
* expected skill: use stricter wildcard matching than `%`

### LIKE case sensitivity

* goal: observe exact-case matching behavior
* SQL concept practiced: case-sensitive `LIKE`
* expected skill: avoid silent misses caused by case mismatch

### to_tsvector()

* goal: convert document text into searchable token form
* SQL concept practiced: `to_tsvector()`
* expected skill: understand the preprocessing side of full-text search

### to_tsquery()

* goal: convert a search phrase into query token form
* SQL concept practiced: `to_tsquery()`
* expected skill: prepare full-text search inputs correctly

### @@ match operator

* goal: match a text vector against a text query
* SQL concept practiced: `@@`
* expected skill: assemble a basic full-text search WHERE clause

### lexemes

* goal: inspect normalized search tokens
* SQL concept practiced: lexeme-based full-text search behavior
* expected skill: explain why full-text search matches more than exact raw strings

### CREATE TYPE enum

* goal: create a simple user-defined enumerated type
* SQL concept practiced: `CREATE TYPE`
* expected skill: define constrained symbolic value sets

### CREATE FUNCTION

* goal: create a simple user-defined SQL function
* SQL concept practiced: `CREATE FUNCTION`
* expected skill: package reusable SQL logic

### CREATE EXTENSION

* goal: enable a PostgreSQL extension safely
* SQL concept practiced: `CREATE EXTENSION`
* expected skill: add database capabilities without manual package hacking

### pg_available_extensions

* goal: inspect which extensions are installable
* SQL concept practiced: `pg_available_extensions`
* expected skill: discover available extension options in a server

### pg_extension

* goal: inspect which extensions are already enabled
* SQL concept practiced: `pg_extension`
* expected skill: audit the current extension footprint

### fuzzystrmatch

* goal: explore extension-based fuzzy text tools
* SQL concept practiced: `fuzzystrmatch`
* expected skill: connect fuzzy matching use cases to extension enablement

### levenshtein()

* goal: compare two strings by edit distance
* SQL concept practiced: `levenshtein()`
* expected skill: quantify near-matches instead of exact matches only

### pg_trgm

* goal: use trigram-based string comparison tools
* SQL concept practiced: `pg_trgm`
* expected skill: understand approximate string similarity workflows

### similarity()

* goal: compare two strings with trigram similarity scoring
* SQL concept practiced: `similarity()`
* expected skill: rank text closeness for fuzzy search or dedupe tasks

## 8. Practice Checkpoints

* Checkpoint 1: inspect schema and types
* Checkpoint 2: date/time transformations
* Checkpoint 3: text parsing and cleanup
* Checkpoint 4: full-text search and extensions
* Checkpoint 5: mixed final review queries

## 9. Expected Output Strategy

Add placeholders for:

* query result screenshots
* saved query outputs
* expected row counts
* expected transformed columns
* notes on where output files will go later

## 10. Troubleshooting Notes

Add placeholders for:

* PostgreSQL version mismatch
* extension not available
* extension permission issue
* date/time type mismatch
* array indexing confusion
* string function syntax confusion

## 11. Future Files Not Yet Created

Planned only, not created yet:

* `sql/00_create_schema.sql`
* `sql/01_seed_data.sql`
* `sql/02_chapter_01_data_types.sql`
* `sql/03_chapter_02_datetime.sql`
* `sql/04_chapter_03_text.sql`
* `sql/05_chapter_04_full_text_extensions.sql`
* `expected_outputs/`
* `troubleshooting.md`
