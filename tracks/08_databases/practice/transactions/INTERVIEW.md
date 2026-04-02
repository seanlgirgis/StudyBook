# Interview Questions — Transactions

> Topics covered: serializable isolation · write skew · deadlock patterns
> Levels: Starter | Mid | Senior | Architect

---

## Level 1 — Starter

**Q1: In d03_serializable_story.md and c046, what does serializable mean in plain language?**
What a good answer covers:
- Serializable means transactions behave as if they ran one-by-one
- The demo forces an abort when interleaving is unsafe
- A retry is required after a serialization failure
- The rule 'one doctor stays on call' is preserved
Why this is asked: Checks foundational understanding of serializable isolation.

**Q2: In c045, what is write skew using the on-call doctors rule?**
What a good answer covers:
- Two doctors both see two on-call doctors and decide to go off
- Each transaction is locally correct but the global rule breaks
- This happens under REPEATABLE READ snapshot behavior
- The final state shows zero doctors on call
Why this is asked: Tests recognition of write skew in the actual demo.

**Q3: In c047, what is a deadlock?**
What a good answer covers:
- Two transactions each hold a lock the other needs
- The system is stuck in a circular wait
- The database detects the cycle and aborts one transaction
- The demo prints a deadlock error code
Why this is asked: Confirms basic deadlock mechanics from the demo.

**Q4: Why can deadlocks happen even when each transaction looks correct by itself?**
What a good answer covers:
- Each transaction acquires locks in a valid order locally
- The interleaving creates a circular wait across transactions
- Correct local logic does not guarantee global progress
Why this is asked: Probes understanding of concurrency hazards beyond single-transaction logic.

---

## Level 2 — Mid

**Q1: Using c045 and c046, compare REPEATABLE READ to SERIALIZABLE.**
What a good answer covers:
- REPEATABLE READ gives a stable snapshot but allows write skew
- SERIALIZABLE detects unsafe interleavings and aborts one transaction
- The retry loop in c046 resolves the conflict
- The business invariant is preserved only under SERIALIZABLE
Why this is asked: Tests the contrast between snapshot isolation and serializable.

**Q2: How does write skew break business invariants in the on-call doctors demo?**
What a good answer covers:
- The invariant is 'at least one doctor on call'
- Both doctors act on the same snapshot and go off call
- The final state violates the invariant despite correct local checks
Why this is asked: Connects anomalies to real business rules.

**Q3: In c047, how do two transactions deadlock by locking resources in opposite order?**
What a good answer covers:
- T1 locks Resource A then waits for B
- T2 locks Resource B then waits for A
- Both are waiting, creating a circular dependency
- The database resolves it by aborting one transaction
Why this is asked: Checks concrete understanding of the demo's deadlock formation.

**Q4: In c048, why does consistent lock ordering reduce deadlocks?**
What a good answer covers:
- Everyone locks resources in the same order (A then B)
- This removes circular wait conditions
- Transactions may block but do not deadlock
Why this is asked: Validates understanding of prevention via lock ordering.

---

## Level 3 — Senior

**Q1: In c046, how does serializable prevent anomalies and what does it cost?**
What a good answer covers:
- The database aborts a transaction when it cannot serialize safely
- The application retries after a 40001 serialization failure
- Costs include extra retries, higher latency, and lower throughput under contention
Why this is asked: Probes judgment on correctness versus cost tradeoffs.

**Q2: When is deadlock retry necessary even after lock ordering (c049)?**
What a good answer covers:
- Not all deadlocks can be prevented in complex systems
- Lock ordering reduces risk but does not eliminate all cases
- The demo retries after 40P01 deadlock errors
Why this is asked: Tests realistic handling of deadlocks beyond prevention.

**Q3: How do you recognize invariant-sensitive workloads that need stronger isolation?**
What a good answer covers:
- Look for cross-row or cross-entity rules like 'at least one on call'
- Snapshot isolation may allow write skew in these cases
- Serializable or explicit locking is required to enforce invariants
Why this is asked: Evaluates ability to choose isolation level based on business rules.

---

## Level 4 — Architect

**Q1: How would you choose serializable versus weaker isolation in real systems with high concurrency?**
What a good answer covers:
- Serializable for invariant-critical workflows where anomalies are unacceptable
- Weaker isolation for throughput when occasional anomalies are tolerable
- Retries and latency must be budgeted under serializable
- The decision should be guided by business risk and contention patterns
Why this is asked: Tests system-level tradeoffs grounded in the demos.

**Q2: How do deadlock handling and serializable retries interact with worker systems, idempotency, and distributed systems?**
What a good answer covers:
- Both deadlocks and serialization failures require application retries
- Idempotency is needed because retries can re-run work
- Orchestrators must treat these as safe, expected failures
- Distributed systems amplify contention and need clear retry/backoff rules
Why this is asked: Probes cross-system integration and production judgment.

---

## Topic - Transfer Happy Path / Rollback

### Level 1 - Starter

**Q1: In c011_transfer_happy_path.py, what does the transaction guarantee for the two account updates?**
What a good answer covers:
- Both the debit and credit happen inside a single transaction
- Commit makes both changes visible together
- Atomicity means either both updates land or neither does
Why this is asked: Confirms baseline transaction mechanics from the happy path demo.

**Q2: In c011_transfer_happy_path.py, why is the commit placed after both updates?**
What a good answer covers:
- Commit finalizes the full transfer, not a partial step
- Placing commit earlier would risk an inconsistent state
- The demo shows commit as the boundary of correctness
Why this is asked: Checks understanding of commit timing in the demo flow.

**Q3: In c012_transfer_rollback_demo.py, what does rollback do after the simulated failure?**
What a good answer covers:
- It undoes the debit that happened before the error
- It restores the account balances to the pre-transfer state
- It prevents partial updates from becoming visible
Why this is asked: Verifies rollback behavior in the failure demo.

**Q4: In c012_transfer_rollback_demo.py, why does rollback protect correctness when one step fails?**
What a good answer covers:
- The debit happens but the credit never executes
- Rollback erases the partial change
- The final state shows no money lost or created
Why this is asked: Tests the core correctness story of rollback in this track.

### Level 2 - Mid

**Q1: Using d01_domain_setup.md and c011_transfer_happy_path.py, what would go wrong if the debit and credit ran in separate transactions?**
What a good answer covers:
- The system could commit the debit without the credit
- The ledger would show money missing from the total
- Separate transactions break the atomic transfer contract
Why this is asked: Probes understanding of why atomicity is required for a ledger.

**Q2: In c012_transfer_rollback_demo.py, what is a common mistake with error handling that would defeat the rollback?**
What a good answer covers:
- Catching the exception but still committing
- Forgetting to call rollback before closing the session
- Allowing partial state to persist after a failure
Why this is asked: Checks practical error handling pitfalls.

**Q3: In c011_transfer_happy_path.py, how would you validate that the transfer was correct beyond just reading the balances?**
What a good answer covers:
- Verify total balance across accounts is unchanged
- Confirm exactly one debit and one credit occurred
- Compare before/after snapshots printed in the demo
Why this is asked: Tests ability to validate correctness, not just outcomes.

**Q4: In c012_transfer_rollback_demo.py, why is raising the error before the credit a meaningful test of rollback?**
What a good answer covers:
- It forces the worst-case partial update scenario
- It proves rollback erases an already-applied debit
- It mirrors real failures that happen mid-transaction
Why this is asked: Ensures the candidate understands the test design in the demo.

### Level 3 - Senior

**Q1: In c012_transfer_rollback_demo.py, how would you design retries to avoid double-debiting after a rollback?**
What a good answer covers:
- Ensure a retry reruns the full transaction from scratch
- Use idempotency keys or a transfer table to guard repeats
- Only commit when both updates succeed
Why this is asked: Probes failure handling and safe retry design.

**Q2: Using d01_domain_setup.md and c011_transfer_happy_path.py, what edge case appears if two transfers touch the same account concurrently?**
What a good answer covers:
- Competing updates can interleave and lose updates without proper isolation
- A single transaction is not enough if concurrent writers conflict
- Additional locking or isolation may be required for correctness
Why this is asked: Tests awareness of concurrency beyond the single-transaction demo.

**Q3: In c011_transfer_happy_path.py, what design decision would you revisit if balances must never go negative?**
What a good answer covers:
- Add a balance check inside the same transaction as the update
- Ensure the check and update are atomic
- Consider failure behavior when the check fails
Why this is asked: Evaluates handling of business invariants in the transfer flow.

### Level 4 - Architect

**Q1: Using c011_transfer_happy_path.py, how would you integrate this transfer into an orchestration DAG with retries while preserving correctness?**
What a good answer covers:
- The transfer step must be idempotent across retries
- Orchestration retries should re-run the full transaction safely
- Dependencies should avoid partial side effects outside the transaction
Why this is asked: Connects the transfer demo to orchestration and retry design.

**Q2: Using c012_transfer_rollback_demo.py, how would you keep downstream streaming consumers and caches consistent after a rollback?**
What a good answer covers:
- Emit events only after commit to avoid phantom updates
- Use exactly-once or idempotent consumer patterns for delivery
- Invalidate or update caches based on committed state only
Why this is asked: Connects rollback behavior to streaming guarantees and cache consistency.

---

## Topic - Dirty Read / Read Committed / Repeatable Read / Phantom Reads

### Level 1 - Starter

**Q1: In c021_dirty_read_protection_demo.py, what is a dirty read and why does the reader not see it?**
What a good answer covers:
- The writer changes Alice without committing
- The reader still sees the old committed balance
- PostgreSQL blocks dirty reads by default
Why this is asked: Checks basic understanding of dirty reads using the demo.

**Q2: In c022_read_committed_non_repeatable_read_demo.py, what does READ COMMITTED allow the reader to observe?**
What a good answer covers:
- Each query sees the latest committed data
- The same transaction can see different values across reads
- The demo shows Alice changing between reads
Why this is asked: Verifies READ COMMITTED behavior in practice.

**Q3: In c023_repeatable_read_snapshot_demo.py, what does REPEATABLE READ change about the reader's view?**
What a good answer covers:
- The reader sees a frozen snapshot from the first read
- Later commits are not visible inside the transaction
- A new session can see the updated balance
Why this is asked: Confirms snapshot behavior in the repeatable read demo.

**Q4: In c024a_phantom_read_read_committed.py, what is a phantom read in this demo?**
What a good answer covers:
- The second range query returns an extra row (Charlie)
- The new row was inserted and committed by another session
- READ COMMITTED allows new rows to appear mid-transaction
Why this is asked: Tests recognition of phantom reads using the range query demo.

### Level 2 - Mid

**Q1: Using c021_dirty_read_protection_demo.py and c022_read_committed_non_repeatable_read_demo.py, why is blocking dirty reads not enough to prevent non-repeatable reads?**
What a good answer covers:
- Dirty reads are uncommitted data; non-repeatable reads are committed changes
- READ COMMITTED blocks dirty reads but allows changes between queries
- The reader still sees different values across reads in c022
Why this is asked: Probes understanding of isolation level tradeoffs.

**Q2: In c023_repeatable_read_snapshot_demo.py, what tradeoff does the frozen snapshot create?**
What a good answer covers:
- The reader is consistent but may be stale
- Writers can commit while the reader still sees old data
- The fresh verification session shows the new balance
Why this is asked: Tests awareness of consistency vs freshness.

**Q3: In c024a_phantom_read_read_committed.py, what common mistake would make the range query unsafe for business logic?**
What a good answer covers:
- Assuming the result set is stable within a transaction
- Making decisions based on a first query that can change later
- Ignoring the possibility of new rows matching the range
Why this is asked: Checks practical risk recognition for phantom reads.

**Q4: In c024b_phantom_read_repeatable_read.py, why does the reader not see Charlie even after the insert commits?**
What a good answer covers:
- REPEATABLE READ keeps a consistent snapshot
- The snapshot does not include rows inserted after it starts
- A fresh session can see Charlie outside the snapshot
Why this is asked: Verifies repeatable read's effect on phantom rows.

### Level 3 - Senior

**Q1: In c022_read_committed_non_repeatable_read_demo.py, when would READ COMMITTED be the right choice despite non-repeatable reads?**
What a good answer covers:
- When freshness and throughput matter more than repeatable reads
- When the application can tolerate values changing mid-transaction
- When follow-up logic does not require stable reads
Why this is asked: Evaluates isolation selection judgment.

**Q2: Using c023_repeatable_read_snapshot_demo.py and c024b_phantom_read_repeatable_read.py, how would you detect stale reads in a long-running transaction?**
What a good answer covers:
- Recognize that a snapshot can lag behind committed data
- Use a fresh session or separate verification query to compare
- Consider shortening transactions or adding retry logic
Why this is asked: Tests handling of snapshot staleness risks.

**Q3: In c024a_phantom_read_read_committed.py, what failure mode happens if you compute a total from the first range query and then apply an update?**
What a good answer covers:
- A new row can appear, making the computed total incorrect
- The update can violate invariants based on outdated totals
- The demo shows the range changing within one transaction
Why this is asked: Probes edge-case reasoning around phantoms.

### Level 4 - Architect

**Q1: Using c023_repeatable_read_snapshot_demo.py, how would you choose isolation for analytics queries feeding a warehouse track (modeling or analytics) versus OLTP reads?**
What a good answer covers:
- Analytics often prefer consistent snapshots for correctness
- OLTP can favor READ COMMITTED for freshness and throughput
- The repeatable read demo shows the snapshot tradeoff explicitly
Why this is asked: Connects isolation choices to modeling/analytics tracks.

**Q2: Using c024a_phantom_read_read_committed.py, how do phantom reads influence cache or streaming delivery guarantees in other tracks?**
What a good answer covers:
- Changing result sets can cause inconsistent cache fills
- Streaming consumers need idempotency or snapshotting to avoid drift
- Isolation level affects downstream consistency guarantees
Why this is asked: Tests cross-track integration with cache/streaming patterns.

---

## Topic - Retry / Idempotency / Dead Letter Queue / Reliable Worker

### Level 1 - Starter

**Q1: In c041_retry_failure_demo.py, what makes the retry safe after the first failure?**
What a good answer covers:
- The failed attempt is rolled back
- The second attempt re-runs the full transfer
- Commit only happens after both updates succeed
Why this is asked: Confirms basic retry mechanics in the demo.

**Q2: In c042_idempotency_demo.py, what does the processed_requests table protect against?**
What a good answer covers:
- Duplicate request processing
- Double-applying the same transfer
- Ensuring only the first claim runs the update
Why this is asked: Checks understanding of idempotency tracking.

**Q3: In c043_dead_letter_queue_demo.py, what is the dead letter queue used for?**
What a good answer covers:
- Isolating a poison job that keeps failing
- Stopping infinite retries from clogging the main queue
- Preserving error details for later inspection
Why this is asked: Verifies the purpose of DLQs in the demo.

**Q4: In c044_mini_reliable_worker_system.py, what three outcomes does the demo show?**
What a good answer covers:
- Successful jobs move to done
- A duplicate request is skipped via idempotency
- A poison job ends up in the dead letter queue
Why this is asked: Ensures the candidate can read the end-to-end story.

### Level 2 - Mid

**Q1: Using c041_retry_failure_demo.py and c042_idempotency_demo.py, why is rollback alone not enough when retries happen?**
What a good answer covers:
- Rollback prevents partial state in a single attempt
- Retries can re-run a request that already succeeded
- Idempotency prevents double-apply across attempts
Why this is asked: Tests the interaction between retry and idempotency.

**Q2: In c043_dead_letter_queue_demo.py, what mistake would cause the poison job to block the queue?**
What a good answer covers:
- Retrying indefinitely without a max attempt threshold
- Never moving failed jobs out of the main queue
- Failing to record attempt_count and enforce a limit
Why this is asked: Checks common DLQ implementation errors.

**Q3: In c044_mini_reliable_worker_system.py, why is the request_id claimed inside the same transaction as job updates?**
What a good answer covers:
- It keeps idempotency and status changes atomic
- Prevents two workers from both processing the same request
- Ensures duplicates are skipped reliably
Why this is asked: Probes atomicity and race prevention.

**Q4: In c041_retry_failure_demo.py, what tradeoff appears if you increase max_attempts too high?**
What a good answer covers:
- More retries can delay other work
- Persistent failures waste resources
- A DLQ is needed once retries stop being useful
Why this is asked: Tests practical retry policy judgment.

### Level 3 - Senior

**Q1: In c042_idempotency_demo.py, what edge case occurs if the idempotency insert is committed but the transfer fails?**
What a good answer covers:
- The request_id is marked processed without the transfer
- Future retries will skip the real work
- The fix is keeping the claim and transfer in one transaction
Why this is asked: Evaluates awareness of partial-commit hazards.

**Q2: Using c044_mini_reliable_worker_system.py, how would you prevent two workers from starving each other when the queue is hot?**
What a good answer covers:
- Keep transactions short and claim only one job at a time
- Use ordered selection with SKIP LOCKED to avoid blocking
- Commit quickly to release locks
Why this is asked: Tests concurrency design decisions in worker loops.

**Q3: In c043_dead_letter_queue_demo.py, how would you decide which errors should go to DLQ versus retry?**
What a good answer covers:
- Transient errors are retried; permanent errors go to DLQ
- Use error type or attempt count thresholds to decide
- Preserve error context for diagnosis
Why this is asked: Checks failure classification judgment.

### Level 4 - Architect

**Q1: Using c044_mini_reliable_worker_system.py, how would you integrate retries and idempotency with orchestration DAG retries?**
What a good answer covers:
- Orchestration retries must not cause double processing
- Idempotency keys should span task and worker layers
- The worker system should treat retries as safe replays
Why this is asked: Connects reliable workers to orchestration track patterns.

**Q2: Using c042_idempotency_demo.py, how would you extend idempotency across streaming delivery guarantees?**
What a good answer covers:
- At-least-once delivery needs idempotent processing
- Track request IDs or offsets to dedupe work
- Ensure the database write and dedupe marker are atomic
Why this is asked: Tests cross-track integration with streaming guarantees.
