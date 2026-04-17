"""
id: lc_0300
title: Longest Increasing Subsequence
source: leetcode
difficulty: medium
primary: arrays
tags: [arrays, dynamic-programming, binary-search]
leetcode_url: https://leetcode.com/problems/longest-increasing-subsequence/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 0300_lc_0300_longest_increasing_subsequence.py
# LeetCode 300: Longest Increasing Subsequence (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return the length of the longest strictly 
# increasing subsequence.
#
# A subsequence is a sequence that can be derived from an array by deleting 
# some or no elements without changing the order of the remaining elements. 
# For example, [3,6,2,7] is a subsequence of the array [0,3,1,6,2,2,7].
#
# EXAMPLES:
# Example 1:
# Input: nums = [10,9,2,5,3,7,101,18]
# Output: 4
# Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
#
# Example 2:
# Input: nums = [0,1,0,3,2,3]
# Output: 4
#
# Example 3:
# Input: nums = [7,7,7,7,7,7,7]
# Output: 1
#
# CONSTRAINTS:
# - 1 <= nums.length <= 2500
# - -10^4 <= nums[i] <= 10^4
# ============================================================================

from typing import List, Callable, Tuple
import copy

# Test cases: (nums, expected_output, description)
tests: List[Tuple[List[int], int, str]] = [
    ([10, 9, 2, 5, 3, 7, 101, 18], 4, "Standard Example 1"),
    ([0, 1, 0, 3, 2, 3], 4, "Standard Example 2"),
    ([7, 7, 7, 7, 7, 7, 7], 1, "Standard Example 3: All identical"),
    ([1], 1, "Edge Case: Single element"),
    ([1, 2, 3, 4, 5], 5, "Boundary: Strictly increasing"),
    ([5, 4, 3, 2, 1], 1, "Boundary: Strictly decreasing"),
    ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6, "Complex: Multiple peaks and valleys"),
    ([-10, -5, -100, -20, 0, 50], 4, "Negative values"),
    ([2, 2, 3, 3, 4, 4], 3, "Duplicates: Not strictly increasing"),
    ([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15], 6, "Stress: Bitonic-like pattern"),
    ([10, 20, 30, 1, 2, 3, 4, 5], 5, "Complex: Resetting subsequence"),
    ([1, 2, 1, 2, 1, 2, 1, 2], 2, "Pattern: Oscillating"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected, desc) in enumerate(tests):
        # Create deep copy to prevent mutation of test case input
        nums_input = copy.deepcopy(nums)
        
        try:
            result = func(nums_input)
            if result == expected:
                print(f"CASE {i+1} PASSED: {desc}")
                passed += 1
            else:
                # Truncate long inputs for visibility
                display_input = str(nums) if len(str(nums)) < 50 else f"{str(nums)[:47]}..."
                print(f"CASE {i+1} FAILED: {desc}")
                print(f"  Input:    {display_input}")
                print(f"  Expected: {expected}")
                print(f"  Actual:   {result}")
        except Exception as e:
            print(f"CASE {i+1} ERROR: {desc}")
            print(f"  Exception: {type(e).__name__}: {e}")

    print(f"\nRESULT: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def lengthOfLIS(nums: List[int]) -> int:
    n = len(nums)
    if n == 0 : return 0
    if n == 1 : return 1
    longest = 0
    LIS = [1] * n
    for i in range(n -1, -1, -1):
        for j in range (i+1, n):
            if nums[i] < nums[j]:
                LIS[i] = max(LIS[i], 1 + LIS[j])
                longest  = max(longest , LIS[i])
    return max(LIS)
    
harness(lengthOfLIS)