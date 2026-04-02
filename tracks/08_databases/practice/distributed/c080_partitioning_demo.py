# Story:
# Distributed partitioning: route keys to shards with a rule.
# This demo compares balanced hashing vs skewed routing.

import hashlib


PARTITIONS = 4
TOTAL_KEYS = 2000
HOT_KEYS = 1400


def _hash_route(key, partitions):
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()
    return int(digest, 16) % partitions


def _skewed_route(key, partitions):
    # Bad routing: keys starting with 'hot' always go to shard 0.
    if key.startswith("hot"):
        return 0
    return ord(key[0]) % partitions


def _build_keys():
    keys = []
    for i in range(HOT_KEYS):
        keys.append(f"hot-{i}")
    for i in range(TOTAL_KEYS - HOT_KEYS):
        keys.append(f"cold-{i}")
    return keys


def _count_partitions(keys, route_fn, partitions):
    counts = [0] * partitions
    for key in keys:
        shard = route_fn(key, partitions)
        counts[shard] += 1
    return counts


def _print_counts(label, counts):
    print("=" * 72)
    print(label)
    total = sum(counts)
    for idx, count in enumerate(counts):
        print(f"Partition {idx}: {count}")
    hot_idx = counts.index(max(counts))
    print(f"Total keys: {total}")
    print(f"Hot partition: {hot_idx} ({counts[hot_idx]})")


def _demo_lookup(key, route_fn, partitions):
    shard = route_fn(key, partitions)
    print(f"Lookup key '{key}' routed to partition {shard}")


def run_partitioning_demo():
    keys = _build_keys()

    balanced_counts = _count_partitions(keys, _hash_route, PARTITIONS)
    _print_counts("Mode A - balanced hash routing", balanced_counts)
    _demo_lookup("hot-42", _hash_route, PARTITIONS)

    skewed_counts = _count_partitions(keys, _skewed_route, PARTITIONS)
    _print_counts("Mode B - skewed routing", skewed_counts)
    _demo_lookup("hot-42", _skewed_route, PARTITIONS)


if __name__ == "__main__":
    run_partitioning_demo()

# Takeaway:
# Partitioning scales when routing is balanced; bad keys create hot shards.
