# ============================================================================
# File: 018_lc_215_kth_largest_element_empty.py
#
# LeetCode 215: Kth Largest Element in an Array (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums and an integer k, return the kth largest 
# element in the array.
#
# Note that it is the kth largest element in the sorted order, not the kth 
# distinct element.
#
# Can you solve it without sorting?
#
# EXAMPLES:
# 1) nums = [3,2,1,5,6,4], k = 2 -> Expected: 5
# 2) nums = [3,2,3,1,2,4,5,5,6], k = 4 -> Expected: 4
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, k, expected_element)
tests: List[Tuple[List[int], int, int]] = [
    ([3, 2, 1, 5, 6, 4], 2, 5),                        # Standard Example 1
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),               # Standard Example 2 (Duplicates)
    ([1], 1, 1),                                       # Edge Case: Single element
    ([2, 1], 1, 2),                                    # Edge Case: Two elements, k=1 (Max)
    ([2, 1], 2, 1),                                    # Edge Case: Two elements, k=2 (Min)
    ([3, 3, 3, 3, 3, 3], 1, 3),                        # Boundary: All identical elements
    ([3, 3, 3, 3, 3, 3], 6, 3),                        # Boundary: All identical elements, max k
    ([-1, -1, -2, -3, -4], 2, -1),                     # Boundary: All negatives with duplicates
    ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 3, 8),           # Boundary: Strictly decreasing
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3, 8),           # Boundary: Strictly increasing
    (list(range(1, 10001)), 1, 10000),                 # Stress test: Large array, k=1
    (list(range(1, 10001)), 10000, 1),                 # Stress test: Large array, k=n
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], int], int]) -> None:
    """
    Test harness for LeetCode #215: Kth Largest Element in an Array.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, k, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            # if they decide to use an in-place sort.
            got = func(nums.copy(), k)
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | k={k}, nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | k={k}, nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

import heapq

# --- USER TO IMPLEMENT SOLUTION BELOW ---
def findKthLargest(nums: List[int], k: int) -> int:
    _heap = []
    
    for num in nums:
        heapq.heappush(_heap,num)
        if len(_heap) > k:
            heapq.heappop(_heap)
            
    return _heap[0]
        


# Execute harness without __main__ block
harness(findKthLargest)