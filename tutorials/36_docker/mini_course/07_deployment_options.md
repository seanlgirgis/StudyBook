# 07 — Deployment Options

[⬅️ Previous: Mini Data Pipeline](06_real_pipeline.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Cheat Sheet](08_cheatsheet.md)

## Goal

Understand where Docker containers can run.

## Option 1 — Local machine

Use Docker Desktop on Windows.

Best for:

- learning
- development
- testing
- small local tools

## Option 2 — A single server

Install Docker on a VM and run containers there.

Best for:

- simple internal apps
- personal servers
- lightweight deployments

## Option 3 — Cloud container services

Examples:

- AWS ECS
- AWS EKS
- Google Cloud Run
- Azure Container Apps

Best for:

- production apps
- scheduled jobs
- scalable APIs
- managed deployments

## Option 4 — Kubernetes

Kubernetes manages many containers across many machines.

Best for:

- large platforms
- complex services
- teams needing orchestration

Not best for your first Docker week.

## Beginner path

```text
Docker Desktop → Docker Compose → Cloud container service → Kubernetes later
```

## Your takeaway

Build the image once. Run it locally first. Deploy it later when the image is proven.

---

[⬅️ Previous: Mini Data Pipeline](06_real_pipeline.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Cheat Sheet](08_cheatsheet.md)
