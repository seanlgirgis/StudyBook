# Apple Cloud Capacity Cheat Sheet Draft

## Automation types

Question:
What do you mean by automation in cloud capacity work?

Answer:
Automation means reducing manual capacity analysis. It includes data automation,
capacity-risk automation, cloud/platform collection automation, and reporting
automation. The workflow is collect telemetry, normalize it, join ownership
metadata, calculate P95/headroom/forecast variance/cost, classify risk or
waste, and export action-ready reports.

## Batch vs streaming

Question:
Do you need streaming for capacity and cost analytics?

Answer:
Usually no. Capacity planning and cost efficiency usually work from periodic
snapshots: 5-minute telemetry, hourly rollups, daily cost files, or scheduled
inventory exports. Streaming is useful for alerting, but batch is usually
better for planning, forecasting, rightsizing, and stakeholder reporting.

## Lambda vs container

Question:
Would you use Lambda or a container job for cloud telemetry collection?

Answer:
Lambda is good for lightweight scheduled pulls or enrichment. A scheduled
container is better for heavier dependencies, larger extracts, or longer
runtime. Airflow or Step Functions are better for multi-step workflows. If
BMC/Helix/CloudWatch already collects the data, automation can focus on
validation, transformation, classification, and reporting.

## df.copy()

Question:
Why use `df.copy()` before modifying a DataFrame?

Answer:
It prevents accidental side effects on the original DataFrame and avoids chained-assignment surprises during transformation steps.

## groupby().agg() named aggregation

Question:
What is the `.groupby().agg()` pattern?

Answer:
Use `output_col=(input_col, agg_fn)`, for example `sample_count=("sample_id", "count")`. Group columns define grain; `.agg()` defines metric summaries.

## as_index=False

Question:
Why use `as_index=False` in groupby?

Answer:
It keeps grouping columns as normal columns in the result, which makes downstream reporting and exports cleaner.

## reset_index(drop=True)

Question:
When do you use `reset_index(drop=True)`?

Answer:
After filtering/sorting when you want a clean sequential index and do not need the old index preserved.

## apply(axis=1)

Question:
How is `apply(..., axis=1)` used for capacity status?

Answer:
`axis=1` applies a function row by row. Each row returns one label (for example `high_capacity_risk`) that is stored in a new status column.

## JSONB tags

Question:
How do you use JSONB tags in SQL?

Answer:
Keep full `tags` for traceability and extract keys using `->>` (for example `tags ->> 'team'`) so metadata can be filtered, grouped, and reported.

## Pandas P95

Question:
How do you calculate P95 in Pandas?

Answer:
Inside `groupby().agg()`, use `lambda x: x.quantile(0.95)`.

## SQL DATE_TRUNC

Question:
Why use `DATE_TRUNC` for telemetry?

Answer:
It buckets timestamps into hourly/daily windows for rollups and trend reporting.

## SQL PERCENTILE_CONT

Question:
What does `PERCENTILE_CONT(0.95) WITHIN GROUP (...)` do?

Answer:
It calculates the 95th percentile value inside each group and is useful for sustained-pressure capacity signals.

## Kubernetes granularity

Question:
Do you analyze Kubernetes only at cluster level?

Answer:
No. Container/workload level for rightsizing, namespace/team for ownership and cost, and cluster/node for headroom and autoscaling pressure.

## HorizonScale models

Question:
How do you describe model choice in HorizonScale?

Answer:
Use practical framing: Prophet for trend/seasonality, scikit-learn for feature-driven prediction/risk scoring, plus explainable threshold/headroom logic.

## HorizonScale validation

Question:
How do you validate forecasting outputs?

Answer:
Back-test against historical windows, compare with later actuals, review false positives/negatives, and prioritize explainability for stakeholder trust.
