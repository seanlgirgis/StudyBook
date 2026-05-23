# Course 4: Data Manipulation in SQL - Flashcards

Status: review deck created

## Flashcard 01
Q: What is a CASE statement used for?
A: To derive category/value outputs from conditional logic.

## Flashcard 02
Q: When does CASE inside WHERE help?
A: When filter logic depends on derived categories.

## Flashcard 03
Q: Why add ELSE in CASE?
A: To avoid accidental NULL buckets and make logic explicit.

## Flashcard 04
Q: What is conditional aggregation?
A: Using aggregate functions over CASE conditions.

## Flashcard 05
Q: COUNT(CASE WHEN ...) returns what?
A: Count of rows where condition produced non-NULL.

## Flashcard 06
Q: SUM(CASE WHEN ...) is best for what?
A: Conditional totals for numeric measures.

## Flashcard 07
Q: AVG(CASE WHEN ... THEN 1 ELSE 0 END) gives what?
A: A percentage-style ratio of true outcomes.

## Flashcard 08
Q: Why can CASE compare two columns?
A: Because WHEN logic can include cross-column comparisons.

## Flashcard 09
Q: Key CASE trap in home/away logic?
A: Forgetting to reverse win/loss checks by team side.

## Flashcard 10
Q: Why does CASE in WHERE often use IS NOT NULL?
A: To keep only rows that matched target CASE branches.

## Flashcard 11
Q: What is a simple subquery?
A: A nested query that can run independently.

## Flashcard 12
Q: Where can simple subqueries appear?
A: SELECT, FROM, WHERE, and other clauses.

## Flashcard 13
Q: Scalar subquery means what?
A: Subquery returns exactly one value.

## Flashcard 14
Q: IN subquery is useful for?
A: Filtering by a derived list of IDs/values.

## Flashcard 15
Q: FROM subquery is useful for?
A: Pre-shaping data before final query logic.

## Flashcard 16
Q: SELECT subquery is useful for?
A: Adding benchmark values without collapsing detail rows.

## Flashcard 17
Q: Main filter and subquery filter relation?
A: Main query filters do not auto-apply inside subqueries.

## Flashcard 18
Q: What is a correlated subquery?
A: A subquery that references outer-query row values.

## Flashcard 19
Q: Why can correlated subqueries be slower?
A: They are re-evaluated for many outer rows.

## Flashcard 20
Q: Can correlated subquery run alone?
A: No, it depends on outer-query context.

## Flashcard 21
Q: What is a nested subquery?
A: A subquery inside another subquery layer.

## Flashcard 22
Q: Why use nested subqueries?
A: For aggregate-of-aggregate and multi-stage transformations.

## Flashcard 23
Q: What is a CTE?
A: A named subquery declared with WITH before main query.

## Flashcard 24
Q: CTE readability benefit?
A: Breaks complex logic into sequential named steps.

## Flashcard 25
Q: Can multiple CTEs be chained?
A: Yes, comma-separated and referenced in later steps.

## Flashcard 26
Q: What does OVER() do?
A: Applies window function over result-set window.

## Flashcard 27
Q: Why use window functions vs GROUP BY?
A: Keep detail rows while adding aggregate/rank context.

## Flashcard 28
Q: What does PARTITION BY do?
A: Creates independent window groups by key columns.

## Flashcard 29
Q: Is PARTITION BY Spark-only?
A: No, it is standard SQL window-function logic.

## Flashcard 30
Q: What does RANK() OVER(ORDER BY ...) do?
A: Ranks rows by ordered metric with tie behavior.

## Flashcard 31
Q: What is a sliding window?
A: A window frame that moves row-by-row for calculations.

## Flashcard 32
Q: Meaning of UNBOUNDED PRECEDING?
A: Frame starts at beginning of partition/window.

## Flashcard 33
Q: Meaning of CURRENT ROW in frame?
A: Frame boundary includes up to current row point.

## Flashcard 34
Q: ROWS BETWEEN is used for what?
A: Defining explicit frame boundaries for window calculations.

## Flashcard 35
Q: Running total frame pattern?
A: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.

## Flashcard 36
Q: Reverse running total frame pattern?
A: ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING.

## Flashcard 37
Q: Final case-study objective?
A: Identify teams that defeated Manchester United in 2013/2014.

## Flashcard 38
Q: Case-study building blocks?
A: CTEs + CASE outcome logic + ranking by goal margin.

## Flashcard 39
Q: Interview-safe claim from this course?
A: Refreshed reusable SQL analytics patterns and logic.


