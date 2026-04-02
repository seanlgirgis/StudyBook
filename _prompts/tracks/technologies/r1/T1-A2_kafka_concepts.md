# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-A2_kafka_concepts.md

SAVE AS: kafka_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate kafka_concepts.md — a concept reference covering the 8 core Kafka abstractions,
each explained in one tight paragraph, followed by a Citi narrative tie-in.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput
- alerts flow: monitoring agents → Kafka → alerting consumers + analytics consumers + ML pipeline

STRUCTURE — produce exactly these sections in order:

# Apache Kafka — Core Concepts

## 1. Topic
One paragraph. Cover: named append-only log, messages never deleted by consumers,
retention period (time or size based), topics as the unit of data organization.
End with: "In Citi's stack, `citi.alerts` holds all HIGH/CRITICAL endpoint alerts."

## 2. Partition
One paragraph. Cover: topics split into N ordered partitions, each partition is an
independent log, partitions enable parallelism, partition count determines max consumer parallelism.
End with: "citi.alerts uses 3 partitions — 3 consumers in a group can read simultaneously."

## 3. Offset
One paragraph. Cover: integer position within a partition, consumer-owned (not broker-owned),
offset commit = checkpoint, replay by seeking to earlier offset, exactly-once vs at-least-once.
End with: "If an alerting consumer crashes, it resumes from its last committed offset — no alerts lost."

## 4. Producer
One paragraph. Cover: client that appends to topics, key-based partitioning (null key = round-robin),
acks=all for durability, batching and linger.ms for throughput, idempotent producers.
End with: "Monitoring agents produce with key=endpoint_id so all events for one endpoint land in the same partition."

## 5. Consumer Group
One paragraph. Cover: logical group of consumers sharing work, each partition assigned to one consumer,
rebalancing when membership changes, group.id isolation, multiple groups = multiple independent reads.
End with: "Alerting and analytics teams each have their own group.id — both read all 100 alerts independently."

## 6. Broker
One paragraph. Cover: server process that stores partitions, leader vs follower replicas,
broker failure and leader election, ZooKeeper vs KRaft for coordination.
End with: "The learning stack runs a single broker — production Citi would run 3+ for fault tolerance."

## 7. Replication Factor
One paragraph. Cover: how many broker copies each partition has, RF=1 means data loss on broker failure,
RF=3 is production standard, ISR (In-Sync Replicas) set, what happens when ISR shrinks.
End with: "RF=1 in the learning stack is intentional — RF=3 requires 3 brokers."

## 8. Retention
One paragraph. Cover: time-based (default 7 days) vs size-based retention, log compaction as alternative
(keeps latest value per key forever), compaction use case = changelog / state reconstruction.
End with: "For endpoint status events, log compaction makes sense — only the latest status per endpoint_id matters."

---

## Quick Reference Table

| Concept | One-line definition | Learning stack value |
|---------|---------------------|----------------------|
| Topic | Named append-only log | citi.alerts |
| Partition | Ordered sub-log within a topic | 3 |
| Offset | Integer position in a partition | consumer-tracked |
| Producer | Client that writes to topics | monitoring agent |
| Consumer Group | Shared readers of a topic | alerting, analytics |
| Broker | Server storing partitions | 1 (localhost:9092) |
| Replication Factor | Partition copy count | 1 (dev only) |
| Retention | How long messages are kept | 7 days (default) |

---

## Interview Flashcards

**Q: Why does partition count matter?**
A: It caps consumer parallelism. A topic with 3 partitions can have at most 3 active consumers
in a group at once. Adding a 4th consumer leaves it idle.

**Q: What happens if a consumer dies before committing its offset?**
A: The partition is reassigned to another consumer in the group, which resumes from the last
committed offset. Messages since the last commit are reprocessed — at-least-once semantics.

**Q: When would you use log compaction instead of time-based retention?**
A: When you need the latest state per key indefinitely — e.g., current endpoint status, user
preferences, device configuration. Time-based retention is for event streams where old events expire.

**Q: What is an ISR and why does it shrink?**
A: In-Sync Replicas — the set of followers caught up with the leader. A follower falls out of ISR
if it lags behind by more than replica.lag.time.max.ms (default 30s). If ISR shrinks below
min.insync.replicas and acks=all, producers receive an error — correct behavior: data safety over availability.

CONSTRAINTS:
- Each concept section: exactly one paragraph, 4-6 sentences, no bullet points within the paragraph
- Citi tie-in is the final sentence of each paragraph
- Quick Reference Table: valid GitHub Flavored Markdown pipe table
- Interview Flashcards: Q bolded, A normal weight, blank line between cards
- No filler phrases ("it's worth noting", "importantly", "in conclusion")

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.


