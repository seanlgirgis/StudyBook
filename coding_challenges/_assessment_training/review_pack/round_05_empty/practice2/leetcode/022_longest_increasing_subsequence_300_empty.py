# ============================================================================
# File: 022_longest_increasing_subsequence_300_empty.py
#
# LeetCode 300: Longest Increasing Subsequence (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return the length of the longest strictly 
# increasing subsequence.
#
# A subsequence is an array that can be derived from another array by 
# deleting some or no elements without changing the order of the remaining elements.
#
# EXAMPLES:
# 1) nums = [10,9,2,5,3,7,101,18] -> Expected: 4
#    Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
# 2) nums = [0,1,0,3,2,3] -> Expected: 4
# 3) nums = [7,7,7,7,7,7,7] -> Expected: 1
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_length)
tests: List[Tuple[List[int], int]] = [
    ([10, 9, 2, 5, 3, 7, 101, 18], 4),             # Standard Example 1
    ([0, 1, 0, 3, 2, 3], 4),                       # Standard Example 2
    ([7, 7, 7, 7, 7, 7, 7], 1),                    # Standard Example 3
    ([], 0),                                       # Edge Case: Empty list
    ([5], 1),                                      # Edge Case: Single element
    ([5, 4, 3, 2, 1], 1),                          # Boundary: Strictly decreasing
    ([1, 2, 3, 4, 5], 5),                          # Boundary: Strictly increasing
    ([-10, -5, 0, -8, -2, -1], 4),                 # Boundary: Negatives
    ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6),             # Complex: Multiple competing subsequences
    ([10, 9, 2, 5, 3, 4], 3),                      # Boundary: Subsequence ends early
    ([3, 5, 6, 2, 5, 4, 19, 5, 6, 7, 12], 6),      # Complex mixed
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], int]) -> None:
    """
    Test harness for LeetCode #300: Longest Increasing Subsequence.
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
                nums_disp = str(nums) if len(nums) <= 12 else f"[{str(nums[:11])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 12 else f"[{str(nums[:11])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def lengthOfLIS(nums: List[int]) -> int:
    dp = [1] * len(nums)
    longest = 0
    for i, num in enumerate(nums):
        maxi = 0
        for j in range(i):
            if nums[j] < nums[i]:
                maxi = max(maxi, dp[j])
        dp[i] += maxi
        longest = max(longest, dp[i])
    return longest
        
            


# Execute harness without __main__ block
harness(lengthOfLIS)
