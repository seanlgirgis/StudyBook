# Database Mastery Stack — Setup Guide
### Sean Edition · WSL2 · D Drive · All 6 Databases

> **Mantra:** Simplicity and clarity is Gold.

---

## What this stack gives you

| Container | Purpose | Port | UI |
|-----------|---------|------|-----|
| `de_postgres` | Relational anchor | 5432 | pgAdmin / DBeaver |
| `de_redis` | Key-value / cache | 6379 | redis-cli |
| `de_cassandra` | Wide-column | 9042 | cqlsh (inside container) |
| `de_neo4j` | Graph | 7687 (bolt) | http://localhost:7474 |
| `de_influxdb` | Time-series | 8086 | http://localhost:8086 |
| `de_elasticsearch` | Search / vector | 9200 | via Kibana |
| `de_kibana` | ES visual explorer | 5601 | http://localhost:5601 |

All data lives on **D drive** — never lost when containers are removed.  
All containers share the `de_network` — they talk to each other by service name.

---

## Prerequisites

- Docker Desktop with WSL2 backend ✅ (confirmed)
- D:\Workspace\Basics\Databases\_setup\ as working directory

---

## First-time setup (do once)

### Step 1 — Create volume folders on D drive

```powershell
cd D:\Workspace\Basics\Databases\_setup

# Create all volume directories
$dirs = @(
    "volumes\postgres",
    "volumes\postgres_init",
    "volumes\redis",
    "volumes\cassandra\data",
    "volumes\neo4j\data",
    "volumes\neo4j\logs",
    "volumes\neo4j\import",
    "volumes\neo4j\plugins",
    "volumes\influxdb\data",
    "volumes\influxdb\config",
    "volumes\elasticsearch\data",
    "volumes\kibana"
)
foreach ($d in $dirs) { New-Item -ItemType Directory -Force -Path $d | Out-Null; Write-Host "Created: $d" }
```

### Step 2 — Set WSL2 memory limit (prevents RAM hogging)

Create or edit `C:\Users\<YourUsername>\.wslconfig`:

```ini
[wsl2]
memory=16GB
processors=10
swap=4GB
```

Restart WSL2 after:
```powershell
wsl --shutdown
```

### Step 3 — Start the stack

```powershell
cd D:\Workspace\Basics\Databases\_setup
docker compose up -d
```

Watch startup:
```powershell
docker compose logs -f
```

Cassandra takes ~60 seconds to be ready. Everything else is up in ~30 seconds.

### Step 4 — One-time Kibana password setup (Elasticsearch only)

Kibana needs its own internal user password set. Run this once after ES is healthy:

```powershell
docker exec -it de_elasticsearch elasticsearch-reset-password -u kibana_system -i
```

When prompted, enter the same password as `KIBANA_PASSWORD` in your `.env` file (`DeKibana2026!`).

Then restart Kibana:
```powershell
docker compose restart kibana
```

### Step 5 — Verify everything

```powershell
python verify_all.py
```

All green = you're ready to learn.

---

## Daily usage

```powershell
# Start everything
docker compose up -d

# Stop everything (data preserved)
docker compose down

# Start just one DB
docker compose up -d postgres

# Check what's running
docker compose ps

# View logs for one container
docker compose logs -f cassandra
```

---

## Shell access into any container

```powershell
# PostgreSQL
docker exec -it de_postgres bash
# then: psql -U de_admin -d de_telemetry

# Redis
docker exec -it de_redis sh
# then: redis-cli -a DeRedis2026!

# Cassandra — CQL shell
docker exec -it de_cassandra cqlsh

# Neo4j
docker exec -it de_neo4j bash
# then: cypher-shell -u neo4j -p DeNeo4j2026!

# InfluxDB
docker exec -it de_influxdb bash
# then: influx

# Elasticsearch
docker exec -it de_elasticsearch bash
```

---

## Copy files into containers

```powershell
# Copy a SQL file into postgres container
docker cp my_schema.sql de_postgres:/tmp/

# Copy CSV into Cassandra
docker cp data.csv de_cassandra:/tmp/

# Drop files for Neo4j import (bind mount — just copy to folder)
copy my_data.csv volumes\neo4j\import\
# Then inside Neo4j: LOAD CSV FROM 'file:///my_data.csv'
```

---

## Connection strings for Python notebooks

```python
# PostgreSQL
import psycopg2
conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="de_telemetry", user="de_admin", password="DeAdmin2026!"
)

# Redis
import redis
r = redis.Redis(host="localhost", port=6379, password="DeRedis2026!", decode_responses=True)

# Cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
cluster = Cluster(["localhost"], port=9042)
session = cluster.connect()

# Neo4j
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "DeNeo4j2026!"))

# InfluxDB
from influxdb_client import InfluxDBClient
client = InfluxDBClient(url="http://localhost:8086", token="de-influxdb-super-secret-token-2026", org="de_org")

# Elasticsearch
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "DeElastic2026!"))
```

---

## Useful URLs

| Service | URL |
|---------|-----|
| Neo4j Browser | http://localhost:7474 |
| InfluxDB UI | http://localhost:8086 |
| Kibana | http://localhost:5601 |
| Elasticsearch health | http://localhost:9200/_cluster/health |

---

## Python packages needed

```bash
pip install psycopg2-binary redis cassandra-driver neo4j influxdb-client elasticsearch --break-system-packages
```

Or from the workspace:
```powershell
pip install -r requirements_databases.txt --break-system-packages
```

---

## Troubleshooting

**Cassandra won't start:**
```powershell
docker compose logs cassandra
# Usually needs more time — wait 90 seconds and retry
```

**Elasticsearch exits immediately:**
```powershell
# WSL2 needs this — run once per WSL session
wsl -d docker-desktop -u root -- sysctl -w vm.max_map_count=262144
```

**Port already in use:**
```powershell
netstat -ano | findstr :5432
# Change the port in .env and restart
```

**Reset a single DB (wipe data and start fresh):**
```powershell
docker compose stop postgres
Remove-Item -Recurse -Force volumes\postgres
New-Item -ItemType Directory volumes\postgres
docker compose up -d postgres
```

---

*Part of Sean's Database Mastery curriculum*  
*Simplicity and clarity is Gold.*
