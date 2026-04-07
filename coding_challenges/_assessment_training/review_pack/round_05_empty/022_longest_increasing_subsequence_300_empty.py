# ============================================================================
# File: longest_increasing_subsequence_300_empty.py
#
# LeetCode 300: Longest Increasing Subsequence (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return the length of the longest strictly 
# increasing subsequence.
# 
# A subsequence is an array that can be derived from another array by 
# deleting some or no elements without changing the order of the remaining 
# elements.
#
# EXAMPLES:
# 1) nums = [10, 9, 2, 5, 3, 7, 101, 18] -> Expected: 4
#    Explanation: The longest increasing subsequence is [2, 3, 7, 101], 
#    therefore the length is 4.
#
# 2) nums = [0, 1, 0, 3, 2, 3] -> Expected: 4
#
# 3) nums = [7, 7, 7, 7, 7, 7, 7] -> Expected: 1
# ============================================================================

from typing import Callable, List, Tuple
import random

# --- TEST CASES ---
# Format: (nums, expected_length)
tests: List[Tuple[List[int], int]] = [
    ([10, 9, 2, 5, 3, 7, 101, 18], 4),
    ([0, 1, 0, 3, 2, 3], 4),
    ([7, 7, 7, 7, 7, 7, 7], 1),
    ([], 0),
    ([1], 1),
    ([1, 2, 3, 4, 5], 5),
    ([5, 4, 3, 2, 1], 1),
    ([4, 10, 4, 3, 8, 9], 3),          # canonical counterexample for greedy
    ([3, 4, -1, 0, 6, 2, 3], 4),       # classic LIS case
    ([2, 2, 2, 2], 1),
    ([-1, -2, -3], 1),
    ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6), # mixed jumps
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


# --- TEST HARNESS ---
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
                nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums_display}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e}")

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
                print(f"Stress {k}: FAILED | expected={expected}, got={got} | nums={nums}")
        except Exception as e:
            print(f"Stress {k}: ERROR  | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{total} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def lengthOfLIS(nums: List[int]) -> int:
    if len(nums) == 0:
        return 0

    dp = [1] * len(nums)
    ret = 1
    
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
                ret = max(ret, dp[i])
                
    return ret

# Execute harness without __main__ block
harness(lengthOfLIS)
