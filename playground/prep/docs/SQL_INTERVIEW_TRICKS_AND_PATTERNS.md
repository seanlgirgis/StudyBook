# SQL Interview Tricks and Patterns

## TOC
- [1. SQL Mental Model](#1-sql-mental-model)
- [2. Basic SELECT and WHERE](#2-basic-select-and-where)
- [3. JOIN Pattern](#3-join-pattern)
- [4. GROUP BY Pattern](#4-group-by-pattern)
- [5. DATE_TRUNC Time Buckets](#5-date_trunc-time-buckets)
- [6. P95 with PERCENTILE_CONT](#6-p95-with-percentile_cont)
- [7. CTE Pattern](#7-cte-pattern)
- [8. Window Functions Mental Model](#8-window-functions-mental-model)
- [9. ROW_NUMBER / RANK / DENSE_RANK](#9-row_number--rank--dense_rank)
- [10. LAG / LEAD](#10-lag--lead)
- [11. Moving Average](#11-moving-average)
- [12. JSONB Tags](#12-jsonb-tags)
- [13. Risky Windows Query](#13-risky-windows-query)
- [14. Rightsizing / Over-Allocation Query](#14-rightsizing--over-allocation-query)
- [15. Cost Rollup](#15-cost-rollup)
- [16. Before/After Deployment Comparison](#16-beforeafter-deployment-comparison)
- [17. SQL to Pandas Translation](#17-sql-to-pandas-translation)
- [18. Fire Drill Q&A](#18-fire-drill-qa)
- [19. Final Memorized SQL Answer](#19-final-memorized-sql-answer)

[Back to TOC](#toc)

## 1. SQL Mental Model
- `telemetry_samples` is the fact table.
- `services` and `hosts` are lookup/dimension tables.
- Most capacity questions become joins + aggregations + time buckets.
- SQL turns raw samples into operational summaries.

Interview sentence:
I think of telemetry SQL as moving from raw event or sample rows into service, host, time-bucket, and ownership summaries.

[Back to TOC](#toc)

## 2. Basic SELECT and WHERE
- Select only columns needed for the question.
- Filter for high CPU, high memory, or high latency.
- Use `AND` for stricter filtering and `OR` for broader risk scans.

Example:
```sql
SELECT
    sampled_at,
    service_id,
    host_id,
    cpu_utilization_pct,
    memory_utilization_pct
FROM telemetry_samples
WHERE cpu_utilization_pct >= 80
   OR memory_utilization_pct >= 80
ORDER BY sampled_at
LIMIT 20;
```

[Back to TOC](#toc)

## 3. JOIN Pattern
- `telemetry_samples` has `service_id` and `host_id`.
- `services` and `hosts` make IDs readable.
- `JOIN` without `LEFT/RIGHT` means `INNER JOIN`.

Example:
```sql
SELECT
    t.sampled_at,
    s.service_name,
    t.host_id,
    t.cpu_utilization_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id;
```

Interview sentence:
I join telemetry to service and host metadata so raw IDs become readable operational dimensions.

[Back to TOC](#toc)

## 4. GROUP BY Pattern
- `GROUP BY` changes grain.
- Raw sample rows become one row per service/host/time bucket.
- Non-grouped columns must be aggregated.

Common aggregates:
- `AVG` typical usage
- `MAX` peak usage
- `COUNT` sample volume
- `SUM` totals like cost or requests

Interview sentence:
GROUP BY changes the question from individual samples to service-level or workload-level summaries.

[Back to TOC](#toc)

## 5. DATE_TRUNC Time Buckets
- Use `DATE_TRUNC('hour', sampled_at)` for hourly rollups.
- Use `DATE_TRUNC('day', sampled_at)` for daily rollups.
- Group by the full `DATE_TRUNC(...)` expression.
- Pandas equivalent: `.dt.floor("h")`.

Example:
```sql
SELECT
    DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('hour', t.sampled_at),
    s.service_name
ORDER BY
    sample_hour,
    s.service_name;
```

Interview sentence:
DATE_TRUNC lets me convert noisy timestamped telemetry into hourly or daily capacity trends.

[Back to TOC](#toc)

## 6. P95 with PERCENTILE_CONT
```sql
ROUND(
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC,
    2
) AS p95_cpu_pct
```

Breakdown:
- `PERCENTILE_CONT(0.95)` = 95th percentile
- `WITHIN GROUP (ORDER BY ...)` = values used for percentile
- `::NUMERIC` = cast so rounding works cleanly
- `ROUND(..., 2)` = 2 decimals
- `AS p95_cpu_pct` = readable output name

Latency nuance:
If `p95_latency_ms` is already a sampled P95 metric, then hourly P95 over that column is P95 of sampled P95 values, not raw request-level P95.

Interview sentence:
Average shows normal usage, max shows worst spike, and P95 shows sustained high pressure while reducing one-off noise.

[Back to TOC](#toc)

## 7. CTE Pattern
- `WITH` creates a named temporary result inside one query.
- Good for readability and multi-step logic.
- Pattern: build rollup first, filter/rank second.

Example:
```sql
WITH hourly_service_rollup AS (
    SELECT ...
)
SELECT *
FROM hourly_service_rollup
WHERE p95_cpu_pct >= 85;
```

Interview sentence:
I use CTEs to make complex telemetry questions readable: first calculate the rollup, then filter or rank the result.

[Back to TOC](#toc)

## 8. Window Functions Mental Model
- `GROUP BY` collapses rows.
- Window functions keep rows visible and add analytics beside each row.
- `OVER()` defines the window.
- `PARTITION BY` defines groups.
- `ORDER BY` defines order inside each group.

Interview sentence:
Window functions are useful when I need row-level telemetry plus context like rank, previous value, moving average, or running total.

[Back to TOC](#toc)

## 9. ROW_NUMBER / RANK / DENSE_RANK
- `ROW_NUMBER()` gives a unique sequence.
- `RANK()` handles ties and may skip numbers.
- `DENSE_RANK()` handles ties without skipping numbers.

Example: rank services by hourly P95 CPU
```sql
WITH hourly AS (
    SELECT
        DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
        s.service_name,
        ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC, 2) AS p95_cpu_pct
    FROM telemetry_samples t
    JOIN services s ON s.service_id = t.service_id
    GROUP BY DATE_TRUNC('hour', t.sampled_at), s.service_name
)
SELECT
    sample_hour,
    service_name,
    p95_cpu_pct,
    RANK() OVER (PARTITION BY sample_hour ORDER BY p95_cpu_pct DESC) AS cpu_risk_rank
FROM hourly;
```

Interview sentence:
I use ranking to find top-risk services, hottest workloads, or most expensive resources.

[Back to TOC](#toc)

## 10. LAG / LEAD
- `LAG()` looks backward.
- `LEAD()` looks forward.
- Useful for current vs previous hour/day comparisons.

Example:
```sql
WITH hourly AS (
    SELECT
        DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
        s.service_name,
        ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC, 2) AS p95_cpu_pct
    FROM telemetry_samples t
    JOIN services s ON s.service_id = t.service_id
    GROUP BY DATE_TRUNC('hour', t.sampled_at), s.service_name
)
SELECT
    sample_hour,
    service_name,
    p95_cpu_pct,
    LAG(p95_cpu_pct) OVER (PARTITION BY service_name ORDER BY sample_hour) AS previous_hour_p95_cpu_pct
FROM hourly;
```

Interview sentence:
LAG helps me detect change over time, such as sudden CPU growth or forecast drift from the previous window.

[Back to TOC](#toc)

## 11. Moving Average
- Smooths noisy telemetry.
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` computes a 3-sample rolling average.
- Good for trend smoothing.

Example:
```sql
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    ROUND(
        AVG(t.cpu_utilization_pct) OVER (
            PARTITION BY s.service_name, t.host_id
            ORDER BY t.sampled_at
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS cpu_moving_avg_3_samples
FROM telemetry_samples t
JOIN services s ON s.service_id = t.service_id;
```

Interview sentence:
A moving average reduces noise so I can see whether pressure is sustained or just a one-sample spike.

[Back to TOC](#toc)

## 12. JSONB Tags
- `tags` stores flexible metadata.
- `tags ->> 'team'` extracts text.
- `tags ? 'region'` checks key existence.
- Useful for team/env/region/ownership reporting.

Example:
```sql
SELECT
    tags,
    tags ->> 'team' AS tag_team,
    tags ->> 'env' AS tag_env,
    tags ->> 'region' AS tag_region
FROM telemetry_samples;
```

Interview sentence:
JSONB tags let me keep flexible telemetry metadata while still extracting ownership and environment fields for reporting.

[Back to TOC](#toc)

## 13. Risky Windows Query
Pattern:
- Build hourly rollup in a CTE.
- Use P95 + threshold filters.
- Return risky service/time windows.

Common filters:
- `p95_cpu_pct >= 85`
- `p95_memory_pct >= 85`
- `p95_of_sampled_p95_latency_ms >= threshold`
- `avg_error_rate_pct >= threshold`

Interview sentence:
This turns raw telemetry into an action list of risky hours and services.

[Back to TOC](#toc)

## 14. Rightsizing / Over-Allocation Query
Compare allocated vs actual:
- `allocated_cpu_cores`
- `actual_cpu_cores`
- `unused_cpu_cores`
- `allocated_memory_gb`
- `actual_memory_gb`
- `unused_memory_gb`

Interview sentence:
Rightsizing starts by comparing allocated capacity to actual usage, then validating with ownership and business context before reducing resources.

[Back to TOC](#toc)

## 15. Cost Rollup
- Use `SUM(cloud_cost_usd)` if cost is incremental per sample.
- Use `AVG`/`MAX` if cost is a snapshot field.
- Group by service/team/region based on question.

Interview sentence:
For cost analysis, I first clarify whether the cost column is incremental or snapshot-based, because that determines whether SUM or AVG/MAX is correct.

[Back to TOC](#toc)

## 16. Before/After Deployment Comparison
Pattern (supported in `sql/05_interview_questions.sql`):
- join deployments to telemetry/service data
- use time windows around `deployed_at`
- calculate before vs after averages
- often implemented with `FILTER` or `CASE`

Interview sentence:
A before/after deployment query helps check whether a release changed latency, errors, or utilization.

[Back to TOC](#toc)

## 17. SQL to Pandas Translation
| SQL Pattern | Pandas Equivalent |
|---|---|
| `DATE_TRUNC('hour')` | `.dt.floor("h")` |
| `GROUP BY` | `groupby()` |
| `AVG` | `mean()` |
| `MAX` | `max()` |
| `COUNT` | `count()` |
| P95 | `quantile(0.95)` |
| `CASE WHEN` | `np.select` / `apply` / boolean masks |
| JSONB extraction | DataFrame columns after normalization |

[Back to TOC](#toc)

## 18. Fire Drill Q&A
1. What is the difference between GROUP BY and window functions?  
GROUP BY collapses rows; window functions keep rows and add calculations beside them.

2. Why use DATE_TRUNC?  
To bucket telemetry into hourly/daily windows for trend analysis.

3. Why P95 instead of average?  
P95 highlights sustained high pressure that averages can hide.

4. What does PERCENTILE_CONT do?  
Calculates a percentile value within an ordered group.

5. What is a CTE?  
A named temporary query block for readability and multi-step logic.

6. Why use LAG?  
To compare current values with previous time windows.

7. How do you rank risky services?  
Compute risk metrics per window, then apply `RANK()` over each time bucket.

8. How do you query JSONB tags?  
Use `->>` to extract text keys and `?` to check key existence.

9. How do you find overallocated services?  
Compare allocated CPU/memory against actual usage and sort by waste/cost.

10. How do you summarize cost?  
Use `SUM` for incremental cost; `AVG`/`MAX` for snapshots.

11. How do you compare before/after deployment?  
Join deployments with telemetry and compute windowed metrics before and after `deployed_at`.

12. How do you explain SQL capacity analysis to a manager?  
SQL converts noisy telemetry into service-level risk, waste, and cost summaries that drive prioritized actions.

[Back to TOC](#toc)

## 19. Final Memorized SQL Answer
In SQL, I move from raw telemetry samples to operational capacity views. I join telemetry to service and host metadata, bucket timestamps with DATE_TRUNC, aggregate with AVG, MAX, SUM, and P95, use CTEs to keep complex logic readable, and use window functions like RANK and LAG when I need ranking or previous-period comparison. The goal is to turn raw telemetry into a service-level action list: capacity risk, rightsizing candidate, cost concern, or normal.
