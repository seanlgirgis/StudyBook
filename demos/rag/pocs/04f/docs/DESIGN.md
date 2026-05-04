# DESIGN.md - POC 04f Deployable Service Layer

## Objective
POC 04f packages the validated deterministic FastAPI service from POC 04e into a deployment-ready service layer for Docker and ECS/Fargate style runtime.

The goal is operational readiness without changing core deterministic behavior:
- preserve mock evidence pipeline behavior
- preserve validation outcomes
- preserve timing metric behavior
- preserve non-LLM, non-tuned deterministic routing

## Key Design Notes
### Deterministic behavior
- Keep deterministic logic from 04e intact.
- No LLM calls, no threshold tuning, no customer data.
- Preserve mock evidence and scenario-based outcomes from 04d/04e.
- Same input should produce contract-consistent output.

### Containerization approach
- Use a minimal Docker runtime for FastAPI service execution.
- Treat containerization as a packaging/runtime concern, not business-logic rewrite.
- Bind host/port explicitly for Docker and ECS/Fargate compatibility.
- Keep startup predictable and reproducible.

### Logging & Observability
- Emit container-friendly logs to stdout/stderr.
- Include request lifecycle and error-path logging.
- Preserve timing metrics in deterministic response payloads.
- Keep observability lightweight and practical for POC stage.

### Testing
- Validate endpoints in containerized context.
- Validate deterministic mock scenarios and negative paths.
- Verify request validation, error behavior, and response structure.
- Verify timing and log presence for operational confidence.

### Deployment Notes
- Required: Dockerfile.
- Optional: docker-compose and ECS/Fargate template/script.
- Use synthetic/mock data only.
- Stay in `pocs/04f` scope; do not move to integrated lane.

## Teaching Notes
This POC demonstrates a common production path: first stabilize deterministic behavior, then package it for deployment without changing model-free business logic.
