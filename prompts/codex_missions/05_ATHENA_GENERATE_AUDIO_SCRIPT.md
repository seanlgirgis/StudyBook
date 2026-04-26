# MISSION 05 — Generate Audio Script: Amazon Athena
# Working directory: D:\Workarea\StudyBook\
# Touches: ..\seanlgirgis.github.io\learning\aws-athena.html (read only)
# Output:  ..\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md
# Phase 1 — Topic 2 of 8

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\Workarea\StudyBook
```
All paths are relative to D:\Workarea\StudyBook\. Use no absolute paths.

---

## THREE REPOSITORIES INVOLVED IN THIS MISSION

```
D:\Workarea\StudyBook\                                         ← ROOT (working directory)
├── ..\jobsearch\                                   ← REPO 2 — output goes here
│       data\interview_prep\audio_prep\aws-athena\    ← create this folder if missing
│           audio_script_aws-athena.md               ← THIS MISSION'S OUTPUT
└── ..\seanlgirgis.github.io\                      ← REPO 3 — read only
        learning\aws-athena.html                     ← read to understand page content
```

---

## PRE-FLIGHT

1. Confirm working directory:
   ```powershell
   Get-Location   # must show D:\Workarea\StudyBook
   ```

2. Read the existing page to understand what the article covers (topics, sections, depth):
   ```
   ..\seanlgirgis.github.io\learning\aws-athena.html
   ```
   Note the section headings. The audio should complement the written content — not contradict it.

3. Create the output folder if it does not exist:
   ```powershell
   New-Item -ItemType Directory -Force -Path "..\jobsearch\data\interview_prep\audio_prep\aws-athena"
   ```

---

## YOUR TASK

Write a complete HOST+SEAN audio dialogue script about Amazon Athena.
This script feeds directly into the GPT-4o TTS pipeline (Mission 06).

Save to: `..\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md`

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

Topic: Amazon Athena
Output filename: final_aws-athena.mp3
Script path: ..\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md

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
  "FIVE dollars per terabyte" | "NINETY percent reduction" | "FUNDAMENTALLY different"

PHONETIC NORMALIZATION — replace every instance, no exceptions:
  AWS→A-W-S   S3→S-3   ETL→E-T-L   SQL→S-Q-L   API→A-P-I
  IAM→I-A-M   VPC→V-P-C   ECS→E-C-S   EMR→E-M-R   RDS→R-D-S
  CTAS→C-T-A-S   DDL→D-D-L   DML→D-M-L   ORC→O-R-C   CSV→C-S-V
  MSK→M-S-K   SQS→S-Q-S   SNS→S-N-S   JDBC→J-D-B-C   JSON→J-S-O-N
  GB→gigabytes   TB→terabytes   MB→megabytes

NUMBERS as spoken words:
  "5 dollars" → "five dollars" | "1 TB" → "one terabyte"
  "10x" → "ten times" | "99.9%" → "NINETY-NINE point nine percent"

NO MARKDOWN in spoken text:
  No ** | no # | no - bullets | no backticks | no numbered lists as digits
  Bullets → "First... Second... Third..."

---

## CONTENT STRUCTURE

Write all 9 sections in order. Each section = HOST question + SEAN answer unless noted.

### SECTION 1 — What Athena Is
HOST: "Let's start from the top. What is Amazon Athena, and why would a data engineer reach for it?"

SEAN covers:
- Athena is serverless, interactive query service — run S-Q-L directly against S-3 with no cluster to manage
- Built on Presto (now Trino) under the hood — ANSI S-Q-L compatible
- No infrastructure: no clusters to provision, no servers to patch, no capacity to reserve
- Pay only for data scanned — FIVE dollars per terabyte, rounded up to ten megabytes per query
- Primary position in the stack: ad-hoc analytics, data discovery, query layer over a data lake
- Not a replacement for Redshift: Athena is optimized for flexibility and low ops overhead,
  Redshift for high-concurrency, sub-second dashboards

### SECTION 2 — How Athena Executes Queries
HOST: "How does it actually work under the hood when you run a query?"

SEAN covers:
- Query is submitted via console, A-P-I, or J-D-B-C driver
- Athena reads the Glue Data Catalog (or Hive Metastore) for table schema and S-3 location
- Presto / Trino engine distributes query across worker nodes A-W-S manages — you never see them
- Results are written to a designated S-3 output location — Athena uses this for query history too
- Key implication: Athena is read-optimized — it doesn't modify S-3 data by default
- Concurrency: Athena can run up to one hundred queries concurrently by default (soft limit, raiseable)

### SECTION 3 — Storage Formats and Why They Matter
HOST: "I hear Parquet and O-R-C come up constantly with Athena. Why does the file format matter so much?"

SEAN covers:
- Athena is billed by bytes scanned — columnar formats are the biggest single lever for cost and speed
- Parquet: columnar, splittable, widely supported — the default recommendation for Athena
  Snappy compression typically cuts file size SIXTY to EIGHTY percent versus uncompressed C-S-V
- O-R-C: columnar, slightly better compression than Parquet in some cases — common in Hive ecosystems
- C-S-V and J-S-O-N: row-based — Athena scans the entire file even for a single-column query
  A query on one column of a ten-gigabyte C-S-V costs ten gigabytes scanned
  The same query on a Parquet version may scan under one gigabyte — NINETY percent cheaper
- Rule: never store raw C-S-V in a production Athena data lake — always convert on ingest

### SECTION 4 — Partitioning Strategy
HOST: "And partitioning — how does that interact with cost?"

SEAN covers:
- Partitioning restricts which S-3 files Athena reads — it's the second biggest cost lever after columnar formats
- Hive-style partitions: folder path encodes partition key — example: year equals 2026, month equals 04, day equals 15
- Athena pushes partition filters down before scanning — a query filtered to one day
  only reads that day's folder, not the entire dataset
- Critical mistake: not filtering on the partition key — Athena scans all partitions regardless of other filters
- Partition projection: define partition logic in table properties — Athena generates partition values
  without reading the Glue Catalog — dramatically faster for high-cardinality date partitions
- Rule of thumb: partition by date at the query granularity you actually use
  If you always query by day, partition by day. If by month, by month.

### SECTION 5 — Cost Model and Optimization
HOST: "Let's go deeper on cost. Five dollars per terabyte sounds cheap, but costs can surprise you."

SEAN covers:
- FIVE dollars per terabyte scanned, rounded to the nearest ten megabytes, one cent minimum per query
- Cost multipliers that catch teams off guard:
  First: running exploratory queries on raw C-S-V logs — one query on a terabyte of access logs costs five dollars
  Second: SELECT star queries — scans every column in a Parquet file, not just what you need
  Third: missing WHERE clause on a partitioned column — full table scan
- Cost reduction playbook, in order of impact:
  First: convert to Parquet or O-R-C — biggest win
  Second: partition by the columns you filter on most
  Third: compress with Snappy or Zstandard
  Fourth: use C-T-A-S to materialize frequent query results back to S-3 as Parquet
- Monitoring: Athena query history shows bytes scanned per query — review weekly during active development

### SECTION 6 — CTAS and INSERT INTO Patterns
HOST: "What are C-T-A-S queries, and when do you use them?"

SEAN covers:
- C-T-A-S stands for Create Table As Select — creates a new Athena table populated by a S-Q-L query result
- Two key use cases:
  First: converting raw C-S-V or J-S-O-N to Parquet in-place — CTAS writes results back to S-3 as columnar files
  Second: materializing expensive joins or aggregations — run once, query the result repeatedly at low cost
- C-T-A-S syntax:
  CREATE TABLE target WITH open-paren format equals 'PARQUET', partitioned_by equals ARRAY brackets close-paren
  AS SELECT ... FROM source WHERE ...
- INSERT INTO: append rows to an existing Athena table backed by S-3 — compatible with C-T-A-S-created tables
- Gotcha: C-T-A-S creates unpartitioned output by default unless you specify partitioned_by in the WITH clause
  Always check partition layout after a C-T-A-S run

### SECTION 7 — Glue Data Catalog Integration
HOST: "Athena and Glue seem tightly coupled. How do they work together?"

SEAN covers:
- Athena uses the Glue Data Catalog as its default metastore — table definitions, schemas, S-3 locations
- Glue Crawlers auto-discover S-3 data and register tables — useful for bootstrapping but not for production
  Crawlers can infer wrong types or create duplicate partitions — review output before relying on it
- In production: define tables manually via D-D-L or Terraform / CloudFormation
  — explicit schema control, versioned, reproducible
- Schema evolution: Athena supports adding columns at the end of a Parquet schema without rewriting files
  — but changing column types or removing columns requires rewriting data
- The Glue Catalog is shared across Athena, E-M-R, Glue jobs, and Redshift Spectrum
  — one schema update is visible everywhere — powerful but be careful with breaking changes

### SECTION 8 — Federated Queries
HOST: "Athena can also query databases outside S-3 — how does that work?"

SEAN covers:
- Federated queries use Lambda-based connectors to query external data sources from Athena
- Supported sources: RDS, Aurora, DynamoDB, Redshift, DocumentDB, on-prem databases via custom connector
- How it works: Athena invokes a Lambda function that translates the S-Q-L predicate into a native query
  against the source system, returns results as Arrow format, Athena joins and aggregates
- Use case: join S-3 data lake tables with live R-D-S operational data in a single S-Q-L query
  without ETL — useful for enrichment queries in reporting pipelines
- Performance caveat: federated queries push predicates to the source, but complex joins pull
  data back to Athena — watch for accidentally scanning entire source tables
  Always filter aggressively on the federated side

### SECTION 9 — Recap Q&A (5 rapid-fire exchanges)
HOST asks each question. SEAN answers in 3–5 sentences. Confident, interview-ready delivery.

Q1: "What's the single biggest thing you can do to reduce Athena query costs?"
Q2: "What's the difference between Athena and Redshift Spectrum?"
Q3: "Your Athena query is scanning ten terabytes even though you have a date partition. What's wrong?"
Q4: "How do you add new columns to an existing Athena table without breaking existing queries?"
Q5: "When would you use C-T-A-S instead of a regular INSERT INTO an existing table?"

---

## POST-WRITE VERIFICATION CHECKLIST

Before saving, verify every item:
- [ ] File header block present at the top (`## API INSTRUCTIONS`)
- [ ] Every block uses exact format `**[HOST — voice: nova]**` or `**[SEAN — voice: onyx]**`
- [ ] Every block ends with `---`
- [ ] No block contains both HOST and SEAN text
- [ ] SEAN opens every answer with a unique conversational bridge
- [ ] No bridge repeated twice in a row
- [ ] Every acronym in the normalization table has been replaced — search for: AWS, S3, ETL, SQL, API, IAM, VPC, CTAS, DDL, DML, ORC, CSV, JSON, GB, TB, MB, MSK, JDBC
- [ ] No markdown formatting inside spoken text (no **, #, backtick)
- [ ] Ellipsis count verified — max 4 per block
- [ ] All 9 sections present
- [ ] Recap Q&A has exactly 5 HOST+SEAN pairs
- [ ] `## END OF SCRIPT` at the bottom
- [ ] File saved to correct relative path: `..\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md`

Report: "MISSION 05 COMPLETE — script saved to ..\jobsearch\data\interview_prep\audio_prep\aws-athena\audio_script_aws-athena.md — [N] blocks — est. [X] min audio"
Or:     "MISSION 05 BLOCKED — [specific problem]"

