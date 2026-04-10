# LeetCode 198: House Robber (Empty)
#
# PROBLEM STATEMENT
# You are given an integer array `nums` where each element represents the amount of
# money in a house along a street. Adjacent houses have connected alarms, so you
# cannot rob two adjacent houses on the same night.
#
# Return the maximum amount of money you can rob without alerting the police.
#
# EXAMPLES
# 1) nums = [1, 2, 3, 1] -> 4
#    Best choice: rob houses with values 1 and 3 (indices 0 and 2).
#
# 2) nums = [2, 7, 9, 3, 1] -> 12
#    Best choice: 2 + 9 + 1 = 12.
#
# WHAT TO IMPLEMENT
# Implement `rob(nums)` in O(n) time (typically dynamic programming).
from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int]] = [
    ([1,2,3,1], 4),
    ([2,7,9,3,1], 12),
    ([2,1,1,2], 4),
    ([], 0),
    ([5], 5),
    ([2, 1, 1, 2, 10], 13),
    ([100, 1, 1, 100], 200),
]

def harness(func: Callable[[List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            got = func(nums[:])
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def rob(nums: List[int]) -> int:
    if len(nums) == 0: return 0
    if len(nums) == 1: return nums[0]
    prev_total_theft = nums[0]
    total_theft = max(nums[0], nums[1])
    for i in range (2, len(nums)):
        prev_total_theft, total_theft = total_theft, max(total_theft , nums[i]+ prev_total_theft)
    return total_theft    
  
harness(rob)
