# AWS IAM for Data Engineers

## What This Covers
This tutorial teaches how to design, evaluate, and explain AWS Identity and Access Management (IAM) for data engineering workloads.

You will learn how to:
- Build least-privilege IAM policies
- Understand trust policies and role assumption
- Apply permission boundaries and guardrails
- Use STS for temporary credentials
- Audit IAM policies for risk

---

## Why This Matters in Interviews
IAM is one of the most common weak areas in data engineering interviews.

Strong candidates:
- Avoid over-permissioned roles
- Explain least privilege clearly
- Understand cross-account access
- Know how pipelines securely access AWS services

Weak candidates:
- Use `"*"` everywhere
- Confuse trust vs permission policies
- Cannot explain STS or role assumption

---

## Key Concepts

### 1. Least Privilege
Grant only the exact actions and resources required.

Example:
- Good: `s3:GetObject` on a specific prefix
- Bad: `s3:*` on `*`

---

### 2. IAM Policy Structure
Every policy includes:
- `Effect`: Allow or Deny
- `Action`: What can be done
- `Resource`: Where it applies
- `Condition` (optional): Constraints

---

### 3. Trust vs Permission Policies
- **Trust Policy** → Who can assume the role
- **Permission Policy** → What the role can do

---

### 4. STS (Temporary Credentials)
Instead of static keys:
- Use `sts:AssumeRole`
- Credentials expire automatically
- Safer for pipelines and production systems

---

### 5. Permission Boundaries
- Define the **maximum allowed permissions**
- Prevent privilege escalation

---

### 6. Explicit Deny
- Always overrides Allow
- Used for hard guardrails

---

### 7. IAM Auditing
Look for:
- `Action: "*"`
- `Resource: "*"`
- Overly broad service access like `s3:*`

---

## Hands-On Walkthrough

### File 01 — `01_iam_policy_documents.py`
Build and validate IAM policies.

Run:
```powershell
python .\01_iam_policy_documents.py
````

Learn:

* S3 prefix-level access
* CloudWatch log scoping
* Policy structure validation

---

### File 02 — `02_roles_and_trust_policies.py`

Create trust policies.

Run:

```powershell
python .\02_roles_and_trust_policies.py
```

Learn:

* Service roles (Glue, Lambda)
* Cross-account access
* External ID usage

---

### File 03 — `03_permission_boundaries.py`

Understand guardrails.

Run:

```powershell
python .\03_permission_boundaries.py
```

Learn:

* Permission boundaries vs policies
* Explicit deny behavior
* IAM evaluation logic

---

### File 04 — `04_sts_assume_role_demo.py`

Use STS.

Run:

```powershell
python .\04_sts_assume_role_demo.py
```

Optional:

```powershell
$env:STUDYBOOK_ASSUME_ROLE_ARN="your-role-arn"
python .\04_sts_assume_role_demo.py
```

Learn:

* Caller identity
* Temporary credentials
* Role assumption flow

---

### File 05 — `05_iam_audit_report.py`

Audit policies.

Run:

```powershell
python .\05_iam_audit_report.py
```

Learn:

* Detect wildcard risks
* Score IAM policies
* Communicate findings

---

## Common Interview Questions

### 1. What is least privilege in IAM?

**Answer:** Grant only the minimum permissions required for a task, scoped by action, resource, and conditions.

---

### 2. What is the difference between trust and permission policies?

**Answer:** Trust policies define who can assume a role; permission policies define what the role can do.

---

### 3. Why use STS instead of access keys?

**Answer:** STS provides temporary credentials that expire, reducing risk and improving security.

---

### 4. What is the confused deputy problem?

**Answer:** When a third party misuses permissions; solved using external IDs in trust policies.

---

### 5. What does explicit deny do?

**Answer:** Overrides all allows and prevents specific actions regardless of other permissions.

---

### 6. What are permission boundaries?

**Answer:** They limit the maximum permissions a role can have, even if additional policies are attached.

---

### 7. Why is `Resource: "*"` dangerous?

**Answer:** It allows access across all resources, increasing blast radius.

---

### 8. Is `arn:aws:s3:::bucket/prefix/*` safe?

**Answer:** Yes, it is a common least-privilege pattern for object-level access.

---

### 9. How do you secure cross-account access?

**Answer:** Use trust policies with specific principals and external IDs.

---

### 10. How would you audit IAM policies?

**Answer:** Look for wildcards, excessive permissions, unused actions, and lack of conditions.

---

## Deep Dive Talking Points

* IAM evaluation order:

  1. Explicit Deny
  2. Allow
  3. Default Deny

* S3 nuance:

  * `ListBucket` applies to bucket
  * `GetObject` applies to objects

* Temporary credentials:

  * Required for production pipelines
  * Reduce credential leakage risk

* Logging permissions:

  * Should be scoped to specific log groups

* Cross-account patterns:

  * Centralized data lake architectures
  * Vendor integrations

---

## How This Shows Up in Production

* Airflow / Spark jobs assume roles
* ETL pipelines read/write S3 securely
* Logging to CloudWatch is restricted
* Cross-account data sharing is controlled
* IAM audits prevent over-permissioned roles

---

## Commands

### Install dependencies

```powershell
pip install boto3 pytest
```

### Run tutorial files

```powershell
python .\01_iam_policy_documents.py
python .\02_roles_and_trust_policies.py
python .\03_permission_boundaries.py
python .\04_sts_assume_role_demo.py
python .\05_iam_audit_report.py
```

---

## What To Say In An Interview (60–90 seconds)

"I design IAM policies using least privilege by scoping actions and resources as tightly as possible. For example, I restrict S3 access to specific prefixes rather than entire buckets.

I separate trust policies from permission policies, ensuring only the correct services or accounts can assume roles. For cross-account access, I use external IDs to prevent confused deputy issues.

In production pipelines, I rely on STS to generate temporary credentials instead of long-lived keys. I also use permission boundaries and explicit deny policies to enforce guardrails and prevent privilege escalation.

Finally, I regularly audit IAM policies for wildcard usage and overly broad access to reduce blast radius and improve security posture."

