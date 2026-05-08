
## TOC
- [Basic SELECT and WHERE](#basic-select-and-where)
- [JOIN Pattern](#join-pattern)
  - [Interview sentence:](#interview-sentence)
- [GROUP BY Pattern](#group-by-pattern)
- [DATE_TRUNC Time Buckets](#date_trunc-time-buckets)
  - [Interview sentence](#interview-sentence-1)
- [P95 with PERCENTILE_CONT](#p95-with-percentile_cont)
- [CTE Pattern](#cte-pattern)
  - [Example: compare each telemetry sample to the previous sample](#example-compare-each-telemetry-sample-to-the-previous-sample)
- [ROW_NUMBER / RANK / DENSE_RANK](#row_number--rank--dense_rank)
  - [Plain English](#plain-english)
  - [Interview sentence](#interview-sentence-2)
- [LAG / LEAD](#lag--lead)
  - [Interview sentence](#interview-sentence-3)
- [Moving Average](#moving-average)
  - [Interview sentence](#interview-sentence-4)
- [JSONB Tags](#jsonb-tags)
  - [Interview sentence](#interview-sentence-5)
- [SQL to Pandas Translation](#sql-to-pandas-translation)
- [Fire Drill Q&A](#fire-drill-qa)
- [Final Memorized SQL Answer](#final-memorized-sql-answer)
- [Basic Grouping with Pandas](#basic-grouping-with-pandas)
  - [Talk while coding:](#talk-while-coding)
- [Basic Grouping with Pure Python](#basic-grouping-with-pure-python)
- [Capacity Risk Detection](#capacity-risk-detection)
- [P95 Utilization](#p95-utilization)
- [Full Telemetry Mini-Project](#full-telemetry-mini-project)

## Basic SELECT and WHERE

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
LIMIT 10;
```

[Back to TOC](#toc)

## JOIN Pattern


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

### Interview sentence:
I join telemetry to service and host metadata so raw IDs become readable operational dimensions.

[Back to TOC](#toc)

## GROUP BY Pattern

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

### Interview sentence
DATE_TRUNC lets me convert noisy timestamped telemetry into hourly or daily capacity trends.

[Back to TOC](#toc)

## DATE_TRUNC Time Buckets
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

### Interview sentence
DATE_TRUNC lets me convert noisy timestamped telemetry into hourly or daily capacity trends.

[Back to TOC](#toc)

## P95 with PERCENTILE_CONT
```sql
ROUND(
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC,
    2
) AS p95_cpu_pct
```



[Back to TOC](#toc)

## CTE Pattern

```sql
WITH hourly_service_rollup AS (
    SELECT ...
)
SELECT *
FROM hourly_service_rollup
WHERE p95_cpu_pct >= 85;
```



### Example: compare each telemetry sample to the previous sample

This example uses `LAG()` to compare the current CPU value to the previous CPU value for the same service and host.

```sql
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,

    LAG(t.cpu_utilization_pct) OVER (
        PARTITION BY s.service_name, t.host_id
        ORDER BY t.sampled_at
    ) AS previous_cpu_pct,

    ROUND(
        t.cpu_utilization_pct
        - LAG(t.cpu_utilization_pct)
        OVER (
            PARTITION BY s.service_name, t.host_id
            ORDER BY t.sampled_at
        ),
        2
    ) AS cpu_change_pct

FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.host_id,
    t.sampled_at;
```

[Back to TOC](#toc)

## ROW_NUMBER / RANK / DENSE_RANK


The first two services tie for first place, and the next service gets second place. No gap.

Use `ROW_NUMBER()` when you need exactly one row per group.

Use `RANK()` when ties should share the same place and gaps are acceptable.

Use `DENSE_RANK()` when ties should share the same place but you do not want gaps.

Example: rank services by hourly P95 CPU

```sql
WITH hourly AS (
    SELECT
        DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
        s.service_name,
        ROUND(
            PERCENTILE_CONT(0.95) WITHIN GROUP (
                ORDER BY t.cpu_utilization_pct
            )::NUMERIC,
            2
        ) AS p95_cpu_pct
    FROM telemetry_samples t
    JOIN services s
        ON s.service_id = t.service_id
    GROUP BY
        DATE_TRUNC('hour', t.sampled_at),
        s.service_name
)
SELECT
    sample_hour,
    service_name,
    p95_cpu_pct,

    ROW_NUMBER() OVER (
        PARTITION BY sample_hour
        ORDER BY p95_cpu_pct DESC
    ) AS row_number_cpu_rank,

    RANK() OVER (
        PARTITION BY sample_hour
        ORDER BY p95_cpu_pct DESC
    ) AS cpu_risk_rank,

    DENSE_RANK() OVER (
        PARTITION BY sample_hour
        ORDER BY p95_cpu_pct DESC
    ) AS dense_cpu_risk_rank

FROM hourly
ORDER BY
    sample_hour,
    cpu_risk_rank,
    service_name;
```

### Plain English

* The CTE first calculates one hourly P95 CPU value per service.
* `PARTITION BY sample_hour` ranks services separately inside each hour.
* `ORDER BY p95_cpu_pct DESC` puts the hottest services first.
* `ROW_NUMBER()` gives each service a unique position.
* `RANK()` allows ties and may skip numbers.
* `DENSE_RANK()` allows ties and does not skip numbers.

### Interview sentence

I use ranking to find top-risk services, hottest workloads, or most expensive resources. `ROW_NUMBER()` is useful when I need one clear winner, `RANK()` is useful when ties should share the same place, and `DENSE_RANK()` is useful when I want tie-aware ranking without gaps.

[Back to TOC](#toc)

## LAG / LEAD
- `LAG()` looks backward.
- `LEAD()` looks forward.
- Useful for current vs previous hour/day comparisons.

Example:
```sql
WITH hourly AS (
    SELECT
        DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
        s.service_name,
        ROUND(PERCENTILE_CONT(0.95)
        WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC, 2) AS p95_cpu_pct
    FROM telemetry_samples t
    JOIN services s ON s.service_id = t.service_id
    GROUP BY DATE_TRUNC('hour', t.sampled_at), s.service_name
)
SELECT
    sample_hour,
    service_name,
    p95_cpu_pct,
    LAG(p95_cpu_pct)
    OVER (PARTITION BY service_name ORDER BY sample_hour)
    AS previous_hour_p95_cpu_pct
FROM hourly;
```

### Interview sentence
LAG helps me detect change over time, such as sudden CPU growth or forecast drift from the previous window.

[Back to TOC](#toc)

## Moving Average
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

### Interview sentence
A moving average reduces noise so I can see whether pressure is sustained or just a one-sample spike.

[Back to TOC](#toc)

## JSONB Tags
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

### Interview sentence
JSONB tags let me keep flexible telemetry metadata while still extracting ownership and environment fields for reporting.

[Back to TOC](#toc)


## SQL to Pandas Translation
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

## Fire Drill Q&A
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

## Final Memorized SQL Answer
In SQL, I move from raw telemetry samples to operational capacity views. I join telemetry to service and host metadata, bucket timestamps with DATE_TRUNC, aggregate with AVG, MAX, SUM, and P95, use CTEs to keep complex logic readable, and use window functions like RANK and LAG when I need ranking or previous-period comparison. The goal is to turn raw telemetry into a service-level action list: capacity risk, rightsizing candidate, cost concern, or normal.

[Back to TOC](#toc)

# Module 3 Python Coding Techniques

[Back to TOC](#toc)

## Basic Grouping with Pandas

Interview problem:


```python
import pandas as pd

records = [
    {"service": "checkout", "cpu": 72, "memory": 68},
        . . . ]

df = pd.DataFrame(records)

result = (
    df.groupby("service", as_index=False)
      .agg(
          avg_cpu=("cpu", "mean"),
          avg_memory=("memory", "mean"),
      )
)

result["avg_cpu"] = result["avg_cpu"].round(2)
result["avg_memory"] = result["avg_memory"].round(2)

print(result)
```

### Talk while coding:

I am grouping by service because capacity decisions are usually made at the service, team, namespace, cluster, or workload level.

Average CPU and memory give a first-pass view of utilization. In production, I would also calculate P95, peak, headroom, growth rate, forecast trend, and forecast-vs-actual variance.

[Back to TOC](#toc)

## Basic Grouping with Pure Python

```python
import pandas as pd

records = [
    {"service": "checkout", "cpu": 72, "memory": 68},
    ... ]

df = pd.DataFrame(records)

result = (
    df.groupby("service", as_index=False)
      .agg(
          avg_cpu=("cpu", "mean"),
          avg_memory=("memory", "mean"),
      )
)

result["avg_cpu"] = result["avg_cpu"].round(2)
result["avg_memory"] = result["avg_memory"].round(2)

print(result)
```

[Back to TOC](#toc)

## Capacity Risk Detection
Interview problem:



```python
import pandas as pd

records = [
    {"service": "checkout", "cpu": 72, "memory": 68},
    .  .  .]

df = pd.DataFrame(records)

summary = (
    df.groupby("service", as_index=False)
      .agg(
          avg_cpu=("cpu", "mean"),
          avg_memory=("memory", "mean"),
      )
)

summary = summary.round(2)

summary["capacity_risk"] = (
    (summary["avg_cpu"] > 75) |
    (summary["avg_memory"] > 75)
)

risk_list = summary[summary["capacity_risk"]]

print(risk_list)
```
[Back to TOC](#toc)

## P95 Utilization
P95 is important in capacity planning.

Average utilization can hide high-demand periods.

Max utilization can overreact to one spike.

P95 gives a better signal for high-end sustained demand.

```python
def percentile(values, percentile_value):
    if not values:
        return None

    sorted_values = sorted(values)
    index = round(
        (percentile_value / 100) * (len(sorted_values) - 1)
    )

    return sorted_values[index]

cpu_values = [45, 52, 60, 75, 80, 92, 95, 97, 99]

p95_cpu = percentile(cpu_values, 95)

print("P95 CPU:", p95_cpu)

```

```python
import pandas as pd

records = [
    {"service": "checkout", "cpu": 72, "memory": 68},
    . . .]

df = pd.DataFrame(records)
result = (
    df.groupby("service", as_index=False)
      .agg(
          avg_cpu=("cpu", "mean"),
          p95_cpu=("cpu", lambda x: x.quantile(0.95)),
          avg_memory=("memory", "mean"),
          p95_memory=("memory", lambda x: x.quantile(0.95)),
      )
)
result = result.round(2)
print(result)

```

[Back to TOC](#toc)

## Full Telemetry Mini-Project

This section combines many realistic steps:

- read CSV telemetry
- clean column names
- convert dates
- convert numeric fields
- handle missing or bad data
- calculate headroom
- calculate forecast variance
- aggregate by service
- classify capacity status
- generate stakeholder recommendations

```python
import pandas as pd
from io import StringIO

csv_data = """
date,service,environment,cpu,memory,forecast_cpu,allocated_cpu,cost
2026-01-01,checkout,prod,72,68,70,100,120.50
2026-01-02,checkout,prod,81,74,75,100,125.00
2026-01-03,checkout,prod,92,85,80,100,132.25
2026-01-01,search,prod,45,52,50,100,90.00
2026-01-02,search,prod,91,88,65,100,118.75
2026-01-03,search,prod,78,76,70,100,110.10
2026-01-01,billing,prod,30,35,35,100,80.00
2026-01-02,billing,prod,,38,40,100,82.50
2026-01-03,billing,prod,28,bad_data,38,100,79.25
"""

# 1. Read telemetry CSV.
df = pd.read_csv(StringIO(csv_data))

# 2. Normalize column names.
df.columns = [col.strip().lower() for col in df.columns]

# 3. Convert date column.
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 4. Convert numeric columns safely.
numeric_columns = [
    "cpu",
    "memory",
    "forecast_cpu",
    "allocated_cpu",
    "cost",
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. Fill missing CPU and memory using service-level average.
for col in ["cpu", "memory"]:
    df[col] = (
        df.groupby("service")[col]
          .transform(lambda x: x.fillna(x.mean()))
    )

# 6. Drop records still missing critical fields.
df = df.dropna(
    subset=[
        "date",
        "service",
        "cpu",
        "memory",
        "forecast_cpu",
        "allocated_cpu",
    ]
)

# 7. Calculate row-level capacity features.
df["cpu_headroom"] = df["allocated_cpu"] - df["cpu"]
df["forecast_variance"] = df["cpu"] - df["forecast_cpu"]

df["forecast_variance_pct"] = (
    df["forecast_variance"] / df["forecast_cpu"] * 100
)

# 8. Aggregate by service.
summary = (
    df.groupby("service", as_index=False)
      .agg(
          avg_cpu=("cpu", "mean"),
          p95_cpu=("cpu", lambda x: x.quantile(0.95)),
          avg_memory=("memory", "mean"),
          p95_memory=("memory", lambda x: x.quantile(0.95)),
          avg_headroom=("cpu_headroom", "mean"),
          avg_forecast_variance_pct=("forecast_variance_pct", "mean"),
          total_cost=("cost", "sum"),
      )
)

# 9. Round output for reporting.
summary = summary.round(2)

# 10. Add capacity risk logic.
def classify_capacity_risk(row):
    if row["p95_cpu"] >= 90:
        return "high_capacity_risk"

    if row["avg_headroom"] <= 15:
        return "watch_headroom"

    if row["avg_cpu"] < 35:
        return "rightsizing_candidate"

    return "normal"

summary["capacity_status"] = summary.apply(
    classify_capacity_risk,
    axis=1,
)

# 11. Add business recommendation.
def recommendation(row):
    if row["capacity_status"] == "high_capacity_risk":
        return (
            "Review scaling plan and forecast next quarter demand"
        )
    if row["capacity_status"] == "watch_headroom":
        return (
            "Monitor closely and validate upcoming demand"
        )
    if row["capacity_status"] == "rightsizing_candidate":
        return (
            "Review for underutilization and possible rightsizing"
        )
    return "No immediate action"

summary["recommendation"] = summary.apply(
    recommendation,
    axis=1,
)
print("=== Cleaned Telemetry ===")
print(df)
print("\n=== Capacity Summary By Service ===")
print(summary)
```
