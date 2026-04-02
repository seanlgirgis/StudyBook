# Kafka Fundamentals - Story Map

## 1. Story (mailroom + inbox)
Your company ships orders all day. The mailroom writes every order onto a clipboard in strict order. Each team has its own inbox and decides how far down the clipboard it has read.

## 2. Core Concepts (street version)
- Producer = the writer (adds events to the log).
- Topic = the shared clipboard (ordered log of events).
- Consumer = the reader (tracks its own position).
- Offset = the line number the reader last processed.

## 3. Producer (what it does)
Producers only append. They do not edit or delete. This makes the log an ordered history.

## 4. Consumer (what it does)
Consumers pull from the log and keep their own offset. Two consumers can read the same topic but be at different positions.

## 5. Offset (why it matters)
Offset is the resume point. If a consumer crashes, it can restart from its last committed offset instead of re-reading everything.

## 6. Failure Mode (re-read vs skip)
- If offsets are not committed, a restart re-reads old events.
- If offsets are committed, a restart skips what was already processed.

## 7. Final Mental Model
Kafka is a shared ordered log. Producers append. Consumers move a pointer (offset) forward as they read.

## 8. Run Order
1. c001_kafka_concepts_demo.py
