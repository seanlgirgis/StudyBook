# Joining Data in SQL — Field Guide

**Course:** Joining Data in SQL  
**Canonical slug:** `joining_data_in_sql`  
**Platform status:** PASSED  
**Documentation status:** Complete  
**Lab coverage:** Integrated course lab created  
**Recall confidence:** Developing  
**Interview readiness:** Needs repetition

---

## Table of Contents

1. [Course Big Picture](#course-big-picture)
2. [Chapter Navigation](#chapter-navigation)
3. [Join Selection Decision Guide](#join-selection-decision-guide)
4. [Chapter 1 — Introducing Inner Joins](#chapter-1--introducing-inner-joins)
5. [Chapter 2 — Outer, Cross, and Self Joins](#chapter-2--outer-cross-and-self-joins)
6. [Chapter 3 — Set Theory for SQL Joins](#chapter-3--set-theory-for-sql-joins)
7. [Chapter 4 — Subqueries](#chapter-4--subqueries)
8. [Core SQL Patterns](#core-sql-patterns)
9. [Common Traps and Corrections](#common-traps-and-corrections)
10. [Interview Translation](#interview-translation)
11. [Memory Nuggets](#memory-nuggets)
12. [Course Lab](#course-lab)
13. [Final Review Checklist](#final-review-checklist)

---

## Course Big Picture

This course teaches four major ways to combine or compare data:

1. **Joins** combine related columns from different tables.
2. **Outer joins** control which unmatched rows remain.
3. **Set operations** combine or compare complete query results vertically.
4. **Subqueries** let one query use the result of another query.

The central question is not merely:

> Which SQL keyword should I use?

The better question is:

> What result population do I need, which rows must survive, and what shape should the final result have?

---

## Chapter Navigation

- [Chapter 1 — Introducing Inner Joins](chapter_01_introducing_inner_joins_field_guide.html)
- [Chapter 2 — Outer Joins, Cross Joins and Self Joins](chapter_02_outer_cross_and_self_joins_field_guide.html)
- [Chapter 3 — Set Theory for SQL Joins](chapter_03_set_theory_for_sql_joins_field_guide.html)
- [Chapter 4 — Subqueries](chapter_04_subqueries_field_guide.html)
- [SQL Join Quick Lookup](sql_join_quick_lookup.html)
- [Integrated Lab Guide](../lab/lab_guide.html)

---

## Join Selection Decision Guide

| Business need | Best starting pattern |
|---|---|
| Keep only rows that match in both tables | `INNER JOIN` |
| Keep every row from the main table | `LEFT JOIN` |
| Keep every row from the table written on the right | `RIGHT JOIN` |
| Keep all rows from both tables | `FULL JOIN` |
| Generate every possible combination | `CROSS JOIN` |
| Compare rows from the same table | Self join |
| Stack results and remove duplicates | `UNION` |
| Stack results and preserve duplicates | `UNION ALL` |
| Keep rows found in both query results | `INTERSECT` |
| Keep rows from the first query not found in the second | `EXCEPT` |
| Keep rows when a related row exists | Semi join with `IN` or `EXISTS` |
| Keep rows when no related row exists | Anti join with `NOT EXISTS` |
| Compare rows to one summary value | Scalar subquery |
| Create an intermediate result table | Subquery in `FROM` |

### Fast decision sequence

1. Identify the main output population.
2. Decide which unmatched rows must remain.
3. Confirm the real business key.
4. Check whether the relationship is one-to-one, one-to-many, or many-to-many.
5. Estimate possible row multiplication.
6. Choose the join, set operator, or subquery pattern.
7. Validate row counts and unmatched records.

---

## Chapter 1 — Introducing Inner Joins

### Core idea

`INNER JOIN` returns rows where the join condition finds a match in both inputs.

```sql
SELECT
    c.name,
    p.year,
    p.population
FROM countries AS c
INNER JOIN populations AS p
    ON c.code = p.country_code;
```

### Aliases

Aliases shorten table references and make column ownership clear.

```sql
FROM countries AS c
INNER JOIN populations AS p
    ON c.code = p.country_code
```

After assigning an alias, use it consistently.

### `ON` versus `USING`

Use `ON` when:

- the key columns have different names;
- the relationship needs multiple conditions;
- the join logic should remain explicit.

```sql
INNER JOIN populations AS p
    ON c.code = p.country_code
```

Use `USING` when both tables share the same key-column name.

```sql
INNER JOIN economies AS e
    USING (code)
```

### Primary and foreign keys

- **Primary key:** uniquely identifies a row in its table.
- **Foreign key:** refers to a key in another table.
- **Cardinality:** determines how many output rows each match creates.

### Multiple joins

Join tables one at a time and include all parts of a composite relationship.

```sql
SELECT
    c.name,
    p.year,
    p.size,
    e.gdp_percapita
FROM countries AS c
INNER JOIN populations AS p
    ON c.code = p.country_code
INNER JOIN economies AS e
    ON c.code = e.country_code
   AND p.year = e.year;
```

Matching only by country could incorrectly combine values from different years.

---

## Chapter 2 — Outer, Cross, and Self Joins

### LEFT JOIN

Keeps every row from the table written after `FROM`.

```sql
SELECT
    c.name,
    e.year,
    e.gdp_percapita
FROM countries AS c
LEFT JOIN economies AS e
    ON c.code = e.country_code;
```

Missing right-side values appear as `NULL`.

### RIGHT JOIN

Keeps every row from the right table.

Many teams rewrite `RIGHT JOIN` as `LEFT JOIN` by swapping the table order because the preserved population is easier to identify.

### `ON` versus `WHERE` with LEFT JOIN

A right-side filter in `WHERE` can remove unmatched rows:

```sql
SELECT
    c.name,
    e.year
FROM countries AS c
LEFT JOIN economies AS e
    ON c.code = e.country_code
WHERE e.year = 2015;
```

A right-side filter in `ON` restricts matches while preserving all left rows:

```sql
SELECT
    c.name,
    e.year
FROM countries AS c
LEFT JOIN economies AS e
    ON c.code = e.country_code
   AND e.year = 2015;
```

### FULL JOIN

Keeps matched rows plus unmatched rows from both sides.

```sql
SELECT
    c.code AS country_code,
    e.country_code AS economy_code
FROM countries AS c
FULL JOIN economies AS e
    ON c.code = e.country_code;
```

Useful for:

- reconciliation;
- migration validation;
- identifying missing keys;
- data-quality comparison.

### CROSS JOIN

Creates every possible combination.

```sql
SELECT
    c.code,
    y.year
FROM countries AS c
CROSS JOIN (
    VALUES (2010), (2015)
) AS y(year);
```

Expected row count:

```text
left rows × right rows
```

Always estimate the size before running a large `CROSS JOIN`.

### Self joins

A self join gives one table two logical roles.

```sql
SELECT
    p1.country_code,
    p1.size AS size2010,
    p2.size AS size2015
FROM populations AS p1
INNER JOIN populations AS p2
    ON p1.country_code = p2.country_code
   AND p1.year = 2010
   AND p2.year = 2015;
```

A broad self join without year restrictions creates all year-to-year combinations.

### Alternative to a self join

For fixed reporting years, conditional aggregation may be simpler:

```sql
SELECT
    country_code,
    MAX(size) FILTER (WHERE year = 2010) AS size2010,
    MAX(size) FILTER (WHERE year = 2015) AS size2015
FROM populations
GROUP BY country_code;
```

---

## Chapter 3 — Set Theory for SQL Joins

### Joins versus set operations

- **Joins:** combine columns horizontally.
- **Set operations:** combine or compare rows vertically.

Each participating query must return:

- the same number of columns;
- columns in the same order;
- compatible data types;
- logically comparable values.

### UNION

Stacks query results and removes duplicate rows.

```sql
SELECT country_code
FROM populations

UNION

SELECT country_code
FROM economies;
```

### UNION ALL

Stacks query results and preserves duplicates.

```sql
SELECT country_code
FROM populations

UNION ALL

SELECT country_code
FROM economies;
```

Use `UNION ALL` when:

- every source row matters;
- duplicates may be meaningful;
- auditability and row counts matter;
- duplicate removal is unnecessary.

### INTERSECT

Returns rows found in both results.

```sql
SELECT name
FROM cities

INTERSECT

SELECT name
FROM countries;
```

An equivalent `INNER JOIN` may need `DISTINCT`:

```sql
SELECT DISTINCT ci.name
FROM cities AS ci
INNER JOIN countries AS c
    ON ci.name = c.name;
```

### EXCEPT

Returns rows from the first query that do not appear in the second.

```sql
SELECT country_code, year
FROM economies

EXCEPT

SELECT country_code, year
FROM populations;
```

Direction matters:

```text
A EXCEPT B ≠ B EXCEPT A
```

### Final ordering

A final `ORDER BY` applies to the complete combined result.

```sql
SELECT country_code
FROM populations

UNION

SELECT country_code
FROM economies

ORDER BY country_code;
```

---

## Chapter 4 — Subqueries

### Core idea

A subquery is a query nested inside another query. It may return:

- one value;
- multiple values;
- an existence test;
- a temporary result table.

### Semi joins

Keep rows when a related row exists.

```sql
SELECT c.name
FROM countries AS c
WHERE EXISTS (
    SELECT 1
    FROM economies AS e
    WHERE e.country_code = c.code
);
```

### Anti joins

Keep rows when no related row exists.

```sql
SELECT c.name
FROM countries AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM economies AS e
    WHERE e.country_code = c.code
);
```

### Why `NOT EXISTS` is safer than `NOT IN`

If the inner query used by `NOT IN` contains `NULL`, SQL may return no rows because the comparison becomes unknown.

Prefer:

```sql
WHERE NOT EXISTS (...)
```

or explicitly filter out `NULL` values.

### Subquery in WHERE

Compare each row against one summary value:

```sql
SELECT
    name,
    population
FROM cities
WHERE population > (
    SELECT AVG(population)
    FROM cities
);
```

### Subquery in SELECT

Return one scalar value per outer row:

```sql
SELECT
    c.name,
    (
        SELECT COUNT(*)
        FROM cities AS ci
        WHERE ci.country_code = c.code
    ) AS city_count
FROM countries AS c;
```

### Subquery in FROM

Create an intermediate table:

```sql
SELECT
    region,
    AVG(country_population) AS average_population
FROM (
    SELECT
        region,
        population AS country_population
    FROM countries
    WHERE population IS NOT NULL
) AS country_data
GROUP BY region;
```

A `FROM` subquery needs an alias in PostgreSQL.

### Correlated subqueries

A correlated subquery refers to the current row from the outer query.

```sql
SELECT c.name
FROM countries AS c
WHERE EXISTS (
    SELECT 1
    FROM cities AS ci
    WHERE ci.country_code = c.code
      AND ci.population > 1000000
);
```

---

## Core SQL Patterns

### Two-table inner join

```sql
SELECT ...
FROM table_a AS a
INNER JOIN table_b AS b
    ON a.key = b.key;
```

### Composite join

```sql
SELECT ...
FROM table_a AS a
INNER JOIN table_b AS b
    ON a.entity_id = b.entity_id
   AND a.period_id = b.period_id;
```

### Preserve the main population

```sql
SELECT ...
FROM main_table AS m
LEFT JOIN detail_table AS d
    ON m.key = d.key;
```

### Find missing relationships

```sql
SELECT m.key
FROM main_table AS m
LEFT JOIN detail_table AS d
    ON m.key = d.key
WHERE d.key IS NULL;
```

### NULL-safe anti join

```sql
SELECT m.key
FROM main_table AS m
WHERE NOT EXISTS (
    SELECT 1
    FROM detail_table AS d
    WHERE d.key = m.key
);
```

### Append all rows

```sql
SELECT ...
FROM source_a

UNION ALL

SELECT ...
FROM source_b;
```

### Shared rows

```sql
SELECT key
FROM source_a

INTERSECT

SELECT key
FROM source_b;
```

### First-only rows

```sql
SELECT key
FROM source_a

EXCEPT

SELECT key
FROM source_b;
```

---

## Common Traps and Corrections

| Trap | Why it is dangerous | Correction |
|---|---|---|
| Joining only on a partial key | Creates false combinations | Include every key field, such as entity plus year |
| Assuming LEFT JOIN preserves the exact left row count | One-to-many matches may multiply rows | Check right-side key uniqueness |
| Filtering right-side fields in `WHERE` | Removes unmatched left rows | Move match filters into `ON` when preservation matters |
| Running a large CROSS JOIN blindly | Output size multiplies rapidly | Calculate expected rows first |
| Self joining without restricting roles | Produces A–A, A–B, B–A, and B–B combinations | Add role, year, hierarchy, or inequality conditions |
| Using `UNION` when duplicates are meaningful | Valid repeated rows disappear | Use `UNION ALL` |
| Reversing `EXCEPT` | Produces the opposite difference | State the first population explicitly |
| Using `=` with a multi-row subquery | Raises a cardinality error | Use `IN`, `EXISTS`, or aggregate to one row |
| Using `NOT IN` with possible `NULL` values | Can return no rows unexpectedly | Use `NOT EXISTS` |
| Forgetting a `FROM` subquery alias | PostgreSQL error | Add `AS alias_name` |
| Assuming a successful query is logically correct | SQL may run while producing bad data | Validate keys, row counts, and duplicates |

---

## Interview Translation

### What does INNER JOIN do?

It returns rows where the join condition finds a match in both inputs. Unmatched rows are excluded.

### How do you choose between INNER JOIN and LEFT JOIN?

I start with the required output population. If unmatched rows should be excluded, I use `INNER JOIN`. If every row from the primary population must remain, I use `LEFT JOIN`.

### Why can a join increase row count?

A key may match several rows. One-to-many and many-to-many relationships create one output row for each valid combination.

### What is a common LEFT JOIN bug?

Filtering a right-side field in `WHERE` can remove `NULL`-extended rows and create inner-join behavior.

### What is the difference between UNION and UNION ALL?

`UNION` removes duplicate rows. `UNION ALL` preserves all rows and usually performs less work.

### How does INTERSECT differ from INNER JOIN?

`INTERSECT` compares compatible result sets and returns common rows. `INNER JOIN` matches tables through a condition and may return fields from both sides.

### What does EXCEPT do?

It returns rows from the first query that are absent from the second. Query order matters.

### What is a semi join?

A semi join returns rows from the first table when at least one related row exists, without returning fields from the second table.

### What is an anti join?

An anti join returns rows from the first table when no related row exists in the second.

### Why is NOT EXISTS safer than NOT IN?

`NOT IN` can behave unexpectedly when the inner result contains `NULL`. `NOT EXISTS` directly tests whether a matching row exists.

### What is a correlated subquery?

It is a subquery that references the outer query and is evaluated logically in the context of each outer row.

---

## Memory Nuggets

1. `INNER JOIN` keeps matches only.
2. `LEFT JOIN` preserves the left population.
3. `FULL JOIN` preserves both populations.
4. `CROSS JOIN` multiplies row counts.
5. A self join means one table, multiple aliases, multiple roles.
6. `UNION` removes duplicates.
7. `UNION ALL` preserves duplicates.
8. `INTERSECT` means common rows.
9. `EXCEPT` means first result minus second result.
10. `IN` tests membership in a list.
11. `EXISTS` tests whether a related row exists.
12. `NOT EXISTS` is the safest common anti-join pattern.
13. A scalar subquery must return one value.
14. A `FROM` subquery acts as a temporary table.
15. Always validate row counts after joins.

---

## Course Lab

The integrated PostgreSQL lab is located under:

```text
../lab/
```

Main files:

```text
lab_guide.html
lab_run_book.md
sql/00_create_schema.sql
sql/01_create_tables.sql
sql/02_insert_sample_data.sql
sql/03_inner_and_outer_joins.sql
sql/04_cross_and_self_joins.sql
sql/05_set_operations.sql
sql/06_subqueries.sql
sql/07_course_challenges.sql
```

The lab intentionally includes:

- unmatched rows;
- one-to-many relationships;
- multiple population years;
- `NULL` foreign keys;
- duplicate-compatible set-operation rows;
- city and country names that intersect;
- examples that expose the `NOT IN`/`NULL` trap.

---

## Final Review Checklist

- [ ] I can explain how joins differ from set operations.
- [ ] I can choose between `INNER`, `LEFT`, `FULL`, and `CROSS JOIN`.
- [ ] I can explain `ON` versus `WHERE` with a `LEFT JOIN`.
- [ ] I can detect accidental row multiplication.
- [ ] I can write and explain a self join.
- [ ] I can use conditional aggregation instead of a self join when appropriate.
- [ ] I can choose between `UNION` and `UNION ALL`.
- [ ] I understand the direction of `EXCEPT`.
- [ ] I can explain `INTERSECT` versus `INNER JOIN`.
- [ ] I can write semi joins and anti joins.
- [ ] I understand the `NOT IN`/`NULL` problem.
- [ ] I can use subqueries in `WHERE`, `SELECT`, and `FROM`.
- [ ] I can validate a query using row counts, key checks, and duplicate checks.

---

## Course Closeout Status

```text
Platform status: PASSED
Documentation coverage: COMPLETE
Lab coverage: DEVELOPING
Recall confidence: DEVELOPING
Interview readiness: NEEDS REPETITION
```

The course is complete at the platform level. The next stage is repetition through the integrated lab and later review through the HTML Field Guide and SQL Quick Lookup.
