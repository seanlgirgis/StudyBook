# Metrics, Logs, and Traces

## 1. Plain-English Definition
- Metrics are numeric signals over time, such as error rate, latency percentiles, CPU, memory, and request volume.
- Logs are event and detail records that describe what happened at a specific moment, including errors, warnings, and context fields.
- Traces are the request journey across services and components, showing where time is spent and where failures occur.

## 2. Operator Mental Model
- Metrics answer: "Is something wrong?"
- Logs answer: "What happened?"
- Traces answer: "Where did the request slow down or fail?"
- Practical flow: start with metrics to detect and scope, use traces to isolate the failing segment, then use logs for exact evidence and remediation detail.

## 3. Sean's Legacy Mapping
- APM dashboards -> modern service dashboards in cloud-native monitoring stacks.
- Thresholds -> alert rules and SLO/SLI alert conditions.
- RCA -> trace and log correlation for faster fault isolation.
- Capacity reports -> metrics and time-series forecasting for demand and risk.
- BMC TrueSight / TSCO, AppDynamics, Dynatrace, CA APM -> same core operational goals now expressed with cloud-native telemetry patterns.

## 4. Interview-Safe Answer
"I use metrics, logs, and traces as one operator workflow. Metrics tell me if the system is drifting, logs give me exact failure context, and traces show where a request is slowing down across services. That maps directly to work I already owned in enterprise APM and capacity engineering, where I used dashboards, thresholds, and RCA to reduce incident time and support operational decisions. In cloud-native environments I apply the same thinking, while continuing to ramp on specific platform implementations."

## 5. What Not To Overclaim
- Do not say: "I owned OpenTelemetry in production."
- Do not say: "I was the Kubernetes observability owner."
- Do not say: "I built Prometheus/Grafana platforms from scratch."
- Use truthful wording: "I understand the model, can explain the pattern, and can execute labs while partnering with platform owners."
