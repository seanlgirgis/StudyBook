# POC 04f Workflow Diagram - Deterministic Docker-First Teaching View

## Diagram
```mermaid
flowchart TD
    A["src/app.py\nDeterministic FastAPI endpoints"] --> B["integrate_04f_docker.ps1\nDocker-first automation runner"]
    T1["tests/test_integration.py\nReal endpoint assertions"] --> B
    T2["tests/test_validation.py\n404 boundary check"] --> B

    B --> C["Docker build\nImage: poc_04f_service"]
    C --> D["Container run\nContainer: poc_04f_service_run\nPort 8000:8000"]

    D --> E["In-container pytest\n/workspace/tests"]
    E --> F["outputs/logs/test_results.log\nExpected: collected 3, passed 3"]

    D --> G["Smoke tests\nGET /health and GET /ping"]
    G --> H["/health -> {\"ok\": true}\nHTTP 200"]
    G --> I["/ping -> {\"ok\": true}\nHTTP 200"]
    G --> J["outputs/logs/smoke_test.log\nExpected: ok=true"]

    E --> K["outputs/example_requests.json"]
    E --> L["outputs/example_responses.json"]

    F --> M["POC_04f_SUMMARY.md\nTeaching snapshot"]
    J --> M
    K --> M
    L --> M

    N["POC_04f_THREAD_INIT.md\nThread teaching context"] --> M
    O["POC_04f_kickoff_prompt.md\nOriginal scope and intent"] --> M
```

## Short Explanation
This flow documents the deterministic Docker-first verification loop for POC 04f.

- `src/app.py` defines deterministic endpoints `/health` and `/ping`, each returning `{"ok": true}`.
- `integrate_04f_docker.ps1` orchestrates build, run, in-container pytest, and smoke checks.
- `tests/test_integration.py` and `tests/test_validation.py` validate endpoint behavior and boundary handling.
- Verification evidence is persisted in:
  - `outputs/logs/test_results.log`
  - `outputs/logs/smoke_test.log`
  - `outputs/example_requests.json`
  - `outputs/example_responses.json`
- `POC_04f_SUMMARY.md` acts as the consolidated onboarding and review snapshot, with thread/kickoff artifacts providing additional context.

## Teaching Notes
- Reproducibility is achieved by running the same Docker-first script and comparing stable outputs.
- Determinism is demonstrated by fixed endpoint contracts and repeatable passing test/smoke evidence.
- Extension path: add tests first, then update automation/evidence, then refresh the summary snapshot.
