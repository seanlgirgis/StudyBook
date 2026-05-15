# BOA Forecast Project Deep Dive

## 1. Plain-English Project Summary
This project converted raw telemetry into early capacity risk visibility so
engineering and management could act before incidents. It was designed for
operational decision support, with practical checks, clear risk language, and
repeatable reporting.


## 2. Original Reporting Automation Foundation
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
- Infrastructure utilization telemetry.
- Application/service throughput and performance indicators.
- Existing KPI feeds used by operations teams.
- Asset metadata for host, application, and service mapping.

## 5. Feature Engineering
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

## 6. Forecast Horizon / Risk Window
- Use a practical short-to-mid forecast window aligned to planning cycles.
- Report likely breach windows instead of only point predictions.
- Communicate confidence and assumptions in plain language.

## 7. Testing and Validation
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
- Risk-ranked service and system views.
- Trend and headroom visuals for operations.
- Threshold/breach outlook for action planning.
- Weekly summary for leadership consumption.

## 9. Management Decision Support
- Translate telemetry into risk bands and action windows.
- Support decisions on scaling, optimization, and prioritization.
- Provide concise executive summaries with assumptions and confidence
  language.

## BOA Informal Signal and CBFR Mapping
[Back to TOC](#table-of-contents)
Informal BOA team signal suggests the interview may care heavily about
production capacity planning, quarterly Capacity Baseline Forecast Reports
(CBFR), critical applications and clusters, BMC TrueSight/TSCO-style data,
dashboarding, and performance-test inputs such as TPS and safety factors.

Use this as alignment language, not as a claim that every detail is confirmed
for the specific role.

How HorizonScale maps:
- CBFR / quarterly report:
  HorizonScale produces baseline, forecast, risk band, owner, and action timing.
- Excel forecasting:
  The original reporting automation story shows how Excel-heavy workflows can
  become repeatable Python/Pandas pipelines.
- BMC TrueSight / TSCO:
  Directly aligned with enterprise capacity telemetry and baseline reporting.
- Dashboarding:
  Forecast outputs should be structured for Power BI, Tableau, or enterprise
  reporting tools.
- Production-only scope:
  Emphasize production critical applications, thresholds, safety margin,
  remediation timing, and operational stability.
- Performance testing / TPS:
  Use test results as engineered limits and compare production telemetry
  against those limits with safety factors.
- AWS / Kubernetes:
  Treat as future or adjacent capacity contexts, not deep ownership claims.

Safe spoken bridge:

```text
This sounds close to capacity baseline forecasting work: production telemetry,
critical applications, BMC-style capacity data, quarterly reports, dashboarding,
and planning decisions. That maps well to my background because I have worked
with enterprise capacity data, Python/Pandas reporting automation, forecasting,
KPI views, and management-ready risk summaries.
```

## 10. Scaling Path to PySpark / Hadoop / Cloud
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
I built a capacity forecasting workflow that converted telemetry trends into
early risk visibility for engineering and leadership. The original version used
Python, SQL, and Pandas to clean and bucket time-series data, compute trend and
headroom features, and rank systems by near-term risk. It was tested with data
quality checks, backtesting, and SME review, then communicated through
dashboards and executive summaries.

## 12. 2-Minute Answer
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
- Do not claim advanced research-model invention.
- Do not claim full solo ownership of Hadoop/cloud platform engineering.
- Do not invent precision metrics you cannot defend.
- Do not let side topics (OpenTelemetry, Kubernetes, GPU, Terraform,
  CloudFormation) displace the core capacity story.
