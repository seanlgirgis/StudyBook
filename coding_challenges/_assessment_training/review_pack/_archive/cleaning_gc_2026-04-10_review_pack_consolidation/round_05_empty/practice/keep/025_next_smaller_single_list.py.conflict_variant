# ============================================================================
# File: 025_next_smaller_single_list.py
#
# Custom Drill: Next Smaller Element (Single List, Non-Circular)
#
# PROBLEM STATEMENT:
# Given a list of integers nums, return a new list answer where answer[i] is:
# - the first strictly smaller value to the right of nums[i], if one exists
# - otherwise -1
#
# This is NOT circular: once you reach the end, you stop.
#
# EXAMPLES:
# 1) nums = [4, 8, 5, 2, 25] -> [2, 5, 2, -1, -1]
# 2) nums = [1, 2, 3]        -> [-1, -1, -1]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_next_smaller_list)
tests: List[Tuple[List[int], List[int]]] = [
    ([4, 8, 5, 2, 25], [2, 5, 2, -1, -1]),           # Standard mixed case
    ([1, 2, 3, 4], [-1, -1, -1, -1]),                # Strictly increasing
    ([4, 3, 2, 1], [3, 2, 1, -1]),                   # Strictly decreasing
    ([2, 2, 2], [-1, -1, -1]),                       # Equal values only (strictly smaller required)
    ([5, 1, 5, 1, 6], [1, -1, 1, -1, -1]),           # Repeated pattern
    ([-2, -1, -3, 0], [-3, -3, -1, -1]),             # Negatives + zero
    ([0], [-1]),                                      # Single element
    ([], []),                                         # Empty input
    ([9, 7, 8, 3, 2, 6], [7, 3, 3, 2, -1, -1]),      # Multiple valleys/peaks
    ([10, 9, 10, 8, 7], [9, 8, 8, 7, -1]),           # Duplicate highs with descending tail
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
def nextSmallerRight(nums: List[int]) -> List[int]:
    if len(nums) == 0 : return []
    out = [-1] * len(nums)
    stack = []     #mono increasing stack of indexes... if cur is smaller than top pop
    for i, num in enumerate(nums):
        while stack and num < nums[stack[-1]]:
            idx = stack.pop()
            out[idx] = num
        stack.append(i)

    return out
    


# Execute harness without __main__ block
harness(nextSmallerRight)
