# LeetCode 146: LRU Cache (Empty)
#
# PROBLEM STATEMENT
# Implement an LRU (Least Recently Used) cache with fixed capacity.
# get(key) returns value or -1. put(key, value) inserts/updates and evicts LRU when full.
# Both operations must be O(1).
#
# EXAMPLE FLOW
# put(1,1), put(2,2), get(1)->1, put(3,3) evicts 2, get(2)->-1
#
# WHAT TO IMPLEMENT
# Implement class `LRUCache` with O(1) get/put.

class LRUCache:
    def __init__(self, capacity: int): pass
    def get(self, key: int) -> int: pass
    def put(self, key: int, value: int) -> None: pass

def harness() -> None:
    print("--- Running Tests for: LRUCache ---")
    try:
        c = LRUCache(2)
        c.put(1, 1); c.put(2, 2); a = c.get(1)
        c.put(3, 3); b = c.get(2)
        c.put(4, 4); d = c.get(1); e = c.get(3); f = c.get(4)
        c2 = LRUCache(2)
        c2.put(2, 1)
        c2.put(2, 2)
        g = c2.get(2)   # 2
        c2.put(1, 1)
        c2.put(4, 1)    # evicts key 2
        h = c2.get(2)   # -1
        ok = (a, b, d, e, f, g, h) == (1, -1, -1, 3, 4, 2, -1)
        print("Test 1: PASSED" if ok else f"Test 1: FAILED | got={(a,b,d,e,f,g,h)}")
    except Exception as ex:
        print(f"Test 1: ERROR | {type(ex).__name__}: {ex}")

harness()

