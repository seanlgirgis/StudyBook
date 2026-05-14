# Cloud Observability Map

## Layers
- Application: request rates, errors, latency, dependency health.
- Platform: Kubernetes cluster/node/pod health.
- Infrastructure: compute, memory, network, storage.
- Business: service KPIs and customer-impact signals.

## Data Flow
Sources -> Collectors/Agents -> Storage -> Query/Visualize -> Alert -> Runbook -> Postmortem

## Operator Focus
- Fast path from signal to decision.
- Consistent naming, ownership tags, and severity model.
- Tight loop between incident learnings and alert tuning.

## What I Can Say In Interview
- “I treat observability as an operating system for reliability decisions.”
