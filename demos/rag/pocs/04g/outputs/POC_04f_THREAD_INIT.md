# POC 04f Thread Initialization - Deterministic Docker-First Workflow

## Purpose
This thread is initialized to teach and explain a deterministic Docker-first workflow for POC 04f.

Teaching reference snapshot:
- `outputs/POC_04f_SUMMARY.md`

## Scope Map (What each folder is for)
- `src/`: deterministic service code and container runtime files (`Dockerfile`, app entrypoint).
- `tests/`: pytest coverage for integration and validation, including placeholder-to-real-test evolution.
- `docs/`: architecture/contract/test-plan guidance (`DESIGN.md`, `CONTRACT.md`, `TEST_PLAN.md`).
- `outputs/`: reproducible evidence (`example_requests.json`, `example_responses.json`, `logs/`).

## Deterministic Endpoints
The current deterministic smoke endpoints are:
- `GET /health`
- `GET /ping`

Expected deterministic result shape:
```json
{"ok": true}
```

## Step-by-Step Docker-First Workflow
1. Build image from `src/Dockerfile`.
2. Run container with fixed host/container port mapping.
3. Execute pytest inside the running container (`tests/` contract).
4. Run smoke checks against `/health` and `/ping`.
5. Persist logs and artifacts under `outputs/logs/` for reproducibility review.

Primary automation entrypoint:
- `integrate_04f_docker.ps1`

## Reproducibility and Determinism Guidance
- Keep endpoint behavior static for deterministic verification.
- Keep tests contract-first: same inputs -> same status and response shape.
- Keep automation fail-hard: if pytest or smoke fails, the run fails.
- Keep outputs inspectable: log each stage so the workflow can be taught and replayed.

## Pytest + Docker Integration Pattern
- Docker provides runtime consistency.
- In-container pytest validates behavior in the same environment used for smoke checks.
- This pairing reduces "works on my machine" drift and improves teaching clarity.

## Placeholder Test and Output/Log Structure
Current teaching value includes visible early-stage scaffolding:
- placeholder integration test exists (`tests/test_integration.py`).
- validation test file is present for extension (`tests/test_validation.py`).
- run logs are grouped under `outputs/logs/`:
  - `pip_runtime_install.log`
  - `pip_pytest_install.log`
  - `test_results.log`
  - `smoke_test.log`

## How to Extend or Teach This POC
1. Replace placeholder tests with endpoint contract assertions (`/health`, `/ping`).
2. Add negative-path tests (bad route, malformed payload once request models are added).
3. Keep `POC_04f_SUMMARY.md` updated after each run so learners can compare snapshots.
4. Demonstrate before/after reproducibility by rerunning the same Docker-first script and diffing logs.
5. Add small, explicit teaching notes in `docs/TEST_PLAN.md` when new checks are introduced.

## Non-Goals
- No LLM/provider calls.
- No threshold tuning.
- No production/customer data.
- No movement to `integrated/servicecall-ai` in this thread.
