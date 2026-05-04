# CONTRACT.md - POC 04f Containerized Deterministic Service

## Purpose
Define runtime and behavior contract for deploying the deterministic FastAPI service in containerized environments while preserving validated 04e behavior.

## Deployment Context
- Service: FastAPI HTTP API
- Runtime: Docker-first, ECS/Fargate-compatible
- Data policy: synthetic/mock evidence only
- Behavior policy: deterministic only

## API Behavior Contract
- Preserve schema-validated request handling.
- Preserve deterministic response structure and outcomes.
- Preserve timing metrics in response payloads.
- Preserve deterministic validation/fallback/escalation behavior.

Prohibited additions in this POC:
- LLM/provider calls
- threshold tuning logic
- customer/production data dependencies

## Port Configuration
- Default host: `0.0.0.0`
- Default port: `8000`
- Container exposes port `8000`
- Port mapping may be overridden by container runtime configuration

## Environment Variables
- `APP_HOST` (default: `0.0.0.0`)
- `APP_PORT` (default: `8000`)
- `LOG_LEVEL` (default: `INFO`)
- `SERVICE_ENV` (default: `docker`)

Rules:
- Missing env vars must fall back to safe defaults.
- Env vars must not change deterministic business outcomes.

## Mock Service Rules
- Use synthetic/mock evidence only.
- No external AI/LLM/network answer-generation calls.
- No customer data read/write.
- Scenario outcomes must remain aligned with 04d/04e validated behavior.

## Error and Observability Contract
- Validation errors return structured client-safe responses.
- Deterministic service failures return predictable status and shape.
- Unexpected errors return sanitized server-safe response and logs.
- Request lifecycle and outcome/timing context should be log-visible.

## Compatibility
POC 04f must remain behavior-compatible with:
- `pocs/04e` API expectations
- `pocs/04d` mock scenario evidence behavior
