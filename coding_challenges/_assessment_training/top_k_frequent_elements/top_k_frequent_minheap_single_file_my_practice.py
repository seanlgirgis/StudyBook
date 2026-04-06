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
def _is_valid_top_k(nums: List[int], k: int, result: List[int]) -> Tuple[bool, str]:
    freq = Counter(nums)

    if not isinstance(result, list):
        return False, f"Result must be List[int], got {type(result).__name__}"

    if len(result) != k:
        return False, f"Result length must be {k}, got {len(result)}"

    # Duplicates in result are not valid for this problem's top-k unique elements
    if len(set(result)) != len(result):
        return False, "Result contains duplicate elements"

    for x in result:
        if x not in freq:
            return False, f"Element {x} is not present in input"

    selected = set(result)
    min_selected_freq = min(freq[x] for x in selected)

    # No excluded element may have strictly greater frequency than the least frequent selected element
    for value, count in freq.items():
        if value not in selected and count > min_selected_freq:
            return False, (
                f"Excluded value {value} has higher frequency ({count}) than "
                f"selected boundary frequency ({min_selected_freq})"
            )

    return True, "ok"


def test_harness(func: Callable[[List[int], int], List[int]], test_cases: List[Tuple[List[int], int, List[int]]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (nums, k, expected) in enumerate(test_cases):
        try:
            result: List[int] = func(nums.copy(), k)
            valid, reason = _is_valid_top_k(nums, k, result)

            if valid:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED")
                print(f"    Reason:       {reason}")
                print(f"    Expected set: {set(expected)}")
                print(f"    Got set:      {set(result) if isinstance(result, list) else result}")
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
    if k == 0: return []
    freq = Counter(nums)
    if k > len(freq): return []
    heap = []
    for n, f in freq.items():
        heapq.heappush(heap, [f, n])
        #if it expands more than k .. pop the smallest
        if len(heap) > k:
            heapq.heappop(heap)
    return [x for _, x in heap]

# Execute harness without __main__ block
test_harness(topKFrequent_minheap, top_k_tests)
