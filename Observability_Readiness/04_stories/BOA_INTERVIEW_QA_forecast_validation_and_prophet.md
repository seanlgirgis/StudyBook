# BOA Interview Q and A: Forecast Validation, Prophet, and Cohorting

## 1. How did you test the forecast?
I used time-based holdout testing, not random sampling. A typical setup was
24 months of history, train on the first 18 months, and test on the next
6 months. Then I compared forecasted values and risk bands against what
actually happened in that holdout period. After that check, I retrained on
the full history and produced the next 3 to 6 months of forecast output.

## 2. Why not randomly sample the data?
Time-series data must preserve order. Random sampling can leak future behavior
into training and make results look better than they are. A holdout period is
closer to reality because it simulates the future we are trying to predict.

## 3. What metrics did you use to compare forecast to actuals?
I used multiple views, depending on the metric and the audience:
- MAE for average absolute error.
- MAPE where appropriate and stable for the denominator.
- RMSE where larger misses needed extra visibility.
- Bias checks for over-forecasting versus under-forecasting.
- Risk-band accuracy for operational decision support.
- False positives and false negatives on at-risk flags.
- Threshold-crossing accuracy for breach timing confidence.

## 4. What does "good enough" mean?
Good enough was not only statistical accuracy. It also meant operational
usefulness. If the forecast reliably identified low headroom and serious
threshold risk early enough for action, it was useful. Acceptable error was
also tied to system criticality, because critical services need tighter
confidence than low-impact workloads.

## 5. What did you adjust when the model missed the test period?
When holdout results missed, I adjusted practical levers:
- Changepoint flexibility.
- Seasonality mode.
- Seasonality strength.
- Holiday and business-calendar effects.
- Aggregation level.
- Outlier handling.
- Caps/floors or headroom framing for bounded metrics.

Then I re-ran holdout testing and checked whether changes improved both forecast
fit and operational signal quality.

## 6. Did every system use the same Prophet settings?
No, not blindly. I grouped systems into behavior-based cohorts such as
steady-state, growth, seasonal, batch-heavy, noisy, critical, and
retirement/migration patterns. I tuned by cohort only when backtesting showed
clear need. I avoided blind per-server tuning because it can overfit and become
hard to operate at scale.

## 6a. Did you forecast all servers together?
No. At large scale, I would use cohort-based forecasting. I would not put all
servers into one pool because a batch platform, API tier, database layer, and
seasonal reporting service behave differently. I would group systems by
function, ownership, usage pattern, and criticality, then forecast and validate
within those cohorts.

## 6b. Did each server have its own custom model?
Not blindly. I would avoid hand-tuning thousands of individual models because
that can overfit and become hard to operate. The safer pattern is to use
explainable cohorts, validate the forecast against actuals, and tune only the
groups or exceptions that fail validation.

## 7. How did you group systems?
I grouped by a combination of:
- Behavior pattern.
- Business calendar sensitivity.
- Criticality.
- Application/service ownership.
- Data quality profile.
- Workload type.

That made settings more explainable and easier to support operationally.

## 8. How did you avoid overfitting?
I used holdout testing, simple baseline comparison, and avoided unnecessary
per-server tuning. I preferred explainable cohort settings and validated
results with SMEs. The final check was practical usefulness: does it improve
real capacity decisions without adding fragile model complexity?

## 9. How did Prophet help?
Prophet helped with seasonality-aware forecasting and practical explainability.
It handled weekly, monthly, quarter-end, and business-calendar behavior better
than a flat trend-only view. I used it as a planning tool for capacity and risk,
not as magic.

## 10. How did SMEs validate the results?
SMEs validated whether flagged systems matched real operating behavior, explained
business events that affected telemetry, identified systems already planned for
retirement or migration, and confirmed whether recommended actions made sense in
the real operating context.

## 11. How did this support management?
It translated technical telemetry into management decision support:
- Dashboards and reports for trend and headroom visibility.
- Exception lists for immediate review.
- Ranked risk views for prioritization.
- Clear risk language and remediation timing.
- Better input to budget and capacity planning conversations.

## One-minute answer if asked about validation
I validated the forecast with time-based holdout testing, not random sampling.
A typical cycle was 24 months of history, train on 18 months, and test on
the next 6 months. I compared forecasted values and risk bands against later
actual behavior, then checked bias, threshold-crossing accuracy, and false
positive/negative balance. If results were off, I adjusted practical settings
like changepoint flexibility, seasonality behavior, calendar effects, and
aggregation level, then re-tested. I also used SME review to confirm that
flagged risk matched real operations and planned changes. The goal was not
research-grade modeling. The goal was reliable, explainable decision support
for capacity risk and management planning.
