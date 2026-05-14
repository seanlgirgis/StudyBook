# BOA Interview Q and A: Capacity Forecasting

## 1) End-to-End Build
Question:
How did you build the forecasting workflow end to end?

Strong safe answer:
I built it as an operator-focused workflow: telemetry ingestion, timestamp normalization, hourly and daily bucketing, grouping by host/application/service, feature engineering for trend and headroom, then risk bands and ranking. The outputs were dashboards for operations and concise summaries for leadership.

Risky answer to avoid:
I built a fully autonomous AI forecasting platform that replaced planning teams.

## 2) Telemetry Inputs
Question:
What inputs did you use?

Strong safe answer:
I used infrastructure and application telemetry, KPI context, and asset metadata so risk signals stayed tied to accountable systems and services.

Risky answer to avoid:
I used every enterprise data source across the company in real time.

## 3) Timestamp Normalization And Bucketing
Question:
Why were timestamp normalization and hourly/daily buckets important?

Strong safe answer:
Without normalized time, trend and backtesting logic becomes unreliable. Hourly buckets helped with operational signal, and daily buckets helped with planning signal.

Risky answer to avoid:
We skipped most time cleanup because the model handled it automatically.

## 4) Feature Engineering
Question:
Which features mattered most?

Strong safe answer:
Rolling averages for sustained trend, rolling peaks for stress behavior, growth slope for direction, and headroom-to-threshold for urgency. Breach flags and risk bands turned those signals into clear action priorities.

Risky answer to avoid:
The model discovered hidden features that I cannot explain.

## 5) Forecasting Logic And Risk Ranking
Question:
How did you score and rank risk?

Strong safe answer:
I used explainable risk logic combining trend, peaks, slope, and headroom. Then I ranked by near-term breach risk and urgency windows so teams could act in order.

Risky answer to avoid:
It was purely black-box scoring with no interpretable rationale.

## 6) ML Depth And Ownership
Question:
Was this advanced machine learning?

Strong safe answer:
I position it as practical forecasting decision support, not deep research ML. The value came from explainable features, disciplined validation, and useful operational outputs.

Risky answer to avoid:
I invented a novel ML algorithm that outperformed all standard methods.

## 7) Data Quality
Question:
How did you handle data quality?

Strong safe answer:
I ran missing timestamp checks, duplicate checks, stale asset checks, impossible value checks, and bucket integrity checks before relying on forecast outputs.

Risky answer to avoid:
We trusted raw telemetry and validated only if something looked wrong.

## 8) Validation And Backtesting
Question:
How did you validate predictions?

Strong safe answer:
I used time-ordered evaluation, backtesting predicted vs actual outcomes, naive baseline comparison, and SME review of false positives.

Risky answer to avoid:
I validated by visual inspection only, and we did not compare against baselines.

## 9) Pandas Choice
Question:
Why Pandas first instead of Spark first?

Strong safe answer:
Pandas was the fastest way to iterate on feature logic and validate decision value early. Once logic stabilized, the same pattern can scale to distributed processing.

Risky answer to avoid:
Pandas was already enterprise-scale enough, so we did not need a scale plan.

## 10) PySpark, Hadoop, Cloud Scale-Up
Question:
How would you scale this for larger volume?

Strong safe answer:
Keep the same feature and risk logic, move heavy transforms to PySpark, store partitioned time-series data in Hadoop/HDFS or cloud lake patterns, and run scheduled governed pipelines feeding dashboards.

Risky answer to avoid:
I single-handedly built and operated the entire enterprise Hadoop and cloud platform stack.

## 11) Executive Reporting
Question:
What did leadership receive?

Strong safe answer:
Leadership got concise risk summaries: what is at risk, likely timing, confidence framing, and recommended action priorities.

Risky answer to avoid:
I only delivered raw metrics and expected executives to interpret details themselves.

## 12) KPI Framing
Question:
How did KPI reporting tie into forecasting?

Strong safe answer:
KPIs provided context for whether forecasted risk aligned with operational priorities and service criticality. They helped anchor ranking and communicate impact clearly.

Risky answer to avoid:
KPI reporting was separate and not relevant to forecasting decisions.

## 13) Scope Guardrail If Asked About Other Tools
Question:
Did this involve OpenTelemetry, Kubernetes, GPU, Terraform, CloudFormation, Prometheus, or Grafana ownership?

Strong safe answer:
For this story, I keep the focus on enterprise capacity forecasting and telemetry decision support. I can discuss adjacent patterns, but I do not overstate production ownership where it was not my primary scope.

Risky answer to avoid:
Yes, I led production ownership for all those platforms end to end.