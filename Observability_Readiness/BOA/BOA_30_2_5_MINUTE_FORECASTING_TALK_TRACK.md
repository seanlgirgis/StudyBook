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

## Optional BOA Team Mapping Bridge
[Back to TOC](#table-of-contents)

Use this only if they ask how your background maps to their environment.

From what I understand, this work is close to production capacity planning:
critical applications and clusters, capacity baseline forecast reports,
quarterly reviews, BMC TrueSight/TSCO-style data, dashboarding, and planning
decisions.

That maps well to my background. I have worked with enterprise capacity and APM
telemetry, built Python/Pandas reporting and forecasting workflows, defined
KPIs, and produced risk views that help engineering and leadership decide where
action is needed.

I am comfortable with Excel-heavy reporting as a starting point, but I can also
help make that process more repeatable, validated, and dashboard-ready through
Python, structured data, and forecasting logic.

Memory line:

```text
I understand the current capacity reporting world, and I can help make it more
repeatable, validated, and dashboard-ready.
```


## Optional Origin Pipeline Bridge

Use this only if asked how the data pipeline started, how manual
reports were automated, or how the forecasting layer became possible.

The forecasting story did not start with Prophet. It started with
getting the reporting pipeline under control. A lot of capacity
reporting begins in a manual Excel-heavy process: extracts, repeated
cleanup, manual calculations, and team reports.

I helped move that toward a Python-based workflow where the data could
be cleaned, normalized, stored more consistently, and used to produce
repeatable report outputs. SQLite was useful as a lightweight structured
store for local or team-level reporting, and Streamlit-style reporting
was a practical way to expose results to the team.

Once that foundation was in place, the next layer was HorizonScale:
using cleaned telemetry to create time buckets, group by host or
service, engineer capacity features, forecast trends, rank risk, and
communicate decisions to engineering and leadership.

Memory line:

```text
The work evolved in layers: first make reporting repeatable, then make
the telemetry structured and trustworthy, then build forecasting and
risk ranking on top of it.
```


## Optional Bank Capacity Operations Bridge

Use this only if they ask about clusters, collection exceptions, BMC
operations, audits, or bank capacity governance.

For production capacity work, I would look beyond the forecast chart. I would
also consider the operating design: clusters, active/active versus
active/passive behavior, load balancing, DR reserve, ESX host versus VM guest
views, collection exceptions, swap or memory exceptions, and business
criticality.

That matters because the same CPU or memory number can mean different things
depending on architecture and criticality. A franchise-critical application,
an active/passive cluster, or a system with missing telemetry needs a more
careful response than a low-criticality standalone server.

The forecast gives the view, but the runbook or playbook turns that view into
action: validate the data, notify the owner, open or track the exception,
collaborate with architecture and application teams, and document the outcome
for governance or audit if needed.

## 5-Minute Deep Technical Answer
HorizonScale is how I explain a capacity forecasting workflow that turned raw
utilization data into planning recommendations.

The business issue was that manual capacity reviews were often too slow and
reactive. If teams only looked at current utilization or waited for threshold
breaches, they could miss early signs of sustained pressure. The goal was
earlier, explainable signals so engineering and leadership could plan
remediation and prioritization before capacity became an incident.

This also maps well to CBFR-style capacity baseline forecasting: production
telemetry, critical applications, quarterly reports, dashboard-ready outputs,
and clear planning recommendations.

Before the forecasting layer, there was a reporting automation foundation.
Manual Excel-heavy capacity reports were moved toward a repeatable Python
workflow with structured storage, report outputs, and team-facing views. That
foundation made the later forecasting work more reliable because the data was
cleaner, more reusable, and less dependent on manual spreadsheet handling.

The HorizonScale workflow then started with telemetry from enterprise
monitoring and capacity systems: timestamps, host or server identifiers,
application and service mappings, environment context, CPU, memory, storage,
utilization values, and threshold context.

The first layer was cleanup and timestamp normalization. I aligned timestamps,
bucketed data into hourly and daily windows, and checked for missing records,
duplicate records, stale hosts, impossible values, and inconsistent mappings.
That mattered because forecast quality depends on data quality.

The second layer was grouping for actionability: host, application, service,
and environment. Host-level views support engineering triage, while service
views support planning and management prioritization.

The third layer was feature engineering with explainable signals: rolling
average, rolling peak, recent maximum, growth slope, volatility, headroom to
threshold, breach flags, and risk bands. These features helped separate one-time
spikes from sustained capacity pressure.

Prophet was part of the real forecasting work. It helped model trend and
seasonality, including weekly, monthly, quarter-end, and business-calendar
patterns, while keeping outputs explainable for operations and leadership.

As newer lab modernization work, I also explored scikit-learn risk scoring on
top of engineered features. I frame that as an extension, not the original
production foundation.

Validation was a major design step. I ran data quality checks, verified feature
calculations, compared predicted vs actual behavior, reviewed false positives
and false negatives, and validated with SMEs.

For holdout-style testing, if 24 months of history were available, I trained on
the first 18 months and tested on the next 6 months. I compared forecasted
values or risk bands against actual outcomes. Only after that backtest looked
reasonable would I retrain on full history and forecast the next 3 to 6 months.

The output was a decision product: dashboards, reports, exception lists, and
ranked risk views with remediation timing and ownership context.

Execution mode was batch-first for planning, with streaming used mainly for
alerting workflows. That kept forecasting and incident-response use cases clear.

The original explainable workflow was SQL, Python, Pandas, and Prophet. The
scale-up path keeps the same logic and moves heavy processing to
PySpark/Hadoop/cloud patterns.

The honest summary is this: my strongest experience is capacity engineering and
telemetry decision support. Prophet was real forecasting work. Scikit-learn
risk scoring is lab modernization work. The broader architecture can scale
without changing the core capacity logic.
