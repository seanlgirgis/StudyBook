# LeetCode 215: Kth Largest Element in an Array (Empty)
#
# PROBLEM STATEMENT
# Given an integer array and an integer k, return the k-th largest element in the array.
# Note: it is k-th largest in sorted order, not k-th distinct.
#
# EXAMPLES
# [3,2,1,5,6,4], k=2 -> 5
# [3,2,3,1,2,4,5,5,6], k=4 -> 4
#
# WHAT TO IMPLEMENT
# Implement `findKthLargest(nums, k)` (heap/quickselect common).
from typing import Callable, List, Tuple
import heapq

tests: List[Tuple[List[int], int, int]] = [
    ([3,2,1,5,6,4], 2, 5),
    ([3,2,3,1,2,4,5,5,6], 4, 4),
    ([1], 1, 1),
    ([-1,-1], 2, -1),
    ([7,6,5,4,3,2,1], 5, 3),
]

def harness(func: Callable[[List[int], int], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, k, expected) in enumerate(tests, 1):
        try:
            got = func(nums[:], k)
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def findKthLargest(nums: List[int], k: int) -> int:
    max_heap = [-n for n in nums]
    heapq.heapify(max_heap)

    for _ in range(k - 1):
        heapq.heappop(max_heap)

    return -heapq.heappop(max_heap)


def findKthLargest_minheap_k(nums: List[int], k: int) -> int:
    min_heap: List[int] = []
    for n in nums:
        heapq.heappush(min_heap, n)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]

harness(findKthLargest)

