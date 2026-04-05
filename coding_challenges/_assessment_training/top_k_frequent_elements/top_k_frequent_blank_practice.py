# LeetCode 347: Top K Frequent Elements (Blank Practice Sheet)

from typing import Callable, List, Tuple

# --- PROBLEM STATEMENT ---
# Given an integer array nums and an integer k, return the k most frequent elements.
# You may return the answer in any order.
#
# Constraints:
# - 1 <= nums.length <= 10^5
# - -10^4 <= nums[i] <= 10^4
# - k is in the range [1, number of unique elements in the array]
# - It is guaranteed that the answer is unique.

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


# --- YOUR IMPLEMENTATION ---
from collections import Counter
def topKFrequent(nums: List[int], k: int) -> List[int]:
    """
    Implement from scratch.

    Goal:
    - Return k most frequent elements.
    - Any order is acceptable.
    """
    freq = Counter(nums)
    res = []
    bckts = [[] for _ in range(len(nums)+1)]
    max_freq = 0
    for n,f in freq.items():
        max_freq = max(max_freq, f)
        bckts[f].append(n)
    for i in range(max_freq, 0 , -1):
        res.extend(bckts[i])
        if len(res) >= k : break
    return res[:k] if len(res) >=k else res

#topKFrequent ([1, 2, 3, 4, 4, 4, 5, 5], 3)
# Execute harness without __main__ block
test_harness(topKFrequent, top_k_tests)
