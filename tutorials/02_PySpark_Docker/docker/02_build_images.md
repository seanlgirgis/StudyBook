# 02 - How To Build Images And Compose

Back to [Docker Pack Index](./README.md)

## Build blocks

- `Dockerfile`: how to build one image
- `docker-compose.yml`: how multiple containers run together
- `.env`: variable values (ports, names, memory)

## Typical build flow

1. Prepare env values.
2. Build image(s): `docker compose build`
3. Start services: `docker compose up -d`
4. Verify: `docker ps`

## Files in this pack

- Compose template: [docker-compose.spark-standalone.sample.yml](./samples/docker-compose.spark-standalone.sample.yml)
- Client image template: [Dockerfile.pyspark-client.sample](./samples/Dockerfile.pyspark-client.sample)
- Env template: [.env.sample](./samples/.env.sample)

## Build command example

```powershell
docker compose -f .\samples\docker-compose.spark-standalone.sample.yml --env-file .\samples\.env.sample up -d
```

Next: [How To Deploy Locally](./03_deploy_local_compose.md)
