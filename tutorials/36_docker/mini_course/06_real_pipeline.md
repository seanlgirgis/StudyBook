# 06 — Mini Data Pipeline

[⬅️ Previous: Use Docker Compose](05_compose.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Deployment Options](07_deployment_options.md)

## Goal

Run a tiny pipeline inside Docker.

## What the pipeline does

The sample app:

1. Reads `/data/sample.txt`
2. Counts the lines
3. Writes `/data/output.txt`

Open the app:

[assets/app/app.py](assets/app/app.py)

## Run it directly with Docker

From the `mini_course` folder:

```powershell
docker run --rm -v ${PWD}/assets/data:/data docker-mini:1.0
```

## Run it with Compose

From `mini_course/assets`:

```powershell
docker compose up --build
```

## Check the result

Open:

[assets/data/output.txt](assets/data/output.txt)

## Why this matters

This is the same pattern used by real containerized pipelines:

```text
Input folder → Containerized job → Output folder
```

Later, the input/output might be S3, Postgres, Kafka, or another service.

The container idea stays the same.

## Your takeaway

A pipeline container should be easy to build, easy to run, and easy to replace.

---

[⬅️ Previous: Use Docker Compose](05_compose.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Deployment Options](07_deployment_options.md)
