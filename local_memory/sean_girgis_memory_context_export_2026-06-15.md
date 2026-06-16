# Sean Girgis — Memory & Project Context Export

**Export date:** June 15, 2026  
**Purpose:** A consolidated Markdown export of the durable context currently used to help maintain continuity across Sean’s conversations, studies, projects, career efforts, and workflows.

> **Important note**
>
> This is a best-effort export of the persistent and contextual information currently available to the assistant. It may contain facts that are outdated, incomplete, inferred from prior work, or duplicated across projects.
>
> Passwords, authentication secrets, API keys, one-time codes, and equivalent security credentials are intentionally excluded even when related account setup was discussed.

---

## 1. Identity and General Context

- Name: **Sean Girgis**
- Email associated with the account: **seanlgirgis@gmail.com**
- Handle: **@seanlgirgis**
- Date of birth recorded in prior context: **June 21, 1968**
- Current age context: approximately **57–58**
- Location context:
  - Richardson, Texas
  - Dallas–Fort Worth area
- Preferred work arrangements:
  - Remote is preferred
  - Dallas, Houston, Austin, and New York City may also be acceptable
- Plans to continue working for at least another 15 years.
- Has expressed a near-term need for income while continuing longer-term technical development.

---

## 2. Learning Style and Collaboration Preferences

### Teaching style

- Learns best through **very small, explicit, bite-sized steps**.
- Often prefers one concept or one action at a time.
- Does not want large lesson dumps.
- Responses for study sessions should usually stay well under one A4 page.
- Concepts may need to be revisited from more than one angle before they fully click.
- Hidden assumptions should be made explicit.
- Interactive learning is preferred:
  1. One small explanation
  2. One tiny task or question
  3. Wait for Sean’s response before continuing
- Sean has said that ADD affects how he learns and organizes information.

### Documentation preferences

- Theory and conceptual meaning should be central.
- Code should be explained clearly rather than merely listed.
- Preserve exact canonical filenames.
- Do not create unnecessary suffixes such as:
  - `_updated`
  - `_final`
  - `_new`
- Prefer relative links inside repositories.
- Prefer consolidated digests and reference guides.
- For major projects, maintain continuity documents such as:
  - `README.md`
  - `MEMORY.md`
  - `CURRENT_STATE.md`
  - `RUNBOOK.md`
  - `CAPABILITIES.md`
  - project constitutions
  - Codex task headers
- For Codex-ready work, Sean prefers exact:
  - paths
  - files to create or modify
  - responsibilities
  - validation commands
  - expected outputs
  - scope limits

### Development workflow preferences

- Sean commonly runs commands manually.
- He prefers implementation prompts that are directly usable by Codex.
- Reusable mechanics should be centralized in shared libraries instead of copied into multiple exercises.
- Production-quality library code should be:
  - documented
  - typed
  - tested
  - reusable
- Generalize first, test it, run an example, then replace duplicated local implementations.
- Keep special cases local only when they are genuinely not generalizable.

---

## 3. Main Career Direction

### Primary technical targets

Sean’s main career direction emphasizes:

- Python
- PySpark
- SQL
- ETL and ELT
- AWS
- Data engineering
- Cloud data platforms
- Forecasting
- RAG and AI application development
- Vector databases
- Text processing

He generally prefers practical data engineering and application-building work over deep machine-learning research.

### Secondary strengths and possible positioning

- Observability and APM
- Capacity planning and efficiency
- Performance engineering
- Performance testing
- Dynatrace
- AppMon
- CA APM
- AppDynamics
- Splunk
- CI/CD
- Infrastructure as Code
- ECS
- CloudFormation
- AWS CDK
- FastAPI
- Kubernetes and EKS
- S3
- Cost optimization
- Monitoring and operational telemetry

### Professional profile

- Senior Data Engineer with more than 20 years of enterprise experience.
- Most recent major tenure included approximately eight years at Citigroup.
- Experience includes:
  - Python and PySpark ETL
  - ML forecasting
  - hybrid AWS/Oracle platforms
  - observability
  - enterprise data systems
- Left Citigroup near the end of 2025.
- Has been seeking senior data engineering, cloud data platform, PySpark, AWS, and AI-adjacent roles.

---

## 4. Active and Recent Job-Search Efforts

### Wipro / Programmers.IO — Senior PySpark Developer

- Role:
  - Senior PySpark Developer
  - Wipro through Programmers.IO
- Location:
  - Dallas hybrid
- Compensation context:
  - approximately $130,000 including QPLC and benefits
- HR contact:
  - Abhinesh Kumar
- Interview systems:
  - BerriBot
  - Karat
- Preparation folder:

```text
D:\Workarea\jobsearch\data\interview_prep\Wipro_ProgrammersIO_Senior_PySpark_Developer_2026_05
```

- Main preparation areas:
  - PySpark execution model
  - transformations versus actions
  - shuffles
  - slow-job diagnosis
  - deduplication
  - joins
  - null handling
  - window functions
  - ETL troubleshooting
  - SQL
  - schedulers
  - Unix shell
  - failure handling
  - production incident response

### Apple — Cloud Capacity & Efficiency Engineer through INSPYR

- Remote role aligned to Pacific time, approximately 9:00 AM–6:00 PM.
- 12-month W-2 contract.
- Compensation context:
  - approximately $60–$70 per hour
- Cloud focus:
  - AWS
  - GCP
- Technical areas:
  - automation
  - Kubernetes
  - EKS
  - S3
  - cloud cost and efficiency
  - HorizonScale
- Two interviews occurred on the same day.
- Final result:
  - rejected
- Perceived reasons:
  - AI depth mismatch
  - banking-background mismatch

Preparation lab:

```text
D:\Workarea\StudyBook\playground\prep
```

Lab concepts included:

- services
- hosts
- telemetry
- incidents
- deployments
- capacity thresholds

### Bank of America — Capacity Forecasting

- Interview date:
  - May 15, 2026 at 1:00 PM
- Primary story:
  - telemetry cleanup
  - bucketization
  - feature engineering
  - forecasting
  - dashboards
- Forecast validation approach:
  - 18 months training
  - 6 months testing
  - later retraining on 24 months
- Forecast tooling:
  - Prophet
  - cohorting
  - 3-month and 6-month windows
- Scale-up story:
  - Pandas to PySpark/Hadoop/cloud
  - partitioning by time and group

Folder:

```text
D:\Workarea\StudyBook\Observability_Readiness\BOA
```

### Sharkforce Consulting / Sr. Data Engineer / Databricks

- Organization:
  - Sharkforce Consulting
- Contacts:
  - Adam Butt
  - Nahal Ghahramani
- Interview:
  - Microsoft Teams
  - May 6, 2026
  - 3:30–4:00 PM
- Local technical lab:

```text
D:\Workarea\StudyBook\docker\sharkforce-pyspark-lab
```

Docker details:

```text
Image: sharkforce-pyspark-lab:0.1
Container: sharkforce-pyspark-lab
Jupyter: http://localhost:8888/lab
```

Confirmed working:

- `docker compose up`
- detached startup
- JupyterLab
- PySpark
- Java
- `SparkSession`
- DataFrame transformations

Constraints for this project:

- Preserve the existing files and persistent mounts.
- Do not change the image or container names.
- Maintain:
  - `README.md`
  - `MEMORY.md`
  - `RUNBOOK.md`
  - `CAPABILITIES.md`
  - `PROMPTS_FOR_CODEX.md`
  - `.gitignore`

### Toyota North America / Toyota Financial Services

A lead Python developer opportunity was evaluated involving:

- scalable Python frameworks
- ETL/ELT
- data validation
- Airflow or Prefect
- cloud-native deployment
- Docker
- AWS
- CI/CD
- technical mentoring
- no sponsorship stated in the posting

### Other tracked job themes

- AWS Data Engineer
- AWS lakehouse and migration
- monitoring engineer
- observability engineer
- Dynatrace/APM
- Snowflake
- dbt
- Fivetran
- Richardson-area senior data engineering
- BOK Financial alerts
- Dice searches using terms such as:
  - AWS
  - Python
  - SQL
  - Glue
  - S3
  - Athena
  - Redshift
  - PySpark
  - Airflow
  - ETL/ELT
  - data quality
  - migration

---

## 5. Job Application Manager Project

Project name:

```text
Job Application Manager
```

Core concept:

- Sean supplies a job URL, site, or search term.
- The system evaluates fit.
- It produces resume and cover-letter intermediate JSON.
- Sean reviews, renders, applies manually, and tracks the application.

Important project files include:

```text
JOB_APPLICATION_MANAGER_CONSTITUTION.md
source_of_truth.json
A1 Evaluate a Job.md
C0 Generate Both Resume and Cover.md
resume_intermediate_v1.json
cover_intermediate_v1.json
PIPELINE_RUNBOOK.md
CHATGPT_HANDOFF_JOBSEARCH.md
pipeline-guide.md
```

Responsibility split:

### Assistant responsibilities

- fit evaluation
- positioning
- grounded resume content
- cover-letter content
- JSON quality
- avoiding unsupported claims

### Sean’s responsibilities

- local duplicate check
- acceptance or rejection
- final rendering
- manual application
- application tracking

Sean also has an AI-powered job-search pipeline using:

- Grok
- RAG
- FAISS
- structured YAML career profile
- retrieval-grounded scoring
- duplicate detection

---

## 6. LTIMindtree / BOA Work Context

### LTIMindtree onboarding

- Joined LTIMindtree near May 28–29, 2026.
- Frisco onboarding location was involved.
- Laptop was allocated through the Frisco office.
- Initial onboarding included:
  - I-9
  - laptop handover
  - orientation
  - LTM email
  - iTime timesheets
  - PaychexFlex
  - Cigna
- Relevant people mentioned:
  - Venus
  - Courtney Demere Harris
  - Rahul Sharma
  - Priyan Gaikwad
  - Dinesh Babu K
- Sean indicated:
  - no invoicing through his own LLC during LTM tenure
  - no dual employment during LTM tenure
- A background-verification discussion included prior Xoriant work through Sean’s own corporation.

### Private work repository (out of scope)

BOA/LTM work-learning materials, training notes, and related backups live in a separate private repository. They are not stored or referenced in `local_memory`.

---

## 7. LifeVault

Project:

```text
LifeVault
```

Working path:

```text
D:\Workarea\StudyBook\Proj_development\LifeVault
```

Purpose:

- personal vault
- family vault
- operations vault
- long-term searchable memory

Preferred architecture:

### Hot layer

Stored locally:

- catalog
- metadata
- summaries
- extracted text
- embeddings
- highly used files

### Cold layer

Stored remotely or in cloud storage:

- original large files
- less frequently used materials

Operational expectation:

- approximately 85% local retrieval hit rate is acceptable
- when the original is not local, show retrieval status and fetch it on demand

---

## 8. DataCamp Organization and Progress

### Root

```text
D:\Workarea\StudyBook\study_maps\DataCamp
```

Sean decided to maintain one unified online-learning library here.

Rules:

- Do not migrate it to a separate `Online_Learning` root.
- `crs_` prefix means Coursera.
- No prefix generally means DataCamp.
- Course folders belong under the shared `courses` root.
- Relative links are preferred.
- Lab and SQL materials stay within the course folder.
- Preserve exact filenames.
- Same-filename replacement is preferred over creating copies.

### Completed or substantially completed SQL courses

- Introduction to SQL
- Intermediate SQL
- Joining Data in SQL
- Data Manipulation in SQL
- PostgreSQL Summary Stats and Window Functions
- Functions for Manipulating Data in PostgreSQL
- Database Design

Database Design concepts included:

- OLTP
- OLAP
- normalization
- slowly changing dimensions
- views
- partitions

Project:

```text
analyzing_students_mental_health
```

Concepts included:

- students table
- CTE
- `GROUP BY`

### Developing AI Applications track

Courses and work included:

#### Working with the OpenAI API

Path:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\working_with_the_openai_api
```

Preferences:

- strong consolidated digest
- consolidated code summary
- certification-prep artifacts
- two-column study documents preferred over three-column layouts

#### AI Ethics

Course completed.

Study focus included:

- ethical principles
- governance
- monitoring
- complaints and feedback channels
- lifecycle integration
- group-level performance
- business value and risk
- sustainability
- fairness
- accountability

Sean prefers AI application building over ethics, but still wants ethics properly covered.

#### Prompt Engineering with the OpenAI API

Work included:

- Chapter 1 labs
- dual-prompt chatbot
- stateful chatbot context
- answer plus updated state
- structured chat state
- validation
- helper classes
- reusable OpenAI support

#### Working with Hugging Face

Work included:

- tokenizer
- sentiment analysis
- dataset loading
- text classification
- zero-shot classification
- summarization
- PDF document Q&A
- parser fixes
- local model execution

Folder:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\working_with_hugging_face
```

#### Introduction to Data Privacy

Course completed.

Concepts included:

- privacy by design
- data classification
- retention
- consent
- jurisdiction
- governance
- third-party privacy risk
- data sovereignty
- breach obligations
- immutable systems
- shifting left
- purpose limitation
- lifecycle control
- legal and reputational risk

#### Developing AI Systems with the OpenAI API

Covered:

- API calls
- response decoding
- JSON
- validation
- errors
- retries
- batching
- token limits
- `tiktoken`
- function calling
- local functions
- weather integration
- Open-Meteo success

### Certification preparation preference

At the end of each DataCamp course or track:

- create strong digest documents
- create consolidated code summaries
- create self-tests
- create certification-prep artifacts
- update parent course and track indexes

---

## 9. Coursera / IBM RAG for Generative AI Applications

### Organization

The Coursera specialization is organized inside the same unified root:

```text
D:\Workarea\StudyBook\study_maps\DataCamp
```

Naming:

- Coursera folders use the `crs_` prefix.

Specialization:

```text
crs_rag_for_generative_ai_applications
```

The specialization has four Coursera/IBM courses.

Workflow:

1. Coursera reconnaissance first
2. Capture the actual course concepts
3. Build tiny local Lego-style labs
4. Reuse the best mechanics in a central library
5. Expand toward complete RAG applications

Primary provider:

- OpenAI

Future provider:

- IBM watsonx
- Sean created a free IBM watsonx account and wants to incorporate it later

### Canonical course location

The canonical course belongs under:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\crs_develop_generative_ai_applications_get_started
```

The older location under the specialization course tree is legacy/noncanonical:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\courses\develop_generative_ai_applications_get_started
```

### Documentation revamp preference

Sean requested a theory-centered rebuild in small review batches, beginning with:

```text
index.html
study_pages\field_guide.html
study_pages\chapter_01_ai_foundations_and_prompt_engineering_field_guide.html
```

The file list may evolve when useful new study documents become apparent.

---

## 10. RAG Application Builder Foundation

Root:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation
```

Purpose:

- unify DataCamp learning
- align with Coursera/IBM RAG material
- build reusable application bricks
- create a shared Python library
- eventually support full RAG and agent applications

Existing project structure includes:

- `index.html`
- roadmap
- reuse map
- alignment matrix
- monitoring plan
- Coursera reconnaissance document
- nine stage folders

### Stage 01 lab

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation\lab\python\stage_01_application_basics
```

Executed bricks include:

```text
01_first_request
15_route_decision_object
16_normalized_response_object
17_use_shared_text_provider
18_instructions_and_prompt
19_output_token_limit
20_structured_ticket_triage
21_validated_ticket_model
```

Concepts covered:

- model routing
- normalized provider responses
- reusable text providers
- instructions and user prompts
- output token limits
- structured output
- typed validation
- Pydantic models
- support-ticket triage

Sean asked to continue next with:

- multistage chat
- system/user roles
- centralized reusable conversation mechanics

Sean also asked for a curriculum tracker and summaries of completed bricks.

---

## 11. Shared Python Library — `rag_foundation`

Path:

```text
D:\py_libs\rag_foundation
```

Purpose:

- production-quality reusable helpers
- support RAG foundation labs
- reduce duplicated provider plumbing
- later support larger applications

Package information:

```text
Name: rag-foundation
Version: 0.1.0
Python: >=3.11
Build backend: setuptools.build_meta
```

Dependencies include:

- `openai`
- `python-dotenv`

Structure includes:

```text
src\rag_foundation
tests
docs
README.md
pyproject.toml
```

Implemented or observed modules:

### Requests

```text
rag_foundation.models.requests.TextGenerationRequest
```

Fields:

- `prompt`
- `instructions`
- `model`
- `max_output_tokens`

### Results

```text
rag_foundation.models.results.BaseGenerationResult
```

Fields include:

- provider
- model
- request ID
- raw response

### OpenAI provider

```text
rag_foundation.providers.openai_text.OpenAITextProvider
```

Responsibilities:

- API key handling
- default model
- client injection
- request execution
- normalized result production

### Supporting utilities

- `ConfigurationError`
- `ProviderError`
- `OpenAIError`
- `get_env`
- `require_env`

Documentation:

```text
docs\OPENAI_TEXT_PROVIDER.md
```

An editable installation attempt initially failed because of a `pyproject.toml` editable metadata issue.

### Quality rule

- `config.py` may remain as-is.
- Future files should follow the higher production standard.
- Shared mechanics should be:
  - typed
  - documented
  - tested
  - reusable

### Monitoring requirements

The library should eventually track:

- input tokens
- output tokens
- total tokens
- estimated cost
- configured budget
- remaining budget
- model usage
- request count
- latency
- retries
- failures
- provider errors
- operational metrics

---

## 12. Python Environments and Local Development

### Preferred central environment root

```text
C:\py_venv
```

### Foundation environment

A Python 3.13.11 environment was created at:

```text
D:\py_venv\rag_application_builder_foundation
```

A navigation helper named `RagCode` was defined in:

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

It changes directory to the foundation Python lab.

### Python versions mentioned

- Global Python:
  - 3.14.3
- Foundation virtual environment:
  - 3.13.11
- Other versions present under:

```text
C:\pyver
```

Including references to:

```text
py10
py119
py312
Python3114
```

### Environment preferences

- Centralize virtual environments.
- Centralize reusable libraries under:

```text
D:\py_libs
```

- Keep project labs separate from reusable libraries.
- Use `.env` files where appropriate.
- Do not commit secrets.

---

## 13. OpenAI Integration Learning System

After completing the current Developing AI Applications work, Sean wants to build a dedicated repository-based learning system for OpenAI integration.

The system should grow through:

1. tiny examples
2. reusable mechanics
3. Lego-style application components
4. larger applications
5. a personal shared Python library

The library should hide repetitive integration plumbing and make application development easier.

Desired reusable areas include:

- client configuration
- requests
- normalized responses
- structured output
- retries
- validation
- conversation handling
- RAG
- agent tools
- monitoring
- cost tracking
- budgets
- observability

---

## 14. RemNote Study System

Sean uses RemNote as the spaced-repetition system for review.

### General organization

- One RemNote space for IT learning is acceptable.
- Folders should provide rational structure.
- Permanent learning material remains in repositories and course chats.
- RemNote contains review cards organized by:
  - course
  - chapter
  - topic
  - technical knowledge
  - career/interview review
  - work/internal learning

Suggested hierarchy includes:

```text
IT Professional Development
├── Active Courses
├── Technical Knowledge
├── Career and Interview Review
└── Archive
```

Additional named areas include:

```text
Coursera
DataCamp
Sean’s Experience and Stories
LTIM Training
BOA Concepts
General Work Skills
```

### Preferred card strategy

- Multiple-choice cards are the primary learning mode.
- Multiple-choice should cover the full topic.
- A separate selective reinforcement mode should use mixed card types for:
  - confusing concepts
  - mistakes
  - code patterns
  - targeted review
- Do not force a fixed percentage for each card type.
- Let the study chat choose proportions according to the topic.

### File organization

Each RemNote chapter should contain a `Study` subfolder.

Numbered Markdown imports should make sequence obvious:

```text
01_...
02_...
03_...
```

Files must be:

- clean
- coherent
- limited to one topic or review unit
- free of junk noise
- tested for actual import behavior

At the end of a course, Sean wants the RemNote study-system constitution recreated by combining:

- the original project guide
- lessons learned from the course
- successful import formats
- card-generation practices

### Coding-card stack

For the current LangChain course, wait until code examples are complete.

Then create a dedicated numbered coding-terms/code-writing stack based on exact code patterns that successfully ran in Sean’s environment, including examples such as:

- `PromptTemplate.from_template()`
- `prompt.invoke()`
- `formatted.to_string()`
- `ChatPromptTemplate.from_messages()`
- `MessagesPlaceholder()`
- LCEL pipes
- `RunnableLambda`
- `RunnableParallel`
- output parsers

---

## 15. Public and Portfolio Projects

### HorizonScale

A time-series forecasting engine that:

- processes more than 8,000 time series
- runs model tournaments
- uses Spark
- supports capacity forecasting
- is part of Sean’s public technical story

### AI-powered job-search pipeline

Uses:

- Grok
- RAG
- FAISS
- structured YAML career profile
- retrieval-grounded fit scoring
- duplicate detection

### Possible YouTube/content niche

Sean has considered a children’s-story content niche based on different cultures and historical settings, including:

- Arab stories
- Persian stories
- Sindbad-style stories
- exposure to different eras and cultures

Sean is skeptical of hype-heavy “easy AI side hustle” claims and wants realistic evaluation of monetization claims.

---

## 16. Git, Backup, and Repository Practices

- Sean uses Git across multiple repositories.
- A helper such as `gitqall.ps1` is used to sync repositories.
- Originals that should not be committed are Git-ignored.
- Sensitive or large originals may be backed up to encrypted storage.
- Repositories should include:
  - memory documents
  - state trackers
  - runbooks
  - clear indexes
  - relative links
  - validation instructions
- Avoid duplicate implementations and duplicate files.
- Preserve canonical paths and names.
- Do not reorganize established roots without explicit agreement.

OneDrive context:

- approximately 1 TB total storage
- approximately 538.8 GiB free was previously noted

---

## 17. Logging and Observability Coding Interests

Sean has practiced or planned structured logging patterns involving:

- structured log files
- JSON logging
- development versus production logging
- `structlog`
- bound loggers
- context variables
- pipeline-stage logging
- extract → transform → load tracing
- DataFrame operation tracing
- error diagnosis

Example paths referenced in prior work included:

```text
LOG_DIR/02_structured.log
LOG_DIR/03_structlog_prod.json
```

Observability is both:

- a career strength
- a design requirement for future AI systems

---

## 18. Known Debugging Example

A prior SQLAlchemy/PostgreSQL error involved:

```text
ProgrammingError: column t.sample_time does not exist
```

The query joined:

- `telemetry_samples`
- `services`
- `hosts`

The database hint suggested that `t.sample_id` may have been intended.

The query attempted to order by:

```text
t.sample_time
s.service_name
h.host_name
```

This reflects Sean’s broader work with telemetry and observability datasets.

---

## 19. Current Focus Priorities

Current direction, in practical order:

1. Continue developing AI application skills.
2. Complete and organize the Coursera IBM RAG specialization.
3. Keep DataCamp materials consolidated and certification-ready.
4. Build the RAG Application Builder Foundation.
5. Expand the reusable `rag_foundation` library.
6. Add observability, token, cost, and budget tracking.
7. Build toward production-style RAG and agent applications.
8. Maintain employability in Python, PySpark, AWS, ETL, data engineering, and observability.
9. Keep BOA/LTM work materials in the separate private work repository — not in `local_memory`.
10. Use RemNote for structured long-term review.

---

## 20. Important Standing Constraints

- Teach in small bites.
- Do not assume hidden steps were understood.
- Avoid large study dumps.
- Preserve exact paths and canonical filenames.
- Do not create unnecessary duplicate files.
- Do not move established roots without agreement.
- Use a shared library for reusable mechanics.
- Keep future library code production-quality.
- Do not commit secrets or sensitive work information.
- Do not store BOA/LTM work materials in `local_memory`.
- Use multiple-choice as the primary RemNote learning mode.
- Use numbered import filenames inside chapter-level `Study` folders.
- Make study documents theory-centered and explain code clearly.
- Build Coursera content from actual course reconnaissance rather than inventing a parallel curriculum.
- Prefer OpenAI as the primary provider while leaving room for IBM watsonx.
- Include monitoring and budget visibility in the AI application architecture.
- Sean runs commands manually and benefits from exact Codex-ready prompts.

---

## 21. Recent Non-Project Topics That May Not Need Long-Term Retention

These topics appeared in conversations but are generally situational rather than core long-term memory:

- Powdery mildew remedies and Canadian products
- plant care in Kingston, Canada
- Arabic translations
- coercion meaning and word root
- RemNote button-layout changes
- bird identification
- screwworm discussions
- LangChain terminology
- fennel tea
- foods and mucus
- DataCamp interface/project visibility
- banking soft-token setup
- Egyptian bank certificates and rates
- brisket meatballs
- medicine identification
- seafood restaurants
- paratha availability
- vehicle lug-nut torque
- Islamic rule in Spain
- Iranian missile-range questions
- phone-number formatting
- Murphy University sessions

These may still exist in conversation history, but they are not central to the durable working profile.

---

## 22. Items That Should Be Reviewed Periodically

The following can become outdated and should not be treated as permanent without verification:

- active job applications
- compensation ranges
- interview dates
- current employment status
- current course progress
- canonical project paths after migrations
- Python versions
- cloud storage capacity
- current RemNote behavior
- current OpenAI, LangChain, DataCamp, Coursera, and IBM product details
- bank rates and financial-product terms
- personal contact and onboarding details

---

## 23. Suggested Use of This File

This file can serve as:

- a continuity handoff for a new ChatGPT project chat
- a personal project-context backup
- a source for project-specific constitutions
- a checklist for correcting outdated memories
- a starting point for deciding what should be remembered or forgotten

When using it in a new chat, it is best to say:

> Treat this as background context. Ask me to confirm anything time-sensitive, and do not assume every path or project status is still current.

---

## 24. Correction and Deletion Process

Sean can request any of the following:

- “Forget this item.”
- “Correct this path.”
- “This project is finished.”
- “Replace this memory with the following.”
- “Do not use this information in future conversations.”
- “Keep this only inside this project.”

Those requests should be applied explicitly rather than silently inferred.
