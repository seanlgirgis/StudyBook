# BOA Forecast Project Deep Dive

## 1. Plain-English Project Summary
This project converted raw telemetry into early capacity risk visibility so
engineering and management could act before incidents. It was designed for
operational decision support, with practical checks, clear risk language, and
repeatable reporting.

## 2. Original Pandas Version
Conceptual flow:
Telemetry extract
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

## 3. Input Telemetry Data
- Infrastructure utilization telemetry.
- Application/service throughput and performance indicators.
- Existing KPI feeds used by operations teams.
- Asset metadata for host, application, and service mapping.

## 4. Feature Engineering
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

## 5. Forecast Horizon / Risk Window
- Use a practical short-to-mid forecast window aligned to planning cycles.
- Report likely breach windows instead of only point predictions.
- Communicate confidence and assumptions in plain language.

## 6. Testing and Validation
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

Validation principle:
- Prefer reliable decision support over model complexity.

## 7. Output Reports and Dashboards
- Risk-ranked service and system views.
- Trend and headroom visuals for operations.
- Threshold/breach outlook for action planning.
- Weekly summary for leadership consumption.

## 8. Management Decision Support
- Translate telemetry into risk bands and action windows.
- Support decisions on scaling, optimization, and prioritization.
- Provide concise executive summaries with assumptions and confidence
  language.

## 9. Scaling Path to PySpark / Hadoop / Cloud
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

## 10. 30-Second Answer
I built a capacity forecasting workflow that converted telemetry trends into
early risk visibility for engineering and leadership. The original version used
Python, SQL, and Pandas to clean and bucket time-series data, compute trend and
headroom features, and rank systems by near-term risk. It was tested with data
quality checks, backtesting, and SME review, then communicated through
dashboards and executive summaries.

## 11. 2-Minute Answer
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

## 12. Whiteboard Architecture Diagram
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

## 13. What Not To Say
- Do not claim advanced research-model invention.
- Do not claim full solo ownership of Hadoop/cloud platform engineering.
- Do not invent precision metrics you cannot defend.
- Do not let side topics (OpenTelemetry, Kubernetes, GPU, Terraform,
  CloudFormation) displace the core capacity story.