# Lab 03: OpenTelemetry Collector Config

## Lab Purpose
Read and explain a minimal OpenTelemetry Collector configuration without heavy coding. This is an interview-readiness lab focused on architecture fluency and safe positioning.

## What The Collector Does
The collector receives telemetry data, optionally processes it, then exports it to a backend destination. In this lab we use simple blocks so the flow is easy to explain.

## How To Read The YAML
1. Start at `receivers` to see what data can come in.
2. Review `processors` to see what data shaping happens.
3. Check `exporters` to see where telemetry goes out.
4. Confirm `service.pipelines` to see which signal types (metrics/traces) use which path.

## Receivers, Processors, Exporters
- Receivers are input doors.
- Processors are middle steps for shaping efficiency or quality.
- Exporters are output routes to observability backends.

## Why `memory_limiter` And `batch` Are Common
- `memory_limiter` is a safety control that helps prevent collector instability under load spikes.
- `batch` improves export efficiency by grouping telemetry before it is sent downstream.
- Together they are common baseline processors in practical collector configs.

## Prometheus Exporter In This Lab
- The Prometheus exporter exposes metrics on an HTTP endpoint.
- Prometheus scrapes that endpoint and stores/query-serves the metric series.
- This lab keeps the pattern simple and focused on collector flow, not full platform build-out.

## Prometheus/Grafana Conceptual Connection
In production-style designs, metrics often flow from OTel collector pipelines toward Prometheus-compatible storage/query layers and then Grafana dashboards/alerts. This lab keeps export simple while preserving the same conceptual pattern.

## Scope Guardrail
This lab intentionally stays focused on OpenTelemetry collector basics for interview readiness. It does not expand into Kubernetes, GPU monitoring, or Terraform workflows yet.

## What Sean Should Be Able To Explain After The Lab
- The collector flow from ingest to export.
- Why a standard telemetry pipeline helps with consistency and tool choice.
- How this model maps to enterprise APM signal governance and RCA workflows.
- What is known confidently versus what should be framed as ramp-up.

## Commands
```powershell
# From this lab directory, read the config
Get-Content .\otel-collector-example.yaml

# Optional local container-style run example (if collector image is available)
# docker run --rm -v "${PWD}\otel-collector-example.yaml:/etc/otelcol/config.yaml" `
#   otel/opentelemetry-collector:latest --config /etc/otelcol/config.yaml
```

## Acceptance Checklist
- Can explain receiver -> processor -> exporter flow in under 60 seconds.
- Can identify traces and metrics pipelines in YAML.
- Can describe conceptual handoff to Prometheus/Grafana.
- Can provide truthful interview wording without overclaiming platform ownership.
