# 05 — Use Docker Compose

[⬅️ Previous: Use Volumes for Data](04_volumes.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Mini Data Pipeline](06_real_pipeline.md)

## Goal

Run the app using Docker Compose.

## What Compose does

Docker Compose lets you define container settings in a YAML file instead of typing long commands.

Open:

[assets/docker-compose.yml](assets/docker-compose.yml)

## Run it

From the `mini_course/assets` folder:

```powershell
docker compose up --build
```

## Stop it

Press `Ctrl+C`, then run:

```powershell
docker compose down
```

## Why Compose matters

Real projects often need more than one container:

- app
- database
- cache
- worker
- scheduler

Compose gives those services one shared control file.

## Your takeaway

Use `docker run` for one-off commands. Use Compose for repeatable local stacks.

---

[⬅️ Previous: Use Volumes for Data](04_volumes.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Mini Data Pipeline](06_real_pipeline.md)
