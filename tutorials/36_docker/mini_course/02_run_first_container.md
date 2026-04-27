# 02 — Run Your First Container

[⬅️ Previous: What Docker Is](01_what_is_docker.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Build Your First Image](03_build_image.md)

## Goal

Run Python inside Docker without installing Python yourself.

## Command

Run this from PowerShell:

```powershell
docker run --rm python:3.11-slim python -c "print('Hello from Docker')"
```

## What happened?

Docker did four things:

1. Found the `python:3.11-slim` image
2. Downloaded it if needed
3. Started a container
4. Ran your Python command

`--rm` means: remove the container after it exits.

## Why this matters

You just ran Python from a clean environment.

This is the foundation of reproducible development.

## Try another command

```powershell
docker run --rm python:3.11-slim python --version
```

## Your takeaway

A container is just a process running inside an isolated environment.

---

[⬅️ Previous: What Docker Is](01_what_is_docker.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Build Your First Image](03_build_image.md)
