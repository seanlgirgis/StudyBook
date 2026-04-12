"""
id: lc_0042
title: Trapping Rain Water
source: leetcode
difficulty: hard
primary: stack
tags: [stack, monotonic-stack, two-pointers, dynamic-programming]
leetcode_url: https://leetcode.com/problems/trapping-rain-water/
status: draft
last_updated: 2026-04-12
notes: 
- key idea: Use a monotonic decreasing stack to find bounded "valleys" or use two pointers to track the maximum heights from left and right.
- time: O(n)
- space: O(n) with stack or O(1) with two-pointer.
"""

# ============================================================================
# File: 042_lc_042_trapping_rain_water_empty.py
# Problem 42: Trapping Rain Water (Hard)
# 
# PROBLEM STATEMENT:
# Given n non-negative integers representing an elevation map where the width 
# of each bar is 1, compute how much water it can trap after raining.
#
# EXAMPLES:
# Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
# Output: 6
# Explanation: The above elevation map (black section) is represented by 
# [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water are being trapped.
#
# Input: height = [4,2,0,3,2,5]
# Output: 9
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[height, expected]]
tests: List[Tuple[List[int], int]] = [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6), # Standard Example 1
    ([4, 2, 0, 3, 2, 5], 9),                   # Standard Example 2
    ([1, 1, 1], 0),                            # Edge Case: Flat surface
    ([3, 2, 1], 0),                            # Edge Case: Strictly decreasing
    ([1, 2, 3], 0),                            # Edge Case: Strictly increasing
    ([], 0),                                   # Edge Case: Empty input
    ([5], 0),                                  # Edge Case: Single bar
    ([2, 0, 2], 2),                            # Boundary: Simple valley
    ([5, 1, 5], 4),                            # Boundary: Deep valley
    ([3, 0, 2, 0, 4], 7),                      # Multiple valleys of different depths
    ([10, 0, 10], 10),                         # Wide gap
    ([4, 2, 3], 1),                            # Partial fill (limited by right wall)
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (height, expected) in enumerate(tests):
        # Deep copy to prevent mutation
        height_copy = list(height)
        
        try:
            result = func(height_copy)
            
            display_input = str(height) if len(str(height)) < 50 else f"{str(height)[:47]}..."
            
            if result == expected:
                print(f"Test {i+1}: PASSED | Input: {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: {display_input}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {display_input}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def trap(height: List[int]) -> int:
    """
    Calculates the total trapped rain water.
    """
    if not len(height):return 0
    l, r = 0, len(height)-1
    max_l , max_r = height[l], height[r]
    water = 0
    while l < r:
        if max_r > max_l:
            l += 1
            if height[l] < max_l:
                water += (max_l - height[l])
            max_l = max(max_l , height[l])
        else:
            r -= 1
            if height[r] < max_r:
                water += (max_r - height[r])
            max_r = max(max_r , height[r])            
        
    return water

harness(trap)