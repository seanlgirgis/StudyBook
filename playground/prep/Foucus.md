## TOC
- [TOC](#toc)
- [1. Interview Target](#1-interview-target)
  - [Keep in your head](#keep-in-your-head)
  - [Tell me about yourself](#tell-me-about-yourself)
  - [What do you mean by automation in this role?](#what-do-you-mean-by-automation-in-this-role)
  - [Do you need streaming for cloud capacity and cost analytics, or is batch enough?](#do-you-need-streaming-for-cloud-capacity-and-cost-analytics-or-is-batch-enough)
  - [How would you automate a monthly AWS capacity report?](#how-would-you-automate-a-monthly-aws-capacity-report)
  - [How would you determine if an EKS workload is overutilized or underutilized?](#how-would-you-determine-if-an-eks-workload-is-overutilized-or-underutilized)
  - [How would you analyze S3 capacity and cost?](#how-would-you-analyze-s3-capacity-and-cost)
  - [What was HorizonScale, and how did it work?](#what-was-horizonscale-and-how-did-it-work)
  - [How did you validate the forecast?](#how-did-you-validate-the-forecast)
  - [How does your physical / virtualization capacity background transfer to cloud capacity?](#how-does-your-physical--virtualization-capacity-background-transfer-to-cloud-capacity)
  - [How would you explain SQL capacity analysis to a manager?](#how-would-you-explain-sql-capacity-analysis-to-a-manager)
  - [What is the difference between GROUP BY and window functions?](#what-is-the-difference-between-group-by-and-window-functions)
  - [Why P95 instead of average?](#why-p95-instead-of-average)
  - [What is a CTE and why use it?](#what-is-a-cte-and-why-use-it)
  - [Why use LAG in telemetry analysis?](#why-use-lag-in-telemetry-analysis)
  - [How do you use JSONB tags in telemetry analysis?](#how-do-you-use-jsonb-tags-in-telemetry-analysis)
  - [How do you find overallocated services?](#how-do-you-find-overallocated-services)
  - [How do you summarize cost correctly?](#how-do-you-summarize-cost-correctly)
  - [How do you avoid unsafe cost cuts?](#how-do-you-avoid-unsafe-cost-cuts)
  - [How do you communicate risk to stakeholders?](#how-do-you-communicate-risk-to-stakeholders)
  - [What would you automate first in this role?](#what-would-you-automate-first-in-this-role)
  - [What questions would you ask them at the end of the interview?](#what-questions-would-you-ask-them-at-the-end-of-the-interview)





## 1. Interview Target

[Back to TOC](#toc)
### Keep in your head

Same decision loop, different resource vocabulary.

The goal is not a dashboard; it is a forecast-driven capacity action loop.

Automation makes the meeting about decisions, not data cleaning.

Batch is usually enough for capacity and cost; streaming is mainly for alerting.

I rightsize with telemetry, ownership, and validation — I do not randomly cut resources.

[Back to TOC](#toc)
### Tell me about yourself

I’m a senior Data and Capacity Engineer. My strongest area is where infrastructure capacity meets data engineering: Python, SQL, telemetry, forecasting, and automation.

The way I think about the work is a data-to-decision loop: collect telemetry, clean and normalize it, calculate utilization, P95, headroom, growth, forecast variance, and rightsizing candidates, then turn that into actions like scaling, rightsizing, capacity approval, waste reduction, or runbook updates.

At Citi, I spent about 8 years in this space. A big part of my work was moving capacity analytics away from manual Excel-style reporting into automated data pipelines. I also helped improve forecasting beyond the out-of-box BMC TrueSight/TSCO reports by building Python-based forecasting workflows that evaluated multiple model approaches and produced 3-to-6-month capacity forecasts for planning.

So for this role, I’m not positioning myself as a deep Kubernetes platform owner. I’m positioning myself as someone who can automate telemetry analysis and turn it into capacity, cost, and planning decisions.

[Back to TOC](#toc)
### What do you mean by automation in this role?
Automation can mean a few things in this role, and they are all valid.

First, data automation: collecting telemetry, cleaning it, normalizing it, and generating reports without manual spreadsheet work.

Second, collection automation: pulling metrics from systems like BMC TrueSight, Helix, CloudWatch, Container Insights, CUR, or S3 Inventory.

Third, platform automation: onboarding or deploying monitoring agents, validating that telemetry is flowing, and keeping the monitoring coverage consistent.

Fourth, cloud automation: using Python/boto3, scheduled jobs, Lambda, containers, Step Functions, or CDK/IaC patterns to automate AWS collection, reporting, or operational tasks.

For capacity work, the goal is to reduce manual effort and create a repeatable loop: collect data, calculate P95/headroom/forecast variance/cost, classify risk or waste, and produce an action-ready report.

[Back to TOC](#toc)
### Do you need streaming for cloud capacity and cost analytics, or is batch enough?
For capacity planning and cost analytics, batch is usually enough. Most planning decisions do not need second-by-second streaming. We usually work from 5-minute telemetry, hourly rollups, daily cost files, monthly trends, or scheduled inventory exports.

I would use streaming only if the use case is operational alerting or near-real-time detection, where latency really matters. For planning, forecasting, rightsizing, and stakeholder reporting, batch is simpler, reliable, easier to validate, and usually the right choice.


[Back to TOC](#toc)
### How would you automate a monthly AWS capacity report?

To automate a monthly AWS capacity report, I would treat it as a scheduled batch workflow.

First, I would collect the data from the right sources: CloudWatch for EC2/ECS utilization, Container Insights for EKS pod/node/workload metrics, S3 Inventory for bucket growth and storage class review, and AWS Cost and Usage Report in S3 for cost by service, tag, account, and region.

Second, I would process the data: clean and normalize it, join ownership and tags, aggregate by service, workload, namespace, account, or bucket, then calculate AVG, P95, counts, sums, headroom, allocation versus actual usage, cost trend, and abnormal growth.

Third, I would classify the findings into action categories: rightsizing candidates, scaling needs, low headroom, lifecycle opportunities, missing tags, or abnormal cost increases.

Finally, I would generate stakeholder outputs — CSV, dashboard, Markdown/PDF report, or a table in the reporting layer — and update runbooks or action trackers.

For scheduling, I would use EventBridge Scheduler as the AWS version of cron. For a lightweight job, EventBridge can trigger Lambda. For heavier processing, I would run a scheduled ECS/Fargate container. If the report has multiple stages like extract, validate, transform, and publish, I would use Step Functions.


[Back to TOC](#toc)
### How would you determine if an EKS workload is overutilized or underutilized?
For EKS capacity, I compare requests, limits, and actual usage for CPU and memory.

If actual CPU usage is close to the CPU limit, that is throttling risk. If memory usage is close to the memory limit, that is OOM/restart risk.

If actual usage is consistently far below the request, the workload may be over-requested and wasting reserved capacity, so it becomes a rightsizing candidate.

If actual usage is comfortably between request and limit, and P95 behavior is stable, then it may be sized correctly.

If request equals limit, there is no burst room, so I would review whether the workload needs more flexibility or a higher limit.
```sh
CPU request utilization = cpu_usage_cores / cpu_request_cores * 100
CPU limit utilization = cpu_usage_cores / cpu_limit_cores * 100

Memory request utilization = memory_usage_gb / memory_request_gb * 100
Memory limit utilization = memory_usage_gb / memory_limit_gb * 100
```
I would not rightsize from one snapshot. I would look at P95 over at least 30 days, separate request utilization from limit utilization, check cost impact, and validate with the owning team before recommending changes. What looks like waste may be intentional headroom for a bursty workload.

[Back to TOC](#toc)
### How would you analyze S3 capacity and cost?
For S3 capacity and cost, I do not think in CPU and memory. I think in storage growth, access pattern, storage class, ownership, and cost.

I would ask: how fast is storage growing by bucket or prefix? Is the data still being accessed? What is the last-access age? Is the data in the right storage class — Standard, Infrequent Access, Glacier, or Deep Archive? And who owns the data — account, team, application, tags — and what is the monthly cost?

The main data sources would be S3 Inventory, S3 Storage Lens, CloudWatch/S3 metrics, and the Cost and Usage Report.

The goal is not blindly deleting data. S3 savings usually come from lifecycle policy, storage class optimization, retention review, and ownership cleanup. For example, old rarely accessed data may move from Standard to IA or Glacier, but only after confirming business and compliance requirements.


[Back to TOC](#toc)
### What was HorizonScale, and how did it work?
HorizonScale was a telemetry-to-decision capacity forecasting workflow. The input was historical infrastructure telemetry like CPU, memory, P95 utilization or latency, allocated capacity, actual usage, ownership, and cost where available.

The workflow cleaned and normalized the telemetry, aggregated it by service or resource, calculated features like P95, headroom, growth rate, threshold breaches, and forecast variance, then used practical forecasting approaches like Prophet, scikit-learn-style feature models, and explainable baselines.

The goal was not model complexity. The goal was to produce capacity decisions: which services had future bottleneck risk, where we had safe rightsizing opportunities, where forecast missed actual demand, and where capacity or budget planning needed attention.

For validation, I used a walk-forward style approach: train on historical periods, hold out later months, compare forecast to actuals with MAE, RMSE, and MAPE, and choose the best practical model per service or resource series.


[Back to TOC](#toc)
###  How did you validate the forecast?
If they ask how I validated it, I would say: given 24 months of telemetry, train candidate models on the first 18 months, test against the last 6 months, compare MAE/RMSE/MAPE per series, pick a champion model per series, retrain on the full history, and forecast the next 3–6 months.



[Back to TOC](#toc)
### How does your physical / virtualization capacity background transfer to cloud capacity?
The decision loop transfers directly, but the resource vocabulary changes.

In physical or virtual capacity, I looked at server CPU, memory, disk, allocation versus actual usage, host headroom, growth, and forecast risk.

In cloud, those ideas map to EC2 instances, ECS tasks, EKS pods and nodes, S3 buckets, storage class, account, region, tags, and cost. VM allocation versus actual usage becomes Kubernetes requests and limits versus actual usage. Host headroom becomes node or cluster headroom.

What does not change is the method: collect telemetry, normalize it, calculate P95, headroom, growth, forecast variance, and classify risk or waste into an action report.

What cloud adds is that cost becomes a first-class metric. Elasticity means I have to watch both risk and waste. Tagging becomes critical because bad tags break ownership and chargeback. And storage class or lifecycle policy become optimization levers that did not exist the same way in physical infrastructure.

  
[Back to TOC](#toc)
### How would you explain SQL capacity analysis to a manager?

 SQL converts noisy telemetry into service-level risk, waste, and cost summaries that drive prioritized actions.


[Back to TOC](#toc)
### What is the difference between GROUP BY and window functions?
GROUP BY collapses many rows into fewer summary rows. For example, many telemetry samples become one service-level average.

Window functions keep the original rows visible and add calculations beside each row, like rank, previous value with LAG, moving average, or running total.

So I use GROUP BY when I want a summary, and window functions when I want row-level detail plus context.


[Back to TOC](#toc)
### Why P95 instead of average?
P95 highlights sustained high pressure that averages can hide. Average tells me normal behavior, max can overreact to one spike, and P95 gives a better signal for capacity planning because it shows the high-end demand most of the time without chasing every outlier.


[Back to TOC](#toc)
### What is a CTE and why use it?
A CTE is a named temporary query block created with WITH. I use it for readability and multi-step logic. For example, first calculate an hourly service rollup, then in the outer query filter risky windows or rank services by P95 CPU.

[Back to TOC](#toc)
### Why use LAG in telemetry analysis?
I use LAG to compare the current telemetry value with the previous time window. For example, I can compare this hour’s P95 CPU with the previous hour’s P95 CPU to detect sudden growth, spikes, or forecast drift.

[Back to TOC](#toc)
### How do you use JSONB tags in telemetry analysis?
I use JSONB tags for flexible telemetry metadata like team, environment, region, or owner. I use `->>` to extract a key as text, like `tags ->> 'team'`, and `?` to check whether a key exists. That lets me keep the full tags object for traceability while still grouping, filtering, and reporting by ownership fields.

[Back to TOC](#toc)
### How do you find overallocated services?
Overallocated = allocated/requested capacity is much higher than actual usage, especially when the cost impact is meaningful.


[Back to TOC](#toc)
### How do you summarize cost correctly?
I first clarify what the cost field means. If it is incremental cost for the time period, I use SUM. If it is a point-in-time snapshot or rate, I use AVG or MAX depending on the question. That matters because using SUM on a snapshot field can exaggerate cost.

[Back to TOC](#toc)
### How do you avoid unsafe cost cuts?
I do not randomly cut resources. I rightsize with telemetry, ownership, and validation.

[Back to TOC](#toc)
### How do you communicate risk to stakeholders?
I communicate risk by translating metrics into business action. I do not just say CPU is high. I explain the risk, impact, owner, recommended action, and timeline. For example: this service has low headroom and rising P95 CPU, the owner is payments, the impact is possible scaling pressure next month, and the recommended action is capacity review or scaling plan within two weeks.


[Back to TOC](#toc)
### What would you automate first in this role?
What I would automate first is the repeatable capacity review package.

The goal is not automation for its own sake. It is making sure that by the time the capacity review meeting starts, the hard work is already done — telemetry is collected, cleaned, tagged with ownership, summarized by service or workload, and classified into risk, waste, or normal.

Then the meeting is about decisions, not data cleaning: which workloads need scaling, which ones are rightsizing candidates, which costs are abnormal, and which owners need follow-up.

[Back to TOC](#toc)
### What questions would you ask them at the end of the interview?
I have three questions.

First, what automation exists today, and where is the biggest manual pain?

Second, how do you measure success for this role in the first 90 days?

Third, if someone performs really well in this role, what would they have improved or delivered in the first few months that would make you say they were the right hire?


