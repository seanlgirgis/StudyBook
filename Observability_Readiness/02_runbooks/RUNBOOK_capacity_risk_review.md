# Runbook: Capacity Risk Review

## Symptoms
- User-visible degradation or reliability risk indicators appear.

## Signals
- Primary service health metrics.
- Supporting platform/infrastructure telemetry.
- Recent deployment or configuration changes.

## First Checks
1. Confirm scope (single service vs broad impact).
2. Validate alert quality and timestamp alignment.
3. Review correlated signals (errors, saturation, dependencies).

## Likely Causes
- Resource saturation.
- Recent change regression.
- Dependency instability.
- Threshold or alert tuning mismatch.

## Remediation
1. Stabilize user impact first.
2. Apply fastest safe mitigation.
3. Validate recovery with objective telemetry.
4. Capture action items for permanent fix.

## Escalation
- Escalate when impact persists beyond initial mitigation window, or cross-team dependencies block recovery.
- Include timeline, current blast radius, attempted mitigations, and risk outlook.

## Interview Story
- Explain how you moved from noisy signals to scoped diagnosis, then to mitigation and business-impact communication.
