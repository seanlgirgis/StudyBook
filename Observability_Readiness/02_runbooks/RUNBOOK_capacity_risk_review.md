# Runbook: Capacity Risk Review

## Objective
Review forecast output, validate true risk, and convert findings into clear management decisions.

## Inputs
- Current forecast output with ranked risk list.
- Trend/headroom dashboards.
- Threshold and breach history.
- Recent change/activity context.

## How To Review Forecast Output
1. Start with top-risk systems by risk band and forecast window.
2. Confirm the key drivers: growth slope, rolling peak behavior, and headroom trend.
3. Check whether the risk signal is consistent across multiple time buckets.
4. Capture the initial recommendation for each top-risk item.

## How To Validate Top-Risk Systems
1. Verify telemetry quality for each system (timestamp continuity, duplicates, stale assets, impossible values).
2. Confirm ownership context (host/application/service mapping).
3. Compare forecast signal to recent actual behavior.
4. Validate with SME/operator input for known business events or exceptions.

## Separate One-Time Spike vs Sustained Trend
- One-time spike indicators:
  - Isolated event window.
  - Quick return to baseline.
  - No sustained headroom decay.
- Sustained trend indicators:
  - Repeating upward utilization pattern.
  - Rolling average and rolling max both rising.
  - Headroom consistently shrinking across windows.

## Explain Risk To Management
Use plain language:
- What is at risk.
- When risk is likely to materialize.
- Confidence level and assumptions.
- Recommended action now vs next review cycle.

## Executive Summary Template
```text
Capacity Risk Summary - [Date]

Top Risks:
1) [System/Service] - [Risk Band]
   - Forecast window: [time range]
   - Main signal: [growth/headroom/threshold trend]
   - Confidence: [low/medium/high] with assumptions
   - Recommended action: [scale/tune/optimize/investigate]

2) [System/Service] - [Risk Band]
   - Forecast window: [time range]
   - Main signal: [growth/headroom/threshold trend]
   - Confidence: [low/medium/high] with assumptions
   - Recommended action: [scale/tune/optimize/investigate]

Notes:
- Distinguish sustained trends from one-time spikes.
- Track false positives and adjust thresholds as needed.
```

## Escalation
Escalate when:
- Risk remains high after first mitigation,
- Cross-team dependencies block remediation,
- Forecast indicates near-term service impact with no safe buffer.

## Interview Story Angle
Explain how you moved from forecast output to validated risk, then to practical management decisions.
