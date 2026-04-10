# ============================================================================
# File: 023_top_k_frequent_elements_347_empty.py
#
# LeetCode 347: Top K Frequent Elements (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums and an integer k, return the k most frequent elements. 
# You may return the answer in any order.
#
# It is guaranteed that the answer is unique.
#
# EXAMPLES:
# 1) nums = [1,1,1,2,2,3], k = 2 -> Expected: [1,2]
# 2) nums = [1], k = 1 -> Expected: [1]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, k, expected_list)
tests: List[Tuple[List[int], int, List[int]]] = [
    ([1, 1, 1, 2, 2, 3], 2, [1, 2]),                   # Standard Example 1
    ([1], 1, [1]),                                     # Standard Example 2
    ([4, 4, 4, 4, 5, 5, 5, 6, 6, 7], 2, [4, 5]),       # Standard: Clear top 2
    ([-1, -1], 1, [-1]),                               # Edge Case: Negative numbers
    ([1, 2, 3, 4], 4, [1, 2, 3, 4]),                   # Boundary: k equals number of unique elements
    ([10, 10, 10, 20, 20, 30], 1, [10]),               # Boundary: k = 1 with multiple options
    ([3, 0, 1, 0], 1, [0]),                            # Boundary: Array with zeroes
    ([5, 5, 5, 5, 5], 1, [5]),                         # Boundary: All identical elements
    ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 2, [3, 4]),       # Increasing frequencies
    ([7, 7, 7, 8, 8, 9, 9, 9, 9, 10], 2, [7, 9]),      # Disjoint frequency gaps
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], int], List[int]]) -> None:
    """
    Test harness for LeetCode #347: Top K Frequent Elements.
    Normalizes the output arrays by sorting to handle order-agnostic matching.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, k, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(nums.copy(), k)
            
            # Sort both the actual and expected outputs for safe comparison
            # since the problem states the answer can be in any order.
            norm_expected = sorted(expected) if expected else []
            norm_got = sorted(got) if got else []
            
            if norm_got == norm_expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 12 else f"[{str(nums[:11])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={norm_expected}, got={norm_got} | k={k}, nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 12 else f"[{str(nums[:11])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | k={k}, nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

import heapq
from collections import Counter
# --- USER TO IMPLEMENT SOLUTION BELOW ---
def topKFrequent(nums: List[int], k: int) -> List[int]:
    _heap = []        #stores tuples of (freq, num) .. max length k .. heapified .. minheap
    counts = Counter(nums)

    for n, f in counts.items():
        heapq.heappush(_heap,(f,n))
        if len(_heap) > k:
            heapq.heappop(_heap)

    return [x for (_,x) in _heap]
        


# Execute harness without __main__ block
harness(topKFrequent)