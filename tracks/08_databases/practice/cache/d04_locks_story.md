# Cache Locks — Story Map

## 1. Story (one key to the supply closet)
There is one key to the supply closet. If two people grab it at once, supplies vanish or double-count. One key means one person at a time.

## 2. Core Concepts (street version)
- Lock = only one actor in the critical section.
- Cache work often happens around shared state.
- Coordination beats chaos.

## 3. What A Lock Is
A guardrail that lets one thread mutate shared state while others wait.

## 4. Why Cache Systems Use Locks
Rebuilds, refreshes, and counters are shared. Locks prevent races and duplicate work.

## 5. What Goes Wrong Without A Lock
Two threads read the same value, both update, one overwrites the other. You get wrong totals or double rebuilds.

## 6. What A Lock Fixes
It serializes the critical section so updates happen once and in order.

## 7. What A Lock Does NOT Fix
Locks do not make work faster. Overuse causes waiting and reduces throughput.

## 8. Final Mental Model
One key, one person inside the closet.

## 9. Run Order
1. c073_locks_demo.py
