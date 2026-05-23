# Course 2: Intermediate SQL - Transcript Clean Notes

Status: partial checkpoint

## A. COUNT and DISTINCT

- `COUNT(*)` counts rows.
- `COUNT(column)` counts non-NULL values.
- `COUNT(DISTINCT column)` counts unique non-NULL values.
- Key trap: `DISTINCT COUNT(column)` is not the same as `COUNT(DISTINCT column)`.

## B. Query Execution Order

Simple model covered:
- `FROM`
- `WHERE`
- `SELECT`
- `LIMIT`

Expanded model covered:
- `FROM`
- `WHERE`
- `GROUP BY`
- `HAVING`
- `SELECT`
- `ORDER BY`
- `LIMIT`

Key keeper:
- `WHERE` filters rows.
- `HAVING` filters groups (after `GROUP BY`).

## C. SQL Style and Readability

- Use readable formatting even when SQL can run in one line.
- Capitalize SQL keywords.
- Use new lines for major clauses.
- Alias columns for clarity.
- Keep semicolon as a good habit.
- Use quoted identifiers when needed (e.g., reserved/conflicting names).

## D. WHERE and Operators

- `WHERE` filters rows before `SELECT` output.
- Numbers typically unquoted; strings in single quotes.
- Covered operators: `>`, `<`, `=`, `>=`, `<=`, `<>`.

## E. AND / OR / BETWEEN / IN

- `AND`: all conditions true.
- `OR`: at least one true.
- `BETWEEN`: inclusive bounds.
- `IN`: cleaner than repeated `OR`.
- Parentheses protect logic when combining `AND` and `OR`.

## F. LIKE / NOT LIKE

- `LIKE` performs pattern matching.
- `NOT LIKE` excludes pattern.
- `%` = zero or more chars.
- `_` = exactly one char.
- Case sensitivity depends on engine; PostgreSQL `LIKE` is case-sensitive.

## G. NULL Handling

- `NULL` = missing/unknown/not recorded.
- `NULL` is not zero and not empty string.
- Use `IS NULL` / `IS NOT NULL`, not `= NULL`.
- `COUNT(column)` ignores `NULL`; `COUNT(*)` counts rows.

## H. Aggregate Functions

- Covered: `COUNT`, `AVG`, `SUM`, `MIN`, `MAX`.
- `SUM` and `AVG` require numeric values.
- `MIN`/`MAX` on text follow sort order (e.g., alphabetical).
- Filter with `WHERE` first, then aggregate the remaining rows.

## I. ROUND, Arithmetic, Integer Division, Alias Timing

- `ROUND(value, n)` supports positive and negative `n`.
- Negative `n` rounds left of decimal point (e.g., tens/hundreds/thousands).
- Arithmetic operators: `+`, `-`, `*`, `/`.
- Integer division can truncate (`2 / 10` -> `0` in integer context).
- Use decimal literals for decimal output (`2.0 / 10.0`).
- Aliases from `SELECT` are generally unavailable in `WHERE`.
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
