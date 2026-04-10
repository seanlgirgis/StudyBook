# ============================================================================
# File: top_k_frequent_elements_347_empty.py
#
# LeetCode 347: Top K Frequent Elements (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums and an integer k, return the k most frequent elements.
# You may return the answer in any order.
#
# Constraints:
# - 1 <= nums.length <= 10^5
# - -10^4 <= nums[i] <= 10^4
# - k is in the range [1, number of unique elements in the array]
# - It is guaranteed that the answer is unique.
#
# EXAMPLES:
# 1) nums = [1,1,1,2,2,3], k = 2 -> Expected: [1,2]
# 2) nums = [1], k = 1 -> Expected: [1]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums_array, k, expected_elements_any_order)
tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]),                     # 1. Standard example
    ([1], 1, [1]),                                       # 2. Single element
    ([4, 4, 4, 6, 6, 2], 1, [4]),                        # 3. k=1
    ([5, 5, 5, 6, 6, 7, 7, 7, 7], 2, [7, 5]),            # 4. Distinct frequencies guaranteed unique
    ([-1, -1, -2, -2, -2, 3], 2, [-2, -1]),              # 5. Negative numbers
    ([10, 10, 20, 20, 20, 30, 30, 30, 30], 2, [30, 20]), # 6. Larger skew
    ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 3, [4, 3, 2]),      # 7. Guaranteed unique cascade
    ([9, 9, 8, 8, 8, 7, 7, 7, 7], 3, [7, 8, 9]),         # 8. Top 3 exact ordering irrelevant
    ([0, 0, 0, 1, 1, 2], 2, [0, 1]),                     # 9. Includes zero
    ([100, 200, 100, 300, 200, 100], 2, [100, 200]),     # 10. Mixed values
    ([9, 9, 9, 9, 9], 1, [9]),                           # 11. Edge Case: All identical
    ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5])                # 12. Edge Case: k equals array length (all distinct)
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[List[int], int], List[int]]) -> None:
    """
    Test harness for LeetCode #347: Top K Frequent Elements.
    Compares results as sets because output order is not important.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0

    for i, (nums, k, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation
            result: List[int] = func(nums.copy(), k)

            # Basic structural checks
            if not isinstance(result, list):
                raise TypeError(f"Result must be List[int], got {type(result).__name__}")
            if len(result) != k:
                raise ValueError(f"Result length must be {k}, got {len(result) if result else 0}")

            # Compare as sets because order may vary
            if set(result) == set(expected):
                display_nums = f"{nums[:8]}..." if len(nums) > 8 else f"{nums}"
                print(f"Test {i}: PASSED (k={k}, nums={display_nums})")
                passed += 1
            else:
                display_nums = f"{nums[:8]}..." if len(nums) > 8 else f"{nums}"
                print(f"Test {i}: FAILED | k={k}, nums={display_nums}")
                print(f"    Expected set: {set(expected)}")
                print(f"    Got set:      {set(result) if result else set()}")
        except Exception as e:
            display_nums = f"{nums[:8]}..." if len(nums) > 8 else f"{nums}"
            print(f"Test {i}: ERROR  | k={k}, nums={display_nums} | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

from collections import Counter
import heapq

# --- USER TO IMPLEMENT SOLUTION BELOW ---
def topKFrequent(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    _heap = []
    for n, f in freq.items():
        heapq.heappush(_heap, (f, n))
        if len(_heap) > k:
            heapq.heappop(_heap)

    return [x for _, x in _heap]
 

 
# Execute harness without __main__ block
test_harness(topKFrequent)
