
## Interview Pattern: Nth Person per Group

Interview question Sean remembered:
"Get the third salesperson by sales volume in each department."

Pattern:
1. Aggregate first by department and salesperson.
2. Rank inside each department.
3. Filter to rank = 3.

```sql
WITH salesperson_sales AS (
SELECT
department,
salesperson,
SUM(sales_amount) AS total_sales
FROM sales
GROUP BY department, salesperson
),

ranked_salespeople AS (
SELECT
department,
salesperson,
total_sales,
ROW_NUMBER() OVER (
PARTITION BY department
ORDER BY total_sales DESC, salesperson ASC
) AS sales_rank
FROM salesperson_sales
)

SELECT
department,
salesperson,
total_sales
FROM ranked_salespeople
WHERE sales_rank = 3
ORDER BY department;
```

Tie-handling note:
- `ROW_NUMBER` returns one exact third salesperson.
- `RANK` includes all tied third-place salespeople.
- `DENSE_RANK` returns the third distinct sales tier.

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

## Interview-safe Translation (Course 05 Completion)
"Window functions are for row-level analytics without losing detail. CROSSTAB is for pivot-style reporting. ROLLUP and CUBE are GROUP BY extensions for subtotals. COALESCE cleans subtotal labels. STRING_AGG compresses ranked rows into a readable list."

## Additional Interview-safe Language
- For reporting, compute vertical rankings first, then pivot if columns are required.
- For multi-measure pivots, prefer FILTER/CASE over forcing multiple values into one CROSSTAB.

