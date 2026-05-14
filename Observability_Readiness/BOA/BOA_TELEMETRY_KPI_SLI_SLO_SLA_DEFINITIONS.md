# BOA Telemetry, KPI, SLI, SLO, SLA Definitions

## 1. Quick mental model
Telemetry is raw signal.
Metrics are measured values.
KPIs are decision signals.
SLIs measure service behavior.
SLOs define the target.
SLAs define the formal commitment.
Runbooks turn signals into repeatable action.

## 2. Telemetry
Telemetry is data emitted by systems that describes system behavior.

Examples:
- CPU
- memory
- storage
- latency
- request count
- error rate
- throughput
- host status
- timestamps
- logs
- traces
- events

BOA-safe sentence:
"Telemetry is the raw signal coming from systems. In capacity work, I use it as
the source material for metrics, KPIs, forecasts, and risk decisions."

## 3. Metric
A metric is a measured value over time.

Examples:
- CPU utilization percentage
- memory used
- storage consumed
- requests per second
- error rate
- P95 latency

BOA-safe sentence:
"A metric tells me what was measured. It does not automatically tell leadership
what action to take."

## 4. KPI
A KPI is a selected metric or derived signal that supports a business
or operational decision.

A metric describes a technical reading. For example, CPU is at 85%.
A KPI gives that reading decision context: CPU headroom is below the
safe threshold for a critical service, and action is needed to avoid a
performance bottleneck.

For capacity, examples of KPIs would be utilization trend, rolling
peaks, recent maximums, growth slope, headroom to threshold, risk band,
forecasted breach window, service criticality, owner, and remediation
status.

The way I define KPIs is from the decision backward. I ask what
operations or leadership needs to decide, then choose the signal that
best supports that action.



## 5. SLI / SLO / SLA
SLI:
Service Level Indicator.
The thing you measure.

Examples:
- availability
- latency
- error rate
- successful request ratio
- job completion rate

SLO:
Service Level Objective.
The target for the SLI.

Examples:
- 99.9% successful requests
- P95 latency under 300 ms
- batch job completes by 6 AM

SLA:
Service Level Agreement.
The formal agreement or commitment, often customer-facing or contractual.

SLIs drive SLOs, and SLOs inform SLAs.

Capacity connection:
Capacity KPIs are not always the same as SLIs/SLOs, but they support the same
reliability conversation. For example, low headroom can be an early warning
that a latency or availability SLO may be at risk.

## 6. Runbooks
A runbook is a repeatable operating procedure that tells the team what to
check, who to contact, how to validate the issue, and what actions to take.

Capacity runbook examples:
- validate metric quality
- confirm timestamp bucket
- confirm host/application/service mapping
- check recent changes
- review headroom and threshold history
- check whether pattern is spike, trend, batch window, or bad data
- contact SME or owner
- choose action:
  tuning, cleanup, right-sizing, capacity expansion, or monitoring

BOA-safe sentence:
"The dashboard shows the risk, the KPI explains why it matters, and the runbook
tells the team what to do next."

## 7. BOA interview answer: How do you define KPIs?
"I separate telemetry, metrics, and KPIs.

Telemetry is the raw signal from the environment: CPU, memory, storage,
timestamps, latency, errors, and events.

Metrics are measured values over time, like average CPU, P95 latency, memory
usage, or storage growth.

KPIs are the selected metrics or derived signals that support a business or
operational decision. In capacity work, I define KPIs around trend, headroom,
threshold risk, forecasted breach window, service criticality, ownership, and
remediation status.

So I do not define KPIs just because a number is available. I start with the
decision: what does operations or leadership need to know, what action might
they take, and what signal best supports that decision?"

## 8. BOA interview answer: How do runbooks fit?
"Runbooks turn forecast output into repeatable action.

If a service moves into a higher risk band, the runbook gives the team a
standard path: validate the data, confirm the service owner, check recent
changes, review headroom and threshold history, involve the SME, and decide
whether the action is tuning, cleanup, right-sizing, capacity expansion, or
continued monitoring.

That matters because forecasting should not stop at a dashboard. The dashboard
shows the risk, the KPI explains why it matters, and the runbook tells the team
what to do next."

## 9. How this connects to HorizonScale
- telemetry is the input
- metrics are calculated from telemetry
- KPIs are selected/derived for decisions
- forecasts project future risk
- risk bands prioritize the work
- dashboards communicate status
- runbooks guide response
- leadership uses summaries for planning, budget, and timing

## 10. Do not say
- Do not say every metric is a KPI.
- Do not say KPIs are just charts.
- Do not claim full enterprise-wide runbook governance if not true.
- Do not turn SLI/SLO/SLA into a textbook answer.
- Do not overclaim deep OpenTelemetry implementation ownership.

## References
- Google SRE Book, Service Level Objectives:
  [https://sre.google/sre-book/service-level-objectives/](https://sre.google/sre-book/service-level-objectives/)
- Google SRE Workbook, Implementing SLOs:
  [https://sre.google/workbook/implementing-slos/](https://sre.google/workbook/implementing-slos/)
- Google SRE Workbook, Alerting on SLOs:
  [https://sre.google/workbook/alerting-on-slos/](https://sre.google/workbook/alerting-on-slos/)
- OpenTelemetry Observability Primer:
  [https://opentelemetry.io/docs/concepts/observability-primer/](https://opentelemetry.io/docs/concepts/observability-primer/)
- OpenTelemetry Signals:
  [https://opentelemetry.io/docs/concepts/signals/](https://opentelemetry.io/docs/concepts/signals/)
- OpenTelemetry Documentation:
  [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)
- FinOps KPIs & Benchmarking:
  [https://www.finops.org/framework/capabilities/kpis-benchmarking/](https://www.finops.org/framework/capabilities/kpis-benchmarking/)
- FinOps KPIs:
  [https://www.finops.org/wg/finops-kpis/](https://www.finops.org/wg/finops-kpis/)
- FinOps Phases:
  [https://www.finops.org/framework/phases/](https://www.finops.org/framework/phases/)
