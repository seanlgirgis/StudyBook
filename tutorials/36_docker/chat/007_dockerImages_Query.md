Yes — exactly.

You now have **Docker source files** in the folder, and Docker has built **images** from them.

Important distinction:

```text
Your folder files = recipes and app code
Docker images = built packages stored inside Docker Desktop
```

To see the images, run:

```powershell
docker images tutorial36-pipeline
```

You should see something like:

```text
tutorial36-pipeline   base-1.0.0        1.87GB
tutorial36-pipeline   optimized-1.0.0   586MB
tutorial36-pipeline   multistage-1.0.0  586MB
```

Your current folder has the recipes:

```text
Dockerfile.base        -> built the big/basic image
Dockerfile.optimized   -> built the cleaner image
Dockerfile.multistage  -> built the builder/runtime image
Dockerfile.dev         -> dev workflow image recipe
```

One-liner:

> The files in `36_docker` are the kitchen recipes; the Docker images are the cooked meals stored in Docker Desktop.
