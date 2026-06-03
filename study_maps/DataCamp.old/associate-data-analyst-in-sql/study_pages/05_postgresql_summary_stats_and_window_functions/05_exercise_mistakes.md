# Exercise Mistakes (Session Notes)

## Mistake 1: Assuming partition keeps one row
- Mistake: treating `PARTITION BY` like `GROUP BY`.
- Fix: remember partition keeps all rows and adds context columns.

## Mistake 2: Missing tie breaker in ROW_NUMBER
- Mistake: only ordering by revenue/date and getting unstable ordering on ties.
- Fix: add `event_id` as tie breaker in `ORDER BY`.

## Mistake 3: Confusing RANK and DENSE_RANK
- Mistake: expecting both to behave the same after ties.
- Fix: `RANK` skips numbers; `DENSE_RANK` does not.

## Mistake 4: Using LAG/LEAD without clear order
- Mistake: forgetting `ORDER BY` in window.
- Fix: define order (`sale_date, event_id`) so previous/next is deterministic.

## Mistake 5: Divide-by-zero in percent change
- Mistake: direct division by previous value.
- Fix: use `NULLIF(previous_revenue, 0)`.

## Mistake 6: Weak daily partition practice data
- Initial issue: one event per day weakened `PARTITION BY sale_date` practice.
- Fix: reseeded to 25 dates with 4 events per date.

## Mistake 7: No same-day ties for ranking
- Initial issue: ranking examples were weak without ties inside day.
- Fix: added same-day ties in revenue.

## Mistake 8: Revenue pattern too smooth for NTILE demo
- Initial issue: smooth sequences made quartiles look date-polished.
- Fix: mixed revenue distribution across dates and regions while keeping ties.
## Lab Data Design Corrections

### 1) One row per day
- Problem: `PARTITION BY sale_date` had no meaningful multi-row group.
- Fix: changed to 25 dates with 4 events per day.

### 2) Ties were global, not inside day
- Problem: `RANK` and `DENSE_RANK` did not clearly show tie behavior per day.
- Fix: added same-day revenue ties such as `900, 700, 700, 400`.

### 3) Revenue too smooth
- Problem: `NTILE` looked fake because quartiles appeared in perfect order by date.
- Fix: mixed high, medium, and low revenues across dates.

### 4) Lesson learned
- Practice data must be shaped to demonstrate the SQL concept.

## Milestone Lessons / Avoid These Mistakes
- Do not use window functions when `GROUP BY` is enough.
  Example: athlete medal counts need `GROUP BY` first.
- Do not let `LAG`/`LEAD` cross unrelated groups.
  Add `PARTITION BY event`, `gender`, or other grouping keys.
- Do not add tie breakers to `RANK`/`DENSE_RANK` when your goal is to preserve ties.
- Do not trust `LAST_VALUE` without an explicit full frame.
- Do not assume Codex knows chat context; documentation prompts must be self-contained.

## Ranking and NTILE Reminders
- Do not use windowing when `GROUP BY` alone answers the question.
- Do not forget `PARTITION BY` when ranking inside groups.
- Do not treat `NTILE` as tie-preserving ranking.
- Do not treat `NTILE` as true percentile calculation.

## Alias Correction: Moving Total vs Moving Average
- `SUM` + sliding frame = moving total.
- `AVG` + sliding frame = moving average.
- Do not label `SUM` output as `Medals_MA`.
- Prefer aliases like `Medals_MT`, `Moving_Total`, or `Medals_3_Game_Total`.

```sql
WITH Country_Medals AS (
SELECT
Year,
Country,
COUNT(*) AS Medals
FROM Summer_Medals
GROUP BY Year, Country
)

SELECT
Year,
Country,
Medals,
SUM(Medals) OVER (
PARTITION BY Country
ORDER BY Year ASC
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS Medals_MT
FROM Country_Medals
ORDER BY Country ASC, Year ASC;
```

This is a 3-game moving total per country, not a moving average.
To make it a moving average, replace `SUM()` with `AVG()` and use an MA alias.

## Final Traps: CROSSTAB, Totals, and Lists
- Do not confuse `CROSSTAB` with a window function.
- Do not leave placeholder text like "source query here" inside `CROSSTAB`.
- Simple `CROSSTAB` source should be row/category/value.
- Output columns in `AS ct (...)` must match pivot categories and value types.
- Simple `CROSSTAB` can misalign if categories are missing; safer form or manual pivot may be better in production.
- `ROLLUP`/`CUBE` NULLs are subtotal labels, not always missing data.
- `COALESCE` changes display label only.
- Display `ORDER BY` can place totals unexpectedly; use `CASE` sort to control placement.
- `STRING_AGG` needs `ORDER BY` inside the aggregate when list order matters.

## Deep Traps Added
- Placeholder text inside CROSSTAB causes syntax errors.
- Keep semicolon outside dollar-quoted source query in StudyBook style.
- Medals_MA naming trap: SUM is moving total, not moving average.
- Do not over-trust polished sample data realism.

