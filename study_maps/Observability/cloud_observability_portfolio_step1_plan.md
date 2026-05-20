# Cloud Observability Portfolio Roadmap — Step 1 and Multi-Month Plan

Owner: Sean Girgis  
Purpose: Build a practical cloud observability, APM, capacity monitoring,
and reporting portfolio using a local PC, Docker/Linux, StudyBubble maps,
web pages, Markdown documents, and safe cloud/vendor trials.

---

## 1. Mission

This roadmap is not only for one interview or one job. It is the longer-term
career bridge from enterprise capacity engineering and APM monitoring into
modern cloud observability.

The target lane is:

```text
Cloud Observability + Capacity Monitoring + APM + Reporting
```

The goal is to reuse Sean's strongest background:

```text
capacity engineering
telemetry
dashboards
thresholds
forecasting
RCA
runbooks
management reporting
enterprise APM experience
```

Then modernize it with:

```text
OpenTelemetry
Prometheus
Grafana
AWS CloudWatch
Dynatrace
Splunk
Datadog
Kubernetes monitoring
Docker-based local labs
cloud-aware runbooks
portfolio documentation
```

This roadmap should remain useful even if the BOA role works out. If a job
starts, this becomes the professional growth roadmap for the next several
months.

---

## 2. Ground Rules

### 2.1 Truth and positioning

Do not pretend to be a deep production owner of every modern cloud tool.

Safe positioning:

```text
I have strong enterprise capacity engineering and monitoring experience.
I am modernizing that background into cloud-native observability by building
hands-on labs with OpenTelemetry, Prometheus, Grafana, CloudWatch, Dynatrace,
Splunk, Datadog, and Kubernetes telemetry.
```

Avoid overclaiming:

```text
deep Kubernetes platform ownership
deep Prometheus production administration
deep Grafana enterprise administration
deep OpenTelemetry production rollout ownership
deep Terraform/CloudFormation ownership
deep GPU monitoring ownership
```

Use careful language:

```text
built labs
created runbooks
studied modern patterns
mapped old APM/capacity experience to new cloud telemetry patterns
can read and explain telemetry
can build dashboard and alerting logic
can connect signals to capacity and business risk
```

---

## 3. Local Base Folder

Recommended base location:

```text
D:\Workarea\StudyBook\cloud_observability_portfolio
```

Recommended high-level structure:

```text
cloud_observability_portfolio/
  README.md
  PROJECT_STATE.md
  ROADMAP.md
  DECISIONS.md
  TASK_BOARD.md
  portfolio_home/
  study_maps/
  labs/
  docs/
  runbooks/
  interview_stories/
  resume_bullets/
  screenshots/
  vendor_trials/
  job_keywords/
```

Purpose of each area:

```text
README.md
  Front door for the portfolio.

PROJECT_STATE.md
  Current status, last completed work, next step, known issues.

ROADMAP.md
  The larger plan across months.

DECISIONS.md
  Key decisions so future AI/Codex sessions do not lose direction.

TASK_BOARD.md
  Active, next, blocked, and completed tasks.

portfolio_home/
  Web page index that links to maps, labs, runbooks, and stories.

study_maps/
  StudyBubble maps and generated single-file HTML outputs.

labs/
  Docker, Python, AWS, OpenTelemetry, Grafana, Splunk, Datadog,
  Dynatrace, and Kubernetes labs.

docs/
  Concept notes, comparison pages, architecture notes, and learning
  summaries.

runbooks/
  Practical incident and capacity response guides.

interview_stories/
  Short, medium, and deep explanations of each portfolio project.

resume_bullets/
  Safe resume bullets created only after real work is completed.

screenshots/
  Evidence images from dashboards, terminals, and lab outputs.

vendor_trials/
  Notes and screenshots from trial environments.

job_keywords/
  Search terms, job-title clusters, and fit notes.
```

---

## 4. Step 1 — Create the Portfolio Foundation

Step 1 should not start by trying every vendor tool at once.

Step 1 is:

```text
Create the portfolio foundation and the first 1000-foot observability map.
```

Deliverables:

```text
01_portfolio_foundation/
  README.md
  docs/
    observability_1000_foot_view.md
    old_to_new_skill_bridge.md
    tool_landscape.md
    glossary.md
  study_maps/
    observability_1000_foot_view.studybubble.json
    outputs/
      observability_1000_foot_view.html
  interview_stories/
    story_01_observability_transition.md
  resume_bullets/
    draft_bullets_01.md
  job_keywords/
    cloud_observability_keywords.md
```

Why this is the best first step:

```text
It organizes the road before building labs.
It turns the direction into a reusable learning system.
It gives StudyBubble something meaningful to render.
It creates an interview-safe explanation of the transition.
It prevents random tool-hopping between AWS, Dynatrace, Splunk, Datadog,
Prometheus, and Grafana.
```

---

## 5. Step 1 Content Scope

### 5.1 Observability 1000-foot map

The first StudyBubble map should explain:

```text
Observability
Telemetry
Metrics
Logs
Traces
APM
Dashboards
Alerts
Runbooks
Capacity monitoring
Forecasting
Cloud monitoring
OpenTelemetry
Prometheus
Grafana
CloudWatch
Dynatrace
Splunk
Datadog
Kubernetes monitoring
```

Keep the first map small enough to study.

Recommended limit:

```text
15 to 21 bubbles
```

If more detail is needed, create child maps later.

### 5.2 Old-to-new skill bridge

Create a document that maps old experience to modern terms.

Example:

```text
Old experience:
Enterprise telemetry, thresholds, RCA, capacity reports, APM tools.

Modern language:
Metrics, logs, traces, service health, SLOs, alerting, dashboards,
OpenTelemetry pipelines, cloud monitoring, Kubernetes signals.
```

Example bridge:

```text
Dynatrace AppMon / CA APM / AppDynamics experience
  -> APM concepts, transaction visibility, service health, response time,
     error rate, topology, root-cause workflows.

BMC TrueSight / TSCO capacity work
  -> telemetry pipelines, headroom, thresholds, forecasting, risk ranking,
     capacity dashboards, executive reporting.

Gomez synthetic monitoring
  -> synthetic checks, availability, user-path monitoring, SLA evidence.

Python forecasting/reporting
  -> modern observability analytics and capacity intelligence.
```

### 5.3 Tool landscape document

Create a simple comparison page.

Include:

```text
OpenTelemetry
  Vendor-neutral telemetry collection and routing pattern.

Prometheus
  Metrics collection and time-series monitoring.

Grafana
  Visualization, dashboards, and alerting.

AWS CloudWatch
  AWS-native metrics, logs, alarms, dashboards, and service visibility.

Dynatrace
  Enterprise APM, OneAgent, topology, problem detection, Davis AI.

Splunk
  Log analytics, SPL, dashboards, alerts, and Splunk Observability Cloud.

Datadog
  SaaS observability platform for metrics, traces, logs, infrastructure,
  APM, dashboards, and alerts.

Kubernetes monitoring
  Pod, node, deployment, service, namespace, requests, limits,
  restarts, and cluster health signals.
```

### 5.4 Glossary

Start with practical definitions only.

Examples:

```text
Metric
  A numeric signal over time, such as CPU percent, memory usage,
  request count, or latency.

Log
  A timestamped event message that explains what happened.

Trace
  A path of one request across services.

Span
  One timed operation inside a trace.

Dashboard
  A visual view of key signals.

Alert
  A rule that notifies people when a condition is risky.

Runbook
  A practical response guide for investigating and handling an issue.

Headroom
  The space between current usage and a warning or failure threshold.

SLO
  A target for service reliability or performance.

OpenTelemetry Collector
  A service that receives, processes, and exports telemetry.
```

---

## 6. Step 1 Acceptance Criteria

Step 1 is complete only when these are true:

```text
[ ] Base folder exists.
[ ] README.md explains the portfolio mission.
[ ] PROJECT_STATE.md says current phase and next step.
[ ] ROADMAP.md contains the multi-month direction.
[ ] DECISIONS.md records naming and folder decisions.
[ ] TASK_BOARD.md lists active and next tasks.
[ ] Observability 1000-foot document exists.
[ ] Old-to-new skill bridge document exists.
[ ] Tool landscape document exists.
[ ] Glossary exists.
[ ] First StudyBubble map exists.
[ ] First StudyBubble single-file HTML output opens locally.
[ ] Portfolio home page links to the first map and documents.
[ ] First interview story exists.
[ ] Draft resume bullets exist but are clearly marked as draft.
[ ] Job keyword list exists.
```

Console/browser acceptance:

```text
[ ] The HTML page opens directly from file://.
[ ] Search or navigation works if included.
[ ] No obvious missing links.
[ ] No broken resource references.
```

---

## 7. Step 2 — Local OpenTelemetry Lab

After the foundation is complete, build the first real technical lab.

Target:

```text
FastAPI + OpenTelemetry SDK + OpenTelemetry Collector + Docker Compose
```

Deliverables:

```text
02_otel_fastapi_collector/
  README.md
  docker-compose.yml
  app/
  otel-collector-config.yaml
  docs/
    architecture.md
    concepts.md
  runbooks/
    runbook_no_traces_seen.md
  screenshots/
  interview_stories/
    story_02_otel_collector.md
```

Goal:

```text
Understand the modern telemetry collection pattern:
application emits telemetry,
collector receives/processes telemetry,
backend receives the telemetry.
```

Safe interview sentence:

```text
I built a small FastAPI lab instrumented with OpenTelemetry and routed
telemetry through the OpenTelemetry Collector so I could understand the
modern vendor-neutral collection pattern.
```

---

## 8. Step 3 — Prometheus and Grafana Capacity Dashboard

Target:

```text
Prometheus + Grafana + node_exporter + cAdvisor or Docker metrics
```

Deliverables:

```text
03_prometheus_grafana_capacity_dashboard/
  README.md
  docker-compose.yml
  prometheus.yml
  grafana_dashboard.json
  docs/
    metrics_explained.md
    capacity_dashboard_design.md
  runbooks/
    runbook_high_cpu.md
    runbook_high_memory.md
  screenshots/
  interview_stories/
    story_03_grafana_capacity_dashboard.md
```

Dashboard panels:

```text
CPU usage
memory usage
disk usage
network I/O
container count
container restart count
threshold line
headroom calculation
```

Safe interview sentence:

```text
I created a local Prometheus and Grafana capacity dashboard that connects
infrastructure metrics to threshold and headroom thinking.
```

---

## 9. Step 4 — Capacity Forecasting from Monitoring Data

This is the strongest differentiator.

Target:

```text
Export or simulate Prometheus-style metrics.
Use Python to engineer forecasting and risk features.
```

Features:

```text
hourly buckets
daily buckets
rolling average
rolling peak
P95
growth slope
headroom to threshold
breach flag
risk band
forecast vs actual comparison
dashboard-ready CSV
```

Deliverables:

```text
04_capacity_forecasting_from_monitoring_data/
  README.md
  src/
  notebooks/
  data/
  outputs/
  docs/
    feature_design.md
    validation_plan.md
  runbooks/
    runbook_capacity_risk_review.md
  interview_stories/
    story_04_capacity_forecasting_bridge.md
```

Safe interview sentence:

```text
I extended monitoring data into capacity forecasting by creating features
like rolling averages, peaks, P95, growth slope, headroom, breach flags,
and risk bands.
```

---

## 10. Step 5 — Logs and Traces Troubleshooting Lab

Target:

```text
FastAPI slow endpoint
FastAPI error endpoint
OpenTelemetry traces
logs
Grafana Loki
Grafana Tempo
incident walkthrough
```

Deliverables:

```text
05_logs_traces_troubleshooting/
  README.md
  docker-compose.yml
  app/
  docs/
    incident_walkthrough.md
    logs_metrics_traces_relationship.md
  runbooks/
    runbook_high_latency.md
    runbook_error_spike.md
  screenshots/
  interview_stories/
    story_05_symptom_to_evidence.md
```

Safe interview sentence:

```text
I built a small incident lab where a dashboard symptom could be followed
to trace and log evidence, similar to how teams investigate performance
or error issues.
```

---

## 11. Step 6 — AWS CloudWatch Monitoring Lab

Use a cost-safe AWS approach.

Possible tracks:

```text
Option A: Lambda monitoring
Option B: EC2 monitoring
Option C: ECS basic monitoring
```

Start with only one.

Deliverables:

```text
06_aws_cloudwatch_monitoring/
  README.md
  docs/
    cloudwatch_metrics.md
    cloudwatch_logs.md
    alarm_design.md
    dashboard_design.md
    cost_safety.md
  runbooks/
    runbook_cloudwatch_high_cpu.md
    runbook_cloudwatch_error_alarm.md
  screenshots/
  interview_stories/
    story_06_aws_cloudwatch_monitoring.md
```

Safe interview sentence:

```text
I built a small AWS CloudWatch monitoring lab focused on metrics, logs,
alarms, dashboards, and runbook thinking.
```

---

## 12. Step 7 — Vendor Refresh Lanes

These should be controlled refresh lanes, not rabbit holes.

### 12.1 Dynatrace refresh

Focus:

```text
OneAgent
Smartscape / topology
services
process groups
hosts
dashboards
synthetic monitoring
Davis AI
problem detection
management zones
SLOs
cloud integrations
Kubernetes visibility
```

Deliverables:

```text
07_dynatrace_refresh/
  README.md
  docs/
    oneagent_notes.md
    davis_ai_notes.md
    topology_notes.md
    synthetic_monitoring_notes.md
    cloud_monitoring_notes.md
  screenshots/
  interview_stories/
    story_07_dynatrace_refresh.md
```

Safe interview sentence:

```text
I used APM and monitoring platforms historically, and I am refreshing
Dynatrace's modern model around OneAgent, topology, Davis AI, cloud
monitoring, and Kubernetes visibility.
```

### 12.2 Splunk refresh

Focus:

```text
index
sourcetype
SPL basics
search
stats
timechart
rex
fields
dashboards
alerts
Splunk Observability Cloud
Splunk OpenTelemetry Collector
```

Deliverables:

```text
08_splunk_refresh/
  README.md
  docs/
    spl_basics.md
    dashboard_notes.md
    alerting_notes.md
    splunk_otel_notes.md
  labs/
    sample_log_investigation.md
  screenshots/
  interview_stories/
    story_08_splunk_refresh.md
```

Safe interview sentence:

```text
I created Splunk practice notes and sample SPL-style investigation flows
for logs, dashboards, alerting, and observability workflows.
```

### 12.3 Datadog refresh

Focus:

```text
infrastructure monitoring
APM
logs
metrics
traces
dashboards
monitors
service map
synthetics
cloud integrations
Kubernetes visibility
OpenTelemetry support
```

Deliverables:

```text
09_datadog_refresh/
  README.md
  docs/
    datadog_overview.md
    monitors_vs_alerts.md
    apm_notes.md
    dashboards_notes.md
    otel_notes.md
  screenshots/
  interview_stories/
    story_09_datadog_refresh.md
```

Safe interview sentence:

```text
I refreshed Datadog concepts around infrastructure monitoring, APM,
logs, traces, dashboards, monitors, and cloud integration patterns.
```

---

## 13. Step 8 — Kubernetes Monitoring Lane

Keep it practical.

Do not try to become a Kubernetes administrator first.

Target:

```text
kind or minikube
sample app
Prometheus/Grafana monitoring
kube-state-metrics
container metrics
basic alerts
capacity runbooks
```

Focus signals:

```text
pod restart
CrashLoopBackOff
Pending pod
node pressure
CPU requests and limits
memory requests and limits
HPA behavior
namespace usage
deployment health
service health
```

Deliverables:

```text
10_kubernetes_monitoring/
  README.md
  docs/
    k8s_monitoring_terms.md
    pod_node_service_signals.md
    requests_limits_capacity.md
  runbooks/
    runbook_pod_restarts.md
    runbook_node_pressure.md
    runbook_pending_pod.md
  screenshots/
  interview_stories/
    story_10_kubernetes_monitoring.md
```

Safe interview sentence:

```text
I am not claiming deep Kubernetes platform ownership yet, but I can read
Kubernetes telemetry and connect pod, node, and service signals to capacity
and reliability risk.
```

---

## 14. Monthly Roadmap

### Month 1 — Foundation and First Local Labs

Goal:

```text
Build orientation, first map, and first Docker-based telemetry lab.
```

Work:

```text
Week 1:
  Portfolio foundation
  Observability 1000-foot map
  glossary
  tool landscape
  old-to-new skill bridge

Week 2:
  FastAPI + OpenTelemetry Collector lab

Week 3:
  Prometheus + Grafana local dashboard

Week 4:
  Capacity dashboard documentation and runbooks
```

Outcome:

```text
Sean can explain observability clearly and show local working evidence.
```

### Month 2 — Capacity Intelligence and Troubleshooting

Goal:

```text
Turn monitoring into Sean's unique capacity intelligence lane.
```

Work:

```text
Week 5:
  Capacity forecasting from monitoring data

Week 6:
  Feature engineering and validation documents

Week 7:
  Logs and traces troubleshooting lab

Week 8:
  Incident walkthroughs and runbooks
```

Outcome:

```text
Sean can show dashboard symptoms, telemetry evidence, and capacity risk
translation.
```

### Month 3 — Cloud and Vendor Coverage

Goal:

```text
Add cloud-native and enterprise vendor credibility.
```

Work:

```text
Week 9:
  AWS CloudWatch monitoring lab

Week 10:
  Dynatrace refresh

Week 11:
  Splunk refresh

Week 12:
  Datadog refresh
```

Outcome:

```text
Sean can speak across cloud-native and enterprise observability stacks.
```

### Month 4 — Kubernetes and Portfolio Packaging

Goal:

```text
Add practical Kubernetes monitoring and package the portfolio.
```

Work:

```text
Week 13:
  Kubernetes local cluster basics

Week 14:
  Kubernetes metrics and dashboard

Week 15:
  Kubernetes runbooks

Week 16:
  Portfolio polish, resume bullets, interview stories, job keyword map
```

Outcome:

```text
Sean has a coherent cloud observability portfolio, not random notes.
```

---

## 15. Cyclic Work Pattern

Every topic should follow the same cycle:

```text
1. Map it.
2. Explain it in plain language.
3. Build a small lab.
4. Capture screenshots.
5. Create a runbook.
6. Write an interview story.
7. Create safe resume bullets.
8. Add job search keywords.
9. Review what changed in Sean's positioning.
```

Do not skip directly to tooling.

A tool is only valuable when it produces:

```text
working evidence
clear explanation
runbook
story
resume-safe bullet
job-search keyword
```

---

## 16. Evidence Standard

Every portfolio project should include evidence.

Minimum evidence:

```text
README.md
architecture or concept document
runbook
screenshots
interview story
resume bullet draft
known limitations
next improvements
```

Screenshots should show:

```text
dashboard
terminal command output
running container
generated report
cloud console view
alert rule
trace/log view
```

Do not include secrets, keys, account IDs, private URLs, or personal data.

---

## 17. Resume Bullet Policy

Only create resume bullets after work exists.

Use three levels:

```text
Level 1: Lab bullet
  Built a local lab...

Level 2: Portfolio bullet
  Created a portfolio project demonstrating...

Level 3: Experience bridge bullet
  Extended prior capacity engineering experience by building...
```

Example safe bullet:

```text
Built a local Prometheus/Grafana capacity monitoring lab with CPU,
memory, disk, container, threshold, and headroom views, supported by
runbook documentation and dashboard screenshots.
```

Avoid:

```text
Owned enterprise Prometheus platform.
Managed production Kubernetes monitoring.
Led Datadog enterprise rollout.
Implemented company-wide OpenTelemetry migration.
```

Unless those are actually true.

---

## 18. Interview Story Template

Each project gets a story with this format:

```text
Problem:
  What real-world problem does this represent?

Setup:
  What did I build?

Signals:
  What telemetry did I collect or study?

Analysis:
  How did I interpret the signals?

Action:
  What dashboard, alert, report, or runbook did I create?

Business value:
  How does this help capacity, reliability, cost, or management decisions?

Limitations:
  What is lab-level vs production-level?

Next step:
  How would this grow in a real environment?
```

---

## 19. Job Keyword Lanes

Use these search phrases while building the portfolio:

```text
Cloud Monitoring Engineer
Observability Engineer
APM Engineer
Capacity Engineer Cloud
Infrastructure Monitoring Engineer
Application Performance Monitoring Engineer
Prometheus Grafana Engineer
OpenTelemetry Engineer
AWS CloudWatch Monitoring Engineer
Splunk Observability Engineer
Dynatrace Engineer
Datadog Monitoring Engineer
SRE Observability
Cloud Operations Monitoring
Kubernetes Monitoring Engineer
Capacity Planning Engineer Cloud
```

More targeted searches:

```text
Grafana Prometheus Capacity Monitoring
OpenTelemetry Collector Python FastAPI
AWS CloudWatch Alarms Dashboards
Dynatrace OneAgent APM Cloud
Splunk SPL Dashboard Alert Monitoring
Datadog APM Infrastructure Monitoring
Kubernetes Pod Node Metrics Grafana
```

---

## 20. First Codex Prompt

Use this after creating the base folder.

```text
We are starting the Cloud Observability Portfolio project.

Base folder:
D:\Workarea\StudyBook\cloud_observability_portfolio

Purpose:
Build a long-term portfolio and learning system for cloud observability,
APM, capacity monitoring, telemetry, dashboards, alerts, runbooks, and
interview stories.

Create the initial project structure only. Do not build technical labs yet.

Create these files:

README.md
PROJECT_STATE.md
ROADMAP.md
DECISIONS.md
TASK_BOARD.md

Create these folders:

portfolio_home
study_maps
labs
docs
runbooks
interview_stories
resume_bullets
screenshots
vendor_trials
job_keywords

Create first project folder:

labs\01_portfolio_foundation

Inside it create:

README.md
docs\observability_1000_foot_view.md
docs\old_to_new_skill_bridge.md
docs\tool_landscape.md
docs\glossary.md
study_maps\observability_1000_foot_view.studybubble.json
interview_stories\story_01_observability_transition.md
resume_bullets\draft_bullets_01.md
job_keywords\cloud_observability_keywords.md

Rules:
- Keep content practical and interview-safe.
- Do not overclaim production ownership of modern tools.
- Emphasize Sean's bridge from enterprise capacity/APM monitoring into
  cloud-native observability.
- First StudyBubble map should be 15 to 21 nodes maximum.
- No broken links.
- Do not create vendor trial work yet.
- Do not create AWS resources yet.
- Do not create Docker labs yet.

After creating files, report:
1. Files created.
2. Folder tree.
3. Any assumptions made.
4. Next recommended task.
```

---

## 21. First StudyBubble Map Scope

Recommended first map title:

```text
Cloud Observability 1000-Foot View
```

Recommended bubbles:

```text
1. Observability
2. Telemetry
3. Metrics
4. Logs
5. Traces
6. APM
7. Dashboards
8. Alerts
9. Runbooks
10. Capacity Monitoring
11. Forecasting
12. OpenTelemetry
13. Prometheus
14. Grafana
15. CloudWatch
16. Dynatrace
17. Splunk
18. Datadog
19. Kubernetes Monitoring
20. Business Reporting
21. Sean's Skill Bridge
```

Main idea:

```text
The map should show how old enterprise capacity/APM experience connects
to modern cloud observability tools.
```

---

## 22. What Not To Do First

Do not start with:

```text
full AWS architecture
paid vendor setup
large Kubernetes cluster
complicated Terraform deployment
too many dashboards
too many StudyBubble maps
GPU monitoring deep dive
production-grade alerting policy
multi-cloud design
```

Those can come later.

The first win is:

```text
A clean portfolio home,
a clear map,
a believable story,
and a stable folder structure.
```

---

## 23. Definition of Done for the First Weekend

By the end of the first work block, the project should have:

```text
[ ] Base folder created.
[ ] Initial Markdown files created.
[ ] Portfolio mission written.
[ ] First StudyBubble topic drafted.
[ ] First generated HTML map opens.
[ ] Glossary started.
[ ] Tool landscape started.
[ ] Old-to-new skill bridge written.
[ ] First interview story drafted.
[ ] First job keyword list drafted.
[ ] TASK_BOARD.md shows the next technical lab.
```

The next technical lab should be:

```text
02_otel_fastapi_collector
```

---

## 24. Long-Term North Star

The final portfolio should prove this:

```text
Sean can take telemetry from systems, understand the signals, build
dashboards, define alerts, create runbooks, forecast capacity risk, and
explain the business impact.

He can bridge older enterprise APM/capacity experience into modern
cloud observability stacks.
```

That is the career story.

That is the roadmap forward.
