## Local PostgreSQL SQL Analysis Ladder - First Pass

### Common mistakes and quick fixes

1. `COUNT(*)` vs `COUNT(column)`
- `COUNT(*)` counts all rows.
- `COUNT(column)` ignores rows where that column is `NULL`.
- Use the one that matches your intent.

2. `WHERE` vs `HAVING`
- `WHERE` filters rows before grouping.
- `HAVING` filters grouped results after aggregation.
- For `inter_dom = 'Inter'`, use `WHERE` before `GROUP BY`.

3. `GROUP BY` is required for non-aggregated selected columns
- If `stay` is selected with averages, `stay` must be in `GROUP BY`.
- Otherwise SQL raises grouping errors.

4. `NULL` rows can distort interpretation
- Missing scores can silently reduce denominator in averages.
- Always run null checks before interpreting results.

5. Small groups may mislead analysis
- A group with very few rows can show unstable averages.
- Always inspect `COUNT(*)` beside averages.
