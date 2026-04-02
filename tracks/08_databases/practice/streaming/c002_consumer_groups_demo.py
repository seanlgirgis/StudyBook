# Story:
# Consumer groups split partitions inside a group, but different groups
# each consume the full stream with their own offsets.


class TopicLog:
    # Topic is an ordered log split into partitions.
    def __init__(self, name, partitions):
        self.name = name
        self.partitions = [[] for _ in range(partitions)]
        self._next_partition = 0

    def append(self, event):
        partition = self._next_partition
        self._next_partition = (self._next_partition + 1) % len(self.partitions)
        self.partitions[partition].append(event)
        offset = len(self.partitions[partition]) - 1
        print(f"[PRODUCER] appended p={partition} offset={offset} event={event}")

    def read(self, partition, offset):
        if offset < 0:
            offset = 0
        log = self.partitions[partition]
        if offset >= len(log):
            return None
        return log[offset]

    def snapshot(self):
        print(f"[TOPIC:{self.name}] log snapshot")
        for pid, log in enumerate(self.partitions):
            for offset, event in enumerate(log):
                print(f"  p={pid} offset={offset} event={event}")


class Consumer:
    # Consumer tracks offsets per partition it owns.
    def __init__(self, name, partitions):
        self.name = name
        self.partitions = partitions
        self.offsets = {pid: 0 for pid in partitions}

    def poll_once(self, topic):
        read_any = False
        for pid in self.partitions:
            offset = self.offsets[pid]
            event = topic.read(pid, offset)
            if event is None:
                continue
            print(f"[CONSUMER:{self.name}] read p={pid} offset={offset} event={event}")
            self.offsets[pid] = offset + 1
            read_any = True
        if not read_any:
            print(f"[CONSUMER:{self.name}] no new events")
        return read_any


class ConsumerGroup:
    # Group assigns partitions so only one consumer owns each partition.
    def __init__(self, name, topic, consumer_names):
        self.name = name
        self.topic = topic
        self.consumer_names = consumer_names
        self.consumers = []

    def assign(self):
        partitions = list(range(len(self.topic.partitions)))
        self.consumers = []
        for i, name in enumerate(self.consumer_names):
            owned = partitions[i::len(self.consumer_names)]
            self.consumers.append(Consumer(name, owned))
        print(f"[GROUP:{self.name}] partition ownership")
        for consumer in self.consumers:
            print(f"  {consumer.name} owns partitions={consumer.partitions}")

    def poll_until_empty(self):
        while True:
            progressed = False
            for consumer in self.consumers:
                progressed = consumer.poll_once(self.topic) or progressed
            if not progressed:
                break


def run_consumer_groups_demo():
    topic = TopicLog("orders", partitions=2)

    print("Consumer groups demo: share work inside group, duplicate across groups")
    print("Step 1: producer appends events")
    topic.append({"order_id": 200, "status": "CREATED"})
    topic.append({"order_id": 201, "status": "CREATED"})
    topic.append({"order_id": 200, "status": "PAID"})
    topic.append({"order_id": 202, "status": "CREATED"})
    topic.snapshot()

    print("Step 2: Group A has two consumers, partitions are split")
    group_a = ConsumerGroup("group-A", topic, ["A1", "A2"])
    group_a.assign()
    group_a.poll_until_empty()

    print("Step 3: Group B is independent and reads full stream")
    group_b = ConsumerGroup("group-B", topic, ["B1"])
    group_b.assign()
    group_b.poll_until_empty()

    print("Summary")
    print("Inside a group, each partition is owned by one consumer.")
    print("Across groups, each group reads the full stream with its own offsets.")


if __name__ == "__main__":
    run_consumer_groups_demo()

# Takeaway:
# Consumer groups split partitions for parallelism, but groups are independent readers.
