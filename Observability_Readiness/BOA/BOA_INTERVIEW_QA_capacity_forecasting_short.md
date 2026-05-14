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
  - [13) How do you define KPIs?](#13-how-do-you-define-kpis)
  - [14) How did runbooks fit into the process?](#14-how-did-runbooks-fit-into-the-process)
  - [Final Memory Spine](#final-memory-spine)
  - [Do Not Say](#do-not-say)


## 1) Walk me through how you built it.
[Back to TOC](#table-of-contents)
I started with telemetry extraction from monitoring and capacity
systems. The first step was cleanup and normalization: normalize
timestamps, standardize host and service identifiers, and make sure
the mappings were reliable.

Then I bucketed the data into hourly and daily windows and grouped it
by host, application, and service so the output would be actionable.

After that I engineered capacity features: rolling averages, rolling
peaks, P95s where useful, headroom to threshold, breach flags, risk
bands, and growth slope.

For forecasting, I used a time-based validation approach. Train on an
older history window, test against a recent holdout window, compare
the forecast against actual behavior, and then refit on the full
history before forecasting the next planning window.

The final output was not just charts. It became reports, exception
lists, dashboards, and management summaries that helped engineering,
business owners, and planning stakeholders decide where action was
needed.

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
- Risk Bands  (OOM - High Risk - Low Risk - Severe Capcity Risk)
- Growth Slope (capture pattern)

## 3) Why Prophet?
[Back to TOC](#table-of-contents)
Prophet was a practical choice because the data was time-series
capacity data, and we needed to handle trend plus seasonality.

Some systems have weekly, monthly, quarter-end, or business-calendar
patterns, so a simple straight-line trend would not always be enough.
Prophet gave us an explainable way to model those patterns and discuss
the forecast with engineers and leadership.

I still treated it as decision support, not deep ML research. The goal
was not to build the most complex model. The goal was to identify
capacity risk earlier and give teams more time to act.

For validation, I used time-based holdout testing. For example, with
24 months of history, train on the first 18 months, test against the
next 6 months, and compare forecasted values or risk bands against
what actually happened.

Then I would review forecast error, false positives, false negatives,
threshold-crossing accuracy, and SME feedback before trusting the
forecast for the next 3 to 6 month planning window.

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
To be honest, we did not start by forecasting every server at once.
We started with a smaller, more controlled set of systems and expanded
from there.

We grouped servers into cohorts based on factors like function,
ownership, criticality, workload type, batch behavior, and whether the
service was customer-facing.

Then we focused first on the higher-risk cohorts, where the forecast
would create the most value. As the approach became more reliable, we
expanded by adding more servers into existing cohorts and creating new
cohorts where the usage pattern was different.

That made the forecasting process more manageable, more defensible,
and easier to operate. We grouped first, forecast second. We did not
dump all servers into one bucket and expect one model to explain
different behaviors.

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
Keep the same forecasting and risk logic first.
Move heavier transforms to distributed data-processing patterns.
Use PySpark/Hadoop/cloud as the architecture scale path.
Do not change core logic just because tooling changes.

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

## 13) How do you define KPIs?
[Back to TOC](#table-of-contents)
See `BOA_TELEMETRY_KPI_SLI_SLO_SLA_DEFINITIONS.md` for the definitions
cheat sheet.

I define KPIs by starting with the business or operational decision first.
For capacity, useful KPIs include utilization trend, rolling peak, recent
maximum, growth slope, headroom to threshold, breach frequency, forecasted
breach window, service criticality, owner, risk band, and remediation status.
A good KPI is actionable, not just a metric on a chart.

## 14) How did runbooks fit into the process?
[Back to TOC](#table-of-contents)
See `BOA_TELEMETRY_KPI_SLI_SLO_SLA_DEFINITIONS.md` for the definitions
cheat sheet.

Runbooks turned forecast output into repeatable action.
If risk increased, we validated data and mapping, confirmed owner, checked
recent changes, reviewed headroom and threshold history, and involved SMEs.
Then we chose the action path: tuning, cleanup, right-sizing, capacity
expansion, or continued monitoring.
That kept response consistent instead of reinventing each investigation.

## Final Memory Spine
[Back to TOC](#table-of-contents)
```text
Clean telemetry -> normalize time -> bucket -> group -> engineer features ->
forecast and rank risk -> validate against actuals and SMEs -> publish
dashboards and action lists -> support leadership planning decisions.
```

## Do Not Say
[Back to TOC](#table-of-contents)
- "I owned deep ML research and invented a new algorithm."
- "Every server had a custom hand-tuned model."
- "Scikit-learn was fully deployed everywhere in production."
- "I owned the full Hadoop/cloud platform end to end."
