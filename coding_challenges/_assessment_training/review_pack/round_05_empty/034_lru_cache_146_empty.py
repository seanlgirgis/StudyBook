# ============================================================================
# File: lru_cache_146_empty.py
#
# LeetCode 146: LRU Cache (Medium)
#
# PROBLEM STATEMENT:
# Design a data structure that follows the constraints of a Least Recently 
# Used (LRU) cache.
#
# Implement the LRUCache class:
# - LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
# - int get(int key) Return the value of the key if the key exists, otherwise return -1.
# - void put(int key, int value) Update the value of the key if the key exists. 
#   Otherwise, add the key-value pair to the cache. If the number of keys exceeds 
#   the capacity from this operation, evict the least recently used key.
#
# The functions get and put must each run in O(1) average time complexity.
#
# EXAMPLES:
# Input
# ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
# [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
# Output
# [null, null, null, 1, null, -1, null, -1, 3, 4]
# ============================================================================

from typing import List, Tuple, Any, Optional

# --- TEST CASES ---
# Format: (commands, args, expected_outputs)
tests: List[Tuple[List[str], List[List[int]], List[Optional[int]]]] = [
    (
        # 1. Standard LC Example
        ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
        [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
        [None, None, None, 1, None, -1, None, -1, 3, 4]
    ),
    (
        # 2. Boundary: Capacity of 1 (Constant eviction)
        ["LRUCache", "put", "get", "put", "get", "get"],
        [[1], [2, 1], [2], [3, 2], [2], [3]],
        [None, None, 1, None, -1, 2]
    ),
    (
        # 3. Edge Case: Updating an existing key (Should update value AND make it most recently used)
        ["LRUCache", "put", "put", "put", "get", "put", "get"],
        [[2], [2, 1], [1, 1], [2, 3], [2], [4, 1], [1]],
        [None, None, None, None, 3, None, -1]
    ),
    (
        # 4. Edge Case: 'get' makes an item most recently used
        ["LRUCache", "put", "put", "get", "put", "get", "get"],
        [[2], [1, 1], [2, 2], [1], [3, 3], [2], [1]],
        [None, None, None, 1, None, -1, 1]
    ),
    (
        # 5. Boundary: 'get' on non-existent items doesn't affect LRU order
        ["LRUCache", "put", "put", "get", "get", "put", "get", "get"],
        [[2], [1, 1], [2, 2], [99], [1], [3, 3], [2], [1]],
        [None, None, None, -1, 1, None, -1, 1]
    )
]

# --- TEST HARNESS ---
def test_harness(target_class: type, test_cases: List[Tuple[List[str], List[List[int]], List[Optional[int]]]]) -> None:
    """
    Test harness for LeetCode #146: LRU Cache.
    Validates sequential state execution and correct eviction tracking.
    """
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed: int = 0
    
    for i, (commands, args, expected) in enumerate(test_cases, 1):
        obj = None
        results: List[Optional[int]] = []
        test_passed: bool = True
        error_msg: str = ""
        
        try:
            # Execute commands
            for step, (cmd, arg) in enumerate(zip(commands, args)):
                if cmd == "LRUCache":
                    obj = target_class(arg[0])
                    results.append(None)
                elif cmd == "put":
                    obj.put(arg[0], arg[1])
                    results.append(None)
                elif cmd == "get":
                    results.append(obj.get(arg[0]))
                else:
                    raise ValueError(f"Unknown command: {cmd}")
            
            # Validate results
            for step, (res, exp) in enumerate(zip(results, expected)):
                if res != exp:
                    test_passed = False
                    error_msg = f"Mismatch at step {step} ({commands[step]}{args[step]}): Got {res}, Expected {exp}"
                    break
                        
        except Exception as e:
            test_passed = False
            error_msg = f"{type(e).__name__}: {e}"
            
        if test_passed:
            print(f"Test {i}: PASSED ({len(commands)} operations, capacity={args[0][0]})")
            passed += 1
        else:
            print(f"Test {i}: FAILED | {error_msg}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
class Node:
    def __init__(self, key: int = 0, val: int = 0):
        # Store both key and value so we can delete from hash-map on eviction.
        self.key = key
        self.val = val
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Sean style picture:
        # 1) Hash map = "address book" (key -> exact node in O(1)).
        # 2) Doubly linked list = "recency timeline":
        #    head <-> most recent ... least recent <-> tail
        # Together they guarantee O(1) get/put/evict.
        self.cache: dict[int, Node] = {}

        # Doubly linked list keeps usage order:
        # head <-> ...most recent... <-> ...least recent... <-> tail
        # Dummy nodes simplify insert/remove edge cases.
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        # List-only unlink; does NOT delete from map.
        # This is reused for move-to-front and eviction paths.
        p, n = node.prev, node.next
        # p and n are always valid because data nodes are between dummy head/tail.
        p.next = n
        n.prev = p

    def _add_to_front(self, node: Node) -> None:
        # Insert right after head => mark as most recently used.
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: Node) -> None:
        # "I touched this key, so make it most recent."
        self._remove(node)
        self._add_to_front(node)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Accessing key makes it most recently used.
        node = self.cache[key]
        self._move_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        # put handles both UPDATE and INSERT in O(1).
        if key in self.cache:
            # Update existing value and refresh recency.
            node = self.cache[key]
            node.val = value
            self._move_to_front(node)
            return

        # Insert new key as most recently used.
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)

        if len(self.cache) > self.capacity:
            # Sean style eviction rule:
            # tail.prev is the oldest untouched key => evict it first (LRU).
            lru = self.tail.prev
            self._remove(lru)
            # Eviction must remove from map too.
            del self.cache[lru.key]


# Execute harness without __main__ block
test_harness(LRUCache, tests)
