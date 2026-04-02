# Transactions Practice Capstone Map

## What This Module Teaches
This module walks from basic transaction safety to production-grade reliability patterns. You learn how to protect data from partial updates, how isolation levels behave, how queues are claimed safely, and how to handle retries, idempotency, and poison jobs without losing correctness.

## Ordered File List (c001–c044)
- c001_setup_schema.py: Create the baseline tables used by the transaction demos.
- c002_reset_demo_data.py: Reset demo data to a known starting state.
- c003_show_current_state.py: Print current database state for quick inspection.
- c011_transfer_happy_path.py: Show a successful transfer committed end-to-end.
- c012_transfer_rollback_demo.py: Show a failed transfer that rolls back safely.
- c021_dirty_read_protection_demo.py: Show dirty reads being blocked by isolation.
- c022_read_committed_non_repeatable_read_demo.py: Demonstrate non-repeatable reads under READ COMMITTED.
- c023_repeatable_read_snapshot_demo.py: Show snapshot behavior under REPEATABLE READ.
- c024a_phantom_read_read_committed.py: Show phantom reads under READ COMMITTED.
- c024b_phantom_read_repeatable_read.py: Show phantom read behavior under REPEATABLE READ.
- c031_row_locking_select_for_update.py: Demonstrate row-level locks with SELECT FOR UPDATE.
- c032_job_queue_skip_locked.py: Demonstrate queue claiming with SKIP LOCKED.
- c041_retry_failure_demo.py: Demonstrate retry logic after a failed transaction.
- c042_idempotency_demo.py: Demonstrate idempotency and duplicate protection.
- c043_dead_letter_queue_demo.py: Demonstrate bounded retries and dead letter queue pattern.
- c044_mini_reliable_worker_system.py: Combine queue claiming, retries, idempotency, and DLQ.

## Concept Ladder
- Commit: make a transaction’s changes permanent.
- Rollback: erase a failed attempt and return to a clean state.
- Dirty read protection: prevent reading uncommitted data.
- Non-repeatable read: same query returns different results in one transaction.
- Repeatable read: keep a stable snapshot during a transaction.
- Phantom read: new rows appear between repeated queries.
- Row locking: block concurrent updates on specific rows.
- Skip locked: let multiple workers claim different jobs safely.
- Retry: re-attempt work after failure without corrupting state.
- Idempotency: duplicates do not apply the same change twice.
- DLQ: remove poison jobs after bounded retries.
- Mini reliable worker system: combine the patterns into one flow.

## Recommended Study Order
1. c001_setup_schema.py
2. c002_reset_demo_data.py
3. c003_show_current_state.py
4. c011_transfer_happy_path.py
5. c012_transfer_rollback_demo.py
6. c021_dirty_read_protection_demo.py
7. c022_read_committed_non_repeatable_read_demo.py
8. c023_repeatable_read_snapshot_demo.py
9. c024a_phantom_read_read_committed.py
10. c024b_phantom_read_repeatable_read.py
11. c031_row_locking_select_for_update.py
12. c032_job_queue_skip_locked.py
13. c041_retry_failure_demo.py
14. c042_idempotency_demo.py
15. c043_dead_letter_queue_demo.py
16. c044_mini_reliable_worker_system.py

## Foundational vs Advanced
Foundational:
- c001_setup_schema.py
- c002_reset_demo_data.py
- c003_show_current_state.py
- c011_transfer_happy_path.py
- c012_transfer_rollback_demo.py
- c021_dirty_read_protection_demo.py
- c022_read_committed_non_repeatable_read_demo.py
- c023_repeatable_read_snapshot_demo.py
- c024a_phantom_read_read_committed.py
- c024b_phantom_read_repeatable_read.py

Advanced:
- c031_row_locking_select_for_update.py
- c032_job_queue_skip_locked.py
- c041_retry_failure_demo.py
- c042_idempotency_demo.py
- c043_dead_letter_queue_demo.py
- c044_mini_reliable_worker_system.py

## What To Review Before Interviews
- When to commit vs rollback, and why partial updates are dangerous.
- The differences between READ COMMITTED and REPEATABLE READ.
- How SELECT FOR UPDATE and SKIP LOCKED enable safe queue processing.
- Why retries need idempotency, and how DLQs stop poison jobs.

## What Maps Directly To Data Engineering Systems
- Queue claiming with SKIP LOCKED maps to job runners and schedulers.
- Retry + idempotency maps to safe reprocessing in batch pipelines.
- DLQ maps to error isolation in streaming and workflow engines.
- Isolation level tradeoffs show up in analytics vs OLTP choices.
