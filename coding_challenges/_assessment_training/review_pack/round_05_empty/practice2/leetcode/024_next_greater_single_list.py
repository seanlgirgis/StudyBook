# ============================================================================
# File: 024_next_greater_single_list_empty.py
#
# Pattern: Next Greater Element (Single Array / List)
# (Foundation for LeetCode 496, 503, 739)
#
# PROBLEM STATEMENT:
# Given an array `nums` of integers, find the Next Greater Element for every 
# element in the array. 
#
# The Next Greater Element of an element x is the first element to the right 
# of x that is strictly greater than x. If no such element exists, output -1 
# for that element.
#
# Return an array containing the Next Greater Element for each corresponding 
# element in the input array.
#
# EXAMPLES:
# 1) nums = [4, 5, 2, 25] -> Expected: [5, 25, 25, -1]
# 2) nums = [13, 7, 6, 12] -> Expected: [-1, 12, 12, -1]
# 3) nums = [1, 2, 3, 4] -> Expected: [2, 3, 4, -1]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_list)
tests: List[Tuple[List[int], List[int]]] = [
    ([4, 5, 2, 25], [5, 25, 25, -1]),                        # Standard Example 1
    ([13, 7, 6, 12], [-1, 12, 12, -1]),                      # Standard Example 2
    ([1, 2, 3, 4], [2, 3, 4, -1]),                           # Boundary: Strictly increasing
    ([4, 3, 2, 1], [-1, -1, -1, -1]),                        # Boundary: Strictly decreasing
    ([], []),                                                # Edge Case: Empty list
    ([5], [-1]),                                             # Edge Case: Single element
    ([2, 2, 2, 2], [-1, -1, -1, -1]),                        # Boundary: All identical elements
    ([3, 1, 2, 4], [4, 2, 4, -1]),                           # Mixed values
    ([10, 3, 12, 4, 2, 9, 13, 8], [12, 12, 13, 9, 9, 13, -1, -1]), # Complex array with multiple peaks
    ([-5, -2, -10, -1], [-2, -1, -1, -1]),                   # Negative numbers
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], List[int]]) -> None:
    """
    Test harness for Next Greater Element (Single List).
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
    for i, num in enumerate(nums):
        while stack and num > nums[stack[-1]] :
            idx = stack.pop()
            out[idx] = num
        stack.append(i)
    return out



# Execute harness without __main__ block
harness(nextGreaterElements)