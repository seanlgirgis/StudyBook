# ============================================================================
# File: 024_next_greater_single_list.py
#
# Custom Drill: Next Greater Element (Single List, Non-Circular)
#
# PROBLEM STATEMENT:
# Given a list of integers nums, return a new list answer where answer[i] is:
# - the first strictly greater value to the right of nums[i], if one exists
# - otherwise -1
#
# This is NOT circular: once you reach the end, you stop.
#
# EXAMPLES:
# 1) nums = [2, 1, 2, 4, 3] -> [4, 2, 4, -1, -1]
# 2) nums = [5, 4, 3]       -> [-1, -1, -1]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_next_greater_list)
tests: List[Tuple[List[int], List[int]]] = [
    ([2, 1, 2, 4, 3], [4, 2, 4, -1, -1]),          # Standard mixed case
    ([1, 2, 3, 4], [2, 3, 4, -1]),                 # Strictly increasing
    ([4, 3, 2, 1], [-1, -1, -1, -1]),              # Strictly decreasing
    ([2, 2, 2], [-1, -1, -1]),                     # Equal values only (strictly greater required)
    ([1, 3, 2, 3], [3, -1, 3, -1]),                # Duplicate highs
    ([-2, -1, -3, 0], [-1, 0, 0, -1]),             # Negatives + zero
    ([0], [-1]),                                    # Single element
    ([], []),                                       # Empty input
    ([5, 1, 5, 1, 6], [6, 5, 6, 6, -1]),           # Repeated pattern with final maximum
    ([9, 7, 8, 3, 2, 6], [-1, 8, -1, 6, 6, -1]),   # Multiple valleys/peaks
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

def nextGreaterRight(nums: List[int]) -> List[int]:
    if len(nums) == 0: return []
    out = [-1] * len(nums)
    stack = []                                     # mono decreasing stack..index storage.. pop if cur number is bigger than top of stack
    
    
    for i, num in enumerate(nums):
        while stack and num > nums[stack[-1]]:
            idx = stack.pop()
            out[idx] = num
        stack.append(i)
    return out
    
harness(nextGreaterRight)
