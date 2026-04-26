# Prompting Workflow — Tutorial Code Generation
# Last updated: 2026-04-25

---

## Overview

prompt.md → ChatGPT (web) → .py files → save → run locally → mark ROADMAP.md

This is the main weekly workflow. One topic at a time.
Each topic takes ~30-60 minutes (generation + review + local testing).

---

## Step 1 — Pick the Next Topic

Open `D:\StudyBook\tutorials\_manager\ROADMAP.md`
Find the first topic where prompt.md = ✅ and .py files = ⬜
That's your next topic.

If prompt.md is ⬜, write it first (see Step 0).

---

## Step 0 (if needed) — Write prompt.md

Reference: `D:\StudyBook\tutorials\_meta\MASTER_PROMPT_TEMPLATE.md`

1. Copy the template
2. Fill in: TOPIC, SLUG, PRIORITY, INFRASTRUCTURE
3. Define 5 tutorial files with:
   - filename (e.g., `01_streams_and_shards.py`)
   - one-line purpose
   - key concepts (3-5 bullet ideas)
   - 5-6 function signatures with purpose
   - main block description
4. Define capstone: brief.md, capstone.py, test_capstone.py
5. Add INFRASTRUCTURE NOTES specific to the topic
6. Save to `tutorials/NN_topic/prompt.md`
7. Mark prompt.md = ✅ in ROADMAP.md

**Container check:** Before writing, check DOCKER_INVENTORY.md to see which
existing Docker container this topic uses. Reference that container's port/credentials
in the INFRASTRUCTURE NOTES — do NOT tell ChatGPT to spin up new Docker.

---

## Step 2 — Open ChatGPT

Use ChatGPT web (not API) — saves tokens.
Option A: New chat in default GPT-4o
Option B: Create "Project 3 — Tutorial Generator" project and paste prompt there

Paste the ENTIRE content of prompt.md into the chat.

---

## Step 3 — Generate Files One at a Time

```
You: [paste prompt.md contents]
ChatGPT: "Understood. Ready. Tell me when to generate file 01."
You: "generate file 01"
ChatGPT: [generates 01_filename.py — full file, complete, runnable]
You: "generate file 02"
... continue through 05 ...
You: "generate capstone"
ChatGPT: [generates brief.md, then capstone.py, then test_capstone.py]
```

**Do not say "next" — always say "generate file 02" etc.**
Specific commands produce better output.

---

## Step 4 — Save Files

Tutorial directory structure:
```
tutorials/NN_topic/
  setup/
    01_filename.py
    02_filename.py
    03_filename.py
    04_filename.py
    05_filename.py
  capstone/
    brief.md
    capstone.py
    test_capstone.py
```

Save each file immediately after generation — don't wait until end.

---

## Step 5 — Review Before Running

Quick review checklist:
- [ ] File header matches TUTORIAL_STANDARDS.md format
- [ ] env vars listed (AWS_REGION, AWS_PROFILE, etc.)
- [ ] Functions have docstrings
- [ ] Main block is present and runnable
- [ ] cleanup() exists for AWS topics
- [ ] No hardcoded credentials

---

## Step 6 — Run Locally

### AWS topics
```powershell
# Set env vars first
$env:AWS_PROFILE = "personal"
$env:AWS_REGION = "us-east-1"
$env:KINESIS_STREAM_NAME = "studybook-test"

python tutorials/01_aws_kinesis/setup/01_streams_and_shards.py
```

### Docker topics (Airflow, Postgres, Kafka, etc.)
```powershell
# Confirm containers are running
docker ps

# Run
python tutorials/03_apache_airflow/setup/01_dag_basics.py
```

### Pure Python topics
```powershell
pip install deltalake pandas pyarrow  # per file header
python tutorials/05_delta_lake/setup/01_delta_basics_and_acid.py
```

---

## Step 7 — Fix and Re-run

Common issues:
- Missing import → add to file
- Wrong env var name → check DOCKER_INVENTORY.md defaults
- AWS permission error → check IAM role has correct policies
- Port wrong for Docker → check DOCKER_INVENTORY.md (Kafka = 29092, Airflow = 8082)

If ChatGPT-generated code has a bug, fix it directly in the .py file.
Do NOT regenerate the whole file — just patch the function.

---

## Step 8 — Update ROADMAP.md

Once all 5 .py files + capstone are saved and tested:
1. Open `D:\StudyBook\tutorials\_manager\ROADMAP.md`
2. Change .py files column to 🔨
3. Change Tested column to ✔️

---

## Tips for Good Generation

**Do say:**
- "generate file 01" (not "next" or "continue")
- "The Kafka bootstrap server is localhost:29092" (reinforce infra details)
- "Make the main block actually demonstrate the key function, not just call it"

**Do ask for fixes like:**
- "The docstring for create_stream() is missing the WHY field — add it"
- "cleanup() is missing — add it as the last function"
- "The main block catches all exceptions with bare `except:` — fix to catch specific types"

**If output is truncated:**
- "Continue from where you left off in 02_filename.py"
- Or: "Complete the main block for 02_filename.py"

---

## Infrastructure Notes Quick Reference

(Full details in DOCKER_INVENTORY.md)

| Infra | What to tell ChatGPT |
|---|---|
| AWS | "Use boto3. Set env vars: AWS_REGION, AWS_PROFILE. Include cleanup()." |
| Postgres (Docker) | "Postgres is running on localhost:5432, db=studybook, user=studybook, pass=studybook" |
| Kafka (Docker) | "Kafka bootstrap server: localhost:29092 (external listener)" |
| Spark (Docker) | "Spark master: spark://localhost:7077. Or use local[*] for simplicity." |
| Pure Python | "No AWS, no Docker. Use local filesystem. Output to OUTPUT_DIR env var or /tmp/studybook/" |
