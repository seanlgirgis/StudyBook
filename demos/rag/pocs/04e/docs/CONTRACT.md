# 04e API Contract

## Purpose
Expose the validated deterministic RAG evidence pipeline (04d/04b) as a live service interface.

## Base
- Framework: FastAPI
- Prefix: `/v1`

## Endpoints

### GET `/v1/health`
Returns service health.

Response:
```json
{
  "status": "ok",
  "poc": "04e"
}
```

### POST `/v1/query`
Runs deterministic pipeline execution over selected scenarios and returns structured run summary with timing.

Request:
```json
{
  "query": "Do you offer AC repair?",
  "context_documents": ["services.md"],
  "scenario_ids": ["std-answer-ready"]
}
```

Fields:
- `query` (required, non-empty string)
- `context_documents` (optional list of strings)
- `scenario_ids` (optional list of scenario ids from 04d mock evidence sets)

Response shape:
- `run_id`
- `total`
- `passed`
- `failed`
- `scenario_results[]` (04d harness result rows including `execution_time_ms`)
- `timing`:
  - `request_duration_ms`
  - `scenario_count`

### POST `/v1/answer`
Returns one structured answer-ready payload with citation spans and timing.

Request: same as `/v1/query`.

Response shape:
- `query`
- `answer_text`
- `citations[]`
- `decision`
- `route_applied`
- `timing`:
  - `request_duration_ms`
  - `scenario_count`

## Error Contract
- `400` for known validation/service errors (e.g., unknown `scenario_ids`)
- `422` for request schema validation errors (FastAPI/Pydantic)
- `500` for unexpected internal errors

## Traceability
Response timing includes service-layer timing and leverages per-scenario timing from 04d harness results.
