# ============================================================================
# File: two_sum_001_empty.py
#
# LeetCode 1: Two Sum (Easy)
#
# PROBLEM STATEMENT:
# Given an array of integers `nums` and an integer `target`, return indices of 
# the two numbers such that they add up to `target`.
#
# You may assume that each input would have exactly one solution, and you 
# may not use the same element twice.
#
# You can return the answer in any order.
#
# EXAMPLES:
# 1) nums = [2, 7, 11, 15], target = 9 -> Expected: [0, 1]
#    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
# 2) nums = [3, 2, 4], target = 6 -> Expected: [1, 2]
# 3) nums = [3, 3], target = 6 -> Expected: [0, 1]
# ============================================================================

from typing import Callable, List, Optional, Tuple

# --- TEST CASES ---
# Format: (nums, target, expected_indices_or_none)
# expected=None means "any valid pair is acceptable".
tests: List[Tuple[List[int], int, Optional[List[int]]]] = [
    ([2, 7, 11, 15], 9, [0, 1]),                  # Standard Example 1
    ([3, 2, 4], 6, [1, 2]),                       # Standard Example 2
    ([3, 3], 6, [0, 1]),                          # Standard Example 3
    ([-1, -2, -3, -4, -5], -8, [2, 4]),           # Edge Case: Negative numbers
    ([0, 4, 3, 0], 0, [0, 3]),                    # Edge Case: Zeros
    ([1000000, 2, 3, 4, 5, -1000000], 0, [0, 5]), # Boundary: Large numbers + negatives
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19, [8, 9]),# Boundary: Elements at the end
    ([1, 4, 5, 6, 9], 10, None),                  # Multiple valid solutions are possible
    ([5, 1, 5], 10, [0, 2]),                      # Duplicate values, different indices
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], int], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, target, expected) in enumerate(tests, 1):
        try:
            # Pass a copy of nums to prevent accidental mutation by the function
            got = func(nums.copy(), target)
            
            # Structural validation first.
            if not isinstance(got, list) or len(got) != 2:
                raise AssertionError(f"Output must be a 2-item list of indices. got={got}")

            if not all(isinstance(idx, int) for idx in got):
                raise AssertionError(f"Indices must be integers. got={got}")

            a, b = got
            if a == b:
                raise AssertionError(f"Indices must be distinct. got={got}")

            if not (0 <= a < len(nums)) or not (0 <= b < len(nums)):
                raise AssertionError(f"Indices out of range for nums length {len(nums)}. got={got}")

            if nums[a] + nums[b] != target:
                raise AssertionError(
                    f"Indices do not form target sum. nums[{a}] + nums[{b}] = {nums[a] + nums[b]}, target={target}"
                )

            # If an expected pair is provided, ensure pair-level match (order-agnostic).
            if expected is not None and sorted(got) != sorted(expected):
                raise AssertionError(f"Wrong pair. expected={expected}, got={got}")

            print(f"Test {i}: PASSED")
            passed += 1
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | target={target}, nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def twoSum(nums: List[int], target: int) -> List[int]:
    lookup = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in lookup:
            return [lookup[complement], i]
        
        lookup[num] = i
    raise ValueError("No valid Two Sum pair found for the given input.")


# Execute harness without __main__ block
harness(twoSum)
