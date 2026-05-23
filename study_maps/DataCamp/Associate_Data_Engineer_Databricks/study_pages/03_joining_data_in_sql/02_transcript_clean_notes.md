# Course 3: Joining Data in SQL - transcript clean notes

Status: placeholder

TODO:
- Add official chapter names after Sean provides the course outline/transcript.
- Add cleaned notes after transcript intake.
- Mark topics as FAST REVIEW / NORMAL STUDY / SLOW DOWN /
  PRACTICE REQUIRED / INTERVIEW IMPORTANT after review.


# Chapter 3: Set Theory for SQL Joins

Status: raw transcript intake started

Topics started:
- UNION
- UNION ALL
- Difference between joins and set operations
- Duplicate handling
- Column count and data type requirements

## INTERSECT

INTERSECT returns only rows that exist in both SELECT results.
It is a set operation, not a join. It stacks/compares selected result sets
instead of joining tables side-by-side.

Important:
INTERSECT compares the full selected row. If two columns are selected, both
columns must match for the row to appear in the final result.

Example:

SELECT country
FROM prime_ministers

INTERSECT

SELECT country
FROM presidents;

This returns countries that appear in both result sets.

## EXCEPT

EXCEPT returns rows from the first SELECT result that do not appear in the
second SELECT result.

Plain English:
EXCEPT means "show me what is in the left query but not in the right query."

Important:
EXCEPT compares the full selected row. If two columns are selected, both
columns must match before a row is excluded.

Example:

SELECT monarch AS leader, country
FROM monarchs

EXCEPT

SELECT prime_minister, country
FROM prime_ministers;

Meaning:
Return monarchs who are not also prime ministers for the same country.

# Chapter 4: Subqueries, Semi Joins, and Anti Joins

Status: raw transcript intake started

## Additive joins

INNER, LEFT, RIGHT, FULL, CROSS, and SELF join patterns can add columns to the
result set. They combine rows side-by-side.

## Semi join

A semi join keeps rows from the first table when a matching value exists in a
second query.

Pattern:

SELECT column1, column2
FROM table_a
WHERE key_column IN (
    SELECT key_column
    FROM table_b
    WHERE condition
);

Meaning:
Keep rows from table_a only when the key appears in the subquery result.

## Anti join

An anti join keeps rows from the first table when a matching value does not
exist in a second query.

Pattern:

SELECT column1, column2
FROM table_a
WHERE key_column NOT IN (
    SELECT key_column
    FROM table_b
    WHERE condition
);

Meaning:
Keep rows from table_a only when the key does not appear in the subquery result.

## Subqueries inside WHERE

A subquery inside WHERE is used to filter rows from the outer query.

Pattern:

SELECT column1, column2
FROM table_a
WHERE key_column IN (
    SELECT key_column
    FROM table_b
    WHERE condition
);

Meaning:
Keep rows from table_a only when key_column appears in the subquery result.

## Subqueries inside SELECT

A subquery inside SELECT calculates a value to display as a column in the final
result.

Pattern:

SELECT outer_column,
       (
           SELECT COUNT(*)
           FROM table_b
           WHERE table_b.match_column = table_a.match_column
       ) AS calculated_value
FROM table_a;

Meaning:
For each row returned by the outer query, calculate an additional value using
the subquery.

Important:
A subquery inside SELECT should be given an alias.

## Subqueries inside FROM

A subquery inside FROM creates a temporary result table that the outer query
can use.

Pattern:

SELECT sub.group_column,
       sub.calculated_value
FROM (
    SELECT group_column,
           MAX(value_column) AS calculated_value
    FROM source_table
    GROUP BY group_column
) AS sub;

Meaning:
First, the inner query builds a summarized result.
Then, the outer query reads from that result as if it were a table.

Important:
A subquery inside FROM should be given an alias.
