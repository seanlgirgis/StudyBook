# Acceptance Criteria

## Local Demo Acceptance

- Website opens locally.
- Chat widget opens and sends a message.
- Backend health check passes.
- Chat response matches the Pydantic response schema.
- Supported answers include citations.
- Unsupported answers fallback safely.
- Risky pricing requests create escalation decisions.
- Every chat creates an outcome event.

## Docker Acceptance

- Docker image builds.
- Container starts.
- /health returns success.
- /chat returns a valid response.

## ECS Fargate Acceptance

- ECS service becomes stable.
- Load balancer health check passes.
- CloudWatch logs receive application logs.
- Cleanup script removes demo resources.
