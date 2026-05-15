# BOA 30 2 5 Minute Forecasting Talk Track

## 30-Second Answer

I built a practical capacity forecasting workflow that turned
infrastructure telemetry into early risk visibility for operations
and leadership.

Using SQL, Python, and Pandas, I normalized timestamps, bucketed
the data hourly and daily, grouped it by host, application, or
service, and calculated trend, peak, and headroom features.

The goal was decision support. Instead of just showing raw CPU,
memory, or utilization charts, the workflow ranked services by
near-term capacity risk so teams could act earlier, communicate
risk clearly, and plan remediation before capacity became an
incident.

## Strong 2-Minute Answer

Raw telemetry by itself does not create a management decision.
The work was to turn infrastructure and application telemetry
into clean features, forecast signals, risk rankings, dashboards,
and action plans.

The pipeline started with telemetry from enterprise monitoring
and capacity tools. The data included timestamps, host or server
names, application and service mappings, CPU, memory, storage,
utilization values, and threshold context.

The first step was cleanup and normalization. I normalized
timestamps, aligned the data into hourly and daily buckets,
standardized host and server names, and validated mappings from
systems like CMDB and BMC. That mattered because a forecast is only
as trustworthy as the data and grouping behind it.

Then I created explainable capacity features: rolling averages,
rolling peaks, recent maximums, growth slope, headroom to threshold,
breach flags, and risk bands. Those features helped separate a
one-time spike from sustained capacity pressure.

From there, the goal was practical forecasting, not deep ML research.
I wanted to identify which systems were trending toward risk, how
much headroom remained, which services were approaching threshold,
and where teams should focus before capacity became an incident.

Validation was important. I checked data quality, verified feature
calculations, compared forecasted risk against later actual behavior,
and reviewed the output with SMEs because capacity numbers need
business and operational context.

The final output was not just a chart. It became dashboards, reports,
exception lists, and ranked risk views for engineering and leadership.
That helped teams discuss remediation, budget, timing, ownership, and
priority using clear risk language.

### Story points
1. Raw telemetry does not create decisions.
2. Inputs came from monitoring and capacity tools.
3. Clean timestamps and mappings.
4. Build explainable features.
5. Forecast practical risk, not deep ML.
6. Validate with data, backtesting, and SMEs.
7. Publish dashboards, reports, and ranked risk views.


## 5-Minute Deep Buildout Story - Ignored .. combined above
If I break it down end to end, I started with telemetry inputs from
infrastructure and application layers, plus KPI context and asset metadata. The
first step was cleanup and normalization: timestamp format alignment, duplicate
handling, missing value checks, and stale record detection. That gave me
reliable time-series inputs.

Next I bucketed data into hourly and daily windows so we could separate noise
from sustained trend. I grouped by host, application, and service because
ownership and action planning happen at those levels. From there I built
explainable features: rolling averages for sustained behavior, rolling peaks for
stress behavior, growth slope for trajectory, and headroom-to-threshold for
operational urgency.

Then I added threshold breach flags and risk bands. This let us move from raw
telemetry to ranked risk. Instead of saying only a metric was high, we could
say which service was likely to hit a limit soon and which action window
mattered first. That ranking fed dashboard and reporting outputs.

Operationally, teams used ranked service views, trend panels, and threshold
outlooks. Leadership received concise summaries with assumptions, confidence
framing, and recommendation language. The objective was not a research-grade
model. The objective was practical, repeatable decision support.

Validation had multiple layers. I checked data quality first: missing
timestamps, impossible values, duplicates, stale assets, and bucket integrity.
Then I validated feature calculations. For forecast behavior, I used
time-ordered testing and backtesting against actual outcomes, and I used simple
baseline comparison. Finally, I reviewed false positives with SMEs so the
output stayed trustworthy and actionable.

For scale-up, I present a safe architecture path. Pandas was ideal for fast
prototyping and feature iteration. At larger volume, the same logic moves to
PySpark for distributed transformation, with Hadoop/HDFS or cloud data lake
storage patterns, partitioned time-series datasets, and scheduled ETL. I
describe this as an explainable scale pattern and collaborative platform
evolution, not solo ownership of every platform layer.

My ownership statement is straightforward: I can clearly explain and defend the
forecasting logic, feature design, risk ranking, validation workflow, and
reporting outputs. On large platform expansion, I partner with data and
platform teams and stay explicit about boundaries.
