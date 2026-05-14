# Capacity Forecasting Playbook

## Objective
Use telemetry-driven forecasting to surface capacity risk early, rank
priorities, and support engineering and management decisions.

## 1. Telemetry Inputs
- Infrastructure telemetry: CPU, memory, storage, and utilization trends.
- Application/service telemetry: throughput, latency-adjacent load indicators,
  transaction volume.
- KPI and threshold context used by operations.
- Asset metadata: host, application, service, and ownership mapping.

## 2. Cleanup And Normalization
- Align timestamps to a consistent timezone and format.
- Remove duplicates and stale asset records.
- Handle missing fields and impossible values.
- Validate telemetry joins against asset/service mappings.

Operator note: data quality happens before model logic.

## 3. Time Bucketing
- Bucket into hourly windows for operational signal.
- Bucket into daily windows for planning signal.
- Preserve bucket boundaries for consistent backtesting.

## 4. Grouping Dimensions
- Group by host/application/service.
- Keep grouping stable so risk ranking maps to accountable teams.
- Use grouping keys consistently through feature, risk, and report layers.

## Cohort-Based Forecasting
- Grouping first, forecast second.
- Validate by cohort against actual behavior and threshold outcomes.
- Tune only where backtesting proves the need.
- Keep settings explainable and avoid blind per-server hand tuning at scale.
- Use cohort outputs to support operational decisions and prioritization.

## 5. Feature Engineering
Core explainable features:
- Rolling averages: sustained trend behavior.
- Rolling peaks: stress behavior and peak pressure.
- Growth slope: rate of change over time.
- Headroom to threshold: remaining margin before breach.
- Threshold breach flags: explicit at-risk signals.
- Risk bands: low/medium/high style operational categories.

## 6. Forecasting And Risk Scoring
- Use short-to-mid horizon windows aligned to planning cycles.
- Combine trend, peaks, slope, and headroom into risk logic.
- Rank entities by urgency and likely breach timing.
- Prioritize sustained trend plus shrinking headroom over single spikes.

## 7. Dashboards And Reporting
Operations output:
- Ranked risk view by service/system.
- Trend + headroom visuals.
- Near-term breach outlook.

Management output:
- What is at risk.
- When risk is likely to materialize.
- Confidence/assumption language.
- Recommended actions and priority order.

## 8. Validation
Data quality testing:
- Missing timestamp checks.
- Duplicate detection.
- Stale asset checks.
- Impossible value checks.
- Bucket integrity checks.

Feature validation:
- Rolling-window correctness checks.
- Slope and headroom calculation checks.
- Breach flag and band assignment checks.

Forecast validation:
- Time-ordered evaluation.
- Backtesting predicted vs actual outcomes.
- Simple baseline comparison.
- SME/business review for false positives and actionability.

## 9. Pandas To PySpark/Hadoop/Cloud Scale-Up Path
Prototype stage:
- SQL + Pandas for fast iteration and explainability.

Scale stage:
- PySpark for distributed feature generation.
- Hadoop/HDFS or cloud data lake storage patterns.
- Partitioned time-series datasets.
- Scheduled ETL and governed output tables.
- Dashboard/reporting consumers on top of stable outputs.

Guardrail:
- Present this as architecture evolution and collaborative platform scaling,
  not full solo ownership of all data platform layers.

## 10. Interview-Safe Language
- I built and validated practical forecasting decision support.
- I focus on explainable features and operational outcomes.
- I avoid overclaiming deep ML research or full platform engineering ownership.
