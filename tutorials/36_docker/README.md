# Docker Tutorial Clean Setup — Lessons 01 to 04

This package is intentionally self-contained.

Run each lesson from its own folder. Do not copy lesson files into the root.

## Folder layout

```text
docker_tutorial_clean_01_to_04/
  01_dockerfile_basics/
  02_multi_stage_builds/
  03b_compose_simple/
  03a_compose_stack/
  04_pipeline_container/
```

## Recommended run order

```powershell
cd 01_dockerfile_basics
python 01_dockerfile_basics.py

cd ..\02_multi_stage_builds
python 02_multi_stage_builds.py

cd ..\03b_compose_simple
docker compose up --build
docker compose down

cd ..\03a_compose_stack
copy .env.example .env
python 03_docker_compose.py
docker compose down

cd ..\04_pipeline_container
python 04_data_pipeline_container.py
```

## Cleanup commands

```powershell
docker compose down
docker system df
```

Use `docker system prune` only when you understand what it removes.
