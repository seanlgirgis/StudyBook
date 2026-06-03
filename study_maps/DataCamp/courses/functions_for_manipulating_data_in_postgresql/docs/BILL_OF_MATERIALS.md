# Bill of Materials: Functions for Manipulating Data in PostgreSQL

## 1. Course Identity

- Course name: Functions for Manipulating Data in PostgreSQL
- Canonical slug: `functions_for_manipulating_data_in_postgresql`
- Track context: DataCamp SQL/PostgreSQL skills lane within `study_maps\DataCamp`
- Dataset: Sakila / DVD Rental
- Artifact status: BOM scaffolded; curriculum outline captured; raw transcript captured; exercises still pending

## 2. Source Inventory

- Curriculum image captured
- Raw combined transcript captured
- Exercise notes pending

## 3. Chapter Inventory

- Chapter 1 covers common PostgreSQL data types, schema inspection, date/time types, and array basics.
- Chapter 2 focuses on date/time arithmetic, current timestamp functions, and extraction/truncation workflows.
- Chapter 3 covers text parsing, case changes, substring work, trimming, padding, and combined string-manipulation patterns.
- Chapter 4 introduces full-text search, user-defined types/functions, PostgreSQL extensions, and fuzzy string matching.

## 4. Topic Inventory

- Data types: text, numeric, date/time, interval, arrays, enums, `tsvector`
- Database discovery: schema inspection, data-type lookup, extension catalogs
- Date/time functions: arithmetic, current time functions, extraction, truncation
- Array operations: creation, indexing, `ANY`, containment checks
- Text/string functions: concatenation, case conversion, replacement, length, substring, trim, pad
- Full-text search: `LIKE`, `to_tsvector`, `to_tsquery`, `@@`
- PostgreSQL extensibility: user-defined types, user-defined functions, extension model
- Extensions and fuzzy matching: enabling extensions, `levenshtein`, `similarity`

## 5. PostgreSQL Function and Operator Inventory

- Metadata and catalogs: `INFORMATION_SCHEMA.COLUMNS`, `pg_type`, `pg_available_extensions`, `pg_extension`
- Date/time math and current-value functions: `AGE`, `NOW`, `CURRENT_TIMESTAMP`, `CURRENT_DATE`, `CURRENT_TIME`
- Date/time extraction and shaping: `EXTRACT`, `DATE_PART`, `DATE_TRUNC`
- Casting and type conversion: `CAST`, `::`
- Array search and containment: `ANY`, `@>`
- String assembly and transformation: `||`, `CONCAT`, `UPPER`, `LOWER`, `INITCAP`, `REPLACE`, `REVERSE`
- String measurement and location: `CHAR_LENGTH`, `LENGTH`, `POSITION`, `STRPOS`
- String slicing: `LEFT`, `RIGHT`, `SUBSTRING`, `SUBSTR`
- String cleanup and padding: `TRIM`, `LTRIM`, `RTRIM`, `LPAD`, `RPAD`
- Search and text indexing: `LIKE`, `to_tsvector`, `to_tsquery`, `@@`
- PostgreSQL extensibility statements: `CREATE TYPE`, `CREATE FUNCTION`, `CREATE EXTENSION`
- Fuzzy matching helpers: `levenshtein`, `similarity`

## 6. Data Type Inventory

- `CHAR`
- `VARCHAR`
- `TEXT`
- `INT`
- `DECIMAL`
- `DATE`
- `TIME`
- `TIMESTAMP`
- `INTERVAL`
- `ARRAY`
- `ENUM / user-defined type`
- `tsvector`

## 7. Field Guide Targets

- PostgreSQL data type decision guide
- Schema and catalog inspection quick reference
- Date/time arithmetic and current-time function guide
- `EXTRACT` and `DATE_TRUNC` lookup table
- Array operators and search patterns
- String manipulation cookbook
- Full-text search quick reference
- PostgreSQL extensions and fuzzy matching field notes

## 8. Lab Run Book Targets

- Inspect a Sakila table and identify column data types
- Compare `TEXT`, `VARCHAR`, and numeric/date column behavior
- Perform date/time arithmetic for rental and return scenarios
- Practice `EXTRACT` and `DATE_TRUNC` on timestamp columns
- Build and query arrays with indexing, `ANY`, and `@>`
- Reformat customer/title text with concatenation, case, trim, and padding
- Parse strings into reusable substrings and cleaned values
- Build a basic full-text search example with `to_tsvector` and `to_tsquery`
- Enable an extension and compare `levenshtein` versus `similarity`

## 9. Fast Review / Slow Down Decisions

- FAST REVIEW: basic text/numeric/date type names, simple casting syntax, simple concatenation/case functions
- NORMAL STUDY: schema inspection tables, current date/time functions, substring/trim/pad patterns
- SLOW DOWN: interval arithmetic, array containment logic, `tsvector` concepts, extension catalog discovery
- PRACTICE REQUIRED: `EXTRACT`/`DATE_TRUNC`, array search operators, combined text parsing pipelines, full-text search queries
- INTERVIEW IMPORTANT: data type choice tradeoffs, casting, timestamp handling, string wrangling, extension awareness, fuzzy matching use cases

## 10. Open Questions / Missing Material

- Exercise prompts still need to be captured.
- Exact DataCamp answer patterns still need to be collected during live pass.
- Local PostgreSQL/Sakila lab setup decision is still pending.
