SAVE AS: infra_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate infra_concepts.md — a concept reference covering IaC, Docker, Kubernetes,
and Terraform core concepts for data engineering contexts.

DATASET CONTEXT — do not deviate:
- Citi narrative: telemetry stack runs on Docker locally, Kubernetes in production,
  Terraform provisions the cloud data platform (S3, Glue, EMR, IAM)

STRUCTURE — produce exactly these sections in order:

# Infrastructure — Core Concepts

## 1. Infrastructure as Code (IaC)
One paragraph. Cover: define infra in version-controlled files, reproducibility eliminates
"it worked on my machine" for environments, declarative (Terraform, Pulumi) vs imperative
(Ansible, scripts), GitOps = infra changes go through PRs, drift = when live state diverges from code.
End with: "Citi's data platform is Terraform-managed — a PR to main.tf provisions S3, Glue catalog, IAM roles, and EMR in one apply."

## 2. Immutable Infrastructure
One paragraph. Cover: servers/containers are never updated in place — they are replaced,
contrast with mutable infrastructure (SSH in, apt-get upgrade), why immutability prevents
configuration drift, containers are inherently immutable (rebuild image, redeploy container),
blue-green deployments as the operational pattern.
End with: "When Airflow upgrades from 2.8.0 to 2.9.0, we update the image tag in docker-compose.yml, pull, and recreate — not SSH in and pip install."

## 3. Container vs VM
One paragraph. Cover: VMs virtualize hardware (hypervisor), containers virtualize the OS
(share the host kernel), containers are milliseconds to start vs minutes for VMs, containers are
megabytes vs gigabytes, tradeoff: containers share the kernel (less isolation), VMs fully isolated.
End with: "Each citi_* container starts in under 2 seconds; an equivalent EC2 instance takes 60-90 seconds to boot."

## 4. Kubernetes Architecture
One paragraph. Cover: control plane (API server, etcd, scheduler, controller-manager) vs worker nodes,
kubelet on each node runs Pods, kube-proxy handles network rules, kubectl is the CLI client,
the control plane is managed by cloud providers in EKS/GKE/AKS.
End with: "In production, Airflow's KubernetesExecutor sends tasks to the API server, which schedules a Pod on a worker node — the scheduler never sees the Pod directly."

## 5. Pod + Deployment
One paragraph. Cover: Pod = smallest schedulable unit (1+ containers, shared network/storage),
Pods are ephemeral (if a node dies, the Pod dies), Deployment = controller that maintains N Pod
replicas, Deployment self-heals (recreates failed Pods), rolling updates with zero downtime,
Deployment does NOT manage stateful workloads (use StatefulSet for Kafka, Postgres).
End with: "A Kafka Connect Deployment with replicas=3 self-heals — if one Pod crashes, K8s recreates it within seconds."

## 6. Terraform State
One paragraph. Cover: terraform.tfstate maps HCL resources to real cloud resource IDs,
plan diffs HCL against state (not against live cloud), remote state on S3+DynamoDB for teams,
state locking prevents concurrent applies, never edit state manually, terraform import brings
unmanaged resources under Terraform control.
End with: "Citi's Terraform state lives in an S3 bucket with DynamoDB locking — two engineers can't apply simultaneously."

## 7. Terraform Plan/Apply Cycle
One paragraph. Cover: init downloads providers, plan computes the diff (+ add, ~ change, - destroy),
plan output is a saved binary (terraform apply tfplan) — apply executes exactly the plan,
-auto-approve skips the confirmation prompt (only in CI), modules encapsulate reusable resource groups.
End with: "Every infra change at Citi goes through a PR: plan output in CI comments, reviewer approves, apply runs in CD pipeline."

## 8. K8s for Data Engineering
One paragraph. Cover: KubernetesExecutor in Airflow (Pod per task, no idle workers), Spark on K8s
(driver submits to API server, executor Pods scale dynamically), StatefulSets for Kafka
(stable pod names + persistent volumes), K8s Secrets for credentials, K8s resource limits
prevent one job from starving others.
End with: "Staff DE interview answer to 'how do you scale Airflow?': switch from LocalExecutor to KubernetesExecutor — tasks spin Pods, no idle workers, cluster autoscaler handles bursts."

---

## Quick Reference Table

| Concept | One-line definition | Citi example |
|---------|---------------------|--------------|
| IaC | Infra defined in version-controlled code | main.tf provisions S3 + Glue + EMR |
| Immutable Infra | Replace containers, never update in place | docker pull new image → recreate |
| Container vs VM | Container shares kernel; VM virtualizes hardware | citi_* containers vs EC2 instances |
| K8s Architecture | Control plane + worker nodes; kubelet runs Pods | EKS on AWS for production |
| Pod + Deployment | Pod = container wrapper; Deployment = self-healing N replicas | KafkaConnect replicas=3 |
| Terraform State | Maps HCL to real resource IDs | S3 + DynamoDB remote state |
| Plan/Apply Cycle | Init → Plan → Apply; plan is the diff | PR → CI plan → CD apply |
| K8s for DE | KubernetesExecutor, Spark on K8s, StatefulSets | Airflow task Pods, Spark executors |

---

## Interview Flashcards

**Q: What is infrastructure drift and how do you detect it?**
A: Drift occurs when someone modifies cloud resources outside of Terraform (via console or CLI).
terraform plan compares HCL against state, not live cloud — so drift is invisible to plan unless
you run terraform refresh first. Use AWS Config or Terraform Cloud drift detection for continuous monitoring.

**Q: Why use StatefulSet instead of Deployment for Kafka?**
A: Deployments give Pods random names and are designed for stateless workloads. Kafka brokers
need stable network identities (kafka-0, kafka-1, kafka-2) and persistent volumes that survive
pod restarts. StatefulSet provides ordered, stable pod names and persistent volume claims that
follow the pod across rescheduling.

**Q: What happens when a Kubernetes node fails?**
A: The controller-manager detects the node as NotReady (kubelet heartbeat stops). Deployments
managed by a ReplicaSet will reschedule their Pods on healthy nodes. Pods without a controller
(bare Pods) are lost. This is why you always use Deployments/StatefulSets, not bare Pods.

**Q: What is the difference between terraform plan and terraform apply?**
A: plan computes and displays what Terraform would do — no changes to cloud. apply executes the
plan. Best practice: save the plan (terraform plan -out=tfplan) then apply that exact saved plan
(terraform apply tfplan) so apply executes exactly what was reviewed, not a re-computed plan.

CONSTRAINTS:
- Each concept: exactly one paragraph, 4-6 sentences, no bullets inside paragraphs
- Citi tie-in is the last sentence of each paragraph
- Table: valid GFM pipe table
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.
