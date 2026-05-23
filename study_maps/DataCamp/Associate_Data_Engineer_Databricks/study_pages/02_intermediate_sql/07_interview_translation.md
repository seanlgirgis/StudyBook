# Course 2: Intermediate SQL - Interview Translation

Status: partial checkpoint

- "I distinguish row count from value count: `COUNT(*)` counts rows, while `COUNT(column)` counts non-NULL values in that column."
- "For cardinality, I use `COUNT(DISTINCT column)` rather than wrapping `COUNT(...)` with `DISTINCT`."
- "I treat SQL as a logical pipeline: `FROM` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `ORDER BY` -> `LIMIT`."
- "I use `WHERE` for row-level filtering and `HAVING` for group-level filtering after aggregation."
- "For multi-condition filters, I use `IN` and `BETWEEN` when they improve readability, and I parenthesize mixed `AND`/`OR`."
- "I treat NULL checks as data quality checks using `IS NULL` and `IS NOT NULL`."
- "I keep SQL readable with clear clause layout and explicit aliases to support team maintenance."
- "I watch for integer division and explicit numeric types to avoid accidental truncation."
- "I avoid referencing SELECT aliases in WHERE because alias creation happens later in the logical order."
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
