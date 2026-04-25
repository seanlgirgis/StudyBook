# Docker for Data Engineers — ChatGPT Project Prompts

Priority: 🔴 Critical — every modern pipeline runs in containers

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Docker for Data Engineers
Slug: docker-data-engineering

Extra coverage required:
- What a container is — process isolation using Linux namespaces and cgroups; not a VM, shares the host OS kernel; starts in milliseconds
- Image vs container — image is the immutable blueprint (layers on disk), container is the running instance of that image
- Dockerfile anatomy — FROM (base image), COPY (files in), RUN (install packages), ENV (environment variables), WORKDIR (working directory), ENTRYPOINT vs CMD (what runs)
- Layer caching — each Dockerfile instruction is a cached layer; COPY requirements.txt and pip install before COPY . to avoid reinstalling packages on every code change
- Multi-stage builds — build stage installs heavy dependencies; final stage copies only the artifact; dramatically reduces image size
- python:3.11-slim vs python:3.11 — slim excludes build tools and most OS packages; use slim for production, full for building C-extension packages
- .dockerignore — exclude .git, __pycache__, .env, data files, and test fixtures from the build context; large contexts slow builds
- Environment variables and secrets — ENV sets build-time vars (non-secret); --env-file at runtime for secrets; never bake credentials into an image layer
- Docker Compose — defining multi-container local dev environments; depends_on for service ordering; named volumes for database persistence; named networks for service discovery
- Volumes and bind mounts — volume for persistent data managed by Docker; bind mount for live code reloading during development
- Building and running pipeline containers — docker build -t name:tag ., docker run --env-file .env name:tag; reading logs with docker logs
- Running in ECS Fargate — what you build locally maps directly to a task definition; image URI from ECR, environment variables from Secrets Manager
- Debugging containers — docker exec -it container_id bash; docker logs --follow; common entrypoint crashes and how to diagnose them

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Containers vs VMs — what isolation actually means
  2. Images & Layers — the build model
  3. Dockerfile Anatomy — key instructions
  4. Layer Caching & Multi-Stage Builds
  5. Environment Variables, Secrets & .dockerignore
  6. Docker Compose — local multi-container dev
  7. Volumes & Networking
  8. Running Pipelines in ECS Fargate
  9. Debugging Containers
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\docker-data-engineering.html
