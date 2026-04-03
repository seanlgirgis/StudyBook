"""
+==============================================================================+
|  NUGGET 03-03 . Contract Validation in Code                                  |
|  Validate event schema before producing and after consuming.                 |
+==============================================================================+

CONCEPTS
--------
  Producer-side Validation:
    Validate the event against the schema CONTRACT before producing.
    Prevents invalid data from ever entering the topic.
    If validation fails: fix in the producer code, not downstream.

  Consumer-side Validation:
    Validate after deserialization.
    Catches: schema drift, wrong producer version, corrupt data.
    On failure: route to DLQ (do not process).

  Contract Validation Approaches:
    1. Manual field checks (this nugget -- most portable, no dependencies).
    2. jsonschema library (JSON Schema draft-7/2020).
    3. Pydantic models (type-safe, pythonic).
    4. Avro + Schema Registry (binary, centralized versioning).

  Schema Registry (Confluent):
    A separate service that stores Avro/JSON/Protobuf schemas.
    Each message carries a schema_id (4 bytes) as a magic header.
    Producer registers schema; consumer fetches schema by id to deserialize.
    NOT required for this local lab -- requires confluent-kafka client.

OPERATIONS COVERED
------------------
  1. Manual contract validator with field types and constraints
  2. Producer-side validation (reject bad events before produce)
  3. Consumer-side validation (DLQ routing on invalid)
  4. Schema contract as code (typed dataclass pattern)

USAGE
-----
    python 03_contract_validation.py
"""
from __future__ import annotations

import json
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from _kafka_connect import BROKER, require_broker, safe_json_deserializer

require_broker(BROKER)

from kafka import KafkaConsumer, KafkaProducer

print("\n-- Nugget 03-03: Contract Validation in Code --")
print(f"  Broker: {BROKER}")
print()

TOPIC = "lab.raw.events"
DLQ_TOPIC = "lab.dlq"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Contract definition (typed dataclass)
# ─────────────────────────────────────────────────────────────────────────────
print("  [1] Contract definition as a typed dataclass:")

@dataclass
class OrderEvent:
    """
    Contract for commerce.order.placed events.
    This dataclass IS the schema contract -- no separate schema file needed.
    """
    order_id:   str
    user_id:    str
    amount:     float
    ts:         int
    currency:   str = "USD"
    channel:    str = "web"
    coupon_code: Optional[str] = None

    def validate(self) -> list[str]:
        errors = []
        if not self.order_id or not self.order_id.strip():
            errors.append("order_id must be a non-empty string")
        if not self.user_id or not self.user_id.strip():
            errors.append("user_id must be a non-empty string")
        if not isinstance(self.amount, (int, float)) or self.amount < 0:
            errors.append(f"amount must be a non-negative number, got {self.amount!r}")
        if not isinstance(self.ts, int) or self.ts <= 0:
            errors.append(f"ts must be a positive integer epoch, got {self.ts!r}")
        if self.currency not in ("USD", "EUR", "GBP", "JPY"):
            errors.append(f"currency must be one of USD/EUR/GBP/JPY, got {self.currency!r}")
        return errors


print(f"    OrderEvent contract fields: {[f.name for f in OrderEvent.__dataclass_fields__.values()]}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Producer-side validation -- reject before sending
# ─────────────────────────────────────────────────────────────────────────────
print("  [2] Producer-side validation:")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks="all",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if isinstance(k, str) else k,
    request_timeout_ms=15_000,
)

candidate_events = [
    # Valid events
    OrderEvent(order_id="ORD-001", user_id="alice", amount=99.99, ts=int(time.time())),
    OrderEvent(order_id="ORD-002", user_id="bob",   amount=0.0,   ts=int(time.time()), currency="EUR"),
    # Invalid events (should be rejected)
    OrderEvent(order_id="",        user_id="carol", amount=50.0,  ts=int(time.time())),  # empty order_id
    OrderEvent(order_id="ORD-003", user_id="dave",  amount=-10.0, ts=int(time.time())),  # negative amount
    OrderEvent(order_id="ORD-004", user_id="eve",   amount=75.0,  ts=int(time.time()), currency="XYZ"),  # bad currency
]

sent_count = rejected_count = 0
for ev in candidate_events:
    errors = ev.validate()
    if errors:
        rejected_count += 1
        print(f"    REJECT  order_id={ev.order_id!r:12}  errors={errors}")
    else:
        envelope = {
            "event_id":       str(uuid.uuid4()),
            "event_type":     "commerce.order.placed",
            "schema_version": 2,
            "produced_at":    datetime.now(timezone.utc).isoformat(),
            "payload":        asdict(ev),
        }
        meta = producer.send(TOPIC, key=ev.user_id, value=envelope).get(timeout=10)
        sent_count += 1
        print(f"    SEND    order_id={ev.order_id!r:12}  amount={ev.amount}  offset={meta.offset}")

producer.flush()
producer.close()
print(f"    Sent: {sent_count}  Rejected at producer: {rejected_count}")
print()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Consumer-side validation
# ─────────────────────────────────────────────────────────────────────────────
print("  [3] Consumer-side validation (with DLQ routing on failure):")

dlq_producer = KafkaProducer(
    bootstrap_servers=BROKER,
    acks=1,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=15_000,
)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    group_id=f"contract_validation_{uuid.uuid4().hex[:8]}",
    auto_offset_reset="earliest",
    consumer_timeout_ms=6_000,
    value_deserializer=safe_json_deserializer,
    enable_auto_commit=False,
)

valid_processed = invalid_routed = schema_errors = 0

for msg in consumer:
    env = msg.value
    if not isinstance(env, dict):
        schema_errors += 1
        consumer.commit()
        continue
    if env.get("event_type") != "commerce.order.placed":
        consumer.commit()
        continue

    payload = env.get("payload", {})
    try:
        order = OrderEvent(
            order_id=payload.get("order_id", ""),
            user_id=payload.get("user_id", ""),
            amount=payload.get("amount", 0),
            ts=payload.get("ts", 0),
            currency=payload.get("currency", "USD"),
            channel=payload.get("channel", "web"),
            coupon_code=payload.get("coupon_code"),
        )
        errs = order.validate()
        if errs:
            raise ValueError(f"Contract violation: {errs}")

        valid_processed += 1
        print(f"    VALID    order_id={order.order_id}  amount={order.amount}  currency={order.currency}")
        consumer.commit()

    except Exception as exc:
        dlq_msg = {
            "dlq_id":         str(uuid.uuid4()),
            "original_topic": msg.topic,
            "original_offset": msg.offset,
            "original_payload": payload,
            "failure_reason": str(exc),
            "failure_ts":     int(time.time()),
        }
        dlq_producer.send(DLQ_TOPIC, value=dlq_msg)
        invalid_routed += 1
        print(f"    INVALID  offset={msg.offset}  reason={str(exc)[:60]}")
        consumer.commit()

dlq_producer.flush()
dlq_producer.close()
consumer.close()

print(f"    Valid: {valid_processed}  Invalid->DLQ: {invalid_routed}")
print()

print("  Nugget 03-03 complete.")
print()
print("  Key takeaways:")
print("    - Validate BEFORE producing to prevent invalid data entering the topic.")
print("    - Validate AFTER consuming to handle schema drift from other producers.")
print("    - Dataclass contracts are lightweight, testable, and self-documenting.")
print("    - Consumer validation failures -> DLQ (not exception propagation).")
print("    - Avro + Schema Registry is the production standard for strict schemas.")
print()

