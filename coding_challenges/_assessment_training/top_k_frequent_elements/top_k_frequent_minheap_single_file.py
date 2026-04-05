# LeetCode 347: Top K Frequent Elements (Min-Heap Variant)

from typing import Callable, List, Tuple
from collections import Counter
import heapq

# --- PROBLEM STATEMENT ---
# Given an integer array nums and an integer k, return the k most frequent elements.
# You may return the answer in any order.
#
# This file demonstrates a min-heap approach:
# - Count frequencies
# - Keep a min-heap of size k based on frequency
# - Complexity: O(n log k), Space: O(n)

# --- TEST CASES ---
# Format: (nums_array, k, expected_elements_any_order)
top_k_tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]),
    ([1], 1, [1]),
    ([4, 4, 4, 6, 6, 2], 1, [4]),
    ([5, 5, 6, 6, 7, 7, 7], 2, [7, 5]),
    ([-1, -1, -2, -2, -2, 3], 2, [-2, -1]),
    ([10, 10, 20, 20, 20, 30, 30, 30, 30], 2, [30, 20]),
    ([1, 2, 3, 4, 4, 4, 5, 5], 3, [4, 5, 1]),
    ([9, 9, 8, 8, 8, 7, 7, 7, 7], 3, [7, 8, 9]),
    ([0, 0, 0, 1, 1, 2], 2, [0, 1]),
    ([100, 200, 100, 300, 200, 100], 2, [100, 200]),
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[List[int], int], List[int]], test_cases: List[Tuple[List[int], int, List[int]]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (nums, k, expected) in enumerate(test_cases):
        try:
            result: List[int] = func(nums.copy(), k)

            if not isinstance(result, list):
                raise TypeError(f"Result must be List[int], got {type(result).__name__}")
            if len(result) != k:
                raise ValueError(f"Result length must be {k}, got {len(result)}")

            if set(result) == set(expected):
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED")
                print(f"    Expected set: {set(expected)}")
                print(f"    Got set:      {set(result)}")
        except Exception as e:
            print(f"Test {i+1}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- MIN-HEAP IMPLEMENTATION ---
def topKFrequent_minheap(nums: List[int], k: int) -> List[int]:
    """Return k most frequent elements using a size-k min-heap.

    Steps:
    1) Count frequencies.
    2) Push (freq, num) into min-heap.
    3) If heap grows beyond k, pop smallest frequency.
    4) Return nums from heap.
    """
    freq = Counter(nums)
    min_heap: List[Tuple[int, int]] = []

    for num, count in freq.items():
        heapq.heappush(min_heap, (count, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return [num for _, num in min_heap]


# Execute harness without __main__ block
test_harness(topKFrequent_minheap, top_k_tests)
