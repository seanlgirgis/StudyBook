# BOA Interview Q and A: Capacity Forecasting (Full Defense)

## Table of Contents

- [1) Walk me through the capacity forecasting workflow.](#1-walk-me-through-the-capacity-forecasting-workflow)
- [2) What problem were you solving?](#2-what-problem-were-you-solving)
- [3) What data did you use?](#3-what-data-did-you-use)
- [4) How did the original reporting pipeline start?](#4-how-did-the-original-reporting-pipeline-start)
- [5) How did you move from Excel/manual reports to Python?](#5-how-did-you-move-from-excelmanual-reports-to-python)
- [6) Why SQLite or lightweight structured storage?](#6-why-sqlite-or-lightweight-structured-storage)
- [7) How did Streamlit or team reporting fit?](#7-how-did-streamlit-or-team-reporting-fit)
- [8) What features did you engineer?](#8-what-features-did-you-engineer)
- [9) Why rolling averages and rolling peaks?](#9-why-rolling-averages-and-rolling-peaks)
- [10) What is headroom to threshold?](#10-what-is-headroom-to-threshold)
- [11) How did you define risk bands?](#11-how-did-you-define-risk-bands)
- [12) Why Prophet?](#12-why-prophet)
- [13) How did Prophet help with seasonality?](#13-how-did-prophet-help-with-seasonality)
- [14) How did you handle month-end, quarter-end, or holiday effects?](#14-how-did-you-handle-month-end-quarter-end-or-holiday-effects)
- [15) How did you validate the model?](#15-how-did-you-validate-the-model)
- [16) Explain 18-month training and 6-month testing.](#16-explain-18-month-training-and-6-month-testing)
- [17) Why not randomly sample time-series data?](#17-why-not-randomly-sample-time-series-data)
- [18) What metrics did you use to compare forecast vs actual?](#18-what-metrics-did-you-use-to-compare-forecast-vs-actual)
- [19) What does good enough mean?](#19-what-does-good-enough-mean)
- [20) What if the model missed the test period?](#20-what-if-the-model-missed-the-test-period)
- [21) Did you forecast all servers together?](#21-did-you-forecast-all-servers-together)
- [22) How did you group thousands of servers?](#22-how-did-you-group-thousands-of-servers)
- [23) What is cohort-based forecasting?](#23-what-is-cohort-based-forecasting)
- [24) Did each server have a custom model?](#24-did-each-server-have-a-custom-model)
- [25) How did you avoid overfitting?](#25-how-did-you-avoid-overfitting)
- [26) How did SMEs validate the forecast?](#26-how-did-smes-validate-the-forecast)
- [27) How did this become dashboards and reports?](#27-how-did-this-become-dashboards-and-reports)
- [28) How did leadership use the output?](#28-how-did-leadership-use-the-output)
- [29) How did this support budget or FinOps-style discussions?](#29-how-did-this-support-budget-or-finops-style-discussions)
- [30) How would you scale this from Pandas to PySpark/Hadoop/cloud?](#30-how-would-you-scale-this-from-pandas-to-pysparkhadoopcloud)
- [31) What did you own directly?](#31-what-did-you-own-directly)
- [32) Where did you partner with platform/data teams?](#32-where-did-you-partner-with-platformdata-teams)
- [33) What would you modernize now?](#33-what-would-you-modernize-now)
- [34) What are risky claims to avoid?](#34-what-are-risky-claims-to-avoid)
- [35) Give me the 60-second version.](#35-give-me-the-60-second-version)


## 1) Walk me through the capacity forecasting workflow.
[Back to TOC](#table-of-contents)
I start with telemetry extraction, cleanup, and timestamp normalization. Then I
bucket data hourly and daily, group by host/application/service, engineer
capacity features, and run forecasting plus risk ranking. The result is not only
a chart. It becomes dashboards, exception lists, and management-ready risk
summaries with timing and ownership context.

## 2) What problem were you solving?
[Back to TOC](#table-of-contents)
The core problem was late visibility into capacity risk. Manual reviews were
too slow and reactive. We needed earlier warning on low headroom and likely
threshold pressure so teams could plan remediation before incidents.

## 3) What data did you use?
[Back to TOC](#table-of-contents)
I used infrastructure and application telemetry, utilization and threshold
context, plus asset mapping for ownership. In practice that meant timestamps,
host identifiers, service/application mapping, and core usage indicators needed
for trend, headroom, and risk interpretation.

## 4) How did the original reporting pipeline start?
[Back to TOC](#table-of-contents)
It started from manual report cycles with repeated spreadsheet work. Data pulls,
cleanup, and rollups were taking too much operator time. That became the first
improvement target before the forecasting layer.

## 5) How did you move from Excel/manual reports to Python?
[Back to TOC](#table-of-contents)
I moved repeated cleanup and shaping steps into Python scripts so the same logic
ran consistently each cycle. That reduced manual variance and created reusable
structured inputs for forecasting and risk ranking.

## 6) Why SQLite or lightweight structured storage?
[Back to TOC](#table-of-contents)
For team-level reporting and iteration speed, lightweight structured storage was
practical. It gave us consistent schemas and repeatable queries without adding
heavy platform overhead early in the workflow.

## 7) How did Streamlit or team reporting fit?
[Back to TOC](#table-of-contents)
Team-facing reporting views helped operational users consume trend and risk
output quickly. The point was visibility and decision support, not front-end
complexity. It made forecast outputs easier to review with SMEs and leadership.

## 8) What features did you engineer?
[Back to TOC](#table-of-contents)
Key features included rolling averages, rolling peaks, recent maximum, growth
slope, volatility, headroom to threshold, breach flags, and risk bands. These
features made the signal more actionable than raw utilization values alone.

## 9) Why rolling averages and rolling peaks?
[Back to TOC](#table-of-contents)
Rolling averages help identify sustained pressure. Rolling peaks show stress
events and upper-bound behavior. Together they reduce the chance of treating a
single spike the same as a sustained trend toward saturation.

## 10) What is headroom to threshold?
[Back to TOC](#table-of-contents)
Headroom is the remaining margin before crossing an operational threshold. It
turns utilization into timing relevance. A moderate trend with low headroom can
be higher operational risk than a high value with stable headroom.

## 11) How did you define risk bands?
[Back to TOC](#table-of-contents)
Risk bands were practical categories based on trend direction, headroom, breach
signals, and near-term timing. The goal was communication clarity: low, medium,
or high-style prioritization that teams could act on quickly.

## 12) Why Prophet?
[Back to TOC](#table-of-contents)
Prophet was part of the real forecasting work because it handled trend and
seasonality in an explainable way. It fit capacity planning needs without
requiring a deep research-model workflow.

## 13) How did Prophet help with seasonality?
[Back to TOC](#table-of-contents)
It helped model recurring behavior patterns that simple straight-line methods
miss. Weekly rhythms, month-end effects, and periodic workload changes were
easier to represent while keeping the output interpretable.

## 14) How did you handle month-end, quarter-end, or holiday effects?
[Back to TOC](#table-of-contents)
I treated business-calendar effects as first-class context during tuning and
validation. We checked whether forecast behavior aligned with known calendar
patterns and SME input before trusting the output for planning decisions.

## 15) How did you validate the model?
[Back to TOC](#table-of-contents)
Validation included data quality checks, feature calculation checks, holdout
testing, and practical review of false positives and false negatives. I also
compared forecasted behavior against later actual outcomes and SME feedback.

## 16) Explain 18-month training and 6-month testing.
[Back to TOC](#table-of-contents)
With 24 months of history, I would train on the first 18 months and hold out
the next 6 months for testing. Then I compare forecasted values or risk bands
against actual outcomes. If the backtest is reasonable, I retrain on full
history and forecast the next 3 to 6 months.

## 17) Why not randomly sample time-series data?
[Back to TOC](#table-of-contents)
Time-series needs order preserved. Random sampling can leak future behavior into
training and create false confidence. Holdout testing simulates real future use.

## 18) What metrics did you use to compare forecast vs actual?
[Back to TOC](#table-of-contents)
I used MAE, MAPE where appropriate, RMSE where useful, and bias checks for
over-forecasting or under-forecasting. Operationally, I also tracked risk-band
accuracy, false positives, false negatives, and threshold-crossing accuracy.

## 19) What does good enough mean?
[Back to TOC](#table-of-contents)
Good enough is not only statistical fit. It means operational usefulness:
identify low headroom and serious threshold risk early enough to act. Tolerance
depends on service criticality and planning impact.

## 20) What if the model missed the test period?
[Back to TOC](#table-of-contents)
I adjusted practical levers like changepoint flexibility, seasonality behavior,
aggregation level, outlier handling, and calendar effects. Then I reran holdout
testing and kept changes only when decision signal quality improved.

## 21) Did you forecast all servers together?
[Back to TOC](#table-of-contents)
No. At scale, one pooled model across everything creates noise. We grouped
first, forecast second. We did not let one model try to explain thousands of
different server behaviors at once.

## 22) How did you group thousands of servers?
[Back to TOC](#table-of-contents)
I grouped by function, ownership, usage pattern, criticality, and workload
behavior. A batch platform, API tier, database layer, and seasonal reporting
service do not share the same curve, so they should not be forecast as one pool.

## 23) What is cohort-based forecasting?
[Back to TOC](#table-of-contents)
It is behavior-based grouping before forecasting. Forecast and validation happen
within cohorts that behave similarly. Backtesting then shows where a cohort
needs adjustment without forcing blind per-server hand tuning.

## 24) Did each server have a custom model?
[Back to TOC](#table-of-contents)
Not blindly. Hand-tuning thousands of individual models can overfit and become
hard to operate. The safer pattern is explainable cohort settings and focused
exception tuning only where validation shows clear need.

## 25) How did you avoid overfitting?
[Back to TOC](#table-of-contents)
I used holdout backtesting, simple baseline comparison, cohort-level settings,
and SME review. I avoided unnecessary complexity and kept the target practical:
better capacity decisions, not model novelty.

## 26) How did SMEs validate the forecast?
[Back to TOC](#table-of-contents)
SMEs confirmed whether flagged risks matched real operating behavior, explained
business events, flagged retirement or migration context, and validated whether
recommended actions made operational sense.

## 27) How did this become dashboards and reports?
[Back to TOC](#table-of-contents)
Forecast and risk outputs were turned into ranked views, exception lists, trend
panels, and summary reports. The output was organized around action timing and
ownership so teams could prioritize confidently.

## 28) How did leadership use the output?
[Back to TOC](#table-of-contents)
Leadership used concise risk summaries to guide timing and prioritization. The
reports supported decisions on remediation windows, capacity planning, and
resource allocation with clearer risk language.

## 29) How did this support budget or FinOps-style discussions?
[Back to TOC](#table-of-contents)
I was not the FinOps owner, but forecasting outputs supported those
conversations. Trend, headroom, and risk windows gave finance, platform, and
application stakeholders more factual inputs for planning tradeoffs.

## 30) How would you scale this from Pandas to PySpark/Hadoop/cloud?
[Back to TOC](#table-of-contents)
Keep the core logic and move heavier data processing to distributed patterns.
Pandas is strong for prototype speed and explainability; PySpark/Hadoop/cloud
patterns are the scale-up path for larger history and broader coverage.

## 31) What did you own directly?
[Back to TOC](#table-of-contents)
I can directly defend telemetry shaping, timestamp normalization, feature
engineering, forecasting workflow choices, holdout validation approach, risk
ranking, and reporting outputs for decision support.

## 32) Where did you partner with platform/data teams?
[Back to TOC](#table-of-contents)
For larger-scale data-platform concerns, I partnered with platform and data
teams. I focus on capacity logic and operational decision support while aligning
with broader engineering ownership boundaries.

## 33) What would you modernize now?
[Back to TOC](#table-of-contents)
I would strengthen data contracts, automate more quality gates, and productionize
cohort pipelines at scale. I would keep the explainable forecasting core and
improve governance, repeatability, and decision-focused reporting.

## 34) What are risky claims to avoid?
[Back to TOC](#table-of-contents)
Avoid claiming deep ML research ownership, full platform ownership, or blanket
per-server custom modeling. Avoid overstating scikit-learn as broad production
use. Keep claims anchored to real workflow ownership and validated outcomes.

## 35) Give me the 60-second version.
[Back to TOC](#table-of-contents)
I built a practical capacity forecasting workflow that turned telemetry into
early risk visibility for engineering and leadership. The foundation was SQL,
Python, and Pandas with explainable features like trend, headroom, and risk
bands. Prophet was part of real forecasting work, and validation used holdout
testing, predicted-vs-actual checks, and SME review. The output was dashboards,
exception lists, and ranked risk views that supported remediation timing and
planning decisions. At scale, we grouped first and forecast second, then used
PySpark/Hadoop/cloud patterns as the architecture path when needed.


## 36) How does this map to BOA-style CBFR work?
[Back to TOC](#table-of-contents)
If the team produces a Capacity Baseline Forecast Report, I would treat that as
the decision product. The work behind it is familiar: collect production
telemetry, map it to applications, clusters, and owners, calculate baseline,
trend, headroom, threshold risk, safety margin, and forecasted breach window,
then publish a clear planning report.

That maps well to my experience because I have worked with enterprise capacity
and APM data, reporting automation, forecasting workflows, and stakeholder-ready
risk summaries.

The strongest bridge is this: I am comfortable with Excel-heavy forecasting as
a starting point, but I can help make the process more repeatable with Python,
Pandas, validation checks, and dashboard-ready outputs.

## 37) How do performance testing, TPS, and safety factors fit?
[Back to TOC](#table-of-contents)
Performance testing gives a controlled view of throughput limits. If a
performance testing or BreakPoint-style feed provides TPS, saturation behavior,
or upper-limit results, I would use that as an input to capacity planning.

Production telemetry shows real usage. Performance testing shows engineered
limits. Together, they help define thresholds and safety factors.

I would not plan production capacity right up to the hard limit. I would use
safety margin because banking workloads can have spikes, month-end and
quarter-end cycles, business events, and unexpected demand.

## 38) How would you support dashboarding?
[Back to TOC](#table-of-contents)
Dashboarding is important because the forecast only creates value if teams can
consume it. I would design dashboard-ready outputs around the decision: which
application or cluster is at risk, when, who owns it, what threshold or safety
factor is involved, and what action is recommended.

A strong capacity dashboard should show baseline, current trend, forecasted
risk window, headroom, threshold, safety margin, risk band, owner, and
remediation status.

I can structure the underlying data for tools like Power BI, Tableau, or other
enterprise dashboards. I would not claim ownership of every dashboard platform,
but I can define the data model and decision views those dashboards need.

## 39) How do BMC TrueSight, TSCO, Helix, Splunk, AWS, and Kubernetes fit?
[Back to TOC](#table-of-contents)
BMC TrueSight and TSCO are directly aligned with my background. I understand
the capacity workflow around production telemetry, baseline reports, threshold
views, forecasting, and planning.

If Helix is part of the environment, I would treat it as a related BMC service
or operations platform context and learn the exact implementation. I would not
overclaim Helix ownership unless the role needs it and I have validated the
details.

Splunk, AWS, and Kubernetes are useful adjacent signal sources or future
capacity contexts. For example, AWS migration and Kubernetes monitoring can add
new telemetry sources, but the core capacity logic remains the same: collect,
validate, map ownership, define KPIs, forecast risk, and publish decision
views.

## 40) How would you describe your fit if the team is not super technical?
[Back to TOC](#table-of-contents)
I would position myself as the technical capacity person who can meet the team
where they are.

If the current process uses Excel, quarterly reports, BMC capacity data, and
manual review, I can understand that workflow and improve it without dismissing
it. I can help make the process more repeatable with Python, Pandas, structured
data, validation checks, and dashboard-ready outputs.

My value is translating between operations, data, forecasting, dashboards, and
management decisions. I can support the team technically while still explaining
the work in plain planning language.
