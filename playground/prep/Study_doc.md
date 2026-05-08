# Module 1 Interview Question

## TOC
- [Module 1 Interview Question](#module-1-interview-question)
  - [TOC](#toc)
  - [1. Interview Target](#1-interview-target)
  - [2. Core Identity Statement](#2-core-identity-statement)
  - [3. Automation in Cloud Capacity Work](#3-automation-in-cloud-capacity-work)
    - [1. Data Automation](#1-data-automation)
    - [2. Capacity-Risk Automation](#2-capacity-risk-automation)
    - [3. Cloud / Platform Collection Automation](#3-cloud--platform-collection-automation)
    - [4. Reporting / Operational Automation](#4-reporting--operational-automation)
    - [5. Batch First, Streaming Only If Needed](#5-batch-first-streaming-only-if-needed)
    - [6. Lambda vs Container vs Orchestrator](#6-lambda-vs-container-vs-orchestrator)
    - [7. How Automation Maps to Current Code Lab](#7-how-automation-maps-to-current-code-lab)
    - [8. Fire Drill Q\&A](#8-fire-drill-qa)
  - [Cloud Telemetry Collection — Batch First](#cloud-telemetry-collection--batch-first)
    - [AWS Native Sources](#aws-native-sources)
    - [Collector Patterns](#collector-patterns)
    - [Frequency Guidance](#frequency-guidance)
    - [Code Impact](#code-impact)
    - [Interview Answer](#interview-answer)
    - [Fire Drill Questions To Add](#fire-drill-questions-to-add)
  - [4. HorizonScale — Code Walkthrough](#4-horizonscale--code-walkthrough)
  - [5. SQL Coverage](#5-sql-coverage)
  - [6. Python Coverage](#6-python-coverage)
  - [7. Kubernetes / EKS Capacity Concepts](#7-kubernetes--eks-capacity-concepts)
    - [Kubernetes Capacity Granularity](#kubernetes-capacity-granularity)
  - [8. S3 Capacity / Cost Concepts](#8-s3-capacity--cost-concepts)
  - [9. Cost Savings / Efficiency Playbook](#9-cost-savings--efficiency-playbook)
  - [10. Interview Runbook — 45 Minutes](#10-interview-runbook--45-minutes)
  - [11. Interview Runbook — 30 Minutes](#11-interview-runbook--30-minutes)
  - [12. Fire Drill Questions](#12-fire-drill-questions)
  - [13. Questions To Ask Them](#13-questions-to-ask-them)
  - [14. Things To Avoid](#14-things-to-avoid)
  - [15. Final 60-Second Close](#15-final-60-second-close)
- [Module 2 SQL Techniques](#module-2-sql-techniques)
  - [SQL Mental Model](#sql-mental-model)
    - [Interview sentence:](#interview-sentence)
  - [Basic SELECT and WHERE](#basic-select-and-where)
  - [JOIN Pattern](#join-pattern)
    - [Interview sentence:](#interview-sentence-1)
  - [GROUP BY Pattern](#group-by-pattern)
  - [DATE\_TRUNC Time Buckets](#date_trunc-time-buckets)
    - [Interview sentence](#interview-sentence-2)
  - [P95 with PERCENTILE\_CONT](#p95-with-percentile_cont)
    - [Interview sentence](#interview-sentence-3)
  - [CTE Pattern](#cte-pattern)
    - [Interview sentence](#interview-sentence-4)
  - [Window Functions Mental Model](#window-functions-mental-model)
    - [Example: compare each telemetry sample to the previous sample](#example-compare-each-telemetry-sample-to-the-previous-sample)
  - [ROW\_NUMBER / RANK / DENSE\_RANK](#row_number--rank--dense_rank)
    - [Plain English](#plain-english)
    - [Interview sentence](#interview-sentence-5)
  - [LAG / LEAD](#lag--lead)
    - [Interview sentence](#interview-sentence-6)
  - [Moving Average](#moving-average)
    - [Interview sentence](#interview-sentence-7)
  - [JSONB Tags](#jsonb-tags)
    - [Interview sentence](#interview-sentence-8)
  - [Risky Windows Query](#risky-windows-query)
    - [Interview sentence](#interview-sentence-9)
  - [Rightsizing / Over-Allocation Query](#rightsizing--over-allocation-query)
    - [Interview sentence](#interview-sentence-10)
  - [Cost Rollup](#cost-rollup)
    - [Interview sentence](#interview-sentence-11)
  - [Before/After Deployment Comparison](#beforeafter-deployment-comparison)
    - [Interview sentence](#interview-sentence-12)
  - [SQL to Pandas Translation](#sql-to-pandas-translation)
  - [Fire Drill Q\&A](#fire-drill-qa)
  - [Final Memorized SQL Answer](#final-memorized-sql-answer)
- [Module 3 Python Coding Techniques](#module-3-python-coding-techniques)
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
- [Module 4 ML - Forecast \_ HorizonScale](#module-4-ml---forecast-_-horizonscale)
  - [The story in one paragraph](#the-story-in-one-paragraph)
  - [1. Purpose](#1-purpose)
  - [2. Safe Positioning](#2-safe-positioning)
  - [3. Business Problem](#3-business-problem)
  - [4. Inputs and Features](#4-inputs-and-features)
  - [5. Pipeline Flow](#5-pipeline-flow)
  - [6. Model Framing](#6-model-framing)
    - [Prophet](#prophet)
    - [scikit-learn](#scikit-learn)
    - [ARIMA / SARIMA](#arima--sarima)
    - [XGBoost / LightGBM](#xgboost--lightgbm)
    - [Explainable baselines](#explainable-baselines)
  - [7. Validation Approach](#7-validation-approach)
  - [8. Capacity and Cost Impact](#8-capacity-and-cost-impact)
  - [9. What To Say (20 seconds)](#9-what-to-say-20-seconds)
  - [10. What To Say (60 seconds)](#10-what-to-say-60-seconds)
  - [11. What Not To Overclaim](#11-what-not-to-overclaim)
  - [12. Rapid Q\&A](#12-rapid-qa)
- [Module 5 Cheat sheet](#module-5-cheat-sheet)
  - [Automation types](#automation-types)
  - [Batch vs streaming](#batch-vs-streaming)
  - [Lambda vs container](#lambda-vs-container)
  - [df.copy()](#dfcopy)
  - [groupby().agg() named aggregation](#groupbyagg-named-aggregation)
  - [as\_index=False](#as_indexfalse)
  - [reset\_index(drop=True)](#reset_indexdroptrue)
  - [apply(axis=1)](#applyaxis1)
  - [JSONB tags](#jsonb-tags-1)
  - [Pandas P95](#pandas-p95)
  - [SQL DATE\_TRUNC](#sql-date_trunc)
  - [SQL PERCENTILE\_CONT](#sql-percentile_cont)
  - [Kubernetes granularity](#kubernetes-granularity)
  - [HorizonScale models](#horizonscale-models)
  - [HorizonScale validation](#horizonscale-validation)
- [Module 6 Odds and repeats](#module-6-odds-and-repeats)
  - [Opener](#opener)
  - [Tell me about a Python automation workflow you built for capacity planning.](#tell-me-about-a-python-automation-workflow-you-built-for-capacity-planning)
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
    - [Glue](#glue)
    - [Redshift](#redshift)
    - [One-liner mental model](#one-liner-mental-model)



## 1. Interview Target

This is not just a SQL role and not just a Python role. It is a capacity,
efficiency, telemetry, automation, and cloud-cost role.

Sean's safest positioning:
Senior capacity/data engineer who automates telemetry analysis into capacity and
cost decisions.

[Back to TOC](#toc)

## 2. Core Identity Statement

I am strongest where capacity engineering meets data engineering. I use Python,
SQL, telemetry, and forecasting to turn infrastructure metrics into capacity
risk, rightsizing opportunities, and stakeholder-ready reports. My deepest
hands-on cloud is AWS, and I understand how the same capacity principles apply
to Kubernetes, EKS, S3, and multi-cloud environments.

[Back to TOC](#toc)

## 3. Automation in Cloud Capacity Work
Automation in this role does not mean only one thing. It can mean data
automation, capacity-risk automation, cloud/platform collection automation, and
reporting/operational automation. The common goal is reducing manual capacity
analysis and turning telemetry into repeatable decisions.

### 1. Data Automation

- collect telemetry
- ingest CSV/Excel exports
- pull from databases or APIs
- normalize column names
- convert dates and numeric fields
- join service ownership, tags, environment, team, account, region, namespace,
  or workload metadata
- produce reusable clean datasets

Interview answer:
Data automation means I do not want analysts manually cleaning the same
telemetry export every time. I would automate the ingestion, cleaning, schema
normalization, ownership tagging, and validation so downstream capacity
calculations are repeatable.

### 2. Capacity-Risk Automation

- calculate AVG / MAX / P95
- calculate headroom
- compare allocated/requested capacity vs actual usage
- detect threshold breaches
- calculate forecast variance
- classify services/workloads as high_capacity_risk, latency_watch,
  rightsizing_candidate, or normal
- generate top-risk or top-waste lists

Interview answer:
Capacity automation means turning raw metrics into decision flags. For example,
the workflow can automatically calculate P95 utilization, headroom, forecast
variance, and cost impact, then classify services or workloads into risk or
rightsizing categories.

### 3. Cloud / Platform Collection Automation

AWS-native or platform sources may include:
- CloudWatch / Container Insights for compute, container, EKS/ECS, pod, node,
  and cluster metrics
- AWS Cost and Usage Report for cost and usage data delivered to S3
- S3 Inventory for bucket/object/storage metadata
- tags and ownership metadata
- centralized collectors such as BMC TrueSight, TSCO, Helix, or similar
  observability/capacity platforms

At Citi, centralized tools such as BMC TrueSight/TSCO/Helix could discover
resources and populate metrics after configuration. Once the resources were
onboarded, the analytics problem became similar to other endpoints: different
columns and rules, but the same pattern of collect, normalize, analyze, and
report.

Interview answer:
If a company already has a centralized platform like BMC/Helix or
CloudWatch/Container Insights, I would use that as the telemetry source where
appropriate. If not, I would use scheduled jobs or native exports. The analysis
pattern is the same: collect the data, normalize it, join ownership metadata,
calculate risk or waste, and report.

### 4. Reporting / Operational Automation

- scheduled scripts
- scheduled Lambda
- scheduled container jobs
- Airflow / Step Functions / batch orchestration
- CSV / Markdown / dashboard exports
- validation checks
- runbook updates
- reducing manual spreadsheet/reporting work

Interview answer:
Reporting automation means the output is not a one-time spreadsheet. The
workflow should create repeatable CSV, Markdown, dashboard, or table outputs
that stakeholders can review consistently.

### 5. Batch First, Streaming Only If Needed

For capacity and cost analytics, batch is usually the default. Streaming is
useful for real-time alerting, but most capacity planning, rightsizing,
forecasting, and cost analysis works from periodic snapshots.

Frequency guidance:
- 1–5 minutes: operational monitoring or alerting
- 5–15 minutes: infrastructure or service telemetry samples
- hourly: capacity rollups and workload pressure trends
- daily: cost usage, rightsizing candidates, S3 inventory, stakeholder reports
- weekly/monthly: forecasting, budget planning, commitment planning, executive
  review

Interview answer:
For capacity and cost analytics, I usually think batch first. We normally do
not need streaming unless the use case is real-time alerting. For planning and
efficiency, periodic snapshots are enough: 5-minute or hourly telemetry, daily
cost files, and scheduled inventory exports.

### 6. Lambda vs Container vs Orchestrator

- Lambda is good for lightweight scheduled pulls or small enrichment jobs.
- A scheduled container job is better for heavier dependencies, larger
  extracts, or longer processing.
- Airflow / Step Functions / batch orchestration is better for multi-step
  workflows: extract, validate, load, transform, report.
- Centralized tools like BMC/Helix/CloudWatch may already handle collection, so
  the automation focus becomes downstream processing and reporting.

Interview answer:
I would choose the automation mechanism based on the workload. Lambda is good
for lightweight scheduled pulls. A container job is better for heavier
dependencies or larger extracts. An orchestrator is better when the workflow
has multiple stages. If a centralized collector already exists, I would use it
and focus automation on validation, transformation, risk classification, and
reporting.

### 7. How Automation Maps to Current Code Lab

- src\db.py handles database connection and query execution
- src\telemetry_queries.py centralizes reusable SELECT queries
- src\capacity_analysis.py calculates flags, summaries, and capacity status
- src\reporting.py exports CSV/Markdown outputs
- scripts\04_export_capacity_summary.py runs the end-to-end workflow
- tests validate connection, SELECT-only safety, and Pandas logic

Answer:
In my lab, the Python side demonstrates the automation pattern. It connects to
PostgreSQL, runs SELECT-only telemetry queries, loads results into Pandas,
calculates capacity summaries and status labels, exports CSV/Markdown reports,
and validates the logic with pytest. In a real environment, the input source
could be BMC/Helix, CloudWatch, CUR, S3 Inventory, or a staging table.

### 8. Fire Drill Q&A

Q: What do you mean by automation?
A: Reducing manual capacity analysis. Automating data collection, cleaning,
P95/headroom/forecast variance calculations, risk classification, and
stakeholder-ready reporting.

Q: Do you need streaming for capacity and cost analytics?
A: Usually no. Capacity planning and cost efficiency usually work from periodic
snapshots, hourly/daily rollups, and historical trends. Streaming is more
useful for alerting.

Q: How would you collect AWS cost data?
A: I would start with AWS Cost and Usage Reports delivered to S3, then process
them with SQL, Python, or Spark and join to tags, accounts, services, and
ownership metadata.

Q: How would you collect EKS metrics?
A: I would use CloudWatch Container Insights or an existing
observability/capacity platform. I would focus on namespace, workload, pod,
node, requests, limits, actual usage, and cost allocation.

Q: How would you collect S3 capacity data?
A: I would use S3 Inventory, cost/usage data, and bucket metadata to analyze
storage growth, object count, storage class, lifecycle opportunity, access
pattern, and cost trend.

Q: Lambda or container for collection?
A: Lambda is good for lightweight scheduled pulls. A container job is better
for heavier dependencies, larger extracts, or longer runtime. An orchestrator
is better for multi-step workflows.

Q: What if the company already has BMC/Helix?
A: Then I would use it as the central telemetry source when appropriate. Once
resources and metrics are onboarded, the analytics pattern is similar to other
endpoints: extract, normalize, join ownership, calculate risk/waste, and
report.

Q: How does this connect to your older physical/virtualization background?
A: The resource model changes, but the capacity method is the same. Physical/VM
work uses servers, VMs, CPU, memory, disk, and endpoint telemetry. Cloud adds
account, region, tags, resource type, requests/limits, storage class, and cost.
The pipeline remains collect, normalize, calculate, classify, and report.

[Back to TOC](#toc)

## Cloud Telemetry Collection — Batch First

For capacity and cost analytics, batch is usually the default. We normally do
not need streaming for capacity planning unless there is an operational
alerting use case. Capacity analysis usually works from periodic snapshots:
5-minute samples, hourly rollups, daily cost files, monthly trends, or
scheduled inventory exports.

### AWS Native Sources

- CloudWatch / Container Insights:
  collects compute, ECS, EKS, Kubernetes, container, pod, node, and cluster
  metrics depending on setup.

- AWS Cost and Usage Report:
  publishes detailed cost and usage data to S3, usually used for cost
  allocation, showback, rightsizing analysis, forecasting, and tag-based
  reporting.

- S3 Inventory:
  produces scheduled reports about S3 objects and metadata, useful for storage
  growth, lifecycle policy analysis, storage class review, and cold-data
  identification.

- Tags / ownership metadata:
  account, region, environment, team, application, service, namespace,
  workload.

### Collector Patterns

1. Centralized platform collector:
Examples: BMC TrueSight, TSCO, Helix, CloudWatch, Container Insights.
Once configured, resources are discovered and metrics are populated centrally.
The analytics code consumes these resources like any other endpoint.

2. Scheduled Lambda:
Good for small periodic API pulls or lightweight enrichment.
Could run hourly or daily depending on need.

3. Scheduled container job:
Good for heavier collectors, more dependencies, larger extracts, or jobs that
need more runtime than Lambda.

4. Airflow / Step Functions / batch orchestration:
Good when the process has multiple stages: extract, validate, load, transform,
report.

5. Direct export files:
CSV/Excel exports from BMC/Helix/TSCO or AWS reports. Read with Pandas for
quick analysis, or load to staging tables for repeatable pipelines.

### Frequency Guidance

- 1–5 minutes:
  alerting or operational monitoring, not usually required for planning reports.

- 5–15 minutes:
  service or infrastructure telemetry sampling.

- Hourly:
  capacity rollups, trend tracking, workload pressure checks.

- Daily:
  cost and usage analysis, S3 inventory, rightsizing candidates, stakeholder
  reports.

- Weekly/monthly:
  forecasting, budget planning, commitment planning, executive review.

### Code Impact

The code pattern does not radically change when moving from physical/VM
telemetry to cloud telemetry. The input schema changes.

Physical/VM columns:
server_id, hostname, cpu_utilization_pct, memory_utilization_pct,
disk_utilization_pct, sampled_at.

Cloud columns:
account_id, region, resource_id, resource_type, service_name, tag_team,
tag_env, cost_usd, usage_quantity.

EKS/Kubernetes columns:
cluster_name, namespace, workload_name, pod_name, container_name, cpu_request,
cpu_limit, cpu_usage, memory_request, memory_limit, memory_usage.

S3 columns:
bucket_name, storage_class, object_count, storage_gb, last_accessed_days,
monthly_cost_usd, lifecycle_policy_status.

The same code idea remains:
read data -> normalize columns -> join ownership/tags -> calculate
utilization/headroom/P95/variance/cost -> classify risk or waste -> export
report.

### Interview Answer

For capacity and cost analytics, I usually think batch first. We normally do not need streaming unless the use case is real-time alerting. For planning and efficiency, periodic snapshots are enough: 5-minute or hourly telemetry, daily cost files, and scheduled inventory exports.

In AWS, I would use native sources where possible: CloudWatch and Container Insights for compute/container metrics, Cost and Usage Reports for cost and usage data in S3, and S3 Inventory for storage/object metadata. If enrichment is needed, I would use a scheduled Lambda for lightweight jobs, a scheduled container for heavier collectors, or an orchestrated batch workflow for multi-step pipelines.

At Citi, the same pattern existed through centralized tools like BMC TrueSight/TSCO and later Helix. Once configured, the system discovered resources and populated metrics. From the analytics side, it became the same problem: different columns and rules, but the same decision loop — collect, normalize, calculate headroom/P95/variance/cost, classify risk or waste, and report.

### Fire Drill Questions To Add

Q: Do you need streaming for cloud capacity analysis?
A: Usually no. Capacity planning is normally batch-oriented. Streaming is useful
for alerting, but planning and efficiency usually work from periodic snapshots,
hourly/daily rollups, and historical trends.

Q: How would you collect AWS cost data?
A: I would start with AWS Cost and Usage Reports delivered to S3, then process
them with SQL/Python/Spark depending on scale. I would join cost data to tags,
accounts, services, and ownership metadata.

Q: How would you collect EKS metrics?
A: I would use CloudWatch Container Insights or an existing observability
platform if already configured. I would focus on namespace, workload, pod,
node, requests, limits, actual usage, and cost allocation.

Q: How would you collect S3 capacity data?
A: I would use S3 Inventory or cost/usage exports to analyze bucket growth,
object count, storage class, lifecycle opportunity, and cost trend.

Q: What if the company already has BMC/Helix?
A: Then I would use it as the central telemetry source when appropriate. Once
resources and metrics are onboarded, the analytics pattern is similar to other
endpoints: extract the data, normalize it, join ownership, calculate risk or
waste, and report.

Q: Lambda or container for collection?
A: Lambda is good for lightweight scheduled pulls. A container job is better for
heavier dependencies, longer runtime, larger data extracts, or more complex
processing.

[Back to TOC](#toc)

## 4. HorizonScale — Code Walkthrough

- Inputs:
  CPU, memory, P95 latency/utilization, requests, forecast, allocated capacity,
  actual usage, cost, ownership/service metadata.

- Code flow:
  1. read telemetry
  2. clean/normalize
  3. convert date/numeric fields
  4. calculate headroom
  5. calculate P95
  6. calculate forecast variance
  7. group by service/workload
  8. classify status
  9. export report/action list

- Outputs:
  capacity risk list
  rightsizing candidates
  forecast misses
  cost/efficiency report
  stakeholder summary

The code side of HorizonScale was a telemetry-to-decision pipeline. I pulled
infrastructure metrics, cleaned and normalized the data, calculated features
like P95 utilization, headroom, forecast variance, and utilization trends, then
grouped by service or workload to classify capacity risk and rightsizing
opportunities. The value was the repeatable decision loop, not just one
dashboard.

[Back to TOC](#toc)

## 5. SQL Coverage

- 01 basic selects:
  table inspection, filtering, simple joins
- 02 joins/group by:
  service/host readable telemetry, grouped summaries
- 03 capacity aggregation:
  AVG, MAX, P95, DATE_TRUNC, cost and risk rollups
- 04 window functions:
  ROW_NUMBER, RANK, LAG, LEAD, moving averages
- 05 interview questions:
  mixed SQL problem solving
- 06 server rollup:
  5-minute samples to hourly capacity rollups, CTEs, JSONB, P95, LAG/RANK

In SQL, I can move from raw telemetry samples to service-level capacity views
using JOIN, GROUP BY, DATE_TRUNC, P95 calculations, CTEs, and window functions.

[Back to TOC](#toc)

## 6. Python Coverage

- db connection helper
- SELECT-only query layer
- Pandas capacity analysis
- status classification
- CSV/Markdown report export
- pytest validation

In Python, I built a small layer over PostgreSQL that runs telemetry queries,
loads results into Pandas, calculates flags and service summaries, classifies
capacity status, exports reports, and validates the logic with pytest.

[Back to TOC](#toc)

## 7. Kubernetes / EKS Capacity Concepts

Conceptually prepared, without claiming deep production platform ownership:
- pods
- nodes
- namespaces
- requests
- limits
- actual usage
- over-requesting
- underutilization
- autoscaling
- bin packing
- cluster headroom
- noisy workload
- cost allocation by namespace/team

### Kubernetes Capacity Granularity

Kubernetes capacity should not be analyzed only at the cluster level. It should
be analyzed at multiple grains, because each grain answers a different
question.

Container level:
Best for exact rightsizing.
Question: Is this container requesting too much or too little CPU/memory?

Pod/workload level:
Best for application capacity.
Question: Is this deployment, job, or service sized correctly?

Namespace/team level:
Best for ownership, showback, and cost allocation.
Question: Which team or namespace is consuming or wasting capacity?

Node/cluster level:
Best for infrastructure capacity.
Question: Does the cluster have enough headroom? Are nodes underused or
saturated? Is autoscaling pressure caused by real usage or inflated requests?

Kubernetes is elastic, but elasticity does not remove the need for rightsizing.
Inflated requests can waste money and reduce bin-packing efficiency.
Underestimated requests or usage close to limits can create throttling, OOM
risk, or reliability issues.

CPU request utilization = cpu_usage_cores / cpu_request_cores * 100
Memory request utilization = memory_usage_gb / memory_request_gb * 100
CPU request waste = cpu_request_cores - cpu_usage_cores
Memory request waste = memory_request_gb - memory_usage_gb

I would not calculate Kubernetes capacity only at the cluster level. I would
look at multiple grains. Container and workload level are best for rightsizing
because that is where requests, limits, and actual usage can be compared.
Namespace and team level are best for ownership and cost reporting. Cluster
level is best for total headroom, node utilization, autoscaling pressure, and
bin-packing efficiency. Kubernetes is elastic, but inflated requests can still
waste money and hurt bin packing, while usage close to limits can create
reliability risk.

For EKS or Kubernetes capacity, I would look at requested CPU/memory versus
actual usage, namespace and workload ownership, pod and node utilization,
autoscaling behavior, and cluster headroom. The same data method applies:
collect metrics, group by workload or namespace, calculate P95 and headroom,
identify over-requesting or saturation, and turn it into scaling or rightsizing
recommendations.

[Back to TOC](#toc)

## 8. S3 Capacity / Cost Concepts

- storage growth
- bucket/object count
- storage class
- lifecycle policies
- access patterns
- old/cold data
- replication
- data transfer
- cost trend

For S3, capacity and efficiency are less about CPU and more about storage
growth, access pattern, lifecycle opportunity, storage class, replication, and
data transfer cost. I would look for fast-growing buckets, rarely accessed
objects, missing lifecycle policies, and ownership/tagging gaps so teams can
reduce waste without risking availability.

[Back to TOC](#toc)

## 9. Cost Savings / Efficiency Playbook

1. Find waste
2. Validate with telemetry
3. Attach ownership
4. Estimate impact
5. Recommend action
6. Track result

Examples:
- underutilized compute
- over-requested Kubernetes workloads
- oversized memory allocation
- cold S3 data without lifecycle
- idle or low-traffic services
- high-cost services with low usage
- forecast over-allocation

I do not start by randomly cutting resources. I start with telemetry and
ownership. I look for low utilization, low headroom risk, over-allocation, or
storage lifecycle opportunities. Then I validate with service owners and turn
the finding into a safe action: rightsize, scale down, add lifecycle policy,
rebalance, or monitor.

[Back to TOC](#toc)

## 10. Interview Runbook — 45 Minutes

- 0-5 minutes: opening and background
- 5-15 minutes: capacity/telemetry story
- 15-25 minutes: automation and HorizonScale code
- 25-35 minutes: SQL/Python/cloud capacity discussion
- 35-42 minutes: Kubernetes/EKS/S3/cost efficiency questions
- 42-45 minutes: questions for them and close

[Back to TOC](#toc)

## 11. Interview Runbook — 30 Minutes

- 0-3 opening
- 3-10 strongest capacity story
- 10-18 technical drill
- 18-25 cloud/cost/automation discussion
- 25-30 questions and close

[Back to TOC](#toc)

## 12. Fire Drill Questions

1. What do you mean by automation?
- I mean replacing manual telemetry pulls and one-off spreadsheets with
  repeatable scripts/pipelines that generate decision-ready outputs.

2. How did HorizonScale work in code?
- Pull telemetry, clean/normalize, compute P95/headroom/variance, classify risk,
  group by service/workload, export recommendations.

3. How do you calculate capacity risk?
- Combine utilization, latency, error rates, headroom, and forecast variance;
  then rank by severity and ownership.

4. Why P95 instead of average?
- Average hides stress behavior. P95 better reflects sustained high pressure and
  user-impact risk.

5. How would you analyze EKS cost?
- Compare requested vs actual CPU/memory by namespace/workload, evaluate
  over-requesting, autoscaling behavior, and ownership mapping.

6. How would you analyze S3 cost?
- Track growth, access pattern, storage class, lifecycle gaps, replication, and
  transfer costs; then prioritize safe optimization actions.

7. How do you find rightsizing candidates?
- Identify sustained low utilization with safe headroom, validate with owners,
  and recommend phased changes.

8. What did you actually build in Python?
- A DB query layer, pandas analysis/flags, service summarization, status
  classification, CSV/Markdown exports, and pytest validation.

9. What SQL would you use for telemetry rollups?
- JOIN + GROUP BY + DATE_TRUNC + percentile functions + CTEs/window functions
  when needed for ranking or trend comparison.

10. What if you do not have deep GCP?
- My hands-on depth is strongest in AWS. I apply transferable capacity methods
  across cloud platforms without over-claiming ownership.

11. How do you validate forecasts?
- Back-testing, forecast-vs-actual comparison, variance analysis, and SME review
  of false positives/negatives.

12. How do you communicate risk to stakeholders?
- Translate metrics into risk, impact, owner, recommended action, and expected
  timeline.

13. What would you automate first in this role?
- A repeatable telemetry-to-risk pipeline with ownership tagging and recurring
  service-level rollups.

14. How do you avoid unsafe cost cuts?
- Require utilization/headroom evidence, owner signoff, phased rollout, and
  post-change validation.

15. How do you handle missing or messy telemetry?
- Document gaps, normalize what is available, add validation checks, and build
  a prioritized telemetry quality backlog.

Q: Do you calculate Kubernetes capacity only at the cluster level?
A: No. I look at multiple grains. Container/workload level is best for
rightsizing, namespace/team level is best for ownership and cost, and cluster
level is best for headroom, autoscaling pressure, and bin-packing efficiency.

Q: Why does container-level data matter if Kubernetes is elastic?
A: Because autoscaling still depends on requests, limits, and actual usage. If
requests are inflated, the cluster may scale unnecessarily or pack workloads
inefficiently. If usage is close to limits, the workload may throttle or become
unstable.

[Back to TOC](#toc)

## 13. Questions To Ask Them

- What are the main capacity signals your team trusts today?
- Are the biggest efficiency opportunities in compute, Kubernetes, storage, or
  data transfer?
- How do you currently connect telemetry to ownership and cost?
- What automation exists today, and where is the manual pain?
- How do you measure success for this role in the first 90 days?

[Back to TOC](#toc)

## 14. Things To Avoid

- Do not claim deep Kubernetes production ownership.
- Do not claim deep GCP production ownership.
- Do not say it was only physical infrastructure.
- Do not say HorizonScale was just a dashboard.
- Do not imply finance ownership of billing systems.
- Do not over-focus on old APM unless tying it to telemetry/capacity.

[Back to TOC](#toc)

## 15. Final 60-Second Close

My strongest match is capacity planning at scale with automation. I have worked
with large infrastructure telemetry, Python, SQL, forecasting, and cloud-style
data pipelines to turn raw metrics into risk, rightsizing, and planning
recommendations. My deepest hands-on cloud is AWS, and I am careful to separate
platform ownership from transferable capacity principles. What I bring is the
ability to automate the decision loop: collect telemetry, calculate utilization
and headroom, identify risk or waste, and produce recommendations that
engineering and leadership can act on.

[Back to TOC](#toc)

# Module 2 SQL Techniques

[Back to TOC](#toc)

## SQL Mental Model
- `telemetry_samples` is the fact table.
- `services` and `hosts` are lookup/dimension tables.
- Most capacity questions become joins + aggregations + time buckets.
- SQL turns raw samples into operational summaries.

### Interview sentence:
I think of telemetry SQL as moving from raw event or sample rows into service, host, time-bucket, and ownership summaries.

[Back to TOC](#toc)

## Basic SELECT and WHERE
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
LIMIT 10;
```

[Back to TOC](#toc)

## JOIN Pattern

- `telemetry_samples` has `service_id` and `host_id`.
- `services` and `hosts` make IDs readable.
- `JOIN` without `LEFT/RIGHT` means `INNER JOIN`.

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

Breakdown:
- `PERCENTILE_CONT(0.95)` = 95th percentile
- `WITHIN GROUP (ORDER BY ...)` = values used for percentile
- `::NUMERIC` = cast so rounding works cleanly
- `ROUND(..., 2)` = 2 decimals
- `AS p95_cpu_pct` = readable output name

Latency nuance:
If `p95_latency_ms` is already a sampled P95 metric, then hourly P95 over that column is P95 of sampled P95 values, not raw request-level P95.

### Interview sentence
Average shows normal usage, max shows worst spike, and P95 shows sustained high pressure while reducing one-off noise.

[Back to TOC](#toc)

## CTE Pattern
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

### Interview sentence
I use CTEs to make complex telemetry questions readable: first calculate the rollup, then filter or rank the result.

[Back to TOC](#toc)

## Window Functions Mental Model

- `GROUP BY` collapses rows.
- Window functions keep rows visible and add analytics beside each row.
- `OVER()` defines the window.
- `PARTITION BY` defines groups.
- `ORDER BY` defines order inside each group.

Interview sentence:

Window functions are useful when I need row-level telemetry plus context like rank, previous value, moving average, or running total.

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

- `ROW_NUMBER()` gives every row a unique sequence number.
- `RANK()` gives tied rows the same rank, but may skip the next number.
- `DENSE_RANK()` gives tied rows the same rank, without skipping numbers.

Layman explanation:

Think about three services with CPU values:

```text
service_a = 95
service_b = 95
service_c = 90
```

With `ROW_NUMBER()`:

```text
service_a = 1
service_b = 2
service_c = 3
```

Every row gets a unique number. No sharing.

With `RANK()`:

```text
service_a = 1
service_b = 1
service_c = 3
```

The first two services tie for first place, so the next service is ranked third.

With `DENSE_RANK()`:

```text
service_a = 1
service_b = 1
service_c = 2
```

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

## Risky Windows Query
Pattern:
- Build hourly rollup in a CTE.
- Use P95 + threshold filters.
- Return risky service/time windows.

Common filters:
- `p95_cpu_pct >= 85`
- `p95_memory_pct >= 85`
- `p95_of_sampled_p95_latency_ms >= threshold`
- `avg_error_rate_pct >= threshold`

### Interview sentence
This turns raw telemetry into an action list of risky hours and services.

[Back to TOC](#toc)

## Rightsizing / Over-Allocation Query
Compare allocated vs actual:
- `allocated_cpu_cores`
- `actual_cpu_cores`
- `unused_cpu_cores`
- `allocated_memory_gb`
- `actual_memory_gb`
- `unused_memory_gb`

### Interview sentence
Rightsizing starts by comparing allocated capacity to actual usage, then validating with ownership and business context before reducing resources.

[Back to TOC](#toc)

## Cost Rollup
- Use `SUM(cloud_cost_usd)` if cost is incremental per sample.
- Use `AVG`/`MAX` if cost is a snapshot field.
- Group by service/team/region based on question.

### Interview sentence
For cost analysis, I first clarify whether the cost column is incremental or snapshot-based, because that determines whether SUM or AVG/MAX is correct.

[Back to TOC](#toc)

## Before/After Deployment Comparison
Pattern (supported in `sql/05_interview_questions.sql`):
- join deployments to telemetry/service data
- use time windows around `deployed_at`
- calculate before vs after averages
- often implemented with `FILTER` or `CASE`

### Interview sentence
A before/after deployment query helps check whether a release changed latency, errors, or utilization.

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

## Final Memorized Answer

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

[Back to TOC](#toc)

# Module 4 ML - Forecast _ HorizonScale

[Back to TOC](#toc)

## The story in one paragraph

**Walk-forward validation for telemetry forecasting:** Given 24 months of telemetry, I would train each candidate model on the first 18 months, then evaluate against the held-out final 6 months using error metrics such as MAE, RMSE, and MAPE per service or resource series. Different services behave differently — some are spiky, some are smooth, some are seasonal, and some are trending — so no single model wins universally. I would score each model per series and select the best-fit champion model for that series. Once the champion is selected, I would retrain it on the full 24 months to capture the most recent signal, then produce the next 6-month forecast. The output feeds directly into capacity decisions: headroom runway, rightsizing windows, quota planning, and budget planning cycles.

Candidate models could include Prophet for trend/seasonality, ARIMA/SARIMA for classical time-series baselines, and feature-based scikit-learn models using lag and rolling-window features. The point is not to force one model everywhere, but to back-test candidates and choose the best practical model per telemetry series.

[Back to TOC](#toc)

## 1. Purpose
This guide is a fast interview talk track for HorizonScale forecasting work:
- what problem it solved
- what telemetry was used
- how data was processed
- which model types were used and why
- how outputs supported capacity and efficiency decisions

[Back to TOC](#toc)

## 2. Safe Positioning
Based on the files inspected, I would position HorizonScale as a practical telemetry-to-forecast pipeline focused on capacity planning decisions, not deep research ML.

[Back to TOC](#toc)

## 3. Business Problem
Manual capacity analysis is slow and reactive. Teams need earlier visibility into:
- likely bottlenecks
- sustained utilization pressure
- underutilized resources
- forecast variance versus actuals

[Back to TOC](#toc)

## 4. Inputs and Features
Typical telemetry inputs discussed in this prep:
- sampled_at / timestamp
- service or host identifiers
- CPU utilization
- memory utilization
- sampled P95 latency
- request and error context
- allocated versus actual resource context
- cost fields and ownership tags where available

Common engineered features:
- AVG / MAX / P95 utilization
- headroom
- growth trend
- seasonal patterns
- forecast variance
- threshold breach indicators

[Back to TOC](#toc)

## 5. Pipeline Flow
1. Read telemetry
2. Clean and normalize schema
3. Convert timestamp and numeric types
4. Aggregate by service/workload and time bucket
5. Create forecast features
6. Run model(s)
7. Compare with actuals and thresholds
8. Classify risk/waste
9. Export stakeholder-ready outputs

[Back to TOC](#toc)

## 6. Model Framing
### Prophet
Good for trend and seasonality in time-series behavior.

### scikit-learn
Useful for feature-driven prediction/risk scoring and complementary model checks.

### ARIMA / SARIMA
Univariate, stationary-ish series

### XGBoost / LightGBM
Lag features + covariates, tabular ML style

### Explainable baselines
Threshold and headroom logic are critical for trust with engineering and leadership.

[Back to TOC](#toc)

## 7. Validation Approach
Practical validation approach:
- back-test on historical windows
- compare forecasted pressure with later actuals
- review false positives and false negatives
- keep models explainable for decision support

[Back to TOC](#toc)

## 8. Capacity and Cost Impact
Forecasting supports better decisions by:
- preventing reactive over-provisioning
- finding rightsizing candidates
- highlighting sustained pressure earlier
- improving forecast-vs-actual planning loops

[Back to TOC](#toc)

## 9. What To Say (20 seconds)
HorizonScale was a telemetry-driven capacity forecasting pipeline. I cleaned and aggregated utilization data, generated forecast features, used practical forecasting methods, and turned outputs into risk and planning recommendations.

[Back to TOC](#toc)

## 10. What To Say (60 seconds)
I used HorizonScale to move from raw telemetry to repeatable planning outputs. The workflow cleaned and normalized time-series data, calculated features like P95 and headroom, ran forecasting methods, and compared output against thresholds and actual behavior. The point was not model complexity by itself; it was giving teams earlier, explainable signals for capacity risk, rightsizing, and cost-aware planning.

[Back to TOC](#toc)

## 11. What Not To Overclaim
- Do not claim deep research ML ownership.
- Do not claim perfect model accuracy.
- Do not claim deep GCP production ownership.
- Do not claim deep Kubernetes platform-admin ownership.
- Do not claim enterprise-wide production scope unless Sean confirms.

[Back to TOC](#toc)

## 12. Rapid Q&A
Q: Why Prophet?
A: Trend/seasonality handling and explainable time-series forecasting.

Q: Why scikit-learn?
A: Feature-driven predictive checks and practical risk scoring support.

Q: How did this support cost decisions?
A: By surfacing underutilization and over-pressure early so teams can rightsize safely.

Q: Batch or streaming?
A: Usually batch-first for planning and efficiency; streaming mainly for alerting.

[Back to TOC](#toc)

# Module 5 Cheat sheet

[Back to TOC](#toc)

## Automation types

Question:
What do you mean by automation in cloud capacity work?

Answer:
Automation means reducing manual capacity analysis. It includes data automation,
capacity-risk automation, cloud/platform collection automation, and reporting
automation. The workflow is collect telemetry, normalize it, join ownership
metadata, calculate P95/headroom/forecast variance/cost, classify risk or
waste, and export action-ready reports.

[Back to TOC](#toc)

## Batch vs streaming

Question:
Do you need streaming for capacity and cost analytics?

Answer:
Usually no. Capacity planning and cost efficiency usually work from periodic
snapshots: 5-minute telemetry, hourly rollups, daily cost files, or scheduled
inventory exports. Streaming is useful for alerting, but batch is usually
better for planning, forecasting, rightsizing, and stakeholder reporting.

[Back to TOC](#toc)

## Lambda vs container

Question:
Would you use Lambda or a container job for cloud telemetry collection?

Answer:
Lambda is good for lightweight scheduled pulls or enrichment. A scheduled
container is better for heavier dependencies, larger extracts, or longer
runtime. Airflow or Step Functions are better for multi-step workflows. If
BMC/Helix/CloudWatch already collects the data, automation can focus on
validation, transformation, classification, and reporting.

[Back to TOC](#toc)

## df.copy()

Question:
Why use `df.copy()` before modifying a DataFrame?

Answer:
It prevents accidental side effects on the original DataFrame and avoids chained-assignment surprises during transformation steps.

[Back to TOC](#toc)

## groupby().agg() named aggregation

Question:
What is the `.groupby().agg()` pattern?

Answer:
Use `output_col=(input_col, agg_fn)`, for example `sample_count=("sample_id", "count")`. Group columns define grain; `.agg()` defines metric summaries.

[Back to TOC](#toc)

## as_index=False

Question:
Why use `as_index=False` in groupby?

Answer:
It keeps grouping columns as normal columns in the result, which makes downstream reporting and exports cleaner.

[Back to TOC](#toc)

## reset_index(drop=True)

Question:
When do you use `reset_index(drop=True)`?

Answer:
After filtering/sorting when you want a clean sequential index and do not need the old index preserved.

[Back to TOC](#toc)

## apply(axis=1)

Question:
How is `apply(..., axis=1)` used for capacity status?

Answer:
`axis=1` applies a function row by row. Each row returns one label (for example `high_capacity_risk`) that is stored in a new status column.

[Back to TOC](#toc)

## JSONB tags

Question:
How do you use JSONB tags in SQL?

Answer:
Keep full `tags` for traceability and extract keys using `->>` (for example `tags ->> 'team'`) so metadata can be filtered, grouped, and reported.

[Back to TOC](#toc)

## Pandas P95

Question:
How do you calculate P95 in Pandas?

Answer:
Inside `groupby().agg()`, use `lambda x: x.quantile(0.95)`.

[Back to TOC](#toc)

## SQL DATE_TRUNC

Question:
Why use `DATE_TRUNC` for telemetry?

Answer:
It buckets timestamps into hourly/daily windows for rollups and trend reporting.

[Back to TOC](#toc)

## SQL PERCENTILE_CONT

Question:
What does `PERCENTILE_CONT(0.95) WITHIN GROUP (...)` do?

Answer:
It calculates the 95th percentile value inside each group and is useful for sustained-pressure capacity signals.

[Back to TOC](#toc)

## Kubernetes granularity

Question:
Do you analyze Kubernetes only at cluster level?

Answer:
No. Container/workload level for rightsizing, namespace/team for ownership and cost, and cluster/node for headroom and autoscaling pressure.

[Back to TOC](#toc)

## HorizonScale models

Question:
How do you describe model choice in HorizonScale?

Answer:
Use practical framing: Prophet for trend/seasonality, scikit-learn for feature-driven prediction/risk scoring, plus explainable threshold/headroom logic.

[Back to TOC](#toc)

## HorizonScale validation

Question:
How do you validate forecasting outputs?

Answer:
Back-test against historical windows, compare with later actuals, review false positives/negatives, and prioritize explainability for stakeholder trust.

[Back to TOC](#toc)

# Module 6 Odds and repeats

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

[Back to TOC](#toc)

## Tell me about a Python automation workflow you built for capacity planning.

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
[Back to TOC](#toc)
### EKS (Elastic Kubernetes Service)

A managed service that makes it easy to run Kubernetes on AWS, providing the flexibility of open-source orchestration with the security and reliability of a managed infrastructure.
[Back to TOC](#toc)
### EC2 (Elastic Compute Cloud)

This service provides scalable virtual servers, giving you full control over the operating system and networking for your applications.
[Back to TOC](#toc)
### ECS (Elastic Container Service)

A highly scalable, high-performance container management service that allows you to run and scale Docker applications without managing a complex orchestration control plane.
[Back to TOC](#toc)
### RDS (Relational Database Service)

This service simplifies the setup, operation, and scaling of relational databases like MySQL, PostgreSQL, or SQL Server by automating administrative tasks like backups and patching.
[Back to TOC](#toc)
### S3 (Simple Storage Service)

An object storage service built to store and retrieve any amount of data from anywhere on the web, offering industry-leading durability, availability, and scalability.
[Back to TOC](#toc)
### Glue
Serverless ETL. Crawls S3 to infer schema, runs Spark jobs to transform/load data. Key use: raw telemetry → clean Parquet → Redshift or Athena. Capacity concern: DPU hours (cost scales with job size and runtime).
[Back to TOC](#toc)
### Redshift
Columnar data warehouse. SQL at scale on structured/semi-structured data. Runs on provisioned nodes or Serverless. Key capacity concerns: node utilization, storage per node, WLM queue pressure, and query concurrency limits.
[Back to TOC](#toc)
### One-liner mental model
> S3 stores it → Glue moves it → Redshift queries it → EC2/ECS/EKS runs the workloads that generate it.
