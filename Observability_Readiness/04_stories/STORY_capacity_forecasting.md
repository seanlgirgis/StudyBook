# Story: Capacity Forecasting

## 60-Second Version
I built a practical capacity forecasting workflow to surface risk earlier and support better operational decisions. I used SQL and Python/Pandas to process telemetry, normalize time, engineer features like rolling trend, growth slope, and headroom, then rank systems by near-term capacity risk. The output fed dashboards and concise management reporting, with validation based on data quality checks, time-ordered backtesting, baseline comparison, and SME review.

## 2-Minute Version
The problem was late visibility into capacity risk. I built a forecast workflow around telemetry we already used operationally. The original implementation was Python and Pandas over SQL extracts. The flow was cleanup, timestamp normalization, hourly/daily buckets, grouping by host/application/service, feature engineering for rolling averages, rolling peaks, growth slope, and headroom, then threshold and risk-band logic to rank likely breach windows.

This was designed as decision support, not research ML. I tested both data quality and forecast behavior: missing/duplicate/stale checks, time bucket validation, feature calculation tests, time-ordered split, backtesting predicted vs actual, naive baseline comparison, and SME/business review of false positives. The output supported both operations and management: ranked risk views, trend/headroom dashboards, and executive summaries with assumptions and confidence language.

For scale, I can explain how to keep the same logic and move from Pandas to PySpark, then persist in Hadoop/HDFS or cloud data lake patterns with partitioned time-series tables and scheduled ETL.

## STAR Format
### Situation
Capacity risk was often discovered too late, creating incident and planning pressure.

### Task
Create a repeatable forecasting process that translated telemetry into earlier and actionable capacity risk signals.

### Actions
- Built original pipeline with SQL + Python/Pandas.
- Engineered interpretable features: trend, peaks, slope, headroom, breach flags.
- Implemented risk ranking and forecast windows by system/service.
- Added validation discipline: quality checks, backtesting, baseline comparison, SME review.
- Delivered dashboards and executive-ready summaries.

### Results
- Earlier visibility into likely capacity risk windows.
- Better prioritization of scaling and optimization actions.
- More consistent communication between engineering and management.

## Original Pandas Version
Telemetry extract
-> Pandas cleanup
-> timestamp normalization
-> hourly/daily buckets
-> group by host/application/service
-> rolling averages / peaks / growth rates
-> threshold/headroom calculation
-> risk ranking
-> dashboard/report/executive summary

## PySpark/Hadoop/Cloud Scaling Version
- Keep feature and risk logic consistent.
- Move heavy transforms to PySpark distributed jobs.
- Store data in Hadoop/HDFS or S3/cloud data lake.
- Use partitioned time-series datasets and scheduled ETL orchestration.
- Feed dashboard/reporting layer with governed outputs.

## Testing and Validation Details
- Missing timestamp, duplicate, stale asset, and impossible value checks.
- Time bucket and feature calculation validation.
- Time-order-respecting train/test split.
- Backtesting predicted vs actual.
- Naive baseline comparison.
- SME/business validation and false positive review.

## Safe Wording (No Invented Metrics)
- I avoid fabricated precision metrics and focus on decision outcomes.
- I describe practical ownership clearly and acknowledge collaborative platform scaling work.
- I position the project as operator-focused forecasting, not deep research ML.
