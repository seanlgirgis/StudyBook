# User Profile

**Last Updated:** 2026-04-10  
**Primary Sources:**  
- `D:\StudyBook\temp\jobsearch\data\source_of_truth.json`  
- `D:\StudyBook\temp\seanlgirgis.github.io` (repo structure and generators)

## Core Career Identity

- Senior Data Engineer and Capacity/Data Engineering leader with 20+ years of enterprise experience.
- Target directions: Senior/Staff Data Engineering, Cloud Data Architecture, AI-enabled Data Engineering.
- Recent core focus: AWS + PySpark + forecasting + agentic AI workflows.
- Domain depth across performance engineering, observability, capacity planning, and data pipeline modernization.

## Current Positioning Signals

- Most recent long tenure: Citi (2017-11 to 2025-12) in senior capacity/data engineering scope.
- Strong legacy-to-modern bridge: C/C++/Oracle/J2EE history plus modern Python/PySpark/AWS/GenAI execution.
- Preferred market: DFW (Plano/Murphy) and remote-friendly roles.

## Demonstrated Project Themes

- AI-powered job search automation pipeline (agentic orchestration, vector similarity, LLM generation and gates).
- HorizonScale-style forecasting and telemetry optimization work (forecast models + operational dashboards).
- Serverless lakehouse patterns on AWS (S3/Glue/Athena/Bedrock + optimization practices).

## Technical Strength Pattern

- Modern strengths: Python, SQL, PySpark, AWS, ETL design, forecasting, automation.
- Platform strengths: monitoring/APM/capacity ecosystems (CA APM, Dynatrace, BMC TrueSight).
- Architecture strength: connecting infra telemetry, analytics, and decision workflows for business outcomes.

## Working Style Preferences

- Prefers direct, practical, outcome-first communication.
- Learns quickly with examples and runnable artifacts.
- Prefers durable project memory in files, not chat-only state.
- Strong emphasis on encryption/secret hygiene and machine-portable setup.

## Operational Anchors

- StudyBook runtime venv: `C:\py_venv\proj_educate`
- JobSearch runtime venv (project-owned): `C:\py_venv\JobSearch`
- Website repo currently has its own env script pointing to: `C:\py_venv\resume_venv`

## JobSearch Source of Truth Rule

- Treat `D:\StudyBook\temp\jobsearch\data\source_of_truth.json` as canonical career/resume data for JobSearch workflows.
- Any generated resume, tailoring, or job-fit logic should reconcile against this file first.

## Website Repo Map (High-Level)

- `D:\StudyBook\temp\seanlgirgis.github.io\generate.py` is the central multi-format build orchestrator.
- Data/layout inputs are YAML-driven under `...\data\` with a `store.yaml` content model plus target layouts.
- Renderers live under `...\renderers\` (`docx`, `html`, `pdf`, `md`).
- Build outputs include `resume/cv` docx/pdf/md/html assets and site components.

## Website Stewardship Directive

- Standing owner directive (2026-04-10): treat Codex as the default steward for
  `https://github.com/seanlgirgis/seanlgirgis.github.io`.
- By default, proactively maintain and improve:
  - blog/article quality and publishing flow,
  - site navigation and discoverability (including sitemap/listing integrity),
  - downloadable artifacts and technical content presentation.
- Use safe, scoped changes and keep publish actions auditable via clear commit messages.

## Search Engine Ownership (Website)

- Canonical site: `https://seanlgirgis.github.io`
- Google Search Console owner account for site submission:
  - `sean.girgis@gmail.com`
- Bing Webmaster owner account for site submission:
  - `seanlgirgis@gmail.com`
- Reminder: keep sitemap submission and verification workflows aligned to these account owners.

## Collaboration Reminder

- Keep responses concise and execution-oriented.
- For job-search support, optimize for:
  - role targeting clarity,
  - quantifiable impact wording,
  - fast iteration loops across resume/profile/site.
## Learning Reminder

- Keep this YouTube channel in recommendations for LeetCode/graph prep when asked:
  - OffByOneCode: `https://www.youtube.com/@offbyonecode/videos`

## Algorithm Learning Preference

- For monotonic stack / next-greater style problems, prefer teaching via this frame:
  - "For whom am I the answer?" (left-to-right scan),
  - stack holds indices still waiting for their next greater,
  - when current value is greater than stack-top value, pop and resolve those indices.
- This frame is preferred over right-to-left "what is greater to my right?" explanations unless explicitly requested otherwise.

## StudyBook Command Shortcuts

- High-frequency index workflow commands to preserve in durable memory:
  - `D:\StudyBook\refresh_index_and_push.ps1` (refreshes `coding_challenges/index.xlsx`, commits, pushes)
  - `D:\StudyBook\search_index.ps1 <needle> [-Limit <n>] [-CaseSensitive] [-h]` (grep-like lookup over `coding_challenges/index.xlsx`)
- Example:
  - `.\search_index.ps1 48`
