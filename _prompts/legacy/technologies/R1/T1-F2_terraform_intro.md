SAVE AS: terraform_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Terraform for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute.

TASK: Generate terraform_intro.ipynb — a Jupyter notebook covering the Terraform mental model,
HCL syntax, state, and a first real infrastructure deployment (AWS S3 bucket as a data lake landing zone).

NOTE: This notebook provisions real AWS resources. Users need an AWS account with CLI configured.
All resources created are free-tier eligible. The notebook cleans up at the end with terraform destroy.

DATASET CONTEXT — do not deviate:
- Citi narrative: the telemetry data pipeline eventually lands in S3 as a data lake.
  Terraform provisions the S3 bucket, IAM role, and KMS key — not done by hand.

TECH STACK CONTEXT — do not deviate:
- Terraform: installed via Chocolatey or from terraform.io/downloads (Windows)
- AWS CLI: configured with aws configure (access key, secret, region us-east-1)
- Terraform project: D:\Workspace\Technologies\citi_terraform\

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Terraform — First Contact"
- 3-paragraph mental model: what IaC is, why not click-ops, Terraform's provider model
  (declarative desired state → plan → apply → state)
- Citi framing: "A new Citi project needs S3 bucket + IAM role + KMS key. A ticket to the cloud
  team takes 2 weeks. With Terraform, a DE provisions it in 10 minutes and it's version-controlled."
- ASCII diagram: [main.tf] → [terraform plan] → [diff: +S3 +IAM +KMS] → [terraform apply] → [AWS Resources]

SECTION 2 — Install Check (code cell + markdown)
- Markdown: "Verify Terraform and AWS CLI are available"
- Code:
  - subprocess.run(["terraform", "version"], ...) → print version
  - subprocess.run(["aws", "sts", "get-caller-identity"], ...) → print account ID and ARN
  - If either fails: print installation instructions and raise RuntimeError

SECTION 3 — Project Structure (code cell + markdown)
- Markdown: H2 "Terraform Project Structure"
  - Explain: main.tf (resources), variables.tf (inputs), outputs.tf (outputs), terraform.tfvars (values)
- Code: create directory D:\Workspace\Technologies\citi_terraform\ and print tree

SECTION 4 — Write Terraform Files (code cell)
- Write 4 files to D:\Workspace\Technologies\citi_terraform\:

  versions.tf:
  ```hcl
  terraform {
    required_version = ">= 1.5"
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
  }

  provider "aws" {
    region = var.aws_region
  }
  ```

  variables.tf:
  ```hcl
  variable "aws_region" {
    description = "AWS region to deploy into"
    type        = string
    default     = "us-east-1"
  }

  variable "project_name" {
    description = "Project prefix for all resource names"
    type        = string
    default     = "citi-telemetry"
  }

  variable "environment" {
    description = "Environment tag (dev/staging/prod)"
    type        = string
    default     = "dev"
  }
  ```

  main.tf:
  ```hcl
  # S3 bucket — data lake landing zone
  resource "aws_s3_bucket" "data_lake" {
    bucket = "${var.project_name}-data-lake-${var.environment}-${data.aws_caller_identity.current.account_id}"
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }

  resource "aws_s3_bucket_versioning" "data_lake" {
    bucket = aws_s3_bucket.data_lake.id
    versioning_configuration {
      status = "Enabled"
    }
  }

  resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
    bucket = aws_s3_bucket.data_lake.id
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  resource "aws_s3_bucket_public_access_block" "data_lake" {
    bucket                  = aws_s3_bucket.data_lake.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }

  data "aws_caller_identity" "current" {}
  ```

  outputs.tf:
  ```hcl
  output "bucket_name" {
    description = "Name of the data lake S3 bucket"
    value       = aws_s3_bucket.data_lake.bucket
  }

  output "bucket_arn" {
    description = "ARN of the data lake S3 bucket"
    value       = aws_s3_bucket.data_lake.arn
  }
  ```

- Print "Terraform files written to citi_terraform/"

SECTION 5 — terraform init (code cell + markdown)
- Markdown: "terraform init downloads providers and sets up the backend"
- Code: subprocess.run(["terraform", "init"], cwd="D:/Workspace/Technologies/citi_terraform", ...)
  Print stdout. Confirm "Terraform has been successfully initialized!"

SECTION 6 — terraform plan (code cell + markdown)
- Markdown: H2 "terraform plan — the diff before you commit"
  - Explain: plan shows exactly what will be created/changed/destroyed, no changes made
- Code: subprocess.run(["terraform", "plan", "-out=tfplan"], cwd=..., ...)
  Print stdout — shows "+3 to add, 0 to change, 0 to destroy"

SECTION 7 — terraform apply (code cell + markdown)
- Markdown: H2 "terraform apply — provision the infrastructure"
  - Note: this creates real AWS resources (S3 bucket). Free tier. Destroyed at end of notebook.
- Code: subprocess.run(["terraform", "apply", "tfplan"], cwd=..., ...)
  Print stdout. Parse outputs: subprocess.run(["terraform", "output", "-json"], ...)
  Print: f"Bucket created: {outputs['bucket_name']['value']}"

SECTION 8 — Terraform State (markdown cell)
- H2: "Terraform State — why it matters"
- Cover: terraform.tfstate file records the mapping between HCL resources and real cloud resources,
  plan computes diff against state (not against live cloud), remote state (S3 + DynamoDB lock) for teams,
  never delete or edit state manually, state drift when someone changes infra outside Terraform.
- Key commands:
  - terraform state list — show all tracked resources
  - terraform state show aws_s3_bucket.data_lake — inspect a resource
  - terraform import — bring existing resource under Terraform management

SECTION 9 — State List (code cell)
- Code: subprocess.run(["terraform", "state", "list"], cwd=..., ...) → print resource names
  subprocess.run(["terraform", "state", "show", "aws_s3_bucket.data_lake"], cwd=..., ...) → print

SECTION 10 — Verify in AWS (code cell + markdown)
- Markdown: "Confirm the bucket exists in AWS"
- Code: subprocess.run(["aws", "s3", "ls"], ...) → print output showing the new bucket

SECTION 11 — terraform destroy (code cell + markdown)
- Markdown: H2 "Clean Up — terraform destroy"
  - IMPORTANT: always destroy learning resources to avoid AWS charges
- Code: subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=..., ...)
  Print stdout. Confirm "Destroy complete! Resources: 4 destroyed."

SECTION 12 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: IaC mental model, wrote 4 HCL files, init/plan/apply cycle, state management,
  bucket in AWS confirmed, destroyed cleanly
- Citi tie-in: "In a real Citi project, main.tf provisions the entire data platform:
  S3 buckets, Glue catalog, IAM roles, EMR cluster, VPC. One PR = full environment."
- Next: "Run infra_concepts.md for K8s + Terraform + IaC vocabulary."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- All subprocess calls: capture_output=True, text=True, cwd set to citi_terraform/ where needed
- Section 11 (destroy) must be the last code cell — never leave resources running
- Section 2 must handle missing terraform/aws gracefully
- No hardcoded AWS account IDs

ACCEPTANCE: Sections 5-11 execute against a real AWS account. Bucket created and destroyed.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

