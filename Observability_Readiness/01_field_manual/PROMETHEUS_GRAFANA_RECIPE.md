# Prometheus + Grafana Recipe

## Goal
Stand up practical monitoring and dashboards for service and platform health.

## Minimal Recipe
- Define scrape targets and retention plan.
- Create recording rules for common SLI math.
- Configure alert rules with owner/severity labels.
- Build Grafana dashboards: service health, platform health, capacity trend.
- Add runbook links in alert annotations.

## Good Dashboard Traits
- Clear status-at-a-glance panel.
- Drilldown paths for triage.
- Capacity trend and headroom view.

## What I Can Say In Interview
- “I prioritize actionable dashboards tied to alerts and runbooks, not vanity visualization.”

## Do Not Overclaim
- Do not overstate deep PromQL/Grafana internals if still ramping.
