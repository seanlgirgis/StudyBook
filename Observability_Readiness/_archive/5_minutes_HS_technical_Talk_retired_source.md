Retired source draft. Useful content was consolidated into BOA_30_2_5_MINUTE_FORECASTING_TALK_TRACK.md and BOA_FORECAST_PROJECT_DEEP_DIVE.md.

HorizonScale 5-minute interview talk guide
20-second hook

"HorizonScale was a telemetry-driven capacity forecasting pipeline — raw utilization data in, explainable risk and planning recommendations out."

Business problem (30 sec)

Manual capacity analysis is slow and reactive. Teams couldn't see bottlenecks, sustained pressure, or waste early enough to act safely.

Inputs & features

Raw telemetry

CPU / memory util P95 latency request + error context allocated vs actual cost + ownership tags
Engineered features

headroom growth trend seasonality forecast variance threshold breach flags
Pipeline flow

Ingest telemetry
→
Clean & normalize
→
Aggregate by service/bucket
→
Engineer features
→
Run model(s)
→
Compare vs actuals & thresholds
→
Classify risk / waste
→
Export planning outputs
Model choices

Prophet

Trend + seasonality in time-series. Explainable forecasts that engineers and leadership trust.

scikit-learn

Feature-driven risk scoring. Complements Prophet with predictive checks on engineered signals.

Rapid Q&A

Why Prophet?

Handles trend + seasonality naturally. Output is explainable.

Why scikit-learn?

Feature-driven risk scoring on top of the forecasted signals.

How did this support cost decisions?

Surfaced underutilization and over-pressure early — safe rightsizing.

Batch or streaming?

Batch-first for planning; streaming mainly for alerting.

Don't overclaim

No deep research ML ownership · No perfect accuracy claims · No deep GCP/K8s platform-admin · No enterprise-wide production scope unless confirmed


That's your complete 5-minute talk card. The flow is: hook → problem → inputs → pipeline → models → Q&A ready.
The "don't overclaim" strip at the bottom is intentionally visible — worth a glance before you walk into the room.


## 5-Minute Deep Technical Answer

HorizonScale is the way I explain a capacity forecasting workflow
that turned raw utilization data into planning recommendations.

The problem was that manual capacity reviews can become too slow
and reactive. If teams only look at current utilization or wait for
threshold breaches, they may miss early signs of capacity pressure.
The goal was to provide earlier, explainable signals so engineering
and leadership could plan remediation, budget, and prioritization
before capacity became an incident.

The workflow started with telemetry from enterprise monitoring and
capacity systems. The core inputs were timestamps, host or server
identifiers, application or service mappings, CPU, memory, storage,
utilization values, and threshold context. Where business context
was available, I also wanted ownership, environment, criticality,
or service mapping so the forecast could be tied to action.

The first layer was data cleanup. I normalized timestamps, aligned
the data into hourly and daily buckets, checked for missing records,
duplicate records, stale hosts, impossible metric values, and
inconsistent mappings. That step mattered because a forecast is only
as reliable as the data behind it. If a host is mapped to the wrong
application, or if timestamps are inconsistent, the risk ranking can
mislead the team.

The second layer was grouping. I wanted the same data to be useful
at different levels: host, application, service, environment, and
sometimes business owner. A host-level view helps engineers
troubleshoot. An application or service-level view helps management
understand impact and priority.

The third layer was feature engineering. I created explainable
capacity features such as rolling average, rolling peak, recent
maximum, growth slope, volatility, headroom to threshold, breach
flags, and risk bands. These features helped separate a one-time
spike from sustained capacity pressure. For example, a server that
hits a high peak once may not be the same risk as a service that
shows steady growth and declining headroom every week.

The forecasting layer was practical and explainable. I would not
describe it as deep ML research. The main goal was to project whether
a system was trending toward threshold risk and when the team might
need to act.

Prophet was part of the real forecasting work because we needed
seasonality-aware time-series forecasting. Some systems have weekly,
monthly, quarter-end, or business-calendar patterns, so a simple
straight-line projection is not always enough. Prophet helped model
those seasonal patterns while still keeping the forecast explainable
enough for capacity and operations discussions.

I still treated the model as decision support, not magic. The
important question was not just whether a model looked sophisticated.
The important question was whether the forecast helped identify
capacity risk earlier, whether the projected trend made sense, and
whether SMEs agreed that the signal matched the real operating
pattern.

For newer lab work, I also explored scikit-learn-style risk scoring
on top of the engineered capacity features. I would frame that as a
modernization extension, not the original production claim. The idea
is to use features like growth slope, headroom, recent peaks, breach
history, volatility, and service criticality to produce a clearer
risk ranking.

Validation was a major part of the design. I checked data quality,
verified feature calculations, compared forecasted risk against later
actual behavior, reviewed false positives and false negatives, and
validated the results with SMEs.

For model testing, I would not train on all available history and
then immediately forecast the future. I would hold out a recent
period to test the forecast first. For example, if I had 24 months
of history, I could train on the first 18 months, test against the
next 6 months, and compare the forecasted values or risk bands
against what actually happened.

Only after that backtest looked reasonable would I use the full
available history to forecast the next planning window, usually the
next 3 to 6 months. That gave the forecast more credibility because
we were not just asking, "Does the chart look good?" We were asking,
"Could this method have warned us correctly before the actual
capacity pattern showed up?"

SME review also mattered because capacity numbers need context. A
system may look risky but be scheduled for retirement. Another system
may look moderate technically but be critical during month-end
processing.

The output was not just a chart. The output was a decision product:
dashboards, reports, exception lists, and ranked risk views. The
report should tell engineering and leadership which systems have low
headroom, which services are trending upward, what the likely action
window is, who owns the service, and what kind of decision is needed.

The deployment pattern was batch-oriented because capacity forecasting
is usually a planning workflow. Daily or weekly batch runs are often
enough for forecasting, reporting, and management review. Real-time
streaming is better suited for immediate alerting and incident
response. So I separate those two use cases: streaming for alerts,
batch forecasting for planning.

The original version is easy to explain with SQL, Python, Pandas, and
Prophet because those tools are strong for telemetry cleanup, time
bucketing, groupby logic, rolling windows, feature engineering, and
seasonality-aware forecasting.

The scale-up path is PySpark, Hadoop, or cloud data processing, where
the same logic can run across larger telemetry history, partitioned by
date, application, host, or metric, and then published into reporting
tables or dashboards.

So the honest summary is this: my strongest experience is capacity
engineering and telemetry decision support. Prophet was part of the
real forecasting work. Scikit-learn risk scoring is a newer lab
extension. And the broader architecture can scale from a Pandas-based
workflow into PySpark, Hadoop, or cloud-style processing without
changing the core capacity logic.
