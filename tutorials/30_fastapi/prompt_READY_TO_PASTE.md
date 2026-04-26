You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\30_fastapi\

TOPIC: FastAPI for Data Engineers
SLUG: 30_fastapi
PRIORITY: DE Fundamentals SHOULD
INFRASTRUCTURE: Pure Python: fastapi, pydantic, uvicorn, pytest TestClient

============================================================
CODING STANDARDS — MANDATORY
============================================================

- Python 3.11+ compatible.
- Use type hints on every function.
- Use f-strings.
- Prefer small, testable functions.
- Avoid hidden global state except clear constants.
- No notebooks.
- No TODO, no pass, no placeholder implementation.
- Every generated file must be complete and runnable.
- Keep examples realistic for Data Engineering interviews.
- Use deterministic seeds for generated data.
- Do not require paid/cloud resources in unit tests unless explicitly called out.


============================================================
README REQUIREMENTS — MANDATORY
============================================================

Generate TWO README files for every topic.

1. Main `README.md` at the topic root.

The main README must be professional, interview-oriented, and include:

- `# <Topic Name>`
- `## What This Covers`
- `## Why This Matters in Interviews`
- `## Key Concepts`
- `## Hands-On Walkthrough`
  - Explain each generated tutorial file in order.
  - Explain what the learner should run and what output means.
- `## Common Interview Questions`
  - Include 8 to 12 practical interview questions.
  - Include strong answer guidance after each question.
- `## Deep Dive Talking Points`
  - Senior-level details, tradeoffs, edge cases, and production concerns.
- `## How This Shows Up in Production`
- `## Commands`
  - Include exact PowerShell commands to install dependencies and run tests.
- `## What To Say In An Interview`
  - Include a 60-90 second spoken explanation.

2. Capstone `capstone/README.md`.

The capstone README must be system-design and interview-story oriented, and include:

- `# Capstone: <Name>`
- `## Scenario`
- `## Architecture Overview`
  - Describe the architecture in words.
- `## Data Flow`
- `## Design Decisions`
- `## Tradeoffs`
- `## Scaling Considerations`
- `## Failure Modes`
- `## Security / Governance Notes`
- `## Interview Questions`
  - Include 8 to 12 scenario-based questions with answer guidance.
- `## How To Explain This Capstone In An Interview`
  - Include a step-by-step narrative.

The README files are not optional. Generate them before the capstone code if requested.


============================================================
TEACHING CODE REQUIREMENTS — MANDATORY
============================================================

Every Python file must include:

1. A file header docstring:

```
"""
FILE: <filename>
TOPIC: <topic>
PURPOSE: <what this file teaches>
COVERS: <concept list>
INTERVIEW FOCUS: <what to say in an interview>
"""
```

2. Teachable comments.

Comments must explain WHY, not just WHAT. Include comments like:

```
# INTERVIEW TIP:
# In an interview, emphasize that this step protects downstream consumers
# from schema drift and silent data quality failures.
```

3. Learning-oriented print statements.

Each script should print:
- What it is doing
- Why the step matters
- What interview concept the learner should remember

4. `main()` function.

Every tutorial file must have a runnable `main()` and:

```
if __name__ == "__main__":
    main()
```

5. Tests must validate business behavior, not just file existence.

Use deterministic sample data and exact assertions where possible.

============================================================
TUTORIAL FILES TO GENERATE
============================================================
Generate these files in order. For each file, include the exact functions listed. You may add helper functions only if they are useful and fully implemented.

===== FILE 01: 01_api_basics.py =====
PURPOSE: Create a basic FastAPI app with health endpoint.
COVERS: routing, status codes, response models

EXACT FUNCTION SIGNATURES:
    def create_app() -> FastAPI:
    def health_response() -> dict[str, str]:
    def version_response() -> dict[str, str]:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_pydantic_request_models.py =====
PURPOSE: Validate request/response payloads.
COVERS: Pydantic models, validation errors, schemas

EXACT FUNCTION SIGNATURES:
    def validate_ingestion_event(payload: dict) -> IngestionEvent:
    def build_event_response(event: IngestionEvent) -> dict:
    def create_validation_app() -> FastAPI:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_dependency_injection.py =====
PURPOSE: Use dependency injection for services/repositories.
COVERS: Depends, testable services, separation of concerns

EXACT FUNCTION SIGNATURES:
    def get_repository() -> InMemoryPipelineRepository:
    def create_pipeline_status_app(repository: object | None = None) -> FastAPI:
    def serialize_pipeline_status(status: dict) -> dict:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_background_tasks.py =====
PURPOSE: Demonstrate background task patterns.
COVERS: BackgroundTasks, async boundaries, queue handoff

EXACT FUNCTION SIGNATURES:
    def enqueue_ingestion_job(job_id: str, payload: dict, queue: list[dict]) -> None:
    def create_background_task_app(queue: list[dict] | None = None) -> FastAPI:
    def job_status_response(job_id: str, status: str) -> dict:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_observability_security.py =====
PURPOSE: Add logging, correlation IDs, API-key concepts.
COVERS: middleware, headers, auth dependencies

EXACT FUNCTION SIGNATURES:
    def generate_correlation_id() -> str:
    def validate_api_key(api_key: str, expected_key: str) -> bool:
    def create_observable_app(expected_api_key: str = 'dev-key') -> FastAPI:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 06: README.md =====
Generate the main tutorial README using the mandatory README requirements above.

============================================================
CAPSTONE REQUIREMENTS
============================================================
CAPSTONE SCENARIO: Build a small API for pipeline status, ingestion events, and health checks.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/pipeline_control_api.py ---
EXACT FUNCTION SIGNATURES:
    def create_pipeline_control_app() -> FastAPI:
    def submit_pipeline_run(payload: dict) -> dict:
    def get_pipeline_run(run_id: str) -> dict:
    def list_pipeline_runs() -> list[dict]:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert health endpoint returns ok
- assert invalid payload returns 422
- assert submitted pipeline run can be retrieved
- assert unauthorized request returns 401 or 403
- assert OpenAPI schema includes expected routes

Additional testing requirements:
- Use deterministic fixtures.
- Assert exact values where possible.
- Test edge cases and failure modes.
- Tests must run with `pytest capstone/test_capstone.py -v` from the topic folder unless the topic README specifies otherwise.

============================================================
GENERATION INSTRUCTIONS
============================================================

Generate ONE file at a time.

When first given this prompt, acknowledge the topic and wait.
When the user says `generate file 01`, generate only FILE 01.
When the user says `next`, generate the next file.
After tutorial files, generate README.md.
Then generate capstone/brief.md, capstone/README.md, capstone code files, and capstone/test_capstone.py.

Do not skip README files.
Do not combine multiple files unless explicitly asked.
Do not use placeholders.
Do not say "left as an exercise".
Do not omit imports.
