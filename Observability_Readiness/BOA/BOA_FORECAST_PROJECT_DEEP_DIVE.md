# BOA Forecast Project Deep Dive

## Table of Contents

- [1. Plain-English Project Summary](#1-plain-english-project-summary)
- [2. Original Reporting Automation Foundation](#2-original-reporting-automation-foundation)
- [3. Original Pandas Version](#3-original-pandas-version)
- [4. Input Telemetry Data](#4-input-telemetry-data)
- [5. Feature Engineering](#5-feature-engineering)
- [Cohort-Based Forecasting at Scale](#cohort-based-forecasting-at-scale)
- [6. Forecast Horizon / Risk Window](#6-forecast-horizon-risk-window)
- [7. Testing and Validation](#7-testing-and-validation)
- [8. Output Reports and Dashboards](#8-output-reports-and-dashboards)
- [9. Management Decision Support](#9-management-decision-support)
- [KPI Definition and Runbook Connection](#kpi-definition-and-runbook-connection)
- [10. Scaling Path to PySpark / Hadoop / Cloud](#10-scaling-path-to-pyspark-hadoop-cloud)
- [11. 30-Second Answer](#11-30-second-answer)
- [12. 2-Minute Answer](#12-2-minute-answer)
- [13. Whiteboard Architecture Diagram](#13-whiteboard-architecture-diagram)
- [14. What Not To Say](#14-what-not-to-say)


## 1. Plain-English Project Summary
[Back to TOC](#table-of-contents)
This project converted raw telemetry into early capacity risk visibility so
engineering and management could act before incidents. It was designed for
operational decision support, with practical checks, clear risk language, and
repeatable reporting.


## 2. Original Reporting Automation Foundation
[Back to TOC](#table-of-contents)
The forecasting work sat on top of an earlier reporting automation layer.
A lot of capacity reporting can start as a manual Excel-heavy process:
extracts, spreadsheet cleanup, repeated calculations, and team reports.

The practical improvement was to move that work toward a Python-based
pipeline: extract the source data, clean and normalize it, store the shaped
data more consistently, and generate repeatable report outputs. SQLite was a
useful lightweight structured store for local or team-level reporting, and
Streamlit-style reporting was a practical way to expose results to the team.

This layer matters because HorizonScale depends on trustworthy prepared data.
Once the telemetry was structured, timestamped, grouped, and reusable, it was
much easier to build time buckets, capacity features, forecasts, risk rankings,
and management-ready outputs.

Safe interview framing:

```text
The work evolved in layers: first make reporting repeatable, then make the
telemetry structured and trustworthy, then build forecasting and risk ranking
on top of it.
```

## 3. Original Pandas Version
[Back to TOC](#table-of-contents)
Conceptual flow:
Manual Excel/report extracts
-> Python cleanup pipeline
-> SQLite/team reporting store where useful
-> repeatable report outputs / Streamlit-style team views
-> telemetry extract for forecasting
-> Pandas cleanup
-> timestamp normalization
-> hourly/daily buckets
-> group by host/application/service
-> rolling averages / peaks / growth rates
-> threshold/headroom calculation
-> risk ranking
-> dashboard/report/executive summary

Why Pandas first:
- Fast prototype and iteration loop.
- Easy feature engineering and validation in one place.
- Good fit for proving decision value before distributed scaling.

## 4. Input Telemetry Data
[Back to TOC](#table-of-contents)
- Infrastructure utilization telemetry.
- Application/service throughput and performance indicators.
- Existing KPI feeds used by operations teams.
- Asset metadata for host, application, and service mapping.

## 5. Feature Engineering
[Back to TOC](#table-of-contents)
Representative features:
- timestamp
- host/application/service
- CPU average, peak, p95
- memory average, peak, p95
- storage used
- transaction volume
- day-of-week
- month/quarter
- rolling average
- rolling max
- growth slope
- headroom percentage
- threshold breach flag
- capacity risk band

Design intent:
- Separate sustained trend from isolated spike.
- Provide interpretable features that operations and management can
  understand.

## Cohort-Based Forecasting at Scale
[Back to TOC](#table-of-contents)
At larger scale, thousands of servers should not be modeled as one pool.
Behavior varies too much, and a single pooled model can create noise and weak
signals.

We grouped first, forecast second. We did not let one model try to explain
thousands of different server behaviors at once.

Grouping dimensions:
- application
- service
- owner
- environment
- criticality
- workload type
- usage pattern

Example cohorts:
- steady-state systems
- growth systems
- seasonal systems
- batch-heavy systems
- noisy systems
- low-utilization / waste candidates
- critical low-headroom systems
- retirement or migration candidates

The forecast approach is applied within groups that behave similarly, then
validated against actual behavior and threshold outcomes. Backtesting decides
whether a cohort needs adjustment. I avoid blind per-server tuning unless
specific exceptions fail validation and need focused review.

## 6. Forecast Horizon / Risk Window
[Back to TOC](#table-of-contents)
- Use a practical short-to-mid forecast window aligned to planning cycles.
- Report likely breach windows instead of only point predictions.
- Communicate confidence and assumptions in plain language.

## 7. Testing and Validation
[Back to TOC](#table-of-contents)
- missing timestamp checks
- duplicate record checks
- stale asset checks
- impossible value checks
- time bucket validation
- feature calculation tests
- train/test split that respects time order
- backtesting predicted vs actual
- simple baseline comparison
- SME/business validation
- false positive review

### Holdout Backtesting Example
For model testing, I would not train on all available history and immediately
forecast the future. I would hold out a recent period to test the forecast
first.

For example, with 24 months of history, train on the first 18 months, test
against the next 6 months, and compare forecasted values or risk bands against
what actually happened.

Only after the backtest looked reasonable would I use the full available
history to forecast the next planning window, usually the next 3 to 6 months.

### Programmatic Comparison
- MAE
- MAPE where appropriate
- RMSE where useful
- bias: over-forecasting vs under-forecasting
- risk-band accuracy
- false positives
- false negatives
- threshold-crossing accuracy

Validation principle:
- Prefer reliable decision support over model complexity.

## 8. Output Reports and Dashboards
[Back to TOC](#table-of-contents)
- Risk-ranked service and system views.
- Trend and headroom visuals for operations.
- Threshold/breach outlook for action planning.
- Weekly summary for leadership consumption.

## 9. Management Decision Support
[Back to TOC](#table-of-contents)
- Translate telemetry into risk bands and action windows.
- Support decisions on scaling, optimization, and prioritization.
- Provide concise executive summaries with assumptions and confidence
  language.

## KPI Definition and Runbook Connection
[Back to TOC](#table-of-contents)
Capacity KPIs should be defined from the decision backward. The goal is not to
show every metric. The goal is to show signals that help operations, engineering,
and leadership decide what action is needed.

Useful capacity KPIs:
- utilization trend
- rolling peak
- recent maximum
- growth slope
- headroom to threshold
- threshold breach count or frequency
- forecasted breach window
- service criticality
- risk band
- owner/application mapping
- remediation status

Runbooks connect those KPIs to action. If a system moves into a higher risk
band, the runbook should guide data validation, owner confirmation, threshold
review, SME review, and action selection.

Typical runbook actions:
- validate metric quality
- confirm timestamp bucket and grouping
- check recent changes or incidents
- compare current behavior to historical pattern
- identify service owner
- confirm business-calendar impact
- decide between tuning, cleanup, right-sizing, capacity expansion, or
  continued monitoring

This is how the forecast becomes operational. The dashboard shows the risk, the
KPI explains why it matters, and the runbook tells the team what to do next.

## 10. Scaling Path to PySpark / Hadoop / Cloud
[Back to TOC](#table-of-contents)
Pandas prototype
-> PySpark distributed processing
-> Hadoop/HDFS or S3/cloud data lake
-> partitioned time-series tables
-> scheduled ETL
-> dashboard/reporting layer

What scales:
- Same feature logic and risk framework.
- Larger data volume and wider endpoint coverage.
- More automated, scheduled, and governed pipeline operations.

## 11. 30-Second Answer
[Back to TOC](#table-of-contents)
I built a capacity forecasting workflow that converted telemetry trends into
early risk visibility for engineering and leadership. The original version used
Python, SQL, and Pandas to clean and bucket time-series data, compute trend and
headroom features, and rank systems by near-term risk. It was tested with data
quality checks, backtesting, and SME review, then communicated through
dashboards and executive summaries.

## 12. 2-Minute Answer
[Back to TOC](#table-of-contents)
The need was simple: capacity risk was too often surfaced late. I built a
practical forecasting pipeline using telemetry we already trusted. In the first
version, I extracted data with SQL and used Pandas for cleanup, timestamp
normalization, hourly and daily bucketing, and grouping by host, application,
and service. I engineered features like rolling averages, rolling max, growth
slope, and headroom percentage, then applied threshold logic and risk bands to
identify likely breach windows.

The output was built for decisions, not model novelty. Operations got ranked
risk views and trend dashboards, while leadership got concise summaries: what is
at risk, when, how confident we are, and what actions are recommended. I
validated with data quality checks, feature tests, time-ordered splits,
backtesting versus actuals, simple baseline comparison, and SME review of false
positives.

For scale, the pattern is straightforward: keep the same logic and move
distributed processing to PySpark, persist in Hadoop/HDFS or cloud data lake
structures with time partitions, run scheduled ETL, and feed the reporting
layer.

## 13. Whiteboard Architecture Diagram
[Back to TOC](#table-of-contents)
```text
[Telemetry Sources]
      |
      v
[SQL/Extract Layer]
      |
      v
[Pandas Data Prep]
(cleanup, timestamp normalization, bucketing)
      |
      v
[Feature Engineering]
(rolling avg/max, growth slope, headroom, breach flags)
      |
      v
[Risk Logic]
(thresholds, risk bands, forecast window ranking)
      |
      +--------------------+
      |                    |
      v                    v
[Ops Dashboard]      [Executive Summary]
```

## 14. What Not To Say
[Back to TOC](#table-of-contents)
- Do not claim advanced research-model invention.
- Do not claim full solo ownership of Hadoop/cloud platform engineering.
- Do not invent precision metrics you cannot defend.
- Do not let side topics (OpenTelemetry, Kubernetes, GPU, Terraform,
  CloudFormation) displace the core capacity story.
