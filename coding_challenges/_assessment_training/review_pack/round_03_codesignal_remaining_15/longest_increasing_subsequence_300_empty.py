# LeetCode 300: Longest Increasing Subsequence (Empty)
#
# PROBLEM STATEMENT
# Given integer array `nums`, return the length of the longest strictly increasing subsequence.
# A subsequence does not need to be contiguous.
#
# EXAMPLES
# [10,9,2,5,3,7,101,18] -> 4 (e.g., [2,3,7,101])
# [7,7,7,7] -> 1
#
# WHAT TO IMPLEMENT
# Implement `lengthOfLIS(nums)`.
from typing import Callable, List, Tuple
import random

tests: List[Tuple[List[int], int]] = [
    ([10, 9, 2, 5, 3, 7, 101, 18], 4),
    ([0, 1, 0, 3, 2, 3], 4),
    ([7, 7, 7, 7, 7, 7, 7], 1),
    ([], 0),
    ([1], 1),
    ([1, 2, 3, 4, 5], 5),
    ([5, 4, 3, 2, 1], 1),
    ([4, 10, 4, 3, 8, 9], 3),          # canonical counterexample
    ([3, 4, -1, 0, 6, 2, 3], 4),       # classic LIS case
    ([2, 2, 2, 2], 1),
    ([-1, -2, -3], 1),
]

def _lis_oracle(nums: List[int]) -> int:
    """O(n^2) DP oracle for correctness checking."""
    n = len(nums)
    if n == 0:
        return 0
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def harness(func: Callable[[List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    total = 0

    print("\n[Deterministic Cases]")
    for i, (nums, expected) in enumerate(tests, 1):
        total += 1
        try:
            got = func(nums[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}, nums={nums}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")

    print("\n[Oracle Stress Cases]")
    rng = random.Random(42)
    stress_cases = 80
    for k in range(1, stress_cases + 1):
        total += 1
        arr_len = rng.randint(0, 10)
        nums = [rng.randint(-8, 8) for _ in range(arr_len)]
        expected = _lis_oracle(nums)
        try:
            got = func(nums[:])
            if got == expected:
                print(f"Stress {k}: PASSED")
                passed += 1
            else:
                print(f"Stress {k}: FAILED | expected={expected}, got={got}, nums={nums}")
        except Exception as e:
            print(f"Stress {k}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{total} tests passed.")

def lengthOfLIS(nums: List[int]) -> int:
    if len(nums) == 0 : return 0
    dp = [1] * len(nums)
    ret = 1
    for i in range(1, len(nums)):
        val_at_i = 1
        for j in range(i):
            if nums[i] > nums[j]:
                val_at_i = max(val_at_i , dp[j] + 1)
        dp[i] = val_at_i
        ret = max(ret, dp[i])
    return ret
                
harness(lengthOfLIS)

