# Observability Readiness Study Project

## Purpose
This repository is a dual-track readiness system:
- Short-time readiness: prepare for the client interview on Monday with focused talk tracks, priority review, and morning checklists.
- Forever readiness: keep a reusable cloud-observability field manual, runbook set, lab recipes, and story bank for future roles and engagements.

## Current Learning Unit
- Topic 1: Metrics, Logs, Traces + OpenTelemetry Collector Flow.
- Why now: this is the core language for most cloud observability interviews and it connects directly to prior enterprise APM and capacity work.
- Output for this unit: clear talk tracks, one lightweight OTel collector lab, and one interview story with safe cloud-native mapping.

## Who This Is For
Primary voice is for an experienced enterprise APM/capacity engineer transitioning to cloud-native observability topics.

## Truth-Based Positioning
### Proven strengths
- Enterprise APM and observability: Dynatrace AppMon, Gomez, CA APM/Introscope/Wily, AppDynamics, BMC TrueSight/TSCO.
- Capacity engineering at scale: telemetry from 6,000+ endpoints, KPI/threshold design, forecasting, RCA, executive reporting.
- Data and automation: Python, SQL, Pandas, PySpark, AWS data platform.

### Adjacent ramp-up topics
- Kubernetes observability, OpenTelemetry, Prometheus, Grafana.
- IaC for observability patterns (Terraform, CloudFormation).
- GPU monitoring patterns.

## Repository Layout
- `00_short_time_readiness/`: Monday interview readiness.
- `01_field_manual/`: evergreen practical reference.
- `02_runbooks/`: incident and operations response playbooks.
- `03_labs/`: small hands-on recipes with interview stories.
- `04_stories/`: behavioral and impact stories.
- `CURRENT_FOCUS.md`: this week priorities.
- `DAILY_LOG.md`: progress log.

## How To Use This Week
1. Start at `CURRENT_FOCUS.md`.
2. Rehearse `00_short_time_readiness/30_2_5_MINUTE_TALK_TRACK.md`.
3. Review runbooks and stories to anchor answers in concrete operations work.
4. Use lab READMEs as honest “next-step hands-on” examples.

## Interview Safety Rules
- Lead with verified prior ownership and measurable outcomes.
- Frame cloud-native topics as active ramp-up tied to existing monitoring fundamentals.
- Never overclaim production ownership of tools you have not run at scale.
