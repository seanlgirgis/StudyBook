# Intermediate SQL — Course Setup Audit

## Audit Purpose

This document records the setup and closeout condition of the DataCamp **Intermediate SQL** course package.

It verifies that the course has:

- a stable canonical folder
- complete chapter guides
- a whole-course Field Guide
- a compact SQL Quick Lookup
- a working local PostgreSQL lab
- documented lab evidence
- a clear course front door
- consistent relative linking
- no unnecessary file renaming or duplicate-version suffixes

---

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

## Canonical Folder Structure

Expected active course structure:

```text
intermediate_sql/
├── index.html
├── README.md
├── STUDYBUBBLE_SESSION_STATE.md
│
├── docs/
│   ├── BILL_OF_MATERIALS.md
│   └── COURSE_SETUP_AUDIT.md
│
├── source_material/
│   ├── README.md
│   ├── course_curriculum_outline.md
│   ├── transcript_raw_combined.md
│   ├── exercise_notes.md
│   └── archive/
│
├── study_pages/
│   ├── field_guide.md
│   ├── field_guide.html
│   ├── chapter_01_selecting_data_field_guide.html
│   ├── chapter_02_filtering_records_field_guide.html
│   ├── chapter_03_aggregate_functions_field_guide.html
│   ├── chapter_04_sorting_and_grouping_field_guide.html
│   └── sql_quick_lookup.html
│
└── lab/
    ├── README.md
    ├── 00_how_to_run.md
    ├── lab_run_book.md
    ├── sql/
    │   ├── 00_create_schema.sql
    │   ├── 01_create_tables.sql
    │   ├── 02_insert_sample_data.sql
    │   └── 03_validation_queries.sql
    ├── expected_outputs/
    │   └── README.md
    ├── notes/
    │   └── troubleshooting.md
    └── source_archive/
```

---

## Setup Audit Checklist

### Course identity and naming

- [x] Course uses stable slug: `intermediate_sql`
- [x] Course folder does not use a track-relative number
- [x] Existing filenames are preserved
- [x] No `_updated`, `_final`, `_new`, or version suffixes are required
- [x] Chapter filenames match chapter names

### Chapter coverage

- [x] Chapter 1 — Selecting Data
- [x] Chapter 2 — Filtering Records
- [x] Chapter 3 — Aggregate Functions
- [x] Chapter 4 — Sorting and Grouping

### Study artifacts

- [x] Main Field Guide Markdown created
- [x] Main Field Guide HTML created
- [x] Chapter 1 Field Guide created
- [x] Chapter 2 Field Guide created
- [x] Chapter 3 Field Guide created
- [x] Chapter 4 Field Guide created
- [x] SQL Quick Lookup created
- [x] Bill of Materials created

### Local PostgreSQL lab

- [x] Dedicated schema created: `intermediate_sql`
- [x] `films` table created
- [x] `people` table created
- [x] `roles` table created
- [x] `reviews` table created
- [x] Sample data loaded
- [x] Validation queries executed
- [x] Chapter 1 lab passed
- [x] Chapter 2 lab passed
- [x] Chapter 3 lab passed
- [x] Chapter 4 lab passed

### Source material

- [x] Course curriculum screenshot received
- [x] Chapter 1 videos received
- [x] Chapter 2 videos received
- [x] Chapter 3 videos received
- [x] Chapter 4 videos received
- [ ] Full combined raw transcript available
- [x] Exercise questions and observations captured during study
- [x] Important local-lab results captured

---

## Chapter Artifact Audit

### Chapter 1

File:

```text
study_pages/chapter_01_selecting_data_field_guide.html
```

Coverage verified:

- `SELECT`
- `FROM`
- `COUNT`
- `DISTINCT`
- query execution
- SQL style
- debugging
- non-standard identifiers
- COUNT variations
- Chapter 1 lab evidence

Status: **COMPLETE**

### Chapter 2

File:

```text
study_pages/chapter_02_filtering_records_field_guide.html
```

Coverage verified:

- `WHERE`
- comparisons
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
- three-valued logic
- Chapter 2 lab evidence

Status: **COMPLETE**

### Chapter 3

File:

```text
study_pages/chapter_03_aggregate_functions_field_guide.html
```

Coverage verified:

- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `ROUND`
- negative precision
- arithmetic
- aliases
- integer division
- `NULLIF`
- aggregate NULL behavior
- safe casting extension
- Chapter 3 lab evidence

Status: **COMPLETE**

### Chapter 4

File:

```text
study_pages/chapter_04_sorting_and_grouping_field_guide.html
```

Coverage verified:

- `ORDER BY`
- `ASC`
- `DESC`
- multi-column sorting
- `GROUP BY`
- grouped aggregates
- multiple grouping fields
- `HAVING`
- `WHERE` versus `HAVING`
- logical execution order
- Chapter 4 lab evidence

Status: **COMPLETE**

---

## Whole-Course Artifact Audit

### Main Field Guide Markdown

File:

```text
study_pages/field_guide.md
```

Purpose:

- whole-course synthesis
- chapter navigation
- major syntax patterns
- common mistakes
- interview translation
- local-lab evidence

Status: **COMPLETE**

### Main Field Guide HTML

File:

```text
study_pages/field_guide.html
```

Purpose:

- browser-based course overview
- chapter navigation
- quick study cards
- execution-order diagram
- interview translation
- lab status

Status: **COMPLETE**

### SQL Quick Lookup

File:

```text
study_pages/sql_quick_lookup.html
```

Purpose:

- smallest useful syntax
- searchable reference
- common traps
- quick decision support

Status: **COMPLETE**

### Bill of Materials

File:

```text
docs/BILL_OF_MATERIALS.md
```

Purpose:

- course inventory
- chapter inventory
- source inventory
- SQL function and operator inventory
- lab inventory
- completion status

Status: **COMPLETE**

---

## PostgreSQL Lab Audit

### Schema

```text
intermediate_sql
```

### Core tables

```text
films
people
roles
reviews
```

### SQL setup files

```text
lab/sql/00_create_schema.sql
lab/sql/01_create_tables.sql
lab/sql/02_insert_sample_data.sql
lab/sql/03_validation_queries.sql
```

### Chapter 1 evidence

```text
COUNT(*)                 = 16
COUNT(budget)            = 15
COUNT(DISTINCT country)  = 10
```

### Chapter 2 evidence

```text
BETWEEN 2018 AND 2021                    = 8 rows
country IN ('Canada', 'Germany')         = 5 rows
imdb_score >= 7.5                        = 5 rows
title LIKE 'B%'                          = Blue Orchard
budget IS NULL                           = No Budget Film
combined country/year filter             = 3 rows
```

### Chapter 3 evidence

```text
AVG(duration)                         = 112.4375000000000000
ROUND(AVG(duration), 2)               = 112.44
ROUND(AVG(budget), -3)                = 21033000
SUM(gross) for release_year >= 2020   = 686900000.00
MAX Canadian imdb_score               = 7.3
COUNT(*)                              = 16
COUNT(budget)                         = 15
AVG(budget)                           = 21033333.333333333333
5 / 2                                 = 2
5.0 / 2                               = 2.5
```

### Chapter 4 evidence

```text
Multi-column ORDER BY: passed
Country groups: 10
Canada film count: 3
United States film count: 3
Germany film count: 2
United Kingdom film count: 2
Highest average genre score: Animation at 8.00
HAVING COUNT(*) >= 2: 4 countries
Grouped release-year averages: passed
Recent grouped filter: Canada, United Kingdom, United States at 2 each
```

Lab status: **PASSED**

---

## Logical Execution Order Verification

The course documentation consistently uses:

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

Status: **VERIFIED**

---

## Link Audit Targets

The following links must exist and remain relative.

### From `index.html`

- `study_pages/field_guide.html`
- `study_pages/field_guide.md`
- `study_pages/chapter_01_selecting_data_field_guide.html`
- `study_pages/chapter_02_filtering_records_field_guide.html`
- `study_pages/chapter_03_aggregate_functions_field_guide.html`
- `study_pages/chapter_04_sorting_and_grouping_field_guide.html`
- `study_pages/sql_quick_lookup.html`
- `lab/00_how_to_run.md`
- `lab/lab_run_book.md`
- `docs/BILL_OF_MATERIALS.md`

### From chapter guides

- `../index.html`
- `field_guide.html`
- `sql_quick_lookup.html`
- previous and next chapter links where applicable

### From Field Guide

- all four chapter guides
- `sql_quick_lookup.html`
- `../lab/lab_run_book.md`
- `../index.html`

### From Quick Lookup

- `field_guide.html`
- `../lab/lab_run_book.md`
- `../index.html`

Current status: **REQUIRES FINAL LINK VALIDATION AFTER INDEX AND README ARE COMPLETED**

---

## Empty or Pending Files

The following files may still require closeout content:

```text
index.html
README.md
STUDYBUBBLE_SESSION_STATE.md
lab/README.md
lab/00_how_to_run.md
lab/lab_run_book.md
lab/expected_outputs/README.md
lab/notes/troubleshooting.md
source_material/README.md
source_material/course_curriculum_outline.md
source_material/exercise_notes.md
source_material/transcript_raw_combined.md
```

Do not delete these files merely because they are empty.

Populate them in place using their exact existing filenames.

---

## Architecture Notes

The active DataCamp course package is intentionally unified under:

```text
study_maps/DataCamp/courses/intermediate_sql
```

This includes:

- study material
- source material
- lab instructions
- SQL files
- expected-output notes
- troubleshooting notes
- course state
- audits

The StudyBubble engine is not part of this course setup and must not be modified for normal course maintenance.

---

## Final Setup Assessment

### What is complete

- all four chapters
- all four chapter field guides
- whole-course Field Guide Markdown
- whole-course Field Guide HTML
- SQL Quick Lookup
- PostgreSQL schema and data
- validation queries
- documented lab evidence
- Bill of Materials

### What remains

- course front door
- course README
- Lab Run Book
- How-to-run guide
- lab README
- session state
- source-material notes
- final relative-link validation

### Setup result

```text
Course setup: VALID
Platform completion: PASSED
Documentation condition: STRONG
Lab condition: STRONG
Closeout condition: IN PROGRESS
```

---

## Canonical Opening Path

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\intermediate_sql\index.html
```
