# Story:
# Polling checks for changes repeatedly. Event-driven ingestion emits changes immediately.
# Multiple consumers can react independently (fan-out).


class EventStream:
    # In-memory stream with publish/subscribe.
    def __init__(self, name):
        self.name = name
        self._events = []
        self._subscribers = []
        self._seq = 0

    def subscribe(self, handler):
        self._subscribers.append(handler)

    def publish(self, event):
        event["seq"] = self._seq
        self._seq += 1
        self._events.append(event)
        print(f"[STREAM:{self.name}] publish seq={event['seq']} op={event['op']} key={event['key']}")
        for handler in self._subscribers:
            handler(event)

    def events_since(self, seq):
        return [e for e in self._events if e["seq"] >= seq]


class SourceTable:
    # CDC-style producer: emits an event on every change.
    def __init__(self, name, stream):
        self.name = name
        self.rows = {}
        self.stream = stream

    def insert(self, key, row):
        self.rows[key] = row
        self.stream.publish({"table": self.name, "op": "INSERT", "key": key, "after": row})

    def update(self, key, patch):
        row = dict(self.rows[key])
        row.update(patch)
        self.rows[key] = row
        self.stream.publish({"table": self.name, "op": "UPDATE", "key": key, "after": row})

    def delete(self, key):
        del self.rows[key]
        self.stream.publish({"table": self.name, "op": "DELETE", "key": key, "after": None})

    def snapshot(self):
        print(f"[TABLE:{self.name}] snapshot")
        for key, row in self.rows.items():
            print(f"  key={key} row={row}")


class PollingConsumer:
    # Polling consumer keeps checking for new events.
    def __init__(self, name, stream):
        self.name = name
        self.stream = stream
        self.cursor = 0

    def poll(self):
        events = self.stream.events_since(self.cursor)
        if not events:
            print(f"[POLL:{self.name}] no new events (wasted check)")
            return
        for event in events:
            print(f"[POLL:{self.name}] got seq={event['seq']} op={event['op']} key={event['key']}")
            self.cursor = event["seq"] + 1


class EventConsumer:
    # Event-driven consumer reacts immediately when the stream pushes events.
    def __init__(self, name):
        self.name = name

    def handle(self, event):
        print(f"[PUSH:{self.name}] got seq={event['seq']} op={event['op']} key={event['key']}")


def run_event_driven_ingestion_demo():
    stream = EventStream("cdc-events")
    source = SourceTable("orders", stream)

    polling = PollingConsumer("analytics", stream)
    search = EventConsumer("search-index")
    billing = EventConsumer("billing-cache")
    stream.subscribe(search.handle)
    stream.subscribe(billing.handle)

    print("Event-driven ingestion demo: polling vs push")
    print("Step 1: polling checks before any events")
    polling.poll()

    print("Step 2: source changes emit events immediately (push)")
    source.insert(10, {"status": "CREATED"})
    source.update(10, {"status": "PAID"})
    source.insert(11, {"status": "CREATED"})
    source.delete(11)
    source.snapshot()

    print("Step 3: polling catches up after the fact")
    polling.poll()

    print("Summary")
    print("Polling wastes checks. Event-driven push reacts instantly and fans out to many consumers.")


if __name__ == "__main__":
    run_event_driven_ingestion_demo()

# Takeaway:
# Event-driven ingestion emits changes once and multiple consumers react without polling.
