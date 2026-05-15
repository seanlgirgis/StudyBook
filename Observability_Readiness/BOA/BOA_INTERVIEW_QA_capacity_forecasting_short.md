# BOA Interview Q and A: Capacity Forecasting (Short Final Drill)

## Table of Contents

- [BOA Interview Q and A: Capacity Forecasting (Short Final Drill)](#boa-interview-q-and-a-capacity-forecasting-short-final-drill)
  - [Table of Contents](#table-of-contents)
  - [1) Walk me through how you built it.](#1-walk-me-through-how-you-built-it)
  - [2) What features did you use?](#2-what-features-did-you-use)
  - [3) Why Prophet?](#3-why-prophet)
  - [4) How did you validate it?](#4-how-did-you-validate-it)
  - [5) Explain 18 months training / 6 months testing.](#5-explain-18-months-training--6-months-testing)
  - [6) Did you forecast all servers together?](#6-did-you-forecast-all-servers-together)
  - [7) How did you handle 10,000 servers?](#7-how-did-you-handle-10000-servers)
  - [8) How did leadership use the output?](#8-how-did-leadership-use-the-output)
  - [9) How did this support budget or planning?](#9-how-did-this-support-budget-or-planning)
  - [10) How would you scale from Pandas to PySpark/Hadoop/cloud?](#10-how-would-you-scale-from-pandas-to-pysparkhadoopcloud)
  - [11) What did you own directly?](#11-what-did-you-own-directly)
  - [12) What is the safest summary of the project?](#12-what-is-the-safest-summary-of-the-project)
  - [Final Memory Spine](#final-memory-spine)
  - [Do Not Say](#do-not-say)


## 1) Walk me through how you built it.
[Back to TOC](#table-of-contents)
I started with telemetry extraction and data cleanup.
Then I normalized timestamps and bucketed data hourly and daily.
I grouped by host, application, and service for actionability.
Next I engineered trend, headroom, and breach features.
Then I forecasted risk windows and ranked systems by urgency.
The output became dashboards, exception lists, and management summaries.
1. Start with telemetry extraction and data cleanup.

2. Normalize timestamps so the time-series data is consistent.

3. Bucket the data into hourly and daily windows.

4. Group the data by host, application, and service so the output is actionable.

5. Engineer capacity features:
   - trend
   - headroom
   - threshold/breach indicators
   - risk signals

6. Forecast risk windows instead of only looking at current utilization.

7. Rank systems by urgency so teams know where to act first.

8. Publish the output as:
   - dashboards
   - exception lists
   - management summaries

## 2) What features did you use?
[Back to TOC](#table-of-contents)
Rolling averages showed sustained trend direction.
Rolling peaks and recent maximum showed stress behavior.
Growth slope and volatility helped identify acceleration risk.
Headroom to threshold showed urgency before a breach.
Breach flags and risk bands made prioritization clearer.

- Rolling Averages features
- Rolling Peaks / P95 features
- Headroom features
- breach flags 
- Risk Bands  (OOM - High Risk - Low Risk - Severe Capacity Risk)
- Growth Slope (capture pattern)

## 3) Why Prophet?
[Back to TOC](#table-of-contents)
Prophet was part of the real forecasting workflow.
It handled trend and seasonality in an explainable way.
That made results easier to discuss with engineers and leadership.
I used it for practical planning support, not deep ML claims.

## 4) How did you validate it?
[Back to TOC](#table-of-contents)
I validated data quality before trusting forecast outputs.
I checked feature math and compared predicted vs actual behavior.
I tracked false positives and false negatives for risk flags.
I reviewed output with SMEs to confirm operational realism.

## 5) Explain 18 months training / 6 months testing.
[Back to TOC](#table-of-contents)
With 24 months of history, I train on the first 18 months.
Then I hold out the next 6 months for testing.
I compare forecasted values or risk bands to actual outcomes.
If that looks reasonable, I retrain on full history.
Then I forecast the next 3 to 6 month planning window.

## 6) Did you forecast all servers together?
[Back to TOC](#table-of-contents)
No, that would create noise at scale.
We grouped first, forecast second.
We did not let one model explain thousands of mixed behaviors.
Forecasts were applied within behavior-based cohorts and validated.

## 7) How did you handle 10,000 servers?
[Back to TOC](#table-of-contents)
I handled scale through cohort-based forecasting.
Systems were grouped by function, ownership, pattern, and criticality.
Batch, API, and database workloads were not pooled as one curve.
That made forecasts more defensible and easier to operate.

## 8) How did leadership use the output?
[Back to TOC](#table-of-contents)
Leadership used concise ranked risk summaries.
They looked at what was at risk, when, and who owned it.
Outputs informed remediation timing and planning priorities.
The goal was clearer decisions, not just better charts.

## 9) How did this support budget or planning?
[Back to TOC](#table-of-contents)
Forecast trend and headroom data supported planning conversations.
It helped frame cost-risk tradeoffs with better timing context.
I was not the FinOps owner, but the outputs supported that bridge.
It made stakeholder discussions more factual and less reactive.

## 10) How would you scale from Pandas to PySpark/Hadoop/cloud?
[Back to TOC](#table-of-contents)
- The logic stays the same: we keep the same forecasting and risk logic.
- We scale by moving heavy data prep and feature engineering to distributed patterns, using PySpark.
- We partition the data—often by time or group—so that Hadoop or cloud storage scales smoothly.
- Instead of changing the core logic, we simply leverage distributed compute to handle larger data sets.
This ensures efficient forecasting as the environment grows.

## 11) What did you own directly?
[Back to TOC](#table-of-contents)
I owned major workflow pieces I can defend clearly.
That includes shaping telemetry, features, forecast usage, and validation.
I also owned risk ranking and reporting for decision support.
For broader platform scale-out, I partnered with specialist teams.

## 12) What is the safest summary of the project?
[Back to TOC](#table-of-contents)
This was practical capacity forecasting decision support.
SQL/Python/Pandas formed the real workflow foundation.
Prophet was real forecasting work in the core flow.
Scikit-learn risk scoring is a newer lab modernization extension.
PySpark/Hadoop/cloud is the scale-up architecture path.

## 15) How does this map to BOA-style CBFR work?
[Back to TOC](#table-of-contents)
This maps closely to capacity baseline forecasting work.

If the team produces quarterly Capacity Baseline Forecast Reports, I would
treat that report as the decision product. The pipeline behind it should
collect production telemetry, map it to applications and clusters, calculate
trend, headroom, safety margin, and risk band, then publish a clear report for
planning and prioritization.

My value is that I understand both sides: the Excel/reporting starting point
and the Python/Pandas/forecasting path that makes the process more repeatable,
validated, and dashboard-ready.

## 16) How do performance testing, TPS, and safety factors fit?
[Back to TOC](#table-of-contents)
Performance testing gives a controlled view of throughput limits, such as TPS
capacity and saturation behavior. Production telemetry shows how the system
behaves under real usage.

I would use both. The test feed helps define safe operating limits and safety
factors. Production telemetry shows whether real usage is trending toward those
limits.

I would not forecast right up to the hard limit. Capacity planning needs safety
margin because production workloads have spikes, business-calendar events, and
unexpected demand.

## 17) How would you support dashboarding?
[Back to TOC](#table-of-contents)
I would make the forecast output dashboard-ready.

The dashboard should show baseline, actual trend, forecasted risk window,
headroom, threshold, safety margin, risk band, service owner, and recommended
action.

I can structure the data so it can feed enterprise reporting tools such as
Power BI, Tableau, or another dashboard platform. I would not overclaim being
the owner of every visualization tool, but I can define the capacity data model
and decision views the dashboard needs.

## 18) What tools or environment signals are relevant?
[Back to TOC](#table-of-contents)
BMC TrueSight and TSCO are directly relevant to my background. I understand the
capacity-planning style: production telemetry, baseline reports, thresholds,
forecast views, and operational planning.

If the environment also uses Helix, Splunk, AWS, or Kubernetes monitoring, I
would treat those as additional signal sources or reporting contexts. My core
strength remains the capacity workflow: collect the telemetry, validate it,
define KPIs, forecast risk, and turn the output into reports, dashboards, and
action plans.

## Final Memory Spine
[Back to TOC](#table-of-contents)
```text
Clean telemetry -> normalize time -> bucket -> group -> engineer features ->
forecast and rank risk -> validate against actuals and SMEs -> publish
dashboards and action lists -> support leadership planning decisions.
For BOA-style teams: CBFR/reporting, dashboarding, TPS safety factors,
BMC capacity data, and production critical applications are natural fits.
```

## Do Not Say
[Back to TOC](#table-of-contents)
- "I owned deep ML research and invented a new algorithm."
- "Every server had a custom hand-tuned model."
- "Scikit-learn was fully deployed everywhere in production."
- "I owned the full Hadoop/cloud platform end to end."
