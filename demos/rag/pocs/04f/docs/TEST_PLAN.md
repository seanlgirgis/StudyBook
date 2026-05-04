# TEST_PLAN.md - POC 04f Containerized Execution

## Objective
Verify that containerized deployment preserves deterministic API behavior from 04e and remains observable/testable in Docker runtime.

## Execution Plan (Containerized)
1. Build Docker image from `src/Dockerfile`.
2. Run container on configured host/port (default `0.0.0.0:8000`).
3. Execute integration and validation tests against running container endpoint.
4. Capture example requests/responses and logs under `outputs/`.
5. Compare outcomes against deterministic expectations from 04d/04e.

## Test Areas
### Integration tests for endpoints inside Docker
- Confirm service starts and endpoint is reachable.
- Confirm valid request path returns expected status and response schema.
- Confirm repeated deterministic input remains contract-consistent.

### Validation of mock evidence scenarios
- Confirm known deterministic success scenarios remain valid.
- Confirm known negative/fallback scenarios behave as designed.
- Confirm escalation/insufficient-evidence paths remain deterministic.

### Logging and timing metrics verification
- Confirm container logs include request lifecycle and error context.
- Confirm timing metric fields remain present in response payloads.
- Confirm timing values are parseable and stable in structure.

## Planned Test Files
- `tests/test_integration.py`
- `tests/test_validation.py`

## Planned Output Artifacts
- `outputs/example_requests.json`
- `outputs/example_responses.json`
- `outputs/logs/` (captured log samples)

## Acceptance Criteria
- Containerized service boots and responds.
- Integration and validation tests pass.
- Deterministic behavior preserved (no LLM calls, no threshold tuning).
- Mock evidence scenario behavior preserved.
- Logging and timing metrics verification completed.
