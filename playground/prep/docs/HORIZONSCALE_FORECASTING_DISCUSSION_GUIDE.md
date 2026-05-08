# HorizonScale Forecasting Discussion Guide

## 1. Purpose
This guide is a fast interview talk track for HorizonScale forecasting work:
- what problem it solved
- what telemetry was used
- how data was processed
- which model types were used and why
- how outputs supported capacity and efficiency decisions

## 2. Safe Positioning
Based on the files inspected, I would position HorizonScale as a practical telemetry-to-forecast pipeline focused on capacity planning decisions, not deep research ML.

## 3. Business Problem
Manual capacity analysis is slow and reactive. Teams need earlier visibility into:
- likely bottlenecks
- sustained utilization pressure
- underutilized resources
- forecast variance versus actuals

## 4. Inputs and Features
Typical telemetry inputs discussed in this prep:
- sampled_at / timestamp
- service or host identifiers
- CPU utilization
- memory utilization
- sampled P95 latency
- request and error context
- allocated versus actual resource context
- cost fields and ownership tags where available

Common engineered features:
- AVG / MAX / P95 utilization
- headroom
- growth trend
- seasonal patterns
- forecast variance
- threshold breach indicators

## 5. Pipeline Flow
1. Read telemetry
2. Clean and normalize schema
3. Convert timestamp and numeric types
4. Aggregate by service/workload and time bucket
5. Create forecast features
6. Run model(s)
7. Compare with actuals and thresholds
8. Classify risk/waste
9. Export stakeholder-ready outputs

## 6. Model Framing
### Prophet
Good for trend and seasonality in time-series behavior.

### scikit-learn
Useful for feature-driven prediction/risk scoring and complementary model checks.

### Explainable baselines
Threshold and headroom logic are critical for trust with engineering and leadership.

## 7. Validation Approach
Practical validation approach:
- back-test on historical windows
- compare forecasted pressure with later actuals
- review false positives and false negatives
- keep models explainable for decision support

## 8. Capacity and Cost Impact
Forecasting supports better decisions by:
- preventing reactive over-provisioning
- finding rightsizing candidates
- highlighting sustained pressure earlier
- improving forecast-vs-actual planning loops

## 9. What To Say (20 seconds)
HorizonScale was a telemetry-driven capacity forecasting pipeline. I cleaned and aggregated utilization data, generated forecast features, used practical forecasting methods, and turned outputs into risk and planning recommendations.

## 10. What To Say (60 seconds)
I used HorizonScale to move from raw telemetry to repeatable planning outputs. The workflow cleaned and normalized time-series data, calculated features like P95 and headroom, ran forecasting methods, and compared output against thresholds and actual behavior. The point was not model complexity by itself; it was giving teams earlier, explainable signals for capacity risk, rightsizing, and cost-aware planning.

## 11. What Not To Overclaim
- Do not claim deep research ML ownership.
- Do not claim perfect model accuracy.
- Do not claim deep GCP production ownership.
- Do not claim deep Kubernetes platform-admin ownership.
- Do not claim enterprise-wide production scope unless Sean confirms.

## 12. Rapid Q&A
Q: Why Prophet?
A: Trend/seasonality handling and explainable time-series forecasting.

Q: Why scikit-learn?
A: Feature-driven predictive checks and practical risk scoring support.

Q: How did this support cost decisions?
A: By surfacing underutilization and over-pressure early so teams can rightsize safely.

Q: Batch or streaming?
A: Usually batch-first for planning and efficiency; streaming mainly for alerting.
