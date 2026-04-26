You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\34_aws_bedrock\

TOPIC: AWS Bedrock for Data Engineers
SLUG: 34_aws_bedrock
PRIORITY: Advanced Cloud NICE
INFRASTRUCTURE: AWS Bedrock concepts + local prompt/request builders; no live model calls required

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

===== FILE 01: 01_bedrock_request_patterns.py =====
PURPOSE: Build model invocation request payloads safely.
COVERS: model IDs, JSON payloads, temperature, max tokens

EXACT FUNCTION SIGNATURES:
    def build_claude_messages_payload(prompt: str, max_tokens: int = 500) -> dict:
    def build_titan_text_payload(prompt: str, max_tokens: int = 500) -> dict:
    def validate_model_request(payload: dict) -> bool:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_prompt_templates_for_data.py =====
PURPOSE: Create prompt templates for data profiling and documentation.
COVERS: prompt structure, grounding, constraints

EXACT FUNCTION SIGNATURES:
    def data_profile_prompt(table_name: str, columns: list[str], stats: dict) -> str:
    def lineage_summary_prompt(job_name: str, inputs: list[str], outputs: list[str]) -> str:
    def quality_explanation_prompt(failed_rules: list[str]) -> str:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_guardrails_and_redaction.py =====
PURPOSE: Redact sensitive data before LLM calls.
COVERS: PII redaction, prompt safety, governance

EXACT FUNCTION SIGNATURES:
    def redact_email(text: str) -> str:
    def redact_account_numbers(text: str) -> str:
    def validate_no_sensitive_tokens(text: str) -> bool:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_response_parsing.py =====
PURPOSE: Parse structured LLM responses safely.
COVERS: JSON parsing, schema checks, fallback handling

EXACT FUNCTION SIGNATURES:
    def parse_json_response(text: str) -> dict:
    def validate_summary_response(response: dict) -> bool:
    def fallback_summary(reason: str) -> dict:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_cost_observability.py =====
PURPOSE: Estimate token cost and track usage.
COVERS: tokens, cost estimation, logging

EXACT FUNCTION SIGNATURES:
    def estimate_tokens(text: str) -> int:
    def estimate_invocation_cost(input_tokens: int, output_tokens: int, price_per_1k_input: float, price_per_1k_output: float) -> float:
    def build_usage_log(model_id: str, input_tokens: int, output_tokens: int) -> dict:

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
CAPSTONE SCENARIO: Design safe LLM-assisted data documentation and quality explanation workflows.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/data_doc_assistant.py ---
EXACT FUNCTION SIGNATURES:
    def build_documentation_prompt(dataset_profile: dict) -> str:
    def redact_profile(profile: dict) -> dict:
    def parse_documentation_response(response_text: str) -> dict:
    def generate_dataset_documentation(profile: dict, response_text: str) -> dict:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert prompts include constraints
- assert redaction removes emails
- assert sensitive-token validator fails on account numbers
- assert JSON parser handles valid JSON
- assert cost estimate is positive and deterministic

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
