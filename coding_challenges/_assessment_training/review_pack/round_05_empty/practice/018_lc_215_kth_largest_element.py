# ============================================================================
# File: lc_215_kth_largest_element.py
#
# LeetCode 215: Kth Largest Element in an Array (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums and an integer k, return the kth largest 
# element in the array.
# 
# Note that it is the kth largest element in the sorted order, not the 
# kth distinct element.
#
# Can you solve it without sorting?
#
# EXAMPLES:
# - nums = [3,2,1,5,6,4], k = 2 -> Expected: 5
# - nums = [3,2,3,1,2,4,5,5,6], k = 4 -> Expected: 4
# ============================================================================

from typing import Callable, List, Tuple


# --- TEST CASES ---
# Format: (nums, k, expected)
tests: List[Tuple[List[int], int, int]] = [
    ([3, 2, 1, 5, 6, 4], 2, 5),
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
    ([1], 1, 1),
    ([-1, -1], 2, -1),
    ([7, 6, 5, 4, 3, 2, 1], 5, 3),
    ([10, 10, 10, 10], 2, 10),              # Boundary: All identical
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 9, 1),    # Boundary: k = length (smallest element)
    ([-5, -1, -3, -4, -2], 3, -3),          # Edge case: All negative
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[List[int], int], int], test_cases: List[Tuple[List[int], int, int]]) -> None:
    """
    Test harness for LeetCode #215: Kth Largest Element in an Array.
    Validates integer output against the expected k-th largest value.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, k, expected) in enumerate(test_cases, 1):
        try:
            # Pass a copy of nums to prevent accidental mutation by the function
            got = func(nums[:], k)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | k={k}, nums={nums_display}")
        except Exception as e:
            nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | k={k}, nums={nums_display}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")

import heapq
# --- USER TO IMPLEMENT SOLUTION BELOW ---
def findKthLargest(nums: List[int], k: int) -> int:
    # Keep a size-k min-heap; heap top is the k-th largest.
    _heap = []
    for num in nums:
        heapq.heappush(_heap, num)
        if len(_heap) > k:
            heapq.heappop(_heap)

    return _heap[0]



# Execute harness without __main__ block
test_harness(findKthLargest, tests)
