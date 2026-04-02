SAVE AS: docker_k8s_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Docker and Kubernetes for the first time in a data engineering context.
No placeholders. No TODO comments. Every cell must execute.

TASK: Generate docker_k8s_intro.ipynb — a Jupyter notebook covering the container mental model,
Docker CLI fundamentals, and a first Kubernetes Pod running a DE workload.

DATASET CONTEXT — do not deviate:
- Citi narrative: the telemetry stack runs in Docker containers — understanding containers is
  prerequisite to understanding every other technology in this stack
- Local Docker Desktop is running on Windows with all the Databases + Technologies stacks active

TECH STACK CONTEXT — do not deviate:
- Docker Desktop is running (confirmed — 6 citi_* containers up)
- kubectl is available (Docker Desktop includes Kubernetes — enable it in settings)
- All docker commands run via subprocess from this notebook

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Docker + Kubernetes — First Contact"
- 3-paragraph mental model: container vs VM, image vs container, why containers matter for DE
- Citi framing: "Every service in the Citi telemetry stack — Kafka, Spark, Airflow, MLflow —
  runs in a Docker container. Understanding containers means understanding your infrastructure."
- ASCII diagram: [Dockerfile] → [docker build] → [Image] → [docker run] → [Container]
  Below: [Container 1] [Container 2] ... → [Docker Compose] → [Stack]

SECTION 2 — Install + Imports (code cell)
- imports: subprocess, json, os, pathlib

SECTION 3 — Docker CLI Fundamentals (code cell + markdown)
- Markdown: H2 "Docker CLI — the 10 commands you use daily"
- Code: run each command via subprocess and print output:
  1. docker version (print Server Engine version)
  2. docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" (show running containers)
  3. docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | head -10
  4. docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
- Print all outputs clearly labeled

SECTION 4 — Inspect a Running Container (code cell + markdown)
- Markdown: "Inspect the citi_kafka container — see its configuration, network, mounts"
- Code:
  - docker inspect citi_kafka → parse JSON → print:
    - Image, Status, IPAddress (from NetworkSettings)
    - Ports mapping
    - Mounts (source → destination)
  - docker logs citi_kafka --tail 5 → print last 5 lines

SECTION 5 — Build a Custom Image (code cell + markdown)
- Markdown: H2 "Building a Custom Image"
  - Explain: Dockerfile = instructions to build an image layer by layer
- Code:
  - Write /tmp/citi_checker/Dockerfile:
    ```
    FROM python:3.11-slim
    RUN pip install psycopg2-binary requests
    COPY check.py /app/check.py
    WORKDIR /app
    CMD ["python", "check.py"]
    ```
  - Write /tmp/citi_checker/check.py:
    ```python
    import psycopg2, json
    conn = psycopg2.connect(host="host.docker.internal", port=5432,
        dbname="de_telemetry", user="de_admin", password="DeAdmin2026!")
    cur = conn.cursor()
    cur.execute("SELECT severity, COUNT(*) FROM alerts GROUP BY severity ORDER BY COUNT(*) DESC")
    rows = cur.fetchall()
    print(json.dumps({row[0]: row[1] for row in rows}, indent=2))
    conn.close()
    ```
  - docker build -t citi-checker:1.0 /tmp/citi_checker/
  - docker run --rm --add-host host.docker.internal:host-gateway citi-checker:1.0
  - Print output (JSON of severity counts)

SECTION 6 — Docker Compose Concepts (markdown cell)
- H2: "Docker Compose — Orchestrating Multiple Containers"
- Cover: services, networks, volumes, depends_on, env_file, health checks
- Show a simplified version of the citi tech stack compose structure (abbreviated YAML in a code fence)
- Key insight: "docker compose up -d starts all services in dependency order; docker compose down removes them"

SECTION 7 — Kubernetes Mental Model (markdown cell)
- H2: "Kubernetes — Container Orchestration at Scale"
- 3-paragraph mental model: cluster (control plane + worker nodes), Pod as smallest unit,
  why K8s vs Docker Compose (self-healing, scaling, rolling deploys, multi-node)
- ASCII diagram:
  ```
  [kubectl] → [API Server] → [Scheduler] → [Worker Node]
                                              ├── Pod: citi-kafka
                                              ├── Pod: citi-spark
                                              └── Pod: citi-airflow
  ```
- Note: "Docker Desktop includes a single-node K8s cluster. Enable: Docker Desktop → Settings → Kubernetes → Enable"

SECTION 8 — Enable K8s Check (code cell + markdown)
- Markdown: "Verify kubectl is available"
- Code:
  - subprocess.run(["kubectl", "version", "--client"], ...) → print output
  - subprocess.run(["kubectl", "cluster-info"], ...) → print output
  - If kubectl not found: print "Enable Kubernetes in Docker Desktop Settings → Kubernetes → Enable Kubernetes → Apply"

SECTION 9 — First Pod: Run citi-checker in K8s (code cell + markdown)
- Markdown: H2 "First Kubernetes Pod"
  - Explain: a Pod is a wrapper around one or more containers with shared network/storage
- Code:
  - Write /tmp/citi-checker-pod.yaml:
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: citi-checker
      labels:
        app: citi-checker
    spec:
      containers:
      - name: citi-checker
        image: citi-checker:1.0
        imagePullPolicy: Never
      hostAliases:
      - ip: "host-gateway"
        hostnames:
        - "host.docker.internal"
      restartPolicy: Never
    ```
  - kubectl apply -f /tmp/citi-checker-pod.yaml
  - Wait 10s then: kubectl logs citi-checker
  - kubectl get pod citi-checker -o wide
  - kubectl delete pod citi-checker
  - Print all outputs

SECTION 10 — Key K8s Objects Cheatsheet (markdown cell)
- H2: "K8s Objects — the 6 you must know for DE interviews"
- Table:

| Object | What it does | DE use case |
|--------|-------------|-------------|
| Pod | Runs one or more containers | A single Spark executor |
| Deployment | Manages N replicas of a Pod, self-healing | Kafka Connect workers |
| Service | Stable network endpoint for Pods | Expose Airflow webserver |
| ConfigMap | Injects non-secret config into Pods | Airflow env vars |
| Secret | Injects secrets (base64) into Pods | DB passwords |
| PersistentVolumeClaim | Attaches durable storage to a Pod | Kafka data volume |

SECTION 11 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: Docker CLI, custom image built + ran, Docker Compose mental model,
  K8s cluster verified, first Pod deployed
- Citi tie-in: "Every Spark executor in production Citi runs as a K8s Pod.
  The KubernetesExecutor in Airflow spins a Pod per task and deletes it when done."
- Next: "Run terraform_intro.ipynb for IaC, then infra_concepts.md for vocabulary."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- All subprocess calls: capture_output=True, text=True
- Section 8 must handle kubectl not found gracefully (print instructions, do not crash)
- Section 9 must handle K8s not enabled gracefully
- No placeholder credentials

ACCEPTANCE: Sections 3-6 execute. Section 8 and 9 execute if K8s enabled.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

