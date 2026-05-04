# 04e API Test Plan

## Scope
Validate the live service integration layer over the 04d deterministic pipeline.

## Test Coverage

### Endpoint correctness
- `GET /v1/health` returns `200` and expected status body.
- `POST /v1/query` returns `200`, pipeline summary fields, and timing fields.
- `POST /v1/answer` returns `200`, structured answer fields, and timing fields.

### Mock evidence + query flow
- Default request path executes 04d scenarios and returns non-empty results.
- Timing fields are present and non-negative.

### Contract compliance
- Unknown `scenario_ids` returns `400` with clear message.
- Missing required `query` returns `422`.
- Response payloads contain required schema fields for run summary and answer shape.

## Non-goals
- No threshold tuning.
- No LLM invocation.
- No customer-facing freeform generation.
- No integrated/servicecall-ai deployment in this POC.
