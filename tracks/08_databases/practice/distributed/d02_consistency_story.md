# Distributed Consistency — Story Map

## 1. Story (multiple menu boards in different rooms)
A restaurant has menu boards in every room. The kitchen changes one board, but the runners update the others later. For a while, different rooms show different prices.

## 2. Core Concepts (street version)
- Replicas = multiple copies of the same data.
- Writes land on one copy first.
- Other copies catch up after a delay.

## 3. What consistency means
How quickly and reliably those copies agree after a change.

## 4. Strong vs eventual consistency
Strong: every read sees the latest write (needs coordination, slower).
Eventual: reads might be stale for a bit, but replicas converge (faster, more available).

## 5. Why replicas exist
They give lower latency, higher availability, and more read capacity.

## 6. What stale reads are
A read that hits a replica that has not received the latest write yet.

## 7. Trade-offs (latency vs correctness)
- Strong consistency: correct-but-slower.
- Eventual consistency: fast-but-sometimes-stale.

## 8. Final mental model
Many boards, one kitchen. Updates ripple outward. Some rooms lag.

## 9. Run Order
1. c081_consistency_demo.py
