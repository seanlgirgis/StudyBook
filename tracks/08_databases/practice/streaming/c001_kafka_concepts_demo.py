# Story:
# Kafka mental model: producers append to an ordered log (topic).
# Consumers read with their own offset, and restart from the last committed position.


class TopicLog:
    # Ordered log of events. Only append.
    def __init__(self, name):
        self.name = name
        self._events = []

    def append(self, event):
        self._events.append(event)
        offset = len(self._events) - 1
        print(f"[PRODUCER] appended offset={offset} event={event}")
        return offset

    def read_from(self, offset, max_items=None):
        if offset < 0:
            offset = 0
        end = len(self._events) if max_items is None else offset + max_items
        return list(enumerate(self._events[offset:end], start=offset))

    def size(self):
        return len(self._events)


class Consumer:
    # Each consumer tracks its own offset (position).
    def __init__(self, name, topic, start_offset=0):
        self.name = name
        self.topic = topic
        self.offset = start_offset
        self.committed_offset = start_offset

    def poll(self, max_items=None):
        events = self.topic.read_from(self.offset, max_items=max_items)
        if not events:
            print(f"[CONSUMER:{self.name}] no new events at offset={self.offset}")
            return

        for offset, event in events:
            print(f"[CONSUMER:{self.name}] read offset={offset} event={event}")
            self.offset = offset + 1

        print(f"[CONSUMER:{self.name}] position now offset={self.offset}")

    def commit(self):
        self.committed_offset = self.offset
        print(f"[CONSUMER:{self.name}] committed offset={self.committed_offset}")

    def restart(self, use_committed=True):
        # Restart from committed offset to skip processed events,
        # or from zero to show re-reading behavior.
        if use_committed:
            self.offset = self.committed_offset
            print(f"[CONSUMER:{self.name}] restarted at committed offset={self.offset}")
        else:
            self.offset = 0
            print(f"[CONSUMER:{self.name}] restarted at offset=0 (re-read)")


def _print_log_snapshot(topic):
    print(f"[TOPIC:{topic.name}] ordered log snapshot")
    for offset, event in topic.read_from(0):
        print(f"  offset={offset} event={event}")


def run_kafka_concepts_demo():
    topic = TopicLog("orders")

    print("Kafka concepts demo: producers, consumers, offsets")
    print("Step 1: producer appends events in order")
    topic.append({"order_id": 100, "status": "CREATED"})
    topic.append({"order_id": 101, "status": "CREATED"})
    topic.append({"order_id": 100, "status": "PAID"})
    _print_log_snapshot(topic)

    print("Step 2: consumer reads from offset 0")
    consumer = Consumer("billing", topic, start_offset=0)
    consumer.poll(max_items=2)
    consumer.commit()

    print("Step 3: producer appends more events")
    topic.append({"order_id": 102, "status": "CREATED"})
    topic.append({"order_id": 101, "status": "PAID"})
    _print_log_snapshot(topic)

    print("Step 4: consumer crashes and restarts with committed offset (skip)")
    consumer.restart(use_committed=True)
    consumer.poll()
    consumer.commit()

    print("Step 5: consumer restarts without commit (re-read)")
    consumer.restart(use_committed=False)
    consumer.poll(max_items=3)

    print("Summary")
    print(f"Final log size: {topic.size()} events")
    print(f"Consumer last committed offset: {consumer.committed_offset}")


if __name__ == "__main__":
    run_kafka_concepts_demo()

# Takeaway:
# Producer appends to an ordered log; consumer moves an offset forward and resumes from it.
