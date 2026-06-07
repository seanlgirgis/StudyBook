# Lab Run Book

## Purpose

Turn the course functions into repeatable muscle memory using a compact rental-style dataset.

## Checkpoints

### Chapter 1 — Data types and arrays

- Inspect `information_schema.columns`.
- Explain the difference between `data_type` and `udt_name`.
- Filter array values with `ANY`.
- Filter array containment with `@>`.

### Chapter 2 — Date/time

- Calculate rental duration.
- Compute expected return timestamps from a day count.
- Identify overdue, unreturned rentals.
- Group rentals by month with `DATE_TRUNC`.
- Compare `EXTRACT` with `DATE_PART`.

### Chapter 3 — Text

- Normalize names and emails.
- Parse username and domain.
- Build fixed-width labels with `LPAD` and `RPAD`.
- Correct fragments using `REPLACE`.
- Validate missing delimiters.

### Chapter 4 — Search and extensions

- Compare `ILIKE` with full-text search.
- Inspect installed extensions.
- Optionally enable `pg_trgm` and `fuzzystrmatch`.
- Compare similarity score and edit distance.

## Completion standard

You can complete the exercises without copying, explain each return type, and identify the trap in each section.
