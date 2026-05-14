# Story: Capacity Forecasting Horizon Scale

## STAR Story

### Situation
Capacity risk was often identified late, which compressed remediation windows and made planning harder for operations and leadership. The environment had broad telemetry coverage, including workflows across 6,000+ infrastructure endpoints, but decision support needed to be more predictive and easier to act on.

### Task
Build a practical capacity forecasting workflow that converted telemetry trends into early, ranked risk visibility and management-ready reporting.

### Action
I built the first version with SQL, Python, and Pandas so we could iterate quickly and keep logic explainable.

Build flow I owned directly:
- Ingested telemetry and aligned it with asset metadata.
- Normalized timestamps and cleaned missing/duplicate/stale records.
- Bucketed data into hourly and daily windows.
- Grouped by host/application/service.
- Engineered rolling averages, rolling peaks, growth slope, headroom-to-threshold, and breach flags.
- Applied risk bands and ranking logic to identify near-term capacity pressure.
- Published dashboard views and concise management summaries.

Validation approach:
- Data quality checks before feature generation.
- Feature logic verification for rolling, slope, headroom, and flags.
- Time-ordered evaluation and backtesting predicted vs actual.
- Naive baseline comparison.
- SME/business review to reduce false positives and improve actionability.

### Result
The outcome was earlier and clearer risk visibility for capacity decisions. Teams had a ranked view of where to act first, and leadership had plain-language summaries that connected risk timing, confidence, and recommended actions.

I present this as operator-focused decision support, not as deep research ML.

## Honest Positioning
- I can defend the end-to-end forecasting logic and validation workflow.
- I do not claim novel research-model invention.
- I describe PySpark/Hadoop/cloud expansion as a safe scale-up pattern and collaborative platform evolution.

## What I Learned
- Explainable features drive trust faster than opaque complexity.
- Data quality discipline has as much impact as forecast math.
- Risk ranking is most useful when tied directly to ownership dimensions.
- Executive reporting needs short, explicit confidence language.

## How I Would Modernize It Now
- Keep the same forecasting and risk logic, but productionize feature pipelines in PySpark.
- Add stronger data contracts and automated quality gates.
- Standardize partitioned time-series storage in Hadoop/HDFS or cloud lake patterns.
- Add repeatable scheduled pipelines and lineage/governance checks.
- Keep dashboards focused on action windows, not metric overload.