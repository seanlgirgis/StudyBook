# ============================================================================
# File: 043_lc_703_kth_largest_in_stream.py
#
# LeetCode 703: Kth Largest Element in a Stream (Easy)
#
# PROBLEM STATEMENT:
# Design a class to find the k-th largest element in a stream.
# Implement:
# - KthLargest(k, nums): initialize with integer k and initial list nums
# - add(val): append val and return the k-th largest element
# ============================================================================

from typing import Any, List, Optional


# Format: (commands, args, expected_returns)
tests: List[tuple[list[str], list[list[int]], list[Optional[int]]]] = [
    (
        ["KthLargest", "add", "add", "add", "add", "add"],
        [[3, 4, 5, 8, 2], [3], [5], [10], [9], [4]],
        [None, 4, 5, 5, 8, 8],
    ),
(
        ["KthLargest", "add", "add", "add"],
        [[1, []], [-3], [-2], [-4]],
        [None, -3, -2, -2], # <-- Changed from [None, -3, -3, -2]
    ),
    (
        ["KthLargest", "add", "add", "add", "add"],
        [[2, 1], [2], [3], [4], [5]],
        [None, 1, 2, 3, 4],
    ),
]


def test_harness(target_class: type, test_cases: List[tuple[list[str], list[list[int]], list[Optional[int]]]]) -> None:
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed = 0
    for i, (commands, args, expected) in enumerate(test_cases, 1):
        obj = None
        results: List[Optional[int]] = []
        ok = True
        err = ""
        try:
            for cmd, arg in zip(commands, args):
                if cmd == "KthLargest":
                    # arg can be [k, ...nums] or [k, nums_list]
                    k = arg[0]
                    nums = arg[1] if len(arg) > 1 and isinstance(arg[1], list) else arg[1:]
                    obj = target_class(k, nums)
                    results.append(None)
                elif cmd == "add":
                    results.append(obj.add(arg[0]))
                else:
                    raise ValueError(f"Unknown command: {cmd}")

            if results != expected:
                ok = False
                err = f"expected={expected}, got={results}"
        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"

        if ok:
            print(f"Test {i}: PASSED ({len(commands)} operations)")
            passed += 1
        else:
            print(f"Test {i}: FAILED | {err}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")

import heapq
#since it largetst we need to use minheap
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self._k = k
        self._heap = list(nums)
        heapq.heapify(self._heap )
        while len(self._heap ) > self._k:
            heapq.heappop(self._heap)          
            

    def add(self, val: int) -> int:
        heapq.heappush(self._heap, val)
        while len(self._heap ) > self._k:
            heapq.heappop(self._heap)   
        return self._heap[0]


test_harness(KthLargest, tests)

