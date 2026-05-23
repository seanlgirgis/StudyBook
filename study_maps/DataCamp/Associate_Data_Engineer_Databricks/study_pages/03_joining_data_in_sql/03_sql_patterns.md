# Course 3: Joining Data in SQL - sql patterns

Status: placeholder

TODO:
- Add official chapter names after Sean provides the course outline/transcript.
- Add cleaned notes after transcript intake.
- Mark topics as FAST REVIEW / NORMAL STUDY / SLOW DOWN /
  PRACTICE REQUIRED / INTERVIEW IMPORTANT after review.


# Chapter 3 SQL Patterns - UNION and UNION ALL

UNION pattern:

SELECT column1, column2
FROM table_a

UNION

SELECT column1, column2
FROM table_b;

Meaning:
Stack both result sets and remove exact duplicate rows.

UNION ALL pattern:

SELECT column1, column2
FROM table_a

UNION ALL

SELECT column1, column2
FROM table_b;

Meaning:
Stack both result sets and keep duplicate rows.

Rules:
- Both SELECT statements must return the same number of columns.
- Matching columns must have compatible data types.
- Final column names come from the first SELECT.
- UNION and UNION ALL do not use ON or USING.

# Chapter 3 SQL Patterns - INTERSECT

INTERSECT pattern:

SELECT column1, column2
FROM table_a

INTERSECT

SELECT column1, column2
FROM table_b;

Meaning:
Return only rows that appear in both SELECT results.

Rules:
- Both SELECT statements must return the same number of columns.
- Matching columns must have compatible data types.
- INTERSECT compares the full selected row.
- INTERSECT does not use ON or USING.
- Result column names come from the first SELECT.

# Chapter 3 SQL Patterns - EXCEPT

EXCEPT pattern:

SELECT column1, column2
FROM table_a

EXCEPT

SELECT column1, column2
FROM table_b;

Meaning:
Return rows from the first SELECT that do not appear in the second SELECT.

Rules:
- EXCEPT is left result minus right result.
- Both SELECT statements must return the same number of columns.
- Matching columns must have compatible data types.
- EXCEPT compares the full selected row.
- EXCEPT does not use ON or USING.
- Result column names come from the first SELECT.

# Chapter 4 SQL Patterns - Semi Joins and Anti Joins

Semi join pattern:

SELECT column1, column2
FROM table_a
WHERE key_column IN (
    SELECT key_column
    FROM table_b
    WHERE condition
);

Meaning:
Return rows from the first table where the key exists in the subquery.

Anti join pattern:

SELECT column1, column2
FROM table_a
WHERE key_column NOT IN (
    SELECT key_column
    FROM table_b
    WHERE condition
);

Meaning:
Return rows from the first table where the key does not exist in the subquery.

Rules:
- Semi and anti joins filter rows.
- They do not add columns from the second table.
- The subquery usually returns one column used as the filter list.
- Semi join uses IN.
- Anti join uses NOT IN.

# Chapter 4 SQL Patterns - Subqueries inside WHERE and SELECT

WHERE subquery pattern:

SELECT column1, column2
FROM table_a
WHERE key_column IN (
    SELECT key_column
    FROM table_b
    WHERE condition
);

Meaning:
Filter the outer query using a list produced by the subquery.

SELECT subquery pattern:

SELECT column1,
       (
           SELECT COUNT(*)
           FROM table_b
           WHERE table_b.key_column = table_a.key_column
       ) AS count_value
FROM table_a;

Meaning:
Add a calculated value to the SELECT result.

Rules:
- WHERE subqueries are commonly used for filtering.
- IN can use a subquery result as its list.
- The filtered column and subquery result must have compatible data types.
- SELECT subqueries calculate displayed values.
- SELECT subqueries need aliases.
- Subqueries may read from the same table or a different table.

# Chapter 4 SQL Patterns - Subqueries inside FROM

FROM subquery pattern:

SELECT sub.column1,
       sub.calculated_value
FROM (
    SELECT column1,
           MAX(column2) AS calculated_value
    FROM table_a
    GROUP BY column1
) AS sub;

Meaning:
Use the subquery as a temporary table in the outer query.

Example:

SELECT DISTINCT
    monarchs.continent,
    sub.most_recent
FROM monarchs,
     (
         SELECT continent,
                MAX(indep_year) AS most_recent
         FROM states
         GROUP BY continent
     ) AS sub
WHERE monarchs.continent = sub.continent
ORDER BY monarchs.continent;

Rules:
- FROM subqueries act like temporary tables.
- FROM subqueries need aliases.
- They are useful when you need to aggregate first and then filter or compare.
- Be careful with duplicates when multiple table-like objects are listed in
  FROM.
