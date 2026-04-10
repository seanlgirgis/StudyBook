from typing import List, Optional, Any
#LeetCode 146 LRU cache == Least Recently Used
# --- TEST CASES ---
# Format: {"commands": [...], "args": [...], "expected": [...]}
lru_cache_tests: List[dict] = [
    {
        # Standard LC Example 1
        "commands": ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
        "args": [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
        "expected": [None, None, None, 1, None, -1, None, -1, 3, 4]
    },
    {
        # Capacity of 1 (Immediate Eviction)
        "commands": ["LRUCache", "put", "get", "put", "get", "get"],
        "args": [[1], [2, 1], [2], [3, 2], [2], [3]],
        "expected": [None, None, 1, None, -1, 2]
    },
    {
        # Updating an existing key (Should mark as recently used and update value)
        "commands": ["LRUCache", "put", "put", "get", "put", "put", "get"],
        "args": [[2], [2, 1], [2, 2], [2], [1, 1], [4, 1], [2]],
        "expected": [None, None, None, 2, None, None, -1]
    }
]

# --- TEST HARNESS ---
def test_harness(target_class: type, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #146: LRU Cache.
    Validates capacity constraints, eviction policies, and key updates.
    """
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases):
        commands: List[str] = tc["commands"]
        args: List[List[Any]] = tc["args"]
        expected: List[Optional[int]] = tc["expected"]
        
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
            print(f"Test {i+1}: PASSED ({len(commands)} operations)")
            passed += 1
        else:
            print(f"Test {i+1}: FAILED | {error_msg}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
class Node:
    def __init__(self, key: int = 0, val: int = 0):
        # Store both key and value so we can delete from hash-map on eviction.
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Hash-map gives O(1) lookup: key -> linked-list node.
        self.cache = {}

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
        p.next = n
        n.prev = p

    def _add_to_front(self, node: Node) -> None:
        # Insert right after head => mark as most recently used.
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: Node) -> None:
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
        # put handles both UPDATE and INSERT.
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
            # Evict least recently used item (node before tail).
            lru = self.tail.prev
            self._remove(lru)
            # Eviction must remove from map too.
            del self.cache[lru.key]



# Execute harness without __main__ block
test_harness(LRUCache, lru_cache_tests)
