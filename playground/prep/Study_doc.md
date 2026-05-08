[Back to TOC](#toc)
# Module 0

## TOC
- [Module 0](#module-0)
  - [TOC](#toc)
  - [Apple Cloud Capacity Telemetry Coding Workbook](#apple-cloud-capacity-telemetry-coding-workbook)
    - [Key line:](#key-line)
- [Module 1 Coding Techniques](#module-1-coding-techniques)
  - [Basic Grouping with Pandas](#basic-grouping-with-pandas)
    - [Talk while coding:](#talk-while-coding)
  - [Basic Grouping with Pure Python](#basic-grouping-with-pure-python)
  - [Capacity Risk Detection](#capacity-risk-detection)
    - [Talk while coding:](#talk-while-coding-1)
  - [P95 Utilization](#p95-utilization)
  - [Full Telemetry Mini-Project](#full-telemetry-mini-project)
    - [Talk while coding:](#talk-while-coding-2)
  - [AWS service mapping](#aws-service-mapping)
  - [Forecasting Models Talking Point](#forecasting-models-talking-point)
  - [Stakeholder Action Loop](#stakeholder-action-loop)
  - [Final Memorized Answer](#final-memorized-answer)
- [Module 1000000](#module-1000000)
  - [Opener](#opener)
  - [ML Forecasting for Business Impact](#ml-forecasting-for-business-impact)
  - [What is the Job:](#what-is-the-job)
  - [Master Diagram in Words](#master-diagram-in-words)
  - [How do you think about cloud capacity planning?](#how-do-you-think-about-cloud-capacity-planning)
    - [One Liner](#one-liner)
  - [AWS Services One Liners?](#aws-services-one-liners)
    - [EKS (Elastic Kubernetes Service)](#eks-elastic-kubernetes-service)
    - [EC2 (Elastic Compute Cloud)](#ec2-elastic-compute-cloud)
    - [ECS (Elastic Container Service)](#ecs-elastic-container-service)
    - [RDS (Relational Database Service)](#rds-relational-database-service)
    - [S3 (Simple Storage Service)](#s3-simple-storage-service)

## Apple Cloud Capacity Telemetry Coding Workbook

I think about cloud capacity as a data and decision loop. First, collect telemetry and ownership data. Then clean and normalize it. Then calculate utilization, P95, headroom, growth, forecast variance, and rightsizing candidates. Finally, turn that analysis into stakeholder actions: scale, rightsize, approve capacity, change quotas, reduce waste, or update runbooks.

### Key line:

The goal is not a dashboard. The goal is a forecast-driven action loop

[Back to TOC](#toc)

# Module 1 Coding Techniques

[Back to TOC](#toc)

## Basic Grouping with Pandas

Interview problem:

You are given infrastructure usage records.

Each record has:

- service
- CPU
- Memory

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

Identify services that may be capacity risks.

A service is risky if:
- average CPU is above 75
- average memory is above 75

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
### Talk while coding:
> This is a simple rule-based capacity risk screen.

> In production, I would not rely only on average utilization.
> I would add P95, peak usage, forecast trend, headroom, business criticality,
> and upcoming demand.

> But this gives a clean starting point for a capacity-risk list.

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
### Talk while coding:
> This is a simplified version of a real telemetry workflow.
> I start by reading raw capacity data from a CSV or exported telemetry
> source. Then I clean the data: normalize column names, convert dates,
> convert numeric fields, and handle missing or bad values.
> After that, I calculate capacity features such as headroom, P95 utilization,
> and forecast variance.
> Then I aggregate by service because the business conversation is usually
> not about one raw metric. It is about which service, namespace, team,
> or workload needs action.
> Finally, I classify the result into capacity risk, watch, normal,
> or rightsizing candidate. That makes the output usable in a stakeholder
> meeting.

[Back to TOC](#toc)

## AWS service mapping

Use this explanation in the interview:

> In AWS, the same pipeline could read telemetry from CloudWatch,
> Container Insights, Cost Explorer, S3 Inventory, or exported billing data.

> For EKS, I would group by cluster, namespace, workload, and team.
> I would compare requests, limits, actual usage, quotas, and autoscaling.

> For ECS/Fargate, I would compare task CPU and memory allocation
> against actual usage to find over-allocation.

> For EC2, I would review instance utilization, Auto Scaling Group behavior,
> baseline demand, burst behavior, and rightsizing candidates.

> For S3, I would track bucket growth, object count, access pattern,
> storage class, lifecycle opportunity, and cost trend.

Key line:

> The resource layer changes, but the capacity method is the same:
> collect telemetry, attach ownership, calculate features, forecast demand,
> and drive action.

[Back to TOC](#toc)

## Forecasting Models Talking Point

If asked what models you used:

> I usually think about forecasting in three layers.

> First, simple statistical baselines: P95, growth rate, headroom,
> and threshold breach risk. These are explainable and useful in
> stakeholder conversations.

> Second, time-series models like Prophet when the signal has trend
> or seasonality. That helps answer when a service, cluster, namespace,
> or storage bucket may hit a threshold.

> Third, feature-based models with scikit-learn when I need to combine
> multiple signals: utilization trend, peak behavior, requests versus actuals,
> scaling events, quota pressure, cost trend, and ownership metadata.

> In practice, I do not pick the most complex model first. I start with
> explainable features and back-testing, then use more advanced models
> when they improve forecast accuracy.

[Back to TOC](#toc)

## Stakeholder Action Loop

This is what makes the analysis valuable.

The output should not be raw telemetry.

The output should be an action list:

- top capacity risks
- top underutilized resources
- services with low headroom
- large forecast-vs-actual variance
- high-cost services
- over-requested Kubernetes namespaces
- fast-growing S3 buckets
- workloads needing capacity approval
- workloads needing rightsizing review

Interview line:

> The value is not just calculating averages.
> The value is turning messy telemetry into a clean action list:
> capacity risk, forecast miss, rightsizing candidate, or no action.

[Back to TOC](#toc)
##  Final Memorized Answer

Use this as your polished answer:

> My telemetry work starts with messy infrastructure data: service,
> CPU, memory, P95, forecast, allocation, ownership, and cost.

> I clean and normalize that data with Python, Pandas, SQL, or PySpark.
> Then I calculate planning features like P95 utilization, headroom,
> growth rate, forecast variance, and rightsizing indicators.

> From there, I aggregate by service, namespace, cluster, team, or workload,
> because that is how capacity decisions are made.

> The final output is not just a dashboard. It is a stakeholder action list:
> where we have capacity risk, where forecast missed actual demand,
> where we are over-allocated, and where we should rightsize, scale,
> approve capacity, or investigate.














































# Module 1000000

[Back to TOC](#toc)

## Opener

I'm a capacity and efficiency engineer with a background in large-scale

infrastructure planning and forecasting. At Citi, I worked with telemetry across

thousands of endpoints to build Python/SQL forecasting and utilization analysis

that supported planning decisions and risk visibility.

Over time, a growing part of that analytics and processing stack moved into AWS,

where I used services like S3, Glue, Redshift, and EC2/ECS-based processing.

My focus is turning infrastructure data into clear capacity recommendations,

efficiency opportunities, and leadership-ready reporting.

Tell me about a Python automation workflow you built for capacity planning.

At Citi, I built Python automation around infrastructure capacity telemetry.

The problem was that capacity planning was too manual and slow.

Telemetry came from tools like BMC TrueSight/TSCO and other monitoring

systems. The raw data had to be cleaned, normalized, aggregated, and turned

into useful planning reports.

I used Python and Pandas to automate the ETL process. The pipeline pulled

P95 utilization data, cleaned inconsistent records, grouped metrics by

server, application, or service, calculated trends and headroom, and prepared

the output for reporting and forecasting.

The value was that capacity reviews became repeatable. Instead of manually

building spreadsheets, we had a structured workflow that supported forecasting,

risk visibility, and executive reporting..

[Back to TOC](#toc)

## ML Forecasting for Business Impact

Situation: Infrastructure provisioning was reactive — problems were caught too late. Task: Build a system that predicts bottlenecks before they hit. Action: Developed ML forecasting models using Prophet and scikit-learn to predict capacity needs 3–6 months ahead. Fed historical time-series telemetry through the pipeline into the models. Accounted for seasonality and holidays. Back-tested multiple model types per server class. Result: Improved provisioning accuracy significantly. Gave the business ample time to act before bottlenecks materialized. Reduced emergency capacity requests.

[Back to TOC](#toc)

## What is the Job:

The job is a capacity decision loop.

Telemetry comes from AWS, Kubernetes, monitoring tools, cost tools, and CMDB.

Python and SQL transform that telemetry into clean historical features.

Forecasting models project demand, capacity risk, and cost.

Dashboards and stakeholder meetings turn the forecast into action:

approve capacity, rightsize, change quotas, adjust scaling, reduce waste, or update runbooks.

[Back to TOC](#toc)

## Master Diagram in Words

AWS / Kubernetes / Cloud resources

↓

CloudWatch, Container Insights, Cost Explorer, TrueSight, CMDB, tags

↓

Historical feature store

↓

Python + SQL cleanup, aggregation, P95, headroom, growth, variance

↓

Forecasting models

↓

Capacity risk, cost projection, rightsizing candidates

↓

Weekly stakeholder review

↓

Change ticket, capacity approval, quota adjustment, runbook, executive report

[Back to TOC](#toc)

## How do you think about cloud capacity planning?

I think about cloud capacity planning as a data and decision loop.

First, I need visibility into usage, cost, and ownership across services like EKS, ECS, EC2, S3, and databases. Then I normalize that telemetry by service, team, environment, cluster, namespace, or workload.

From there, I use Python and SQL to calculate utilization, P95, headroom, growth rate, forecast vs actual, and rightsizing candidates. Then forecasting models help project where demand, capacity risk, or cost will go over the next quarter.

The final step is stakeholder action. The forecast only matters if it drives a decision: adjust capacity, approve a request, change quotas, rightsize resources, update a runbook, or explain variance to leadership.

### One Liner

The goal is not just a dashboard. The goal is a forecast-driven capacity action loop.

[Back to TOC](#toc)

## AWS Services One Liners?

### EKS (Elastic Kubernetes Service)

A managed service that makes it easy to run Kubernetes on AWS, providing the flexibility of open-source orchestration with the security and reliability of a managed infrastructure.

### EC2 (Elastic Compute Cloud)

This service provides scalable virtual servers, giving you full control over the operating system and networking for your applications.

### ECS (Elastic Container Service)

A highly scalable, high-performance container management service that allows you to run and scale Docker applications without managing a complex orchestration control plane.

### RDS (Relational Database Service)

This service simplifies the setup, operation, and scaling of relational databases like MySQL, PostgreSQL, or SQL Server by automating administrative tasks like backups and patching.

### S3 (Simple Storage Service)

An object storage service built to store and retrieve any amount of data from anywhere on the web, offering industry-leading durability, availability, and scalability.
