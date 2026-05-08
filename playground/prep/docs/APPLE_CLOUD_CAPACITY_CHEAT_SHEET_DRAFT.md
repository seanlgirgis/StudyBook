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
