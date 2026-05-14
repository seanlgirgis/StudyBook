# Story: APM Troubleshooting Under Pressure

## Situation
A business-critical application showed rising response times during a peak operating window, and stakeholder concern escalated quickly due to potential customer impact.

## Problem
The team needed a fast, evidence-based diagnosis to separate application issues from infrastructure symptoms and reduce incident duration.

## Actions
- Pulled APM service and transaction dashboards to confirm the latency spike and define impacted transactions.
- Compared current behavior against threshold baselines and prior trend windows.
- Coordinated telemetry checks across application and infrastructure teams to rule out broad platform failure.
- Narrowed likely fault domain to a specific dependency path and guided targeted remediation.
- Communicated technical status and business risk updates in plain language to leadership.

## Signals Used
- Response time and error-rate metrics from APM dashboards.
- Dependency-level timing patterns and transaction detail views.
- Supporting infrastructure utilization and saturation indicators.

## RCA Angle
Used a structured RCA workflow: detect anomaly, scope blast radius, isolate dependency bottleneck, validate fix, and update operational controls to reduce recurrence.

## Dashboard/Threshold Angle
Thresholds and dashboard segmentation were key to early detection and rapid triage. Post-incident, thresholds were tuned to improve signal quality and reduce alert noise.

## Modern OpenTelemetry Mapping
The same troubleshooting logic maps to cloud-native telemetry:
- Metrics detect the anomaly.
- Traces show where latency concentrates in the request path.
- Logs provide detailed error evidence.
- A collector-based pipeline standardizes how those signals are routed and correlated.

## Safe Wording
"I led enterprise APM troubleshooting workflows and RCA with strong telemetry discipline. In cloud-native environments, I apply the same operator pattern and map it to OpenTelemetry-style pipelines while continuing to ramp on specific platform implementations."

## What Not To Overclaim
- Do not claim production ownership of OpenTelemetry platform rollout unless explicitly true.
- Do not claim Kubernetes observability platform ownership unless explicitly true.
- Do not claim end-to-end Prometheus/Grafana platform build ownership unless explicitly true.
