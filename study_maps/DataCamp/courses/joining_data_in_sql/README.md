# Joining Data in SQL

Canonical DataCamp course package.

## Identity

- Course: Joining Data in SQL
- Canonical slug: `joining_data_in_sql`
- Track: SQL Fundamentals
- Track position: Course 3
- Platform status: PASSED
- Documentation coverage: COMPLETE
- Lab coverage: DEVELOPING
- Recall confidence: DEVELOPING
- Interview readiness: NEEDS REPETITION

## Primary opening page

```text
index.html
```

## Course chapters

1. Introducing Inner Joins
2. Outer Joins, Cross Joins and Self Joins
3. Set Theory for SQL Joins
4. Subqueries

## Main study artifacts

```text
study_pages/
|-- field_guide.md
|-- field_guide.html
|-- sql_quick_lookup.html
|-- chapter_01_introducing_inner_joins_field_guide.html
|-- chapter_02_outer_cross_and_self_joins_field_guide.html
|-- chapter_03_set_theory_for_sql_joins_field_guide.html
`-- chapter_04_subqueries_field_guide.html
```

## Integrated lab

The course includes one compact PostgreSQL lab covering all four chapters.

```text
lab/
|-- README.md
|-- 00_how_to_run.md
|-- lab_guide.html
|-- lab_run_book.md
|-- sql/
|   |-- 00_create_schema.sql
|   |-- 01_create_tables.sql
|   |-- 02_insert_sample_data.sql
|   |-- 03_inner_and_outer_joins.sql
|   |-- 04_cross_and_self_joins.sql
|   |-- 05_set_operations.sql
|   |-- 06_subqueries.sql
|   `-- 07_course_challenges.sql
|-- expected_outputs/
|   `-- README.md
`-- notes/
    `-- troubleshooting.md
```

The lab reinforces:

- inner, outer, cross, and self joins
- one-to-many row multiplication
- `ON` versus `WHERE`
- `UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT`
- semi joins and anti joins
- `NOT EXISTS` versus the `NOT IN`/`NULL` trap
- subqueries in `WHERE`, `SELECT`, and `FROM`

## Package structure

```text
joining_data_in_sql/
|-- index.html
|-- README.md
|-- STUDYBUBBLE_SESSION_STATE.md
|-- docs/
|   |-- BILL_OF_MATERIALS.md
|   `-- COURSE_SETUP_AUDIT.md
|-- source_material/
|   |-- README.md
|   |-- course_curriculum_outline.md
|   |-- transcript_raw_combined.md
|   |-- exercise_notes.md
|   `-- archive/
|-- study_pages/
|   |-- field_guide.md
|   |-- field_guide.html
|   |-- sql_quick_lookup.html
|   |-- chapter_01_introducing_inner_joins_field_guide.html
|   |-- chapter_02_outer_cross_and_self_joins_field_guide.html
|   |-- chapter_03_set_theory_for_sql_joins_field_guide.html
|   `-- chapter_04_subqueries_field_guide.html
`-- lab/
    |-- README.md
    |-- 00_how_to_run.md
    |-- lab_guide.html
    |-- lab_run_book.md
    |-- sql/
    |-- expected_outputs/
    `-- notes/
```

## Recommended study order

1. Open `index.html`.
2. Review `study_pages/field_guide.html`.
3. Use the chapter guides for detailed review.
4. Use `study_pages/sql_quick_lookup.html` while writing SQL.
5. Run the integrated lab in file order.
6. Complete `lab/sql/07_course_challenges.sql`.
7. Revisit interview questions and memory checks.

## Course takeaways

- Join selection begins with row preservation.
- Join conditions must represent the complete business key.
- One-to-many relationships can increase row counts.
- Outer-join filter placement changes results.
- Set operators compare compatible query results vertically.
- `UNION ALL` preserves rows; `UNION` removes duplicates.
- `EXCEPT` is directional.
- Semi joins and anti joins test existence without returning second-table columns.
- `NOT EXISTS` is safer than `NOT IN` when `NULL` may appear.
- Subqueries can return one value, many values, an existence test, or a temporary table.

## Architecture rule

Track pages own ordering. This course folder uses the stable reusable slug:

```text
joining_data_in_sql
```

The active course package, including study materials and the integrated lab, remains together under:

```text
study_maps\DataCamp\courses\joining_data_in_sql
```

## Git

Sean manages Git for this repository.
