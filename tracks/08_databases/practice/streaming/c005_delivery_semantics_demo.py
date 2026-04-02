# Story:
# At-least-once delivery can duplicate events on retry.
# Exactly-once effect comes from deduplication or idempotent processing.


class EventStream:
    # Simple ordered stream of events.
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)
        print(f"[STREAM] publish id={event['id']} amount={event['amount']}")


class AtLeastOnceConsumer:
    # Processes events, but a retry can process the same event twice.
    def __init__(self, name):
        self.name = name
        self.total = 0

    def process_with_retry(self, event, simulate_failure=False):
        # Simulate a failure after processing but before ack.
        self.total += event["amount"]
        print(f"[ALO:{self.name}] applied id={event['id']} total={self.total}")
        if simulate_failure:
            print(f"[ALO:{self.name}] crash before ack -> retry delivers duplicate")
            # Retry delivers the same event again.
            self.total += event["amount"]
            print(f"[ALO:{self.name}] applied duplicate id={event['id']} total={self.total}")


class ExactlyOnceConsumer:
    # Deduplicates by event id to get exactly-once effect.
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.seen_ids = set()

    def process_with_retry(self, event, simulate_failure=False):
        # Even if retried, dedupe prevents double apply.
        self._apply_if_new(event)
        if simulate_failure:
            print(f"[EO:{self.name}] crash before ack -> retry delivers duplicate")
            self._apply_if_new(event)

    def _apply_if_new(self, event):
        if event["id"] in self.seen_ids:
            print(f"[EO:{self.name}] skip duplicate id={event['id']} total={self.total}")
            return
        self.seen_ids.add(event["id"])
        self.total += event["amount"]
        print(f"[EO:{self.name}] applied id={event['id']} total={self.total}")


def run_delivery_semantics_demo():
    stream = EventStream()
    event = {"id": "pay-001", "amount": 100}

    print("Delivery semantics demo: at-least-once vs exactly-once")
    print("Step 1: producer publishes payment event")
    stream.publish(event)

    print("Step 2: at-least-once consumer retries and duplicates")
    alo = AtLeastOnceConsumer("billing")
    alo.process_with_retry(stream.events[0], simulate_failure=True)

    print("Step 3: exactly-once effect via dedup")
    eo = ExactlyOnceConsumer("billing")
    eo.process_with_retry(stream.events[0], simulate_failure=True)

    print("Summary")
    print(f"At-least-once total (duplicate): {alo.total}")
    print(f"Exactly-once total (deduped): {eo.total}")


if __name__ == "__main__":
    run_delivery_semantics_demo()

# Takeaway:
# At-least-once can duplicate. Exactly-once effect requires idempotency or dedup.
