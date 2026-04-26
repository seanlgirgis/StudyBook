# ChatGPT Prompt — Docker Tutorial (READY TO PASTE)
# Paste everything between the triple-backtick fences into ChatGPT

```
TOPIC: Docker for Data Engineers
SLUG: 36_docker
PRIORITY: DE Fundamentals
INFRASTRUCTURE: Docker Desktop (local) — no cloud account needed

===== CODING STANDARDS =====

FILE HEADER — every Python helper file must start with:
# ============================================================
# Topic   : Docker for Data Engineers
# File    : NN_filename.py (or Dockerfile, docker-compose.yml)
# Covers  : one-line description
# Prereqs : Docker Desktop installed and running
# Run     : see instructions inside file
# ============================================================

STYLE RULES:
- Every Dockerfile is production-quality: non-root user, HEALTHCHECK, .dockerignore, minimal layers
- All docker-compose.yml files use version-less format (Compose V2 — no "version:" key)
- Python files use subprocess.run() to demonstrate docker CLI commands; always capture=True, text=True
- Always show WHY a best practice matters (security, caching, size)
- Use explicit tags — never :latest in production Dockerfiles
- No placeholder comments, no TODO, no pass, no NotImplementedError

===== FILE 01: 01_dockerfile_basics.py =====

PURPOSE: Core Dockerfile instructions, image layers, build cache, .dockerignore
COVERS: FROM, COPY, RUN, ENV, ARG, CMD, ENTRYPOINT, EXPOSE, USER, WORKDIR

GENERATE THESE FILES (01 is a bundle):

01_dockerfile_basics.py   ← Python script that explains concepts and runs docker commands
Dockerfile.base           ← Demonstrates all core instructions
Dockerfile.optimized      ← Same app but layer-optimized version
.dockerignore             ← Proper ignore rules for a Python data pipeline
app/pipeline.py           ← Tiny sample pipeline the Dockerfiles build

--- app/pipeline.py ---
#!/usr/bin/env python3
"""Sample pipeline: reads a CSV from /data/input, counts rows, writes summary to /data/output."""
import sys, csv, json, pathlib

def main():
    input_path = pathlib.Path("/data/input/records.csv")
    output_path = pathlib.Path("/data/output/summary.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not input_path.exists():
        print("No input file — generating synthetic data")
        records = [{"id": i, "value": i * 1.5} for i in range(1000)]
        input_path.parent.mkdir(parents=True, exist_ok=True)
        with open(input_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["id","value"])
            writer.writeheader(); writer.writerows(records)
    with open(input_path) as f:
        rows = list(csv.DictReader(f))
    summary = {"row_count": len(rows), "source": str(input_path)}
    output_path.write_text(json.dumps(summary, indent=2))
    print(f"Processed {len(rows):,} rows → {output_path}")

if __name__ == "__main__":
    main()

--- Dockerfile.base --- (UNOPTIMIZED — used to show what NOT to do)
FROM python:3.11
RUN pip install pandas pyarrow
COPY . .
CMD ["python", "app/pipeline.py"]

--- Dockerfile.optimized --- (PRODUCTION QUALITY — explain each choice inline as comments)
# Pin exact version: reproducible builds. Never use :latest in production.
FROM python:3.11.9-slim-bookworm AS base

# Why: set at build time, not overridable at runtime (use ENV for runtime config)
ARG APP_VERSION=1.0.0

# Why: prevents interactive prompts during apt-get, sets locale for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    APP_VERSION=${APP_VERSION}

WORKDIR /app

# Why: copy requirements FIRST so this layer caches — only rebuilds when deps change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Why: copy app code LAST — changes here don't invalidate the pip layer
COPY app/ ./app/

# Why: non-root user prevents container breakout privilege escalation
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser && \
    chown -R appuser:appgroup /app
USER appuser

# Why: HEALTHCHECK lets orchestrators (ECS, Kubernetes) know if container is alive
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Why: CMD is overridable, ENTRYPOINT is not. Use ENTRYPOINT for the binary, CMD for default args.
ENTRYPOINT ["python"]
CMD ["app/pipeline.py"]

--- requirements.txt ---
pandas==2.2.2
pyarrow==15.0.2

--- .dockerignore ---
# Never send these to the build context (slows build, security risk)
.git/
.gitignore
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.mypy_cache/
.venv/
venv/
*.egg-info/
dist/
build/
.env
.env.*
*.duckdb
*.parquet
data/
*.log
node_modules/
.DS_Store

--- 01_dockerfile_basics.py ---
PURPOSE: Run docker build/run/inspect commands and explain each Dockerfile instruction.

EXACT FUNCTION SIGNATURES:

def build_image(tag: str, dockerfile: str, context: str = ".") -> bool:
    """
    Run: docker build -t {tag} -f {dockerfile} {context}
    Print build output line by line.
    Return True if exit code 0.
    """

def compare_image_sizes(tags: list[str]) -> None:
    """
    Run: docker images --format "{{.Repository}}:{{.Tag}}\t{{.Size}}" for each tag.
    Print comparison table showing base vs optimized image size.
    """

def inspect_layers(tag: str) -> None:
    """
    Run: docker history {tag} --no-trunc --format "{{.Size}}\t{{.CreatedBy}}"
    Print each layer with its size and the command that created it.
    Explain which layers are largest and why.
    """

def run_pipeline_container(tag: str, input_dir: str, output_dir: str) -> str:
    """
    Run: docker run --rm -v {input_dir}:/data/input -v {output_dir}:/data/output {tag}
    Return stdout from container.
    """

def explain_caching() -> None:
    """
    Print explanation of Docker layer caching with example:
    - Change requirements.txt → invalidates pip layer and all subsequent
    - Change app/pipeline.py → only rebuilds the COPY app/ layer (pip layer reused)
    Show the actual layer cache hit/miss in build output.
    """

MAIN BLOCK:
  Show build + compare + inspect sequence. Run the container and print output.

===== FILE 02: 02_multi_stage_builds.py =====

PURPOSE: Multi-stage builds — slim production images, separate builder from runtime
COVERS: AS builder pattern, COPY --from, build vs runtime deps, size reduction

GENERATE THESE FILES:

Dockerfile.multistage   ← Builder stage + runtime stage
Dockerfile.dev          ← Development stage with extra tools
02_multi_stage_builds.py ← Explanation and docker commands

--- Dockerfile.multistage ---
# Stage 1: Builder — install all build tools and compile deps
FROM python:3.11.9-slim-bookworm AS builder

WORKDIR /build

# Install build dependencies (not needed in final image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install to a prefix so we can COPY --from this exact directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime — tiny image, no build tools, no compilers
FROM python:3.11.9-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Copy ONLY the installed packages from builder — no gcc, no build caches
COPY --from=builder /install /usr/local

WORKDIR /app
COPY app/ ./app/

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup appuser && \
    chown -R appuser:appgroup /app
USER appuser

CMD ["python", "app/pipeline.py"]

--- Dockerfile.dev ---
# Development image: includes debugger, test tools, hot reload
FROM python:3.11.9-slim-bookworm AS dev

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Dev image mounts source code as volume — never COPY app code in dev
CMD ["python", "-m", "pytest", "-xvs"]

--- 02_multi_stage_builds.py ---

EXACT FUNCTION SIGNATURES:

def build_and_compare_stages() -> None:
    """
    Build both single-stage and multi-stage images.
    Print size comparison:
      python:3.11 (base)      → ~1.0 GB
      Dockerfile.base         → ~1.1 GB
      Dockerfile.optimized    → ~180 MB
      Dockerfile.multistage   → ~140 MB
    Explain: builder stage is discarded; only --from copies land in final image.
    """

def demonstrate_copy_from() -> None:
    """
    Show COPY --from pattern for multiple uses:
    1. Copy built artifacts from builder stage
    2. Copy config from a dedicated config stage
    3. Copy binary from official image into custom image:
         FROM golang:1.22 AS gobuilder
         RUN go build -o /myapp .
         FROM scratch AS final
         COPY --from=gobuilder /myapp /myapp
    """

def dev_vs_prod_workflow() -> None:
    """
    Print the two-command developer workflow:
    
    DEV (hot-reload, mounts source):
      docker build -f Dockerfile.dev -t pipeline:dev .
      docker run --rm -v $(pwd)/app:/app/app pipeline:dev
    
    PROD (immutable, slim):
      docker build --target runtime -f Dockerfile.multistage -t pipeline:prod .
      docker run --rm pipeline:prod
    
    Explain: same Dockerfile, different --target. Dev mounts code, prod bakes it in.
    """

MAIN BLOCK: build_and_compare_stages(); dev_vs_prod_workflow()

===== FILE 03: 03_docker_compose.py =====

PURPOSE: Docker Compose for multi-service data stacks
COVERS: services, networks, volumes, depends_on, health checks, env files

GENERATE THESE FILES:

docker-compose.yml             ← Full data stack: pipeline app + postgres + redis
docker-compose.override.yml    ← Dev overrides (bind mounts, debug ports)
.env.example                   ← Template for environment variables
03_docker_compose.py           ← Python helper to manage the stack

--- docker-compose.yml ---
services:
  pipeline:
    build:
      context: .
      dockerfile: Dockerfile.optimized
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=${DB_NAME:-studybook}
      - DB_USER=${DB_USER:-pipeline}
      - DB_PASSWORD=${DB_PASSWORD:?DB_PASSWORD must be set}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - pipeline_data:/data
    networks:
      - internal
    restart: on-failure:3

  postgres:
    image: postgres:16.2-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-studybook}
      POSTGRES_USER: ${DB_USER:-pipeline}
      POSTGRES_PASSWORD: ${DB_PASSWORD:?DB_PASSWORD must be set}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init_db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-pipeline} -d ${DB_NAME:-studybook}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - internal

  redis:
    image: redis:7.2.4-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - internal

volumes:
  postgres_data:
  pipeline_data:

networks:
  internal:
    driver: bridge

--- docker-compose.override.yml ---
# Dev overrides — applied automatically when running docker compose up in dev
services:
  pipeline:
    build:
      dockerfile: Dockerfile.dev
    volumes:
      - ./app:/app/app:ro   # mount source for hot-reload
    environment:
      - LOG_LEVEL=DEBUG
    ports:
      - "5678:5678"          # debugpy port

  postgres:
    ports:
      - "5432:5432"          # expose to host for DBeaver/pgAdmin access in dev only

--- 03_docker_compose.py ---

EXACT FUNCTION SIGNATURES:

def compose_up(detach: bool = True) -> bool:
    """Run docker compose up --build (-d if detach). Return True on success."""

def compose_down(volumes: bool = False) -> None:
    """Run docker compose down (--volumes if volumes=True). Print status."""

def wait_for_healthy(service: str, timeout: int = 60) -> bool:
    """
    Poll docker compose ps {service} every 2 seconds until health = healthy.
    Return True if healthy within timeout, False if timeout.
    Print: "Waiting for {service}... (10s)" with progress.
    """

def run_in_service(service: str, command: list[str]) -> str:
    """
    Run: docker compose exec {service} {command}
    Return stdout. Raise RuntimeError on non-zero exit.
    """

def print_stack_status() -> None:
    """
    Run: docker compose ps --format json
    Parse and print a formatted service status table:
      Service    | Status    | Health   | Ports
      pipeline   | running   | healthy  | -
      postgres   | running   | healthy  | 5432/tcp
      redis      | running   | healthy  | 6379/tcp
    """

MAIN BLOCK:
  print_stack_status()  # show current state
  # Demonstrate: compose_up() → wait_for_healthy("postgres") → run_in_service("postgres", ["psql", ...])

===== FILE 04: 04_data_pipeline_container.py =====

PURPOSE: Containerizing a data pipeline end-to-end — patterns for DE
COVERS: volume mounts, secrets, env vars, signals (SIGTERM), graceful shutdown

GENERATE THESE FILES:

Dockerfile.pipeline     ← Production pipeline Dockerfile with graceful shutdown
app/graceful_pipeline.py ← Pipeline that handles SIGTERM cleanly
04_data_pipeline_container.py ← Explanation and run patterns

--- app/graceful_pipeline.py ---
"""
Production-grade pipeline container: reads from /data/input, processes, writes to /data/output.
Handles SIGTERM for graceful shutdown (critical for ECS, Kubernetes).
"""
import signal, sys, time, json, os, logging, pathlib

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

class Pipeline:
    def __init__(self):
        self.shutdown_requested = False
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)

    def _handle_sigterm(self, signum, frame):
        log.info("SIGTERM received — finishing current batch and shutting down gracefully")
        self.shutdown_requested = True

    def process_batch(self, batch_id: int) -> dict:
        """Simulate one batch of processing. Check shutdown_requested between batches."""
        log.info(f"Processing batch {batch_id}")
        time.sleep(0.1)
        return {"batch_id": batch_id, "rows_processed": 1000}

    def run(self):
        log.info(f"Pipeline starting | version={os.environ.get('APP_VERSION', 'dev')}")
        results = []
        for batch_id in range(100):
            if self.shutdown_requested:
                log.info("Shutdown requested — stopping after current batch")
                break
            result = self.process_batch(batch_id)
            results.append(result)
        summary = {"total_batches": len(results), "total_rows": sum(r["rows_processed"] for r in results)}
        output = pathlib.Path("/data/output/summary.json")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(summary, indent=2))
        log.info(f"Pipeline complete: {summary}")

if __name__ == "__main__":
    Pipeline().run()

--- 04_data_pipeline_container.py ---

EXACT FUNCTION SIGNATURES:

def demonstrate_volume_patterns() -> None:
    """
    Show all volume mount patterns with use cases:
    
    1. Named volume (persistent data):
         docker run -v pipeline_data:/data pipeline:prod
         Use: database files, output that must survive container restart
    
    2. Bind mount (dev hot-reload):
         docker run -v $(pwd)/data:/data/input:ro pipeline:prod
         Use: feed input files from host, read-only for safety
    
    3. tmpfs mount (fast, non-persistent scratch space):
         docker run --tmpfs /tmp:size=512m pipeline:prod
         Use: temp files, intermediate processing — gone on stop
    
    4. Secret mount (Docker Swarm / BuildKit secrets):
         docker run --secret id=db_password pipeline:prod
         Never use ENV for secrets in production.
    
    Print each with example docker run command and use case.
    """

def demonstrate_env_and_secrets() -> None:
    """
    Show 4 ways to pass config, ranked by security:
    
    1. --env-file (GOOD): docker run --env-file .env pipeline:prod
    2. -e flag (OK for non-secrets): docker run -e LOG_LEVEL=DEBUG pipeline:prod
    3. Docker secrets (BEST for sensitive): mount at /run/secrets/db_password
    4. AWS Secrets Manager / Parameter Store (BEST for cloud):
         container reads from SSM at startup — never in environment at all
    
    Show: read_secret_from_file(secret_name) → reads /run/secrets/{name}
    Print: security ranking and why ENV vars leak into ps, docker inspect, logs
    """

def sigterm_demo() -> None:
    """
    Show why SIGTERM handling matters for DE containers:
    
    1. Start container in background
    2. docker stop sends SIGTERM, waits 10s, then SIGKILL
    3. Without handler: data corruption (partial write, uncommitted transaction)
    4. With handler: finish current batch, flush buffers, exit cleanly
    
    Show docker stop --time 30 for pipelines that need more than 10s to finish.
    Print: "Always handle SIGTERM in long-running pipeline containers"
    """

def resource_limits() -> None:
    """
    Show resource constraint flags for pipeline containers:
    
    docker run \
      --memory=2g \              # OOM kill if exceeded (protects host)
      --memory-swap=2g \         # disable swap (makes OOM predictable)
      --cpus=2.0 \               # 2 CPU cores max
      --pids-limit=200 \         # prevent fork bombs
      pipeline:prod
    
    For Compose: resources.limits.memory, resources.limits.cpus
    Print: "Always set memory limits for pipeline containers — runaway jobs kill the host"
    """

MAIN BLOCK: Print all patterns with explanations. No actual docker run needed for this file.

===== FILE 05: 05_docker_for_de.py =====

PURPOSE: Docker patterns specific to data engineering — ECR push, ECS pattern, multi-arch
COVERS: ECR push workflow, ECS task definition, healthcheck for pipelines, multi-platform builds

GENERATE THESE FILES:

05_docker_for_de.py   ← Full DE-specific Docker patterns

EXACT FUNCTION SIGNATURES:

def ecr_push_workflow() -> None:
    """
    Print the 5-step ECR push workflow (no live AWS call — show commands with explanation):
    
    Step 1: Authenticate
      aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {account}.dkr.ecr.us-east-1.amazonaws.com
    
    Step 2: Build with production tag
      docker build -t pipeline:1.2.3 --build-arg APP_VERSION=1.2.3 .
    
    Step 3: Tag for ECR
      docker tag pipeline:1.2.3 {account}.dkr.ecr.us-east-1.amazonaws.com/pipeline:1.2.3
      docker tag pipeline:1.2.3 {account}.dkr.ecr.us-east-1.amazonaws.com/pipeline:latest
    
    Step 4: Push
      docker push {account}.dkr.ecr.us-east-1.amazonaws.com/pipeline:1.2.3
    
    Step 5: Verify
      aws ecr describe-images --repository-name pipeline --query 'sort_by(imageDetails,&imagePushedAt)[-1]'
    
    Print each step with explanation.
    """

def ecs_task_definition_template() -> dict:
    """
    Return a boto3-ready ECS task definition dict for a batch pipeline container:
    {
        "family": "data-pipeline",
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE"],
        "cpu": "1024",
        "memory": "2048",
        "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
        "taskRoleArn": "arn:aws:iam::ACCOUNT:role/pipelineTaskRole",
        "containerDefinitions": [{
            "name": "pipeline",
            "image": "ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pipeline:1.2.3",
            "essential": True,
            "environment": [{"name": "LOG_LEVEL", "value": "INFO"}],
            "secrets": [{"name": "DB_PASSWORD", "valueFrom": "arn:aws:ssm:..."}],
            "logConfiguration": {"logDriver": "awslogs", "options": {"awslogs-group": "/ecs/pipeline", "awslogs-region": "us-east-1", "awslogs-stream-prefix": "pipeline"}},
            "stopTimeout": 120,  # give container 120s to handle SIGTERM before SIGKILL
            "healthCheck": {"command": ["CMD-SHELL", "python -c \"import sys; sys.exit(0)\""], "interval": 30, "timeout": 10, "retries": 3},
        }]
    }
    Print the dict as pretty JSON with inline comments explaining key fields.
    """

def multi_platform_build() -> None:
    """
    Print multi-architecture build pattern (Apple Silicon + x86 servers):
    
    # One-time setup: create a multi-platform builder
    docker buildx create --name multiplatform --use
    
    # Build and push for both ARM64 (Apple/Graviton) and AMD64 (Intel/AMD):
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pipeline:1.2.3 \
        --push \
        .
    
    Why this matters for DE:
    - Mac M1/M2/M3 laptops build ARM64 by default
    - AWS EC2 Graviton instances are ARM64 (30% cheaper)
    - Without multi-platform: container runs slow under emulation or crashes
    
    Print the commands with explanation.
    """

def docker_de_cheatsheet() -> None:
    """
    Print the 15 most-used Docker commands for data engineers:
    
    BUILD & RUN:
      docker build -t name:tag .                    # build image
      docker run --rm -it name:tag bash             # interactive shell
      docker run --rm -v $(pwd)/data:/data name:tag # mount data dir
      docker run --env-file .env name:tag           # load env vars
    
    INSPECT & DEBUG:
      docker ps -a                                  # all containers (incl stopped)
      docker logs -f container_id                  # follow logs
      docker exec -it container_id bash             # shell into running container
      docker stats                                  # live resource usage
      docker inspect container_id                  # full metadata JSON
    
    COMPOSE:
      docker compose up --build -d                  # rebuild and start detached
      docker compose down -v                        # stop and remove volumes
      docker compose logs -f service_name          # follow service logs
      docker compose exec service bash             # shell into service
    
    MAINTENANCE:
      docker system prune -af --volumes             # remove everything unused (careful!)
      docker images --filter dangling=true -q | xargs docker rmi   # remove untagged images
    """

MAIN BLOCK:
  ecr_push_workflow()
  print(json.dumps(ecs_task_definition_template(), indent=2))
  multi_platform_build()
  docker_de_cheatsheet()

===== CAPSTONE =====

Generate these files (all COMPLETE and FULLY RUNNABLE):

--- capstone/brief.md ---
Title: Containerized Data Pipeline Stack
Scenario: Build a production-ready containerized ETL pipeline that:
  1. Generates synthetic transaction data
  2. Loads it into PostgreSQL
  3. Runs a transformation job
  4. Writes results to a mounted output directory
  All services run via Docker Compose, pipeline container handles SIGTERM gracefully,
  PostgreSQL has a health check, secrets are never in ENV.

--- capstone/Dockerfile ---
Production-quality multi-stage Dockerfile for the ETL pipeline.

--- capstone/docker-compose.yml ---
Services: pipeline + postgres. Pipeline depends_on postgres (service_healthy).
Volumes: postgres_data (named), output_data (named), plus bind mount for input.

--- capstone/app/etl.py ---
ETL pipeline that:
  1. Reads /data/input/transactions.json (or generates synthetic if not present)
  2. Connects to PostgreSQL (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD from env)
  3. Creates transactions table if not exists
  4. Inserts all records
  5. Runs aggregation query: SELECT region, SUM(amount), COUNT(*) GROUP BY region
  6. Writes result to /data/output/summary.json
  7. Handles SIGTERM with graceful shutdown (finish current insert batch)

--- capstone/app/generate_data.py ---
Generates 10K synthetic transactions as /data/input/transactions.json.

--- capstone/test_capstone.py ---

EXACT TEST FUNCTIONS:

def test_dockerfile_exists_and_has_healthcheck():
    """Read capstone/Dockerfile, assert 'HEALTHCHECK' is in content."""
    content = pathlib.Path("capstone/Dockerfile").read_text()
    assert "HEALTHCHECK" in content
    assert "USER" in content           # non-root user
    assert "python:3.11" in content    # pinned version

def test_compose_has_healthcheck_for_postgres():
    import yaml
    compose = yaml.safe_load(pathlib.Path("capstone/docker-compose.yml").read_text())
    pg = compose["services"]["postgres"]
    assert "healthcheck" in pg

def test_compose_pipeline_depends_on_postgres():
    import yaml
    compose = yaml.safe_load(pathlib.Path("capstone/docker-compose.yml").read_text())
    pipeline = compose["services"]["pipeline"]
    assert "postgres" in pipeline.get("depends_on", {})

def test_etl_generates_data_if_missing():
    import tempfile, json
    with tempfile.TemporaryDirectory() as tmp:
        input_path = pathlib.Path(tmp) / "input" / "transactions.json"
        # simulate missing input — ETL should generate it
        # call the generate function directly
        from app.generate_data import generate_transactions
        records = generate_transactions(100)
        assert len(records) == 100
        assert all("amount" in r for r in records)

def test_etl_aggregation_logic():
    """Test the aggregation SQL logic with SQLite in-memory (no postgres needed)."""
    import sqlite3, json
    records = [
        {"tx_id": "T1", "region": "NORTH", "amount": 100.0},
        {"tx_id": "T2", "region": "NORTH", "amount": 200.0},
        {"tx_id": "T3", "region": "SOUTH", "amount": 50.0},
    ]
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE transactions (tx_id TEXT, region TEXT, amount REAL)")
    con.executemany("INSERT INTO transactions VALUES (?, ?, ?)", [(r["tx_id"], r["region"], r["amount"]) for r in records])
    result = con.execute("SELECT region, SUM(amount), COUNT(*) FROM transactions GROUP BY region ORDER BY region").fetchall()
    assert result[0] == ("NORTH", 300.0, 2)
    assert result[1] == ("SOUTH", 50.0, 1)
    con.close()

===== GENERATION INSTRUCTIONS =====

Generate files ONE AT A TIME in this order:
  01_dockerfile_basics.py + Dockerfile.base + Dockerfile.optimized + .dockerignore + app/pipeline.py + requirements.txt
  02_multi_stage_builds.py + Dockerfile.multistage + Dockerfile.dev
  03_docker_compose.py + docker-compose.yml + docker-compose.override.yml + .env.example
  04_data_pipeline_container.py + app/graceful_pipeline.py + Dockerfile.pipeline
  05_docker_for_de.py
  capstone/brief.md
  capstone/Dockerfile + capstone/docker-compose.yml
  capstone/app/etl.py + capstone/app/generate_data.py
  capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO, no pass.
After each file bundle, wait for me to say "next".

Acknowledge these instructions, then wait for me to say "generate file 01".
```
