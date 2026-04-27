# 03 — Build Your First Image

[⬅️ Previous: Run Your First Container](02_run_first_container.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Use Volumes for Data](04_volumes.md)

## Goal

Build your own Docker image from a Dockerfile.

## Look at the Dockerfile

Open:

[assets/Dockerfile](assets/Dockerfile)

It says:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app/ ./app/
CMD ["python", "app/app.py"]
```

## Build the image

From the `mini_course` folder:

```powershell
docker build -t docker-mini:1.0 ./assets
```

## Run the image

```powershell
docker run --rm docker-mini:1.0
```

## What happened?

Docker read the Dockerfile and built an image named:

```text
docker-mini:1.0
```

Then it ran your Python app from inside the container.

## Why this matters

You now control the runtime environment instead of relying on whatever is installed on your computer.

## Your takeaway

A Dockerfile is a recipe. An image is the built result.

---

[⬅️ Previous: Run Your First Container](02_run_first_container.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Use Volumes for Data](04_volumes.md)
