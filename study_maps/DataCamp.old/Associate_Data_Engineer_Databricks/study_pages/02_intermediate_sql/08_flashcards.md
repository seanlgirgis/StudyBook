# Course 2: Intermediate SQL - Flashcards

Status: partial checkpoint

Q: What does `COUNT(*)` measure?
A: Total rows.

Q: What does `COUNT(column)` measure?
A: Non-NULL values in that column.

Q: What does `COUNT(DISTINCT column)` measure?
A: Unique non-NULL values.

Q: Is `BETWEEN` inclusive or exclusive?
A: Inclusive.

Q: Which clause filters raw rows?
A: `WHERE`.

Q: Which clause filters grouped results?
A: `HAVING`.

Q: What wildcard means any-length string?
A: `%`.

Q: What wildcard means exactly one character?
A: `_`.

Q: How do you test for missing values?
A: `IS NULL` / `IS NOT NULL`.

Q: Why can `2 / 10` be surprising?
A: Integer division can return truncated integer result.

Q: Why might `WHERE profit > ...` fail when `profit` is an alias in SELECT?
A: `WHERE` is evaluated before SELECT aliases are created.

Q: What does `ROUND(x, -2)` do?
A: Rounds to nearest hundred.
\n\n## Completion Delta\n- Added ORDER BY, GROUP BY, HAVING, percentage arithmetic, span/decade, unit conversion, and final completion classification coverage.
