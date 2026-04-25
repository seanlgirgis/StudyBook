# MISSION 02 — Generate Audio Script: Amazon EC2
# Working directory: D:\StudyBook\
# Touches: temp\seanlgirgis.github.io\learning\aws-ec2.html (read only)
# Output:  temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md
# Phase 1 — TEST CASE (first of 8)

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\StudyBook
```
All paths are relative to D:\StudyBook\. Use no absolute paths.

---

## THREE REPOSITORIES INVOLVED IN THIS MISSION

```
D:\StudyBook\                                      ← ROOT (working directory)
├── temp\jobsearch\                                ← REPO 2 — output goes here
│       data\interview_prep\audio_prep\aws-ec2\    ← create this folder if missing
│           audio_script_aws-ec2.md               ← THIS MISSION'S OUTPUT
└── temp\seanlgirgis.github.io\                   ← REPO 3 — read only
        learning\aws-ec2.html                     ← read to understand page content
```

---

## PRE-FLIGHT

1. Confirm working directory:
   ```powershell
   Get-Location   # must show D:\StudyBook
   ```

2. Read the existing page to understand what the article covers (topics, sections, depth):
   ```
   temp\seanlgirgis.github.io\learning\aws-ec2.html
   ```
   Note the section headings. The audio should complement the written content — not contradict it.

3. Create the output folder if it does not exist:
   ```powershell
   New-Item -ItemType Directory -Force -Path "temp\jobsearch\data\interview_prep\audio_prep\aws-ec2"
   ```

---

## YOUR TASK

Write a complete HOST+SEAN audio dialogue script about Amazon EC2.
This script feeds directly into the GPT-4o TTS pipeline (Mission 03).

Save to: `temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md`

Target: ~14–18 speaker blocks | ~10–13 minutes of audio at natural speaking pace.

---

## SCRIPT FORMAT (NON-NEGOTIABLE)

File must begin with this exact header:
```
## API INSTRUCTIONS

Target model: gpt-4o-mini-tts (preferred) / gpt-4o-mini-audio-preview (fallback)
HOST voice: nova — warm, curious, professional female
SEAN voice: onyx — deep, authoritative male
Process each [SPEAKER] block as a separate API call. Export as MP3. Merge in sequence.

Topic: Amazon EC2
Output filename: final_aws-ec2.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md

---
```

Every speaker block uses this EXACT format — no variation:
```
**[HOST — voice: nova]**

Spoken text here...

---

**[SEAN — voice: onyx]**

Spoken text here...

---
```

Rules:
- One blank line after speaker label, before spoken text
- `---` divider after EVERY block without exception
- Never two speakers in one block
- Never put label text inside the spoken body
- Chunk size: ~1,200–1,800 characters per block

File must end with: `## END OF SCRIPT`

---

## SPEAKER PERSONAS

HOST (nova):
- Warm, curious, professional
- Short turns: 1–3 sentences max
- Sets up each topic naturally — does not lecture
- Short affirmations between questions: "Got it." "Makes sense." "And that matters because..."

SEAN (onyx):
- Calm, senior, credible — never nervous or uncertain
- Measured in technical sections, firm on outcomes and tradeoffs
- Every answer opens with a unique conversational bridge — ROTATE, never repeat same one twice in a row:
  "So... basically..." | "Here's the thing..." | "Here's the key insight..."
  "Right... so the way I think about this..." | "Let me give you a concrete example..."
  "Two things matter here..." | "Now... the important distinction is..."
- Clear ending on every answer — no rambling

---

## MANDATORY TEXT RULES

CONTRACTIONS — convert all formal phrases without exception:
  "I have not" → "I haven't"  |  "It is" → "It's"  |  "Do not" → "Don't"
  "That is" → "That's"  |  "I am" → "I'm"  |  "We have" → "We've"  |  "You will" → "You'll"

PAUSING via punctuation:
  ,       micro pause (~0.3s) — use naturally
  ...     thoughtful pause (~1.0s) — after key claims, before pivots — MAX 4 per block
  ......  topic shift (~2.0s) — between major concept shifts — use sparingly
  —       sharp contrast — use sparingly

ALL CAPS emphasis — key metrics and contrast words only — MAX 3 per block:
  "NINETY percent" | "FUNDAMENTALLY different" | "EXACTLY the same primitive"

PHONETIC NORMALIZATION — replace every instance, no exceptions:
  AWS→A-W-S   ECS→E-C-S   EBS→E-B-S   AMI→A-M-I   ASG→A-S-G
  ALB→A-L-B   NLB→N-L-B   IAM→I-A-M   VPC→V-P-C   RDS→R-D-S
  EMR→E-M-R   ETL→E-T-L   API→A-P-I   SQL→S-Q-L   ENI→E-N-I
  SSM→S-S-M   IOPS→I-O-P-S   SLA→S-L-A

NUMBERS as spoken words:
  "8 years" → "eight years" | "15 minutes" → "fifteen minutes"
  "10x" → "ten times" | "99.99%" → "NINETY-NINE point NINETY-NINE percent"
  "1TB" → "one terabyte" | "3,000 IOPS" → "THREE THOUSAND I-O-P-S"

NO MARKDOWN in spoken text:
  No ** | no # | no - bullets | no backticks | no numbered lists as digits
  Bullets → "First... Second... Third..."

---

## CONTENT STRUCTURE

Write all 9 sections in order. Each section = HOST question + SEAN answer unless noted.

### SECTION 1 — Why EC2 Exists
HOST: "Let's start at the foundation. What problem does E-C-2 solve — why does it exist?"

SEAN covers:
- Before EC2: provisioning physical servers took weeks, huge capital cost
- EC2's answer: rent virtual machines by the hour, scale in minutes, pay for what you use
- Position vs serverless: EC2 gives full OS control — Lambda has a fifteen-minute ceiling,
  no persistent processes, no custom system libraries
- Key mental model: EC2 is not obsolete in the serverless era — it's the right choice when
  you need persistent processes, high-throughput I/O, or control that managed services don't give you

### SECTION 2 — Instance Types
HOST: "There are hundreds of instance types. How do you choose?"

SEAN covers:
- Naming convention: family + generation + attributes + size (example: r7g.2xlarge)
- Key families for data engineers:
  - m (general purpose): balanced C-P-U and memory — good default starting point
  - r (memory optimized): Spark executors, large joins, Redis — pick this when RAM is the bottleneck
  - c (compute optimized): C-P-U-bound transformations, Kafka brokers
  - i (storage optimized): high local NVMe I/O — HDFS DataNodes, Cassandra
  - t (burstable): dev/test, jump hosts — cheap but throttles under sustained load
- Graviton (ARM) instances: twenty to forty percent better price-to-performance for Python
  and J-V-M workloads — worth evaluating for any containerized workload
- Practical rule: start with m5 or m6g, move to r-family when memory becomes the bottleneck

### SECTION 3 — Purchasing Options
HOST: "What about cost? On-demand, reserved, spot — when do you use each?"

SEAN covers:
- On-demand: pay per second, no commitment — use for unpredictable or development workloads
- Reserved instances: one or three year commitment, up to SEVENTY-TWO percent cheaper
  — use for stable, always-on baseline capacity
- Spot instances: up to NINETY percent cheaper, but A-W-S can reclaim with two-minute warning
  — right for stateless batch jobs, fault-tolerant Spark workers, Fargate Spot
  — NEVER use spot for stateful workloads like databases or job coordinators
- Data engineering pattern: reserved instances for baseline plus spot workers for burst jobs

### SECTION 4 — Storage
HOST: "Storage — E-B-S, instance store, E-F-S — what's the difference and when does each apply?"

SEAN covers:
- E-B-S (Elastic Block Store): network-attached, persistent — survives instance stop and start
  - gp3: general purpose S-S-D — three thousand I-O-P-S baseline, cost-effective default
  - io2: high-performance — up to sixty-four thousand I-O-P-S — for demanding databases
  - Key gotcha: E-B-S is availability-zone-locked — can't attach to an instance in a different A-Z
- Instance store: local NVMe on the physical host — fastest possible I/O, but GONE when instance stops
  — right for Spark shuffle space, temporary scratch data, HDFS DataNode local storage
- E-F-S (Elastic File System): shared NFS mountable across multiple instances
  — good for shared config or Lambda layers, but higher latency than E-B-S
- Rule: E-B-S for persistence, instance store for raw speed, E-F-S for sharing across instances

### SECTION 5 — Networking and IAM
HOST: "How does E-C-2 fit into the network, and how does it get permission to talk to other A-W-S services?"

SEAN covers:
- Every instance lives in a V-P-C subnet — private subnets have no direct internet access
- Security groups are stateful firewalls at the instance level — inbound and outbound rules
- Data engineering pattern: compute in private subnet, access S-3 and Glue via V-P-C endpoints
  — no internet traffic, lower cost, more secure
- I-A-M instance profiles: the right way to grant A-W-S service access to an instance
  — attach a role, credentials rotate automatically
  — NEVER hardcode A-W-S access keys on an E-C-2 instance — common and dangerous mistake
- Principle of least privilege: the instance role should only have permissions it actually needs

### SECTION 6 — Auto Scaling
HOST: "How does Auto Scaling work with E-C-2, and why does it matter for data workloads?"

SEAN covers:
- Auto Scaling Groups (A-S-G): define min, desired, and max instance counts
- Scaling policies: target tracking is simplest — "keep C-P-U at sixty percent"
  — step scaling for more control, scheduled scaling for predictable patterns
- Key concept: instances in an A-S-G are cattle, not pets
  — they launch, do work, terminate — no S-S-H, no manual intervention
  — user data script bootstraps the instance on launch
- A-L-B in front of the A-S-G distributes traffic and handles health checks
- Data engineering connection: E-M-R clusters are Auto Scaling Groups under the hood
  — understanding A-S-Gs makes you better at tuning E-M-R cluster scaling behavior

### SECTION 7 — EC2 in a Real Data Engineering Stack
HOST: "Where does E-C-2 actually show up in a data engineering stack day-to-day?"

SEAN covers:
- Most managed A-W-S data services are E-C-2 under the hood:
  Redshift nodes, R-D-S instances, E-M-R cluster nodes, M-S-K brokers — all E-C-2
  Understanding E-C-2 makes every other A-W-S service more predictable
- Direct E-C-2 use cases in data engineering:
  — Custom E-T-L workers that outgrow Lambda's fifteen-minute ceiling
  — Self-managed Kafka brokers when you need lower latency than M-S-K provides
  — Bastion hosts for accessing private-network databases
  — Airflow schedulers and workers that need persistent state
- The decision rule: use E-C-2 when you need persistent processes, custom runtimes,
  or more control than the managed service gives you

### SECTION 8 — Common Mistakes
HOST: "What do engineers get wrong with E-C-2?"

SEAN covers these specific mistakes:
- Hardcoding A-W-S credentials instead of using I-A-M instance profiles
- Routing S-3 traffic over the public internet instead of V-P-C endpoints — costs money, slower, less secure
- Not tagging instances — leads to runaway costs and no visibility into what's running
- Using spot instances for stateful workloads — data loss when A-W-S reclaims
- E-B-S volume in wrong availability zone — can't attach cross-A-Z
- Forgetting DeleteOnTermination on data E-B-S volumes — default is true for root volume,
  your data volume gets deleted when instance terminates unless you explicitly set it to false

### SECTION 9 — Recap Q&A (5 rapid-fire exchanges)
HOST asks each question. SEAN answers in 3–5 sentences. Confident, interview-ready delivery.

Q1: "What's the difference between an E-B-S-backed and an instance-store-backed instance?"
Q2: "When would you use a spot instance, and when absolutely not?"
Q3: "How does an E-C-2 instance get permission to read from S-3?"
Q4: "What's the difference between a security group and a network A-C-L?"
Q5: "You have an E-T-L job that takes four hours and runs every night.
     What instance type and purchasing option would you recommend, and why?"

---

## POST-WRITE VERIFICATION CHECKLIST

Before saving, verify every item:
- [ ] File header block present at the top (`## API INSTRUCTIONS`)
- [ ] Every block uses exact format `**[HOST — voice: nova]**` or `**[SEAN — voice: onyx]**`
- [ ] Every block ends with `---`
- [ ] No block contains both HOST and SEAN text
- [ ] SEAN opens every answer with a unique conversational bridge
- [ ] No bridge repeated twice in a row
- [ ] Every acronym in the normalization table has been replaced — search for: AWS, EBS, AMI, ASG, ALB, NLB, IAM, VPC, ETL, API, ENI, SSM, IOPS, ECS, EMR, RDS, EFS
- [ ] No markdown formatting inside spoken text (no **, #, backtick)
- [ ] Ellipsis count verified — max 4 per block
- [ ] All 9 sections present
- [ ] Recap Q&A has exactly 5 HOST+SEAN pairs
- [ ] `## END OF SCRIPT` at the bottom
- [ ] File saved to correct relative path: `temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md`

Report: "MISSION 02 COMPLETE — script saved to temp\jobsearch\data\interview_prep\audio_prep\aws-ec2\audio_script_aws-ec2.md — [N] blocks — est. [X] min audio"
Or:     "MISSION 02 BLOCKED — [specific problem]"
