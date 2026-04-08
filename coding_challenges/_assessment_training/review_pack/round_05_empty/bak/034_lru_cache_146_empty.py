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
        # Real cache entry. Keep both key and value:
        # - value for get()
        # - key so eviction can delete from hash map in O(1)
        self.key = key
        self.val = val
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class DoublyLinkedList:
    def __init__(self):
        # Dummy sentinels:
        # head <-> ...real nodes... <-> tail
        # Most recently used (MRU) lives near head.
        # Least recently used (LRU) lives near tail.
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node: Node) -> None:
        # Unlink one node from timeline:
        # p <-> node <-> n   ==>   p <-> n
        p = node.prev
        n = node.next
        # For real nodes, both prev and next must exist due to sentinels.
        assert p is not None and n is not None
        p.next = n
        n.prev = p

    def add_to_front(self, node: Node) -> None:
        # Insert node right after head (mark as MRU).
        first_real = self.head.next
        assert first_real is not None

        node.next = self.head.next
        node.prev = self.head
        first_real.prev = node
        self.head.next = node

    def move_to_front(self, node: Node) -> None:
        # Access/update means this key is now most recently used.
        self.remove(node)
        self.add_to_front(node)

    def pop_lru(self) -> Node:
        # LRU real node is right before tail.
        lru = self.tail.prev
        assert lru is not None and lru is not self.head
        self.remove(lru)
        return lru


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Sean style architecture:
        # 1) hash map: key -> node (fast lookup)
        # 2) linked list: recency order (fast reorder/evict)
        self.cache: dict[int, Node] = {}
        self.dll = DoublyLinkedList()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.dll.move_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        # Case 1: update existing key, then refresh recency.
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self.dll.move_to_front(node)
            return

        # Case 2: insert new key as MRU.
        node = Node(key, value)
        self.cache[key] = node
        self.dll.add_to_front(node)

        # If over capacity, evict LRU from both list and map.
        if len(self.cache) > self.capacity:
            lru = self.dll.pop_lru()
            del self.cache[lru.key]


# Execute harness without __main__ block
test_harness(LRUCache, tests)
