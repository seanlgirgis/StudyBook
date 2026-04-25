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

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\docker-data-engineering.html
