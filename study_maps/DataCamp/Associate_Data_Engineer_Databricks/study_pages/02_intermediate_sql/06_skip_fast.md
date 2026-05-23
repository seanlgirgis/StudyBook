# Course 2: Intermediate SQL - Skip/Fast Classification

Status: completion checkpoint

## FAST REVIEW
- SQL formatting basics
- Simple SELECT/FROM/LIMIT
- Basic WHERE filters
- ASC/DESC basics

## NORMAL STUDY
- ORDER BY multiple fields
- Aggregate functions
- SQL style and aliases
- LIKE / NOT LIKE
- IN
- NULL handling

## SLOW DOWN
- COUNT(*) vs COUNT(column) vs COUNT(DISTINCT column)
- Order of execution
- BETWEEN inclusive boundaries
- Integer division
- GROUP BY rules
- HAVING vs WHERE
- Alias timing

## PRACTICE REQUIRED
- COUNT(DISTINCT ...)
- BETWEEN
- IN
- LIKE wildcards
- ROUND negative parameter
- Arithmetic expressions
- GROUP BY with COUNT/AVG
- HAVING aggregate filters
- Full reporting query with WHERE + GROUP BY + HAVING + ORDER BY + LIMIT

## INTERVIEW IMPORTANT
- WHERE filters rows; HAVING filters groups
- COUNT(column) ignores NULLs
- NULL checks are data completeness checks
- Aggregate functions summarize filtered subsets
- GROUP BY changes row-level data into grouped summaries
- Selected non-aggregate fields must appear in GROUP BY
- ORDER BY can use aliases; WHERE/HAVING generally should not rely on aliases
- Readable SQL matters in team environments
