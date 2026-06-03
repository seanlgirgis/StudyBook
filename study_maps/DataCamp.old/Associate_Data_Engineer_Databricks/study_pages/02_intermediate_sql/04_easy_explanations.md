# Course 2: Intermediate SQL - Easy Explanations

Status: partial checkpoint

- `COUNT(*)` answers: "How many rows are there?"
- `COUNT(column)` answers: "How many rows have a real value in this column?"
- `COUNT(DISTINCT column)` answers: "How many different values appear here?"

- `WHERE` is the pre-filter. It removes rows before calculations/final display.
- `HAVING` is the post-group filter. It removes groups after grouping.

- `BETWEEN a AND b` includes both endpoints.
- `IN (...)` is shorthand for many OR checks.

- `LIKE` is text pattern matching:
  `%` many/zero characters, `_` exactly one character.

- `NULL` means missing or unknown, not zero.
- `IS NULL` / `IS NOT NULL` are the correct checks.

- Aggregates summarize many rows into one value.
- `WHERE` decides the input set; aggregate summarizes that set.

- `ROUND(value, -2)` means round to the nearest hundred.
- Negative precision rounds left of decimal.

- Integer division can truncate decimals.
- Use decimal numbers (`2.0 / 10.0`) when decimal output is needed.

- Alias names from `SELECT` are created too late for `WHERE` in most SQL flows.
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
