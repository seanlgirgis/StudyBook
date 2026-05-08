








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
