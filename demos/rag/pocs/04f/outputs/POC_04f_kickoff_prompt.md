# POC 04f Kickoff Prompt (Persisted)

We are starting POC 04f: Integration of the validated RAG pipeline (from POC 04e) into a deployable service layer.

Objective:
- Take the deterministic FastAPI service from POC 04e.
- Make it ready for containerized deployment (Docker/ECS/Fargate).
- Preserve all existing mock evidence, test harness, timing metrics, and validation behavior.
- Include logging, error handling, and observability.
- Keep service deterministic: no threshold tuning, no LLM calls, no customer data.

Deliverables:
1. src/
   - Dockerfile for the FastAPI service
   - docker-compose.yaml (optional for local dev)
   - deployment scripts or ECS/Fargate template (optional)
   - updated app.py / routes.py / service.py as needed for containerized execution
2. tests/
   - Integration tests confirming endpoints work correctly in containerized context
   - Validation of mock scenarios
3. docs/
   - CONTRACT.md updated for deployment context
   - TEST_PLAN.md updated for containerized execution
4. outputs/
   - Example requests/responses from containerized service
   - Timing and logs
5. Updated project tracking files reflecting 04f start and closure once implemented

Requirements:
- Preserve existing deterministic behavior of 04e
- Include minimal but complete containerization and deployable service
- Ensure persistence via Codex before implementation
- Structure folders: pocs/04f/src, tests, docs, outputs
