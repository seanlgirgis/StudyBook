# Intermediate SQL — Bill of Materials

## Course Identity

- **Course name:** Intermediate SQL
- **Canonical slug:** `intermediate_sql`
- **Canonical course folder:** `study_maps/DataCamp/courses/intermediate_sql`
- **Platform:** DataCamp
- **Platform status:** PASSED
- **Documentation coverage:** COMPLETE
- **Lab coverage:** STRONG
- **Recall confidence:** STRONG
- **Interview readiness:** NEEDS REPETITION

---

## Course Chapters

### Chapter 1 — Selecting Data

Status: **COMPLETE**

Topics:

- `SELECT`
- `FROM`
- selecting one, many, or all columns
- `DISTINCT`
- `COUNT(*)`
- `COUNT(column)`
- `COUNT(DISTINCT column)`
- conditional counting
- logical query execution
- debugging syntax errors
- SQL style and formatting
- quoted and non-standard identifiers

Primary artifact:

- `../study_pages/chapter_01_selecting_data_field_guide.html`

### Chapter 2 — Filtering Records

Status: **COMPLETE**

Topics:

- `WHERE`
- comparison operators
- numeric filtering
- text filtering
- `AND`
- `OR`
- parentheses and condition precedence
- `BETWEEN`
- `LIKE`
- `NOT LIKE`
- PostgreSQL `ILIKE`
- `IN`
- `NOT IN`
- `IS NULL`
- `IS NOT NULL`
- three-valued logic

Primary artifact:

- `../study_pages/chapter_02_filtering_records_field_guide.html`

### Chapter 3 — Aggregate Functions

Status: **COMPLETE**

Topics:

- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- aggregate functions with `WHERE`
- `ROUND()`
- negative rounding precision
- arithmetic expressions
- aliases
- integer division
- division-by-zero protection with `NULLIF`
- aggregate behavior with `NULL`
- casting text before numeric aggregation
- safe validation before casting

Primary artifact:

- `../study_pages/chapter_03_aggregate_functions_field_guide.html`

### Chapter 4 — Sorting and Grouping

Status: **COMPLETE**

Topics:

- `ORDER BY`
- `ASC`
- `DESC`
- multi-column sorting
- `GROUP BY`
- grouping by multiple columns
- grouped aggregates
- `HAVING`
- `WHERE` versus `HAVING`
- aliases in `ORDER BY`
- logical query execution order

Primary artifact:

- `../study_pages/chapter_04_sorting_and_grouping_field_guide.html`

---

## Study Artifacts

| Artifact | Path | Status |
|---|---|---|
| Course home | `../index.html` | Pending final linking |
| Main Field Guide Markdown | `../study_pages/field_guide.md` | COMPLETE |
| Main Field Guide HTML | `../study_pages/field_guide.html` | COMPLETE |
| Chapter 1 Field Guide | `../study_pages/chapter_01_selecting_data_field_guide.html` | COMPLETE |
| Chapter 2 Field Guide | `../study_pages/chapter_02_filtering_records_field_guide.html` | COMPLETE |
| Chapter 3 Field Guide | `../study_pages/chapter_03_aggregate_functions_field_guide.html` | COMPLETE |
| Chapter 4 Field Guide | `../study_pages/chapter_04_sorting_and_grouping_field_guide.html` | COMPLETE |
| SQL Quick Lookup | `../study_pages/sql_quick_lookup.html` | COMPLETE |
| Lab Run Book | `../lab/lab_run_book.md` | Pending closeout |
| How to Run Lab | `../lab/00_how_to_run.md` | Pending closeout |
| Course README | `../README.md` | Pending closeout |
| Session State | `../STUDYBUBBLE_SESSION_STATE.md` | Pending closeout |

---

## Source Material Inventory

| Source | Status | Notes |
|---|---|---|
| Course curriculum screenshot | AVAILABLE | Four chapters confirmed |
| Chapter 1 videos | AVAILABLE | Querying a database, Query execution, SQL style |
| Chapter 2 videos | AVAILABLE | Filtering numbers, Multiple criteria, Filtering text, NULL values |
| Chapter 3 videos | AVAILABLE | Summarizing data, Summarizing subsets, Aliasing and arithmetic |
| Chapter 4 videos | AVAILABLE | Sorting results, Grouping data, Filtering grouped data, Congratulations |
| Combined raw transcript | NOT AVAILABLE | Do not claim full transcript coverage |
| Exercise screenshots and notes | PARTIAL | Important questions and lab results captured during study |
| Local PostgreSQL lab files | AVAILABLE | Schema, tables, sample data, and validation queries |

---

## SQL Function and Operator Inventory

### Selection and counting

- `SELECT`
- `FROM`
- `DISTINCT`
- `COUNT(*)`
- `COUNT(column)`
- `COUNT(DISTINCT column)`
- `COUNT(expression)`
- `COUNT(CASE WHEN ...)`
- `FILTER (WHERE ...)`

### Filtering

- `WHERE`
- `=`
- `!=`
- `<>`
- `>`
- `>=`
- `<`
- `<=`
- `AND`
- `OR`
- `BETWEEN`
- `LIKE`
- `NOT LIKE`
- `ILIKE`
- `IN`
- `NOT IN`
- `IS NULL`
- `IS NOT NULL`

### Aggregation and arithmetic

- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `ROUND`
- `+`
- `-`
- `*`
- `/`
- `%`
- `NULLIF`
- `CAST`
- PostgreSQL `::type`

### Sorting and grouping

- `ORDER BY`
- `ASC`
- `DESC`
- `GROUP BY`
- `HAVING`
- `LIMIT`

---

## Core SQL Patterns

### Basic selection

```sql
SELECT title,
       release_year
FROM films;
```

### Filter rows

```sql
SELECT title
FROM films
WHERE release_year >= 2020;
```

### Aggregate a filtered subset

```sql
SELECT AVG(imdb_score)
FROM films
WHERE country = 'Canada';
```

### Group and summarize

```sql
SELECT country,
       COUNT(*) AS film_count
FROM films
GROUP BY country;
```

### Filter grouped results

```sql
SELECT country,
       COUNT(*) AS film_count
FROM films
GROUP BY country
HAVING COUNT(*) >= 2;
```

### Full logical pattern

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

## Logical Query Execution Order

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

---

## Local PostgreSQL Lab Inventory

### Schema

- `intermediate_sql`

### Tables

- `films`
- `people`
- `roles`
- `reviews`

### SQL files

- `../lab/sql/00_create_schema.sql`
- `../lab/sql/01_create_tables.sql`
- `../lab/sql/02_insert_sample_data.sql`
- `../lab/sql/03_validation_queries.sql`

### Validated evidence

#### Chapter 1

- `COUNT(*) = 16`
- `COUNT(budget) = 15`
- `COUNT(DISTINCT country) = 10`

#### Chapter 2

- `BETWEEN 2018 AND 2021` returned 8 rows
- Canada or Germany returned 5 rows
- `imdb_score >= 7.5` returned 5 rows
- `title LIKE 'B%'` returned `Blue Orchard`
- `budget IS NULL` returned `No Budget Film`
- combined country and year filter returned 3 rows

#### Chapter 3

- `AVG(duration) = 112.4375000000000000`
- `ROUND(AVG(duration), 2) = 112.44`
- `ROUND(AVG(budget), -3) = 21033000`
- recent total gross = `686900000.00`
- highest Canadian IMDb score = `7.3`
- `COUNT(*) = 16`
- `COUNT(budget) = 15`
- `AVG(budget) = 21033333.333333333333`
- `5 / 2 = 2`
- `5.0 / 2 = 2.5`

#### Chapter 4

- multi-column sorting passed
- country grouping returned 10 groups
- Canada and United States each returned 3 films
- Germany and United Kingdom each returned 2 films
- Animation had the highest average score at `8.00`
- `HAVING COUNT(*) >= 2` returned 4 countries
- grouped release-year averages passed
- recent-film grouped filter returned Canada, United Kingdom, and United States with 2 films each

---

## Learning Priority Classification

### FAST REVIEW

- basic `SELECT`
- basic `FROM`
- simple comparisons
- basic `ORDER BY`

### NORMAL STUDY

- `DISTINCT`
- `BETWEEN`
- `LIKE`
- `IN`
- basic aggregates
- aliases

### SLOW DOWN

- `NULL` behavior
- `COUNT(*)` versus `COUNT(column)`
- integer division
- negative `ROUND` precision
- grouping granularity
- logical execution order

### PRACTICE REQUIRED

- compound `AND` and `OR`
- `GROUP BY`
- `HAVING`
- multi-column sorting
- aggregate queries with filters
- casting dirty text safely

### INTERVIEW IMPORTANT

- logical execution order
- `WHERE` versus `HAVING`
- `ORDER BY` versus `GROUP BY`
- aggregate NULL behavior
- `COUNT(*)` versus `COUNT(column)`
- non-aggregate selected columns and `GROUP BY`
- safe arithmetic and division

---

## Remaining Closeout Work

- complete `../lab/lab_run_book.md`
- complete `../lab/00_how_to_run.md`
- complete `../lab/README.md`
- complete `../README.md`
- complete `../index.html`
- complete `../STUDYBUBBLE_SESSION_STATE.md`
- verify all relative links
- record final course closeout status

---

## Final Course Position

Intermediate SQL is complete on DataCamp and strongly supported by local PostgreSQL practice.

The course is ready for:

- maintenance review
- interview repetition
- occasional SQL muscle-memory drills
- linking from track and course navigation pages
