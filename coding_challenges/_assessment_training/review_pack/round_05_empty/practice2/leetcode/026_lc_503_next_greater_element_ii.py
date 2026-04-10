# ============================================================================
# File: 026_lc_503_next_greater_element_ii_empty.py
#
# LeetCode 503: Next Greater Element II (Medium)
#
# PROBLEM STATEMENT:
# Given a circular integer array nums (i.e., the next element of 
# nums[nums.length - 1] is nums[0]), return the next greater number for 
# every element in nums.
#
# The next greater number of a number x is the first greater number to its 
# traversing-order next in the array, which means you could search circularly 
# to find its next greater number. If it doesn't exist, return -1 for this number.
#
# EXAMPLES:
# 1) nums = [1,2,1] -> Expected: [2,-1,2]
#    Explanation: The first 1's next greater number is 2; 
#    The number 2 can't find next greater number; 
#    The second 1's next greater number needs to search circularly, which is also 2.
# 2) nums = [1,2,3,4,3] -> Expected: [2,3,4,-1,4]
# ============================================================================

from collections import deque
from typing import Callable, Deque, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_list)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 1], [2, -1, 2]),                                 # Standard Example 1
    ([1, 2, 3, 4, 3], [2, 3, 4, -1, 4]),                     # Standard Example 2
    ([5, 4, 3, 2, 1], [-1, 5, 5, 5, 5]),                     # Boundary: Strictly decreasing (circular wrap finds max)
    ([1, 2, 3, 4, 5], [2, 3, 4, 5, -1]),                     # Boundary: Strictly increasing
    ([], []),                                                # Edge Case: Empty list
    ([5], [-1]),                                             # Edge Case: Single element
    ([2, 2, 2, 2, 2], [-1, -1, -1, -1, -1]),                 # Boundary: All identical elements
    ([-1, 0, -1], [0, -1, 0]),                               # Negative numbers
    ([1, 5, 3, 6, 8, 2, 9, 10, 4], [5, 6, 6, 8, 9, 9, 10, -1, 5]), # Complex: Mixed peaks and valleys
    ([100, 1, 11, 1, 120, 111, 123, 1, -1, -100], 
     [120, 11, 120, 120, 123, 123, -1, 100, 100, 100]),      # Complex: Deep valleys wrapping around to the start
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], List[int]]) -> None:
    """
    Test harness for LeetCode #503: Next Greater Element II.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(nums.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def nextGreaterElements(nums: List[int]) -> List[int]:
    stack = []     # mono stack increasing.. Store indexes
    out = [-1] * len(nums)
    lenth = len(nums)
    for j in range(2* lenth):
        i = j % lenth
        num = nums[i]
        
        while stack and num > nums[stack[-1]] :
            idx = stack.pop()
            out[idx] = num
        stack.append(i)
    return out

harness(nextGreaterElements)

