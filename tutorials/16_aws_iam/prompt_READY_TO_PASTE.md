You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\16_aws_iam\

TOPIC: AWS IAM for Data Engineers
SLUG: 16_aws_iam
PRIORITY: Capital One SHOULD / AWS Security
INFRASTRUCTURE: AWS account + boto3; must support dry-run/mocked conceptual mode where possible

============================================================
CODING STANDARDS — MANDATORY
============================================================

- Python 3.11+ compatible.
- Use type hints on every function.
- Use f-strings.
- Prefer small, testable functions.
- Avoid hidden global state except clear constants.
- No notebooks.
- No TODO, no pass, no placeholder implementation.
- Every generated file must be complete and runnable.
- Keep examples realistic for Data Engineering interviews.
- Use deterministic seeds for generated data.
- Do not require paid/cloud resources in unit tests unless explicitly called out.


============================================================
README REQUIREMENTS — MANDATORY
============================================================

Generate TWO README files for every topic.

1. Main `README.md` at the topic root.

The main README must be professional, interview-oriented, and include:

- `# <Topic Name>`
- `## What This Covers`
- `## Why This Matters in Interviews`
- `## Key Concepts`
- `## Hands-On Walkthrough`
  - Explain each generated tutorial file in order.
  - Explain what the learner should run and what output means.
- `## Common Interview Questions`
  - Include 8 to 12 practical interview questions.
  - Include strong answer guidance after each question.
- `## Deep Dive Talking Points`
  - Senior-level details, tradeoffs, edge cases, and production concerns.
- `## How This Shows Up in Production`
- `## Commands`
  - Include exact PowerShell commands to install dependencies and run tests.
- `## What To Say In An Interview`
  - Include a 60-90 second spoken explanation.

2. Capstone `capstone/README.md`.

The capstone README must be system-design and interview-story oriented, and include:

- `# Capstone: <Name>`
- `## Scenario`
- `## Architecture Overview`
  - Describe the architecture in words.
- `## Data Flow`
- `## Design Decisions`
- `## Tradeoffs`
- `## Scaling Considerations`
- `## Failure Modes`
- `## Security / Governance Notes`
- `## Interview Questions`
  - Include 8 to 12 scenario-based questions with answer guidance.
- `## How To Explain This Capstone In An Interview`
  - Include a step-by-step narrative.

The README files are not optional. Generate them before the capstone code if requested.


============================================================
TEACHING CODE REQUIREMENTS — MANDATORY
============================================================

Every Python file must include:

1. A file header docstring:

```
"""
FILE: <filename>
TOPIC: <topic>
PURPOSE: <what this file teaches>
COVERS: <concept list>
INTERVIEW FOCUS: <what to say in an interview>
"""
```

2. Teachable comments.

Comments must explain WHY, not just WHAT. Include comments like:

```
# INTERVIEW TIP:
# In an interview, emphasize that this step protects downstream consumers
# from schema drift and silent data quality failures.
```

3. Learning-oriented print statements.

Each script should print:
- What it is doing
- Why the step matters
- What interview concept the learner should remember

4. `main()` function.

Every tutorial file must have a runnable `main()` and:

```
if __name__ == "__main__":
    main()
```

5. Tests must validate business behavior, not just file existence.

Use deterministic sample data and exact assertions where possible.


============================================================
AWS CLEANUP RULES — MANDATORY FOR THIS TOPIC
============================================================

For any file that creates AWS resources:

- Use `AWS_PROFILE = os.getenv("AWS_PROFILE", "study")`
- Use `AWS_REGION = os.getenv("AWS_REGION", "us-east-1")`
- Use unique resource names with a short uuid suffix.
- Print a visible warning immediately after creating billable resources:
  `⚠️ COST WARNING: <resource> is billable until deleted.`
- Wrap resource creation and demo logic in `try/finally`.
- Call cleanup from `finally`.
- Cleanup must be idempotent and tolerate already-deleted resources.
- Print exactly:
  `✅ Cleanup complete. No ongoing charges.`
  as the last cleanup message.
- Optional AWS integrations must be gated by environment variables and must not crash when unset.
- Capstone tests should not require live AWS unless explicitly stated; prefer local builders, policy JSON, or mocked behavior.

============================================================
TUTORIAL FILES TO GENERATE
============================================================
Generate these files in order. For each file, include the exact functions listed. You may add helper functions only if they are useful and fully implemented.

===== FILE 01: 01_iam_policy_documents.py =====
PURPOSE: Build and validate IAM policy documents as Python dictionaries.
COVERS: least privilege, IAM JSON, actions/resources/conditions

EXACT FUNCTION SIGNATURES:
    def build_s3_read_only_policy(bucket_name: str, prefix: str) -> dict:
    def build_cloudwatch_logs_policy(log_group_arn: str) -> dict:
    def validate_policy_structure(policy: dict) -> bool:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_roles_and_trust_policies.py =====
PURPOSE: Create trust policies and explain role assumption.
COVERS: trust policy principals, sts:AssumeRole, external IDs

EXACT FUNCTION SIGNATURES:
    def build_assume_role_trust_policy(service_principal: str) -> dict:
    def build_cross_account_trust_policy(account_id: str, external_id: str) -> dict:
    def explain_trust_policy(policy: dict) -> list[str]:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_permission_boundaries.py =====
PURPOSE: Demonstrate permission boundaries and guardrails.
COVERS: permission boundaries, explicit deny, blast radius

EXACT FUNCTION SIGNATURES:
    def build_permission_boundary(allowed_services: list[str]) -> dict:
    def build_explicit_deny_policy(denied_actions: list[str]) -> dict:
    def evaluate_action_against_policy(action: str, policy: dict) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_sts_assume_role_demo.py =====
PURPOSE: Assume a role with STS when environment variables are configured.
COVERS: STS, temporary credentials, safe skipping

EXACT FUNCTION SIGNATURES:
    def get_sts_client(profile_name: str | None = None):
    def assume_role(role_arn: str, session_name: str, external_id: str | None = None) -> dict:
    def print_caller_identity() -> dict:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_iam_audit_report.py =====
PURPOSE: Generate a local IAM audit-style report from sample policies.
COVERS: audit findings, wildcard detection, over-permissioned policies

EXACT FUNCTION SIGNATURES:
    def find_wildcard_actions(policy: dict) -> list[str]:
    def find_wildcard_resources(policy: dict) -> list[str]:
    def score_policy_risk(policy: dict) -> dict[str, int | str]:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 06: README.md =====
Generate the main tutorial README using the mandatory README requirements above.

============================================================
CAPSTONE REQUIREMENTS
============================================================
CAPSTONE SCENARIO: Design least-privilege IAM permissions for a data pipeline that reads S3, writes CloudWatch logs, and assumes a processing role.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/iam_design.py ---
EXACT FUNCTION SIGNATURES:
    def build_data_pipeline_role_policy(bucket_name: str, prefix: str, log_group_arn: str) -> dict:
    def build_data_pipeline_trust_policy(service_principal: str) -> dict:
    def audit_pipeline_policy(policy: dict) -> dict[str, object]:
    def export_policy_bundle(output_dir: str, bucket_name: str, prefix: str, log_group_arn: str) -> list[str]:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert no Action is '*'
- assert no Resource is '*' in final capstone policy
- assert policy has S3 read and CloudWatch log permissions
- assert trust policy allows sts:AssumeRole
- assert audit risk is low

Additional testing requirements:
- Use deterministic fixtures.
- Assert exact values where possible.
- Test edge cases and failure modes.
- Tests must run with `pytest capstone/test_capstone.py -v` from the topic folder unless the topic README specifies otherwise.

============================================================
GENERATION INSTRUCTIONS
============================================================

Generate ONE file at a time.

When first given this prompt, acknowledge the topic and wait.
When the user says `generate file 01`, generate only FILE 01.
When the user says `next`, generate the next file.
After tutorial files, generate README.md.
Then generate capstone/brief.md, capstone/README.md, capstone code files, and capstone/test_capstone.py.

Do not skip README files.
Do not combine multiple files unless explicitly asked.
Do not use placeholders.
Do not say "left as an exercise".
Do not omit imports.
