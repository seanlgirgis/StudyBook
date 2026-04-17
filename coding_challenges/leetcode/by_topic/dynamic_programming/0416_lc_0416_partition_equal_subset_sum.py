"""
id: lc_0416
title: Partition Equal Subset Sum
source: leetcode
difficulty: medium
primary: dynamic programming
tags: [arrays, dynamic programming, knapsack]
leetcode_url: https://leetcode.com/problems/partition-equal-subset-sum/
status: draft
last_updated: 2026-04-17
notes: |
    - key idea: 
    - time: 
    - space: 
"""

# ============================================================================
# File: 0416_lc_0416_partition_equal_subset_sum.py
# LC 416: Partition Equal Subset Sum (Medium)
# 
# PROBLEM STATEMENT:
# Given an integer array nums, return true if you can partition the array into 
# two subsets such that the sum of the elements in both subsets is equal or 
# false otherwise.
# 
# EXAMPLES:
# 1. Input: nums = [1,5,11,5] -> Output: true (subset [1, 5, 5] and [11])
# 2. Input: nums = [1,2,3,5] -> Output: false
# 
# CONSTRAINTS:
# - 1 <= nums.length <= 200
# - 1 <= nums[i] <= 100
# ============================================================================

from typing import List, Callable, Tuple
import copy

# (Input, Expected Output, Description)
tests: List[Tuple[List[int], bool, str]] = [
    # Standard Examples
    ([1, 5, 11, 5], True, "Example 1: Standard partitionable case"),
    ([1, 2, 3, 5], False, "Example 2: Sum is odd, impossible"),
    
    # Edge Cases
    ([1], False, "Edge Case: Single element"),
    ([10, 10], True, "Edge Case: Two identical elements"),
    ([1, 3], False, "Edge Case: Two different elements"),
    ([0, 0], True, "Edge Case: Zeroes (though constraints say nums[i] >= 1)"),
    
    # Boundary / Sum Logic
    ([1, 1, 1, 1], True, "Boundary: All identical elements (even count)"),
    ([1, 1, 1], False, "Boundary: All identical elements (odd count)"),
    ([1, 2, 5], False, "Logic: Sum is even (8) but no subset sums to 4"),
    ([2, 2, 2, 2, 2, 10], True, "Logic: Large element equals sum of others"),
    
    # Complex / Stress
    ([1, 2, 3, 4, 5, 6, 7], True, "Complex: Sum 28, target 14"),
    ([100] * 10 + [50] * 2, True, "Stress: Large values with multiple ways to sum"),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False, "Complex: Sum 55 (odd), immediate false"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected, desc) in enumerate(tests):
        # Use deepcopy to ensure user logic doesn't mutate test input
        arg_copy = copy.deepcopy(nums)
        
        try:
            result = func(arg_copy)
            if result == expected:
                print(f"Test {i+1} [PASSED]: {desc}")
                passed += 1
            else:
                print(f"Test {i+1} [FAILED]: {desc}")
                print(f"   Input: {nums[:10]}{'...' if len(nums) > 10 else ''}")
                print(f"   Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1} [ERROR]: {desc}")
            print(f"   Exception: {e}")

    print(f"\nResult: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def can_partition(nums: List[int]) -> bool:
    s = sum(nums)
    if (s % 2 ) !=  0 : return False  # has to be even
    target = s//2
    n = len(nums)
    canReach = [[False] * (target + 1) for _ in range(n + 1)]
    canReach[0][0] = True
    for i in range(1, n + 1):
        for s in range(target + 1):
            skip = canReach[i - 1][s]
            take = s >= nums[i - 1] and canReach[i - 1][s - nums[i - 1]]
            canReach[i][s] = skip or take

    return canReach[n][target]

harness(can_partition)