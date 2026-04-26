# 03 - How To Deploy Locally

Back to [Docker Pack Index](./README.md)

## Local deploy checklist

1. Docker Desktop is running.
2. Ports are free (`7077`, `8081`, optional `8085`).
3. Start master + worker.
4. Confirm both are healthy with `docker ps`.

## Start example

```powershell
docker compose -f .\samples\docker-compose.spark-standalone.sample.yml --env-file .\samples\.env.sample up -d
```

## Stop example

```powershell
docker compose -f .\samples\docker-compose.spark-standalone.sample.yml down
```

## Verify example

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Expected services:

- one master container
- at least one worker container

Next: [Why We Use Two Containers](./04_why_two_containers.md)
