# Amazon ECS + Docker — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: ECS and Docker
Slug: aws-ecs
Extra coverage required: Docker fundamentals — images, layers, the union filesystem, containers vs VMs,
Dockerfile best practices — layer caching, multi-stage builds to shrink runtime image size,
ECR — image lifecycle policies, vulnerability scanning, immutable tags and why latest is dangerous,
ECS architecture — clusters, services, task definitions, task revisions, and how they fit together,
Fargate vs EC2 launch type — the full tradeoff: operational overhead, cost, density, GPU support,
task execution role vs task role — which one does what and the most common confusion between them,
awsvpc networking — one ENI per task, security group per task, private IP allocation,
ECS service auto scaling — target tracking on CPU and memory, step scaling, scaling cooldown,
ECS for data pipelines — scheduled tasks for batch jobs, one-off run-task for backfill, long-running workers,
secrets management — injecting Secrets Manager and SSM Parameter Store values at task startup,
blue/green deployments with CodeDeploy — traffic shifting, automatic rollback, deployment lifecycle hooks,
CloudWatch Container Insights — task-level metrics, log routing with awslogs driver,
health checks — container health check vs load balancer health check — what each proves,
Fargate Spot for cost reduction on fault-tolerant batch workloads,
common failure patterns — task fails to start, image pull errors, out-of-memory, missing IAM permissions.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-ecs -ChunkSize 750
```

Upload final_aws-ecs.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-ecs.mp3` is live on R2.

```
Topic: ECS and Docker
Slug: aws-ecs
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ecs.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-ecs.html
