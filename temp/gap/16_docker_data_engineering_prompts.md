# Docker for Data Engineers — ChatGPT Project Prompts

Priority: 🔴 Critical — every modern pipeline runs in containers

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Docker for Data Engineers
Slug: docker-data-engineering
Extra coverage required: what a container is — process isolation using Linux namespaces and cgroups, not a VM,
image vs container — image is the blueprint, container is the running instance,
Dockerfile anatomy — FROM, COPY, RUN, ENV, WORKDIR, ENTRYPOINT vs CMD — what each does and common pitfalls,
layer caching — how Docker caches each instruction, why order of COPY and RUN matters for build speed,
multi-stage builds — using a build stage to compile dependencies and a slim final stage, why this reduces image size,
python:3.11-slim vs python:3.11 — what's in each, why slim matters for production images,
.dockerignore — what to exclude, why large data files and .git don't belong in the image,
environment variables and secrets — ENV vs ARG, never baking secrets into images, --env-file at runtime,
Docker Compose — defining multi-container setups for local development, depends_on, networks, volumes,
volumes and bind mounts — persisting data outside the container, local development patterns,
networking — container-to-container communication in compose, exposing ports to the host,
building and running data pipeline containers — docker build, docker run, reading output logs,
running pipelines in ECS — how what you build locally maps to a task definition in ECS Fargate,
Python dependency management in Docker — pip install --no-cache-dir, requirements.txt, pinning versions,
debugging containers — docker exec -it, docker logs, common entrypoint debugging patterns,
real scenario: containerizing a Python ETL pipeline that reads from S3, transforms with Pandas, writes back to S3.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug docker-data-engineering -ChunkSize 750
```

Upload final_docker-data-engineering.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_docker-data-engineering.mp3` is live on R2.

```
Topic: Docker for Data Engineers
Slug: docker-data-engineering
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_docker-data-engineering.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\docker-data-engineering.html
