````md
# Talking to Your Local Docker Engine

## Big idea

When you type:

```powershell
docker images
docker ps
docker run ...
docker build ...
````

you are not just running random commands.

You are using the Docker CLI to talk to the local Docker Engine.

## Mental model

PowerShell
→ Docker CLI
→ Docker Engine / Docker Desktop
→ local images, containers, volumes, networks

## What to ask Docker

### What images do I have?

```powershell
docker images
```

Use this after `docker build`.

Expected: image names, tags, sizes.

---

### What containers are running?

```powershell
docker ps
```

Use this after `docker run` or `docker compose up`.

Expected: running containers only.

---

### What containers exist, including stopped ones?

```powershell
docker ps -a
```

Use this when something ran and disappeared.

Expected: running + stopped containers.

---

### What happened inside a container?

```powershell
docker logs <container_name_or_id>
```

Use this when a container started but failed.

Expected: app logs.

---

### What images/containers/volumes are using space?

```powershell
docker system df
```

Use this when Docker Desktop gets large.

Expected: storage summary.

---

### What is inside an image?

```powershell
docker history <image_name:tag>
```

Use this after building images.

Expected: image layers and sizes.

## Key idea

`docker build` creates images.

`docker run` creates containers.

`docker images` asks Docker Engine what images exist.

`docker ps` asks Docker Engine what containers are running.

```

So yes: this belongs in the tutorial. It makes the whole thing much easier to understand before Compose.
```
