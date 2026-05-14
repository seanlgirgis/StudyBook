# BOA Interview Q and A: Capacity Forecasting (Short Final Drill)

## Table of Contents

- [1) Walk me through how you built it.](#1-walk-me-through-how-you-built-it)
- [2) What features did you use?](#2-what-features-did-you-use)
- [3) Why Prophet?](#3-why-prophet)
- [4) How did you validate it?](#4-how-did-you-validate-it)
- [5) Explain 18 months training / 6 months testing.](#5-explain-18-months-training-6-months-testing)
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

## 2) What features did you use?
[Back to TOC](#table-of-contents)
Rolling averages showed sustained trend direction.
Rolling peaks and recent maximum showed stress behavior.
Growth slope and volatility helped identify acceleration risk.
Headroom to threshold showed urgency before a breach.
Breach flags and risk bands made prioritization clearer.

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
