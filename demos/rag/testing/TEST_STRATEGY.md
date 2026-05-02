# Test Strategy

## Goals

ServiceCall AI must prove that it can:

1. Retrieve the right documents.
2. Answer with citations.
3. Refuse unsupported answers.
4. Classify customer intake.
5. Escalate risky cases.
6. Log outcomes.
7. Serve responses through FastAPI.
8. Support a website chat widget.
9. Run locally, in Docker, and eventually on ECS Fargate.

## Test Layers

- Unit tests
- Pydantic schema validation tests
- Retrieval tests
- Citation tests
- Guardrail tests
- Escalation tests
- Outcome logging tests
- API tests
- UI smoke tests
- Docker smoke tests
- Deployment smoke tests
- Manual demo tests
