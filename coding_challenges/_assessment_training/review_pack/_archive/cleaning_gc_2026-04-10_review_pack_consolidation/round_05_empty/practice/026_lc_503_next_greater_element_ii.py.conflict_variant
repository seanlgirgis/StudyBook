# ============================================================================
# File: 026_lc_503_next_greater_element_ii.py
#
# LeetCode 503: Next Greater Element II (Medium)
#
# PROBLEM STATEMENT:
# Given a circular integer array nums (the next element of nums[nums.length - 1]
# is nums[0]), return the next greater number for every element in nums.
# The next greater number of x is the first greater number to its traversing-order
# next in the array, which means you could search circularly to find its next
# greater number. If it doesn't exist, return -1 for this number.
#
# EXAMPLES:
# 1) nums = [1,2,1] -> Expected: [2,-1,2]
# 2) nums = [1,2,3,4,3] -> Expected: [2,3,4,-1,4]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_next_greater_list)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 1], [2, -1, 2]),                     # Standard example
    ([1, 2, 3, 4, 3], [2, 3, 4, -1, 4]),         # Standard example
    ([5, 4, 3, 2, 1], [-1, 5, 5, 5, 5]),         # Wrap-around needed
    ([2, 2, 2], [-1, -1, -1]),                   # All equal
    ([1], [-1]),                                 # Single element
    ([], []),                                    # Empty list
    ([3, 1, 2], [-1, 2, 3]),                     # Small mixed
    ([2, 1, 2, 4, 3], [4, 2, 4, -1, 4]),         # Classic non-circular + circular effect on last
    ([-2, -1, -3], [-1, -1, -2]),                # Negatives
    ([9, 7, 8, 3, 2, 6], [-1, 8, 9, 6, 6, 9]),   # Multiple wraps
]


# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            result = func(nums.copy())
            if result == expected:
                nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: PASSED (nums={nums_display})")
                passed += 1
            else:
                nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={result} | nums={nums_display}")
        except Exception as e:
            nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_display}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def nextGreaterElements(nums: List[int]) -> List[int]:
    n = len(nums)
    if n == 0 : return []
    # loop twice .. Identify indx as %n
    stack = []     # mono stack .. 
    out = [-1] * n
    
    for i in range (len(nums) * 2):
        idx = i % n
        num = nums[idx]
        while stack and num > nums[stack[-1]]:
            index = stack.pop()
            out[index] = num
        stack.append(idx)
     
    return out



# Execute harness without __main__ block
harness(nextGreaterElements)
