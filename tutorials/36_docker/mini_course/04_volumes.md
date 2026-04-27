# 04 — Use Volumes for Data

[⬅️ Previous: Build Your First Image](03_build_image.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Use Docker Compose](05_compose.md)

## Goal

Use a local folder as container data storage.

## Problem

Containers are temporary.

If a container writes data inside itself, that data can disappear when the container is removed.

## Solution

Mount a folder from your computer into the container.

From the `mini_course` folder:

```powershell
docker run --rm -v ${PWD}/assets/data:/data docker-mini:1.0
```

## What this means

```text
${PWD}/assets/data  →  /data inside the container
```

The container reads and writes files through `/data`.

Your Windows folder keeps the results.

## Check the output

Open:

[assets/data/output.txt](assets/data/output.txt)

You should see a line count written by the container.

## Why this matters

Data engineering containers usually need external data:

- input files
- output files
- logs
- checkpoints

Volumes are how containers safely work with that data.

## Your takeaway

Use images for code. Use volumes for data.

---

[⬅️ Previous: Build Your First Image](03_build_image.md) | [🏠 Start](00_START_HERE.md) | [Next ➡️ Use Docker Compose](05_compose.md)
