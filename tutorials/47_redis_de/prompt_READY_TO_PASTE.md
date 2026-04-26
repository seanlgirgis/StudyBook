You are generating a self-directed Data Engineering interview-prep tutorial.

The output must be COMPLETE, FULLY RUNNABLE, and TEACHABLE. Do not create placeholders, TODOs, ellipses, `pass`, or intentionally incomplete code. Generate one file at a time and wait for the user to say "next".

All files must be written as if they will be saved under:
D:\Workarea\StudyBook\tutorials\47_redis_de\

TOPIC: Redis for Data Engineers
SLUG: 47_redis_de
PRIORITY: Advanced Cloud NICE
INFRASTRUCTURE: Pure Python dict fallback; redis package optional; no live Redis required by tests

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
TUTORIAL FILES TO GENERATE
============================================================
Generate these files in order. For each file, include the exact functions listed. You may add helper functions only if they are useful and fully implemented.

===== FILE 01: 01_cache_patterns.py =====
PURPOSE: Teach cache-aside and TTL patterns.
COVERS: cache hits/misses, TTL, invalidation

EXACT FUNCTION SIGNATURES:
    def cache_key(namespace: str, identifier: str) -> str:
    def get_or_compute(cache: dict, key: str, compute_fn) -> dict:
    def set_with_ttl(cache: dict, key: str, value: object, ttl_seconds: int) -> dict:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 02: 02_idempotency_keys.py =====
PURPOSE: Use Redis-like keys to prevent duplicate processing.
COVERS: SETNX, idempotency, replay safety

EXACT FUNCTION SIGNATURES:
    def idempotency_key(event_id: str) -> str:
    def claim_event(cache: dict, event_id: str) -> bool:
    def mark_event_complete(cache: dict, event_id: str) -> None:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 03: 03_counters_rate_limits.py =====
PURPOSE: Implement counters and simple rate limits.
COVERS: INCR, windows, throttling

EXACT FUNCTION SIGNATURES:
    def increment_counter(cache: dict, key: str) -> int:
    def fixed_window_rate_limit(cache: dict, actor: str, limit: int, window_id: str) -> bool:
    def counter_report(cache: dict, prefix: str) -> dict[str, int]:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 04: 04_queues_streams_concepts.py =====
PURPOSE: Teach queues and stream-like patterns.
COVERS: lists, streams, consumer groups concepts

EXACT FUNCTION SIGNATURES:
    def enqueue_job(queue: list[dict], job: dict) -> int:
    def dequeue_job(queue: list[dict]) -> dict | None:
    def build_stream_event(event_type: str, payload: dict) -> dict:

REQUIREMENTS:
- Include the mandatory file header.
- Include teachable comments and at least two `INTERVIEW TIP` comments.
- Include deterministic demo data or safe local defaults.
- Include a `main()` that demonstrates the functions and prints learning output.
- The script must run directly from the topic folder.

===== FILE 05: 05_operational_tradeoffs.py =====
PURPOSE: Explain persistence, eviction, clustering, and risks.
COVERS: RDB/AOF, eviction, memory, hot keys

EXACT FUNCTION SIGNATURES:
    def recommend_eviction_policy(use_case: str) -> str:
    def estimate_memory_mb(item_count: int, avg_item_kb: float) -> float:
    def detect_hot_keys(access_counts: dict[str, int], threshold_pct: float) -> list[str]:

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
CAPSTONE SCENARIO: Use Redis patterns for caching, idempotency, counters, and lightweight pipeline coordination.

--- capstone/brief.md ---
Write a concise business scenario, learner tasks, expected deliverables, and success criteria.

--- capstone/README.md ---
Generate the capstone README using the mandatory capstone README requirements above.

--- capstone/redis_pipeline_coordinator.py ---
EXACT FUNCTION SIGNATURES:
    def create_pipeline_cache() -> dict:
    def claim_pipeline_event(cache: dict, event_id: str) -> bool:
    def cache_dimension_lookup(cache: dict, dimension_key: str, value: dict) -> dict:
    def record_pipeline_metric(cache: dict, metric_name: str) -> int:
    def pipeline_cache_report(cache: dict) -> dict[str, object]:
REQUIREMENTS:
- Must be runnable and importable.
- Must include interview-focused comments.
- Must use deterministic inputs for local testing.

--- capstone/test_capstone.py ---
Create pytest tests with these exact business expectations:
- assert cache key includes namespace
- assert duplicate event cannot be claimed twice
- assert counter increments exactly
- assert rate limit blocks above threshold
- assert hot key detection catches skew

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
