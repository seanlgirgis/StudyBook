# Story:
# Distributed consistency: replicas agree over time, not instantly.
# This demo shows fresh reads from primary vs stale reads from replicas.

import threading
import time


REPLICA_LAGS = {
    "replica-1": 1.0,
    "replica-2": 2.5,
}


class Node:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.version = 0
        self._lock = threading.Lock()

    def apply(self, value, version):
        with self._lock:
            self.value = value
            self.version = version

    def read(self):
        with self._lock:
            return self.value, self.version


def _log(start, message):
    elapsed = time.perf_counter() - start
    print(f"[{elapsed:6.2f}s] {message}")


def _replicate(start, replica, value, version, delay):
    _log(start, f"Replication scheduled to {replica.name} in {delay:.1f}s")
    time.sleep(delay)
    replica.apply(value, version)
    _log(start, f"{replica.name} applied v{version} value={value}")


def run_consistency_demo():
    start = time.perf_counter()
    primary = Node("primary")
    replicas = [Node(name) for name in REPLICA_LAGS.keys()]

    _log(start, "Write V1 to primary")
    version = 1
    primary.apply("V1", version)

    threads = []
    for replica in replicas:
        delay = REPLICA_LAGS[replica.name]
        thread = threading.Thread(
            target=_replicate,
            args=(start, replica, "V1", version, delay),
            daemon=True,
        )
        thread.start()
        threads.append(thread)

    value, ver = primary.read()
    _log(start, f"Read from primary -> v{ver} value={value} (fresh)")

    for replica in replicas:
        value, ver = replica.read()
        _log(start, f"Read from {replica.name} -> v{ver} value={value} (stale)")

    wait_for = max(REPLICA_LAGS.values()) + 0.2
    _log(start, f"Waiting {wait_for:.1f}s for replicas to catch up")
    time.sleep(wait_for)

    for replica in replicas:
        value, ver = replica.read()
        _log(start, f"Read from {replica.name} -> v{ver} value={value} (fresh)")

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    run_consistency_demo()

# Takeaway:
# Primary reads are always fresh, replicas can be stale until they converge.
