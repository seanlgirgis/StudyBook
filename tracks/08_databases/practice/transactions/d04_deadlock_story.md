# Deadlocks — Story Map

## Story
Two workers need two tools. Each grabs one tool first, then both reach for the other.

## Scenario
T1 locks A → wants B  
T2 locks B → wants A  

Both are waiting. No one can move.

## Failure
This is a deadlock: a circular wait.
Each transaction holds a lock the other needs.

## Detection
The database detects the cycle and kills one transaction.
That is the only way progress can continue.

## Fix
Use consistent lock ordering:
Everyone locks A, then B.

## Pattern
- Keep transactions short.
- Always lock resources in a predictable order.

## Production Reality
- Deadlocks are normal in concurrent systems.
- The database resolves them by killing one transaction.
- Applications must retry when that happens.

Deadlock handling pattern:
- detect (40P01)
- rollback
- retry

## Deeper System Model
Deadlock requires:
- mutual exclusion
- hold and wait
- no preemption
- circular wait

Mental model:
Deadlock = cycle in wait graph

## System
Deadlocks are progress failures, not correctness failures.
Serializable aborts for **correctness**.
Deadlock aborts for **progress**.

## Run Order
1. c047_deadlock_demo.py
2. c048_deadlock_fix_ordering.py
3. c049_deadlock_retry_pattern.py
