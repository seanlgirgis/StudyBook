# Story:
# CDC turns table changes (insert/update/delete) into events.
# Downstream consumers can react to events without rescanning the whole table.


class ChangeTable:
    # In-memory table that emits CDC events for each change.
    def __init__(self, name):
        self.name = name
        self.rows = {}
        self._events = []
        self._seq = 0

    def _emit(self, op, key, before, after):
        event = {
            "seq": self._seq,
            "table": self.name,
            "op": op,
            "key": key,
            "before": before,
            "after": after,
        }
        self._seq += 1
        self._events.append(event)
        print(f"[CDC] emit seq={event['seq']} op={op} key={key}")

    def insert(self, key, row):
        self.rows[key] = row
        self._emit("INSERT", key, None, row)

    def update(self, key, patch):
        before = dict(self.rows[key])
        after = dict(self.rows[key])
        after.update(patch)
        self.rows[key] = after
        self._emit("UPDATE", key, before, after)

    def delete(self, key):
        before = dict(self.rows[key])
        del self.rows[key]
        self._emit("DELETE", key, before, None)

    def snapshot(self):
        print(f"[TABLE:{self.name}] snapshot")
        for key, row in self.rows.items():
            print(f"  key={key} row={row}")

    def events_since(self, seq):
        return [e for e in self._events if e["seq"] >= seq]


class DownstreamIndex:
    # Downstream system maintains its own state by applying CDC events.
    def __init__(self):
        self.state = {}

    def apply(self, event):
        op = event["op"]
        key = event["key"]
        if op == "INSERT":
            self.state[key] = event["after"]
        elif op == "UPDATE":
            self.state[key] = event["after"]
        elif op == "DELETE":
            if key in self.state:
                del self.state[key]
        print(f"[DOWNSTREAM] applied seq={event['seq']} op={op} key={key}")

    def snapshot(self):
        print("[DOWNSTREAM] snapshot")
        for key, row in self.state.items():
            print(f"  key={key} row={row}")


def run_cdc_demo():
    table = ChangeTable("customers")
    downstream = DownstreamIndex()
    last_seq = 0

    print("CDC demo: changes become events")
    print("Step 1: initial inserts")
    table.insert(1, {"name": "Ava", "tier": "free"})
    table.insert(2, {"name": "Ben", "tier": "free"})
    table.snapshot()

    print("Step 2: downstream consumes events (no full rescan)")
    for event in table.events_since(last_seq):
        downstream.apply(event)
        last_seq = event["seq"] + 1
    downstream.snapshot()

    print("Step 3: update and delete on source")
    table.update(1, {"tier": "pro"})
    table.delete(2)
    table.snapshot()

    print("Step 4: downstream consumes only new events")
    for event in table.events_since(last_seq):
        downstream.apply(event)
        last_seq = event["seq"] + 1
    downstream.snapshot()

    print("Summary")
    print("CDC emits insert/update/delete events so consumers react without rescanning.")


if __name__ == "__main__":
    run_cdc_demo()

# Takeaway:
# CDC captures row changes as events so downstream systems stay in sync cheaply.
