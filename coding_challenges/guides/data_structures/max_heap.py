"""
MaxHeap Wrapper
---------------
Python's heapq is a MIN-heap by default.
This wrapper negates values internally so you never have to write -val yourself.
"""

import heapq


class MaxHeap:
    """
    Max-heap wrapper around Python's heapq.
    Internally stores negated values — you always work with normal numbers.

    Usage:
        h = MaxHeap()
        h.push(5)
        h.push(10)
        h.push(1)
        h.pop()    # -> 10  (largest)
        h.peek()   # -> 5   (next largest, no removal)
        len(h)     # -> 2
    """

    def __init__(self, nums=None):
        """
        Create a MaxHeap, optionally from an existing list.

        MaxHeap([3, 1, 4, 1, 5])  -> ready to pop 5 first
        """
        if nums is None:
            self._heap = []
        else:
            self._heap = [-n for n in nums]
            heapq.heapify(self._heap)   # O(n) build

    def push(self, val):
        """Push a value onto the heap. O(log n)"""
        heapq.heappush(self._heap, -val)

    def pop(self):
        """Remove and return the largest value. O(log n)"""
        if not self._heap:
            raise IndexError("pop from empty heap")
        return -heapq.heappop(self._heap)

    def peek(self):
        """Return the largest value without removing it. O(1)"""
        if not self._heap:
            raise IndexError("peek at empty heap")
        return -self._heap[0]

    def push_pop(self, val):
        """Push val then pop the max. More efficient than push+pop. O(log n)"""
        return -heapq.heappushpop(self._heap, -val)

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return bool(self._heap)

    def __repr__(self):
        return f"MaxHeap({sorted([-x for x in self._heap], reverse=True)})"


# ─────────────────────────────────────────────────────────────────────
# Tuple support — for (priority, value) pairs
# ─────────────────────────────────────────────────────────────────────

class MaxHeapTuple:
    """
    Max-heap for (priority, value) tuples.
    Pops the tuple with the HIGHEST priority first.

    Usage:
        h = MaxHeapTuple()
        h.push(1, "low priority task")
        h.push(9, "urgent task")
        h.push(5, "medium task")
        h.pop()   # -> (9, "urgent task")
    """

    def __init__(self):
        self._heap = []

    def push(self, priority, value):
        heapq.heappush(self._heap, (-priority, value))

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty heap")
        neg_pri, value = heapq.heappop(self._heap)
        return (-neg_pri, value)

    def peek(self):
        if not self._heap:
            raise IndexError("peek at empty heap")
        neg_pri, value = self._heap[0]
        return (-neg_pri, value)

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return bool(self._heap)

    def __repr__(self):
        sorted_items = sorted([(-p, v) for p, v in self._heap], reverse=True)
        return f"MaxHeapTuple({sorted_items})"


# ─────────────────────────────────────────────────────────────────────
# Demo + Tests
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("MaxHeap Demo")
    print("=" * 50)

    h = MaxHeap()
    for val in [3, 1, 4, 1, 5, 9, 2, 6]:
        h.push(val)
        print(f"  push({val})  -> heap top = {h.peek()}")

    print()
    print("Popping all values (largest first):")
    while h:
        print(f"  pop() -> {h.pop()}")

    print()
    print("Build from list:")
    h2 = MaxHeap([10, 4, 7, 2, 9])
    print(f"  {h2}")
    print(f"  pop() -> {h2.pop()}")
    print(f"  pop() -> {h2.pop()}")

    print()
    print("=" * 50)
    print("MaxHeapTuple Demo")
    print("=" * 50)

    ht = MaxHeapTuple()
    ht.push(1, "low")
    ht.push(9, "urgent")
    ht.push(5, "medium")
    ht.push(9, "also urgent")
    print(f"  peek -> {ht.peek()}")
    while ht:
        print(f"  pop() -> {ht.pop()}")

    print()
    print("=" * 50)
    print("LC Pattern: Top K Frequent Elements")
    print("=" * 50)

    # Use MaxHeap to get top-k largest
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    from collections import Counter
    freq = Counter(nums)                      # {1:3, 2:2, 3:1}
    h3 = MaxHeap()
    for num, count in freq.items():
        h3.push(count * 1000 + num)           # encode freq+num (simple trick)

    # Cleaner: use MaxHeapTuple
    ht2 = MaxHeapTuple()
    for num, count in freq.items():
        ht2.push(count, num)                  # priority=frequency, value=number

    result = [ht2.pop()[1] for _ in range(k)]
    print(f"  Top {k} frequent in {nums}: {result}")  # [1, 2]
