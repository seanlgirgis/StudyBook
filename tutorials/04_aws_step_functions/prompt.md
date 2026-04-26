# ChatGPT Prompt — AWS Step Functions Tutorial
# Paste everything between the === markers into ChatGPT

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Each file must be production-quality, heavily commented,
and fully runnable.

TOPIC: AWS Step Functions for Data Engineers
SLUG: aws-step-functions
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: AWS (boto3, real AWS account)

===== CODING STANDARDS =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : AWS Step Functions
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install boto3 | AWS credentials configured | IAM role for Step Functions
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. Explain ASL (Amazon States Language) concepts inline.
Always include cleanup() functions — Step Functions state machines have no free tier.

===== FILES TO GENERATE =====

01_state_machine_basics.py
  Purpose: Create and execute Step Functions state machines — Pass, Wait, Succeed, Fail states
  Key concepts: ASL definition, state types, execution, polling for completion
  Functions:
    - create_state_machine(name, definition_dict, role_arn) — create from ASL dict
    - start_execution(state_machine_arn, input_dict, execution_name) — start and return ARN
    - wait_for_completion(execution_arn, poll_interval=5, timeout=300) — poll until done
    - get_execution_history(execution_arn) — show state transitions
    - delete_state_machine(arn) — cleanup
  Main block: create Pass→Succeed machine, execute, show history, cleanup

02_task_states_and_lambda.py
  Purpose: Task states — integrate with Lambda, handle timeouts and heartbeats
  Key concepts: Task state, Lambda integration (.sync vs .sync:2), TimeoutSeconds, HeartbeatSeconds
  Functions:
    - build_lambda_task_state(lambda_arn, timeout_s, heartbeat_s) — generate ASL task state dict
    - create_pipeline_with_lambda(name, role_arn, lambda_arns) — multi-step Lambda pipeline
    - demonstrate_sync_patterns() — show .sync vs .sync:2 integration patterns
    - handle_lambda_errors(state_machine_arn) — show error output from failed execution
  Main block: build a 3-step data pipeline state machine definition (no real Lambda needed — use mock)

03_parallel_and_map_states.py
  Purpose: Fan-out with Parallel and Map states — process collections concurrently
  Key concepts: Parallel branches, Map state over array, MaxConcurrency, ResultSelector
  Functions:
    - build_parallel_state(branch_definitions) — run multiple branches simultaneously
    - build_map_state(iterator_definition, max_concurrency) — process each item in array
    - demonstrate_parallel_etl() — ASL for: parallel extract from 3 sources, merge results
    - demonstrate_map_processing() — ASL for: process array of S3 files with Map state
    - compare_parallel_vs_map() — explain when to use each with concrete examples
  Main block: show both ASL definitions, explain output structure

04_error_handling_and_retry.py
  Purpose: Production error handling — Catch, Retry, compensating transactions
  Key concepts: Retry with exponential backoff, Catch by error type, ResultPath, compensate
  Functions:
    - build_retry_config(max_attempts, interval_s, backoff_rate, error_types) — retry dict
    - build_catch_clause(error_types, next_state, result_path) — catch clause dict
    - create_resilient_pipeline(name, role_arn) — state machine with retry and catch
    - demonstrate_compensation_pattern() — on failure, trigger cleanup/rollback branch
    - simulate_failure_and_recovery(state_machine_arn) — run with bad input, show catch firing
  Main block: build resilient pipeline ASL, explain each retry/catch decision

05_express_workflows_and_cost.py
  Purpose: Standard vs Express workflows — when to use each, cost model, high-volume patterns
  Key concepts: Standard (exactly-once, auditable) vs Express (at-least-once, high-throughput, cheaper)
  Functions:
    - calculate_standard_cost(n_state_transitions) — price per 1000 transitions
    - calculate_express_cost(n_executions, avg_duration_ms, avg_memory_gb) — price formula
    - recommend_workflow_type(executions_per_day, requires_exactly_once, max_duration_s) — decision
    - create_express_workflow(name, role_arn, definition) — Express type state machine
    - show_execution_difference() — Standard has execution history, Express does not
  Main block: run cost calculator for 3 scenarios, show recommendation

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Data Pipeline Orchestrator
  Scenario: Build a Step Functions state machine that orchestrates a multi-step
    data pipeline: validate input → trigger Glue job (simulated) → check output
    → send SNS notification on success or failure.
  What to build:
    - State machine with: ValidateInput → StartGlueJob → WaitForGlue (polling loop)
      → ValidateOutput → NotifySuccess / NotifyFailure
    - Polling loop: use Wait + Lambda check pattern (simulate with Pass states)
    - Error handling: Retry on transient errors, Catch on validation failure → NotifyFailure
    - Cost estimate: calculate for 100 daily executions
  Acceptance criteria:
    - State machine creates and executes successfully
    - Failure path triggers correctly when input is invalid
    - Cost estimate printed for both Standard and Express options

capstone/capstone.py — build, execute, monitor, cleanup
capstone/test_capstone.py — test ASL generation functions, mock boto3

===== INFRASTRUCTURE NOTES =====

AWS account required. Step Functions needs an IAM role.
STEP_FUNCTIONS_ROLE_ARN must be set in environment.
Standard workflow pricing: $0.025 per 1000 state transitions.
Express workflow pricing: $1.00 per 1M requests + duration.
Always delete test state machines in cleanup() — no ongoing cost but clean hygiene.
Use us-east-1 as default region.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
