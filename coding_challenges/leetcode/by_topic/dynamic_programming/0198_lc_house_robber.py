"""
id: lc_0198
title: House Robber
source: leetcode
difficulty: medium
primary: dynamic-programming
tags: [arrays, dynamic-programming]
leetcode_url: https://leetcode.com/problems/house-robber/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 0198_lc_house_robber.py
# LeetCode #198: House Robber (Medium)
#
# PROBLEM STATEMENT:
# You are a professional robber planning to rob houses along a street. Each house 
# has a certain amount of money stashed, the only constraint stopping you from 
# robbing each of them is that adjacent houses have security systems connected 
# and it will automatically contact the police if two adjacent houses were broken 
# into on the same night.
#
# Given an integer array nums representing the amount of money of each house, 
# return the maximum amount of money you can rob tonight without alerting the police.
#
# EXAMPLES:
# Input: nums = [1,2,3,1]
# Output: 4 (Rob house 1 (money=1) and then rob house 3 (money=3). Total = 1+3=4)
#
# Input: nums = [2,7,9,3,1]
# Output: 12 (Rob house 1 (2), house 3 (9), house 5 (1). Total = 2+9+1=12)
# ============================================================================

from typing import List, Callable, Tuple

# (Input, Expected, Description)
tests: List[Tuple[List[int], int, str]] = [
    ([1, 2, 3, 1], 4, "Example 1: Basic case"),
    ([2, 7, 9, 3, 1], 12, "Example 2: Alternating large values"),
    ([], 0, "Edge Case: No houses"),
    ([5], 5, "Edge Case: Single house"),
    ([1, 2], 2, "Boundary: Two houses (rob max)"),
    ([10, 1, 1, 10], 20, "Pattern: Robbing ends, skipping middle two"),
    ([1, 10, 1], 10, "Pattern: Middle house is significantly larger"),
    ([0, 0, 0, 0], 0, "Constraint: All houses have zero money"),
    ([1, 1, 1, 1, 1, 1], 3, "Constraint: Constant values"),
    ([100, 1, 1, 100, 1, 1, 100], 300, "Stress: Long path with clear winners"),
    ([4, 1, 2, 7, 5, 3, 1], 14, "Complex: 4 + 7 + 3 = 14"),
    ([2, 1, 1, 2], 4, "Symmetry: Robbing first and last"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    
    for i, (nums_in, expected, desc) in enumerate(tests):
        # Use deep copy to prevent mutation during test
        nums_copy = list(nums_in)
        
        try:
            result = func(nums_copy)
            
            if result == expected:
                print(f"Test {i+1} PASSED: {desc}")
                passed += 1
            else:
                input_str = str(nums_in) if len(str(nums_in)) < 50 else f"{str(nums_in)[:47]}..."
                print(f"Test {i+1} FAILED: {desc}")
                print(f"   Input:    {input_str}")
                print(f"   Expected: {expected}")
                print(f"   Actual:   {result}")
                
        except Exception as e:
            print(f"Test {i+1} ERROR: {desc}")
            print(f"   Exception: {type(e).__name__}: {e}")

    print(f"\nResult: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def rob(nums: List[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n = len(nums)
    if n == 0: return 0
    if n == 1: return nums[0]
    nums[1] = max(nums[0], nums[1])
    for i in range(2,n):
        nums[i] = max(nums[i-1],nums[i]+ nums[i-2])
    return nums[-1]

harness(rob)