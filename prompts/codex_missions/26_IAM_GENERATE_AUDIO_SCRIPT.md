# MISSION 26 — Generate Audio Script: AWS IAM
# Working directory: D:\StudyBook\
# No existing HTML page to read — this is a new topic (Phase 2)
# Output: temp\jobsearch\data\interview_prep\audio_prep\aws-iam\audio_script_aws-iam.md
# Phase 2 — Topic 1 of 12 (IAM is foundational — do before all other Phase 2 topics)

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\StudyBook
```
All paths are relative to D:\StudyBook\. Use no absolute paths.

---

## REPOSITORIES INVOLVED IN THIS MISSION

```
D:\StudyBook\                                         ← ROOT (working directory)
└── temp\jobsearch\                                   ← REPO 2 — script source goes here
        data\interview_prep\audio_prep\aws-iam\        ← create if missing
            audio_script_aws-iam.md                   ← THIS MISSION'S OUTPUT (text — in repo)

D:\temp\studybook_audio\aws-iam\                      ← AUDIO OUTPUT (outside repo — NOT committed)
    audio_clips\                                      ← generated MP3 clips (binary — never in repo)
    final_aws-iam.mp3                                 ← stitched final (binary — never in repo)
    UPLOAD_INSTRUCTIONS.md                            ← R2 upload guide
```

IMPORTANT: Audio clips and MP3 files are binary artifacts stored OUTSIDE the repository under
D:\temp\studybook_audio\. They are NEVER written into D:\StudyBook\ or any subdirectory of it.
Only the text script (audio_script_aws-iam.md) lives in the repo.

No existing HTML page to read. Write the script from the content outline below.

---

## PRE-FLIGHT

1. Confirm working directory:
   ```powershell
   Get-Location   # must show D:\StudyBook
   ```

2. Create the output folder if it does not exist:
   ```powershell
   New-Item -ItemType Directory -Force -Path "temp\jobsearch\data\interview_prep\audio_prep\aws-iam"
   ```

---

## YOUR TASK

Write a complete HOST+SEAN audio dialogue script about AWS IAM (Identity and Access Management).
This script feeds directly into the GPT-4o TTS pipeline (run via master pipeline after this mission).

Save to: `temp\jobsearch\data\interview_prep\audio_prep\aws-iam\audio_script_aws-iam.md`

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

Topic: AWS IAM
Output filename: final_aws-iam.mp3
Script path: temp\jobsearch\data\interview_prep\audio_prep\aws-iam\audio_script_aws-iam.md

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
  "NEVER hardcode" | "ALWAYS use roles" | "ZERO standing permissions"

PHONETIC NORMALIZATION — replace every instance, no exceptions:
  AWS→A-W-S   IAM→I-A-M   ARN→A-R-N   STS→S-T-S   MFA→M-F-A
  EC2→E-C-2   S3→S-3      ECS→E-C-S   EMR→E-M-R   RDS→R-D-S
  VPC→V-P-C   API→A-P-I   SDK→S-D-K   CLI→C-L-I   JSON→J-S-O-N
  SCP→S-C-P   ACL→A-C-L   SSO→S-S-O   ABAC→A-B-A-C  RBAC→R-B-A-C

NUMBERS as spoken words:
  "0 permissions" → "zero permissions" | "1 role" → "one role"
  "90 days" → "ninety days" | "15 minutes" → "fifteen minutes"

NO MARKDOWN in spoken text:
  No ** | no # | no - bullets | no backticks | no numbered lists as digits
  Bullets → "First... Second... Third..."

---

## CONTENT STRUCTURE

Write all 9 sections in order. Each section = HOST question + SEAN answer unless noted.

### SECTION 1 — What IAM Is
HOST: "Let's start at the very beginning. What is I-A-M, and why does every A-W-S conversation come back to it?"

SEAN covers:
- I-A-M is the permissions system for all of A-W-S — controls WHO can do WHAT to which resource
- Three questions I-A-M answers: Who is making the request? Are they authenticated? Are they authorized?
- Scope: I-A-M is global — not tied to a region. One I-A-M setup governs your entire A-W-S account
- Why it comes up everywhere: every service (S-3, E-C-2, Glue, Lambda, Redshift) checks I-A-M on every API call
  — you can't use A-W-S securely without understanding I-A-M
- The mental model: I-A-M is a policy engine that evaluates "allow" or "deny" at the moment of each request

### SECTION 2 — The Four Core Primitives
HOST: "Walk me through the building blocks — users, groups, roles, policies. How do they fit together?"

SEAN covers:
- Users: individual identity with long-term credentials (username + password or access keys)
  — use for humans who sign in to the console, or for legacy programmatic access
  — access keys are static credentials that NEVER expire unless you rotate them — high risk if leaked
- Groups: collection of users — attach policies to the group, all members inherit permissions
  — simplifies management: change one group policy instead of updating twenty users
- Roles: identity WITHOUT long-term credentials — grants temporary credentials via S-T-S
  — designed for services, applications, and cross-account access
  — the modern standard: ALWAYS prefer roles over users for anything non-human
- Policies: JSON documents that define permissions — attached to users, groups, or roles
  — the policy is what actually grants or denies access — everything else is just a container

### SECTION 3 — Policy Document Anatomy
HOST: "What does an I-A-M policy actually look like? What are the required pieces?"

SEAN covers:
- Every policy is J-S-O-N with a Statement array. Each statement has four key fields:
  First: Effect — either "Allow" or "Deny". Deny ALWAYS wins — explicit deny overrides any allow.
  Second: Action — the A-W-S A-P-I calls being permitted or denied (example: s3-colon-GetObject, or s3-colon-star for all S-3 actions)
  Third: Resource — the specific A-R-N the action applies to. Star means all resources — avoid this in production.
  Fourth: Condition — optional constraints (example: only allow if request comes from a specific V-P-C, or only if M-F-A is active)
- The evaluation logic: default is implicit deny. A-W-S evaluates all applicable policies.
  If any policy has an explicit Deny — request denied, full stop.
  If at least one Allow exists and no explicit Deny — request allowed.
  If neither — implicit deny.
- Principle of least privilege: grant only the specific actions on the specific resources needed, nothing more

### SECTION 4 — Roles vs Users — The Critical Distinction
HOST: "You mentioned roles are the modern standard. Can you make the distinction concrete?"

SEAN covers:
- Users have permanent credentials — access keys that live on disk, in environment variables,
  in config files. If that machine is compromised, the key is compromised — FOREVER until you rotate it.
- Roles issue temporary credentials via S-T-S — tokens that expire in fifteen minutes to twelve hours.
  Even if leaked, they expire. The blast radius is bounded by time.
- The rule: NEVER give a service or application a user's access key.
  An E-C-2 instance should have an I-A-M role. A Lambda function has an execution role.
  An E-C-S task has a task role. A Glue job has a service role. No exceptions.
- Interview signal: if a candidate says "I put the A-W-S credentials in the environment variables on the server"
  that's an immediate red flag. The correct answer is always: attach a role.

### SECTION 5 — How Services Get Permissions
HOST: "So when an E-C-2 instance needs to read from S-3, how does that actually work mechanically?"

SEAN covers:
- Instance profile: an I-A-M role attached to an E-C-2 instance at launch
  — the instance metadata service (at 169.254.169.254) vends temporary credentials
  — the A-W-S S-D-K automatically fetches and refreshes these — zero configuration needed in code
- Lambda execution role: attached at function creation — Lambda assumes this role on every invocation
  — must include permissions for CloudWatch Logs (otherwise logs fail silently)
- E-C-S task role: separate from the task execution role.
  Task execution role: E-C-S agent pulling the image and writing logs.
  Task role: what YOUR application code inside the container can do.
  These are two different roles — confusing them is a common mistake.
- Glue service role: attached to Glue jobs — needs S-3 read/write, Glue Catalog access,
  and any other service the job touches (Secrets Manager, KMS, etc.)

### SECTION 6 — AssumeRole and Cross-Account Access
HOST: "What about AssumeRole? When and why would you use it?"

SEAN covers:
- AssumeRole is the mechanism for one identity to temporarily become another role
  — call S-T-S AssumeRole, receive temporary credentials, use them for the target role's permissions
- Key use cases:
  First: cross-account access — a role in account A assumes a role in account B to access its resources.
  This is the standard pattern for multi-account architectures.
  Second: elevated permissions — require M-F-A to assume a sensitive admin role, even for existing users.
  Third: CI/CD pipelines — GitHub Actions assumes an I-A-M role instead of storing long-term credentials.
- Trust policy: the role has TWO policy documents. The permission policy (what it can do).
  And the trust policy (who is ALLOWED to assume it).
  The trust policy explicitly names the principals allowed to call AssumeRole on this role.
- Common data engineering pattern: a central data platform account has an I-A-M role that
  all data pipeline accounts can assume to write results to a shared data lake S-3 bucket.

### SECTION 7 — IAM in a Data Engineering Stack
HOST: "What does good I-A-M hygiene look like in practice for a data engineering team?"

SEAN covers:
- Every pipeline component has its own role with scoped permissions:
  Glue crawlers: read S-3, write Glue Catalog — nothing else.
  Glue ETL jobs: read source S-3, write target S-3, access Secrets Manager for credentials — nothing else.
  Lambda triggers: read SQS or S-3 events, write to the target — nothing else.
  Redshift: spectrum role to read S-3, KMS key usage for encryption — scoped to specific buckets.
- S-3 bucket policies layer on top: even if a role has S-3 full access,
  the bucket policy can further restrict to specific prefixes or specific roles only.
  Defense in depth.
- Audit tooling: I-A-M Access Analyzer identifies overly permissive policies and external access.
  AWS Config tracks policy changes over time.
  CloudTrail logs every I-A-M API call — who changed what, when.
- Team hygiene: use permission boundaries to cap what developers can grant themselves.
  Nobody in the data team should be able to create a role with admin access.

### SECTION 8 — Common Mistakes
HOST: "What are the I-A-M mistakes you see most often in data engineering environments?"

SEAN covers these specific mistakes:
- Hardcoding access keys in application code or environment variables — use roles instead, always.
- Star-star policies: Effect Allow, Action star, Resource star — effectively admin access, terrible in production.
- Confusing the E-C-S task role with the task execution role — the application has no permissions,
  only the agent does — debugging this wastes hours.
- Not setting up resource-based conditions on S-3 bucket policies — relying only on identity policies
  means any credential with S-3 access can read the bucket, even from outside your account.
- Forgetting CloudWatch Logs permissions on Lambda execution roles — the function runs but logs disappear.
- Using the root account for anything — root has permanent, irrevocable full access to everything.
  Enable M-F-A on root, generate no root access keys, never use it day-to-day.

### SECTION 9 — Recap Q&A (5 rapid-fire exchanges)
HOST asks each question. SEAN answers in 3–5 sentences. Confident, interview-ready delivery.

Q1: "What's the difference between an I-A-M role and an I-A-M user?"
Q2: "An explicit Deny and an explicit Allow exist on the same resource for the same action. What happens?"
Q3: "Your Glue job can't read from S-3. It has an I-A-M role. What do you check first?"
Q4: "What is a trust policy and how is it different from a permission policy?"
Q5: "Your CI/CD pipeline needs to deploy to A-W-S. How do you set that up securely?"

---

## POST-WRITE VERIFICATION CHECKLIST

Before saving, verify every item:
- [ ] File header block present at the top (`## API INSTRUCTIONS`)
- [ ] Every block uses exact format `**[HOST — voice: nova]**` or `**[SEAN — voice: onyx]**`
- [ ] Every block ends with `---`
- [ ] No block contains both HOST and SEAN text
- [ ] SEAN opens every answer with a unique conversational bridge
- [ ] No bridge repeated twice in a row
- [ ] Every acronym replaced — search for: AWS, IAM, ARN, STS, MFA, EC2, S3, ECS, EMR, RDS, VPC, API, SDK, CLI, JSON, SCP, SSO
- [ ] No markdown formatting inside spoken text (no **, #, backtick)
- [ ] Ellipsis count verified — max 4 per block
- [ ] All 9 sections present
- [ ] Recap Q&A has exactly 5 HOST+SEAN pairs
- [ ] `## END OF SCRIPT` at the bottom
- [ ] File saved to: `temp\jobsearch\data\interview_prep\audio_prep\aws-iam\audio_script_aws-iam.md`

Report: "MISSION 26 COMPLETE — script saved — [N] blocks — est. [X] min audio"
Or:     "MISSION 26 BLOCKED — [specific problem]"

---

## AFTER THIS MISSION

Run the audio pipeline using the master runbook:
`prompts\codex_missions\Existing_work_pipeline_execution_master.md`

Topic slug: `aws-iam`
Script path: `temp\jobsearch\data\interview_prep\audio_prep\aws-iam\audio_script_aws-iam.md`

The pipeline will write ALL audio artifacts to D:\temp\studybook_audio\aws-iam\ (outside the repo):
  D:\temp\studybook_audio\aws-iam\audio_clips\    ← individual MP3 clips (binary — never commit)
  D:\temp\studybook_audio\aws-iam\final_aws-iam.mp3  ← stitched final (binary — never commit)
  D:\temp\studybook_audio\aws-iam\UPLOAD_INSTRUCTIONS.md

DO NOT copy or move any .mp3 files into D:\StudyBook\ or any subdirectory.
Binary audio files do not belong in the repository.

After Sean uploads final_aws-iam.mp3 to R2 and confirms it plays in the browser at:
`https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-iam.mp3`

Tell Codex: "IAM audio uploaded — run Mission 27"
