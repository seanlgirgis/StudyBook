# 08 — Docker Cheat Sheet

[⬅️ Previous: Deployment Options](07_deployment_options.md) | [🏠 Start](00_START_HERE.md)

## Build

```powershell
docker build -t docker-mini:1.0 ./assets
```

## Run

```powershell
docker run --rm docker-mini:1.0
```

## Run with a volume

```powershell
docker run --rm -v ${PWD}/assets/data:/data docker-mini:1.0
```

## List running containers

```powershell
docker ps
```

## List all containers

```powershell
docker ps -a
```

## List images

```powershell
docker images
```

## Remove an image

```powershell
docker rmi docker-mini:1.0
```

## Compose up

```powershell
cd assets
docker compose up --build
```

## Compose down

```powershell
docker compose down
```

## Clean unused Docker objects

Careful: this removes unused containers, networks, images, and cache.

```powershell
docker system prune
```

## Final takeaway

Docker is not one command. It is a workflow:

```text
write Dockerfile → build image → run container → mount data → compose services → deploy later
```

---

[⬅️ Previous: Deployment Options](07_deployment_options.md) | [🏠 Start](00_START_HERE.md)
