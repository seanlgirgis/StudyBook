# 03A — Compose Data Stack

Run:

```powershell
copy .env.example .env
python 03_docker_compose.py
```

Check database:

```powershell
docker compose exec postgres psql -U pipeline -d studybook -c "SELECT * FROM pipeline_runs ORDER BY id DESC;"
```

Stop:

```powershell
docker compose down
```

Destroy database volume too:

```powershell
docker compose down --volumes
```
