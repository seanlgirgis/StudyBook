# Intermediate SQL

## Course Identity

- **Course name:** Intermediate SQL
- **Canonical slug:** `intermediate_sql`
- **Platform:** DataCamp
- **Canonical course folder:** `study_maps/DataCamp/courses/intermediate_sql`

## Course Status

- **Platform status:** PASSED
- **Documentation coverage:** COMPLETE
- **Lab coverage:** STRONG
- **Recall confidence:** STRONG
- **Interview readiness:** NEEDS REPETITION

## Primary Opening Path

Open the course from:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\intermediate_sql\index.html
```

The course home links to the main Field Guide, chapter guides, SQL Quick Lookup,
lab materials, and course documentation.

---

## Course Purpose

This course strengthens practical SQL skills in four areas:

1. selecting data
2. filtering records
3. aggregate functions
4. sorting and grouping

The course package includes both study material and a validated local PostgreSQL lab.

---

## Recommended Study Order

1. [Course Home](index.html)
2. [Main Field Guide](study_pages/field_guide.html)
3. [Chapter 1 — Selecting Data](study_pages/chapter_01_selecting_data_field_guide.html)
4. [Chapter 2 — Filtering Records](study_pages/chapter_02_filtering_records_field_guide.html)
5. [Chapter 3 — Aggregate Functions](study_pages/chapter_03_aggregate_functions_field_guide.html)
6. [Chapter 4 — Sorting and Grouping](study_pages/chapter_04_sorting_and_grouping_field_guide.html)
7. [SQL Quick Lookup](study_pages/sql_quick_lookup.html)
8. [Lab Run Book](lab/lab_run_book.md)
9. [How to Run the Lab](lab/00_how_to_run.md)

---

## Main Study Artifacts

### Whole-course guides

- [Field Guide HTML](study_pages/field_guide.html)
- [Field Guide Markdown](study_pages/field_guide.md)
- [SQL Quick Lookup](study_pages/sql_quick_lookup.html)

### Chapter guides

- [Chapter 1 — Selecting Data](study_pages/chapter_01_selecting_data_field_guide.html)
- [Chapter 2 — Filtering Records](study_pages/chapter_02_filtering_records_field_guide.html)
- [Chapter 3 — Aggregate Functions](study_pages/chapter_03_aggregate_functions_field_guide.html)
- [Chapter 4 — Sorting and Grouping](study_pages/chapter_04_sorting_and_grouping_field_guide.html)

### Course documentation

- [Bill of Materials](docs/BILL_OF_MATERIALS.md)
- [Course Setup Audit](docs/COURSE_SETUP_AUDIT.md)
- [Session State](STUDYBUBBLE_SESSION_STATE.md)

---

## Local PostgreSQL Lab

The course lab uses a dedicated schema:

```sql
intermediate_sql
```

Core tables:

```text
films
people
roles
reviews
```

SQL setup files:

- [00_create_schema.sql](lab/sql/00_create_schema.sql)
- [01_create_tables.sql](lab/sql/01_create_tables.sql)
- [02_insert_sample_data.sql](lab/sql/02_insert_sample_data.sql)
- [03_validation_queries.sql](lab/sql/03_validation_queries.sql)

Supporting lab files:

- [Lab README](lab/README.md)
- [How to Run](lab/00_how_to_run.md)
- [Lab Run Book](lab/lab_run_book.md)
- [Expected Outputs](lab/expected_outputs/README.md)
- [Troubleshooting](lab/notes/troubleshooting.md)

---

## Course Coverage

### Chapter 1 — Selecting Data

- `SELECT`
- `FROM`
- `DISTINCT`
- `COUNT(*)`
- `COUNT(column)`
- `COUNT(DISTINCT column)`
- query execution
- debugging
- SQL formatting

### Chapter 2 — Filtering Records

- `WHERE`
- comparison operators
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

### Chapter 3 — Aggregate Functions

- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `ROUND`
- arithmetic
- aliases
- integer division
- `NULLIF`
- casting

### Chapter 4 — Sorting and Grouping

- `ORDER BY`
- `ASC`
- `DESC`
- multi-column sorting
- `GROUP BY`
- grouped aggregates
- `HAVING`
- `WHERE` versus `HAVING`
- logical execution order

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

## Validated Lab Highlights

- `COUNT(*) = 16`
- `COUNT(budget) = 15`
- `COUNT(DISTINCT country) = 10`
- Chapter 2 filters passed
- aggregate and rounding queries passed
- integer division behavior verified
- country grouping returned 10 groups
- `HAVING COUNT(*) >= 2` returned 4 countries
- recent grouped filter returned Canada, United Kingdom, and United States

---

## Source Material

Available:

- course curriculum screenshot
- chapter video files
- selected exercise screenshots and notes
- local PostgreSQL lab files
- validated query outputs

Not fully available:

- complete combined transcript

The absence of a complete transcript does not affect the current course completion status,
but it should be recorded honestly in the Bill of Materials and source-material notes.

---

## Maintenance Mode

The course is complete and now belongs in maintenance and review mode.

Recommended future use:

- review the SQL Quick Lookup
- explain interview questions aloud
- rerun selected lab queries
- practice writing `GROUP BY` and `HAVING` from memory
- revisit NULL behavior and logical execution order
- update documentation only when new mistakes or stronger examples appear

---

## File Naming Rule

Preserve existing filenames exactly.

Do not append suffixes such as:

```text
_updated
_final
_new
_v2
```

Revise files in place using their original names.
