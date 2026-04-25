# Amazon EC2 — ChatGPT Project Prompts

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Amazon EC2
Slug: aws-ec2
Extra coverage required: instance families — compute, memory, storage, and GPU optimized — when to reach for each,
On-Demand vs Reserved vs Spot vs Savings Plans — cost tradeoffs and real commitment math,
EBS vs instance store — persistence, IOPS, throughput, and what survives a stop,
EBS volume types — gp3 vs io2 vs st1 and when each makes sense,
VPC networking on EC2 — ENIs, security groups, placement in subnets,
IAM instance profiles and the metadata service — how the SDK gets credentials automatically,
Auto Scaling Groups — launch templates, scaling policies, cooldown, lifecycle hooks,
load balancers — ALB vs NLB and when data engineers care about each,
placement groups — cluster for low latency, spread for fault isolation, partition for large distributed jobs,
EC2 in data engineering — when EC2 beats Lambda, Fargate, and Glue for heavy workloads,
AMIs and golden images — baking dependencies vs bootstrapping at launch,
user data and cloud-init for bootstrap automation,
cost optimization — rightsizing, Spot for batch, Savings Plans math.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug aws-ec2 -ChunkSize 750
```

Upload final_aws-ec2.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_aws-ec2.mp3` is live on R2.

```
Topic: Amazon EC2
Slug: aws-ec2
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-ec2.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-ec2.html
