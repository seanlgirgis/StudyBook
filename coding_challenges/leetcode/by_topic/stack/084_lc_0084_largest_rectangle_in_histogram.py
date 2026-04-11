"""
id: lc_0084
title: Largest Rectangle in Histogram
source: leetcode
difficulty: hard
primary: stack
tags: [stack, monotonic-stack, arrays]
leetcode_url: https://leetcode.com/problems/largest-rectangle-in-histogram/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 084_lc_0084_largest_rectangle_in_histogram.py
# LC084: Largest Rectangle in Histogram (Hard)
# 
# Given an array of integers heights representing the histogram's bar height 
# where the width of each bar is 1, return the area of the largest rectangle 
# in the histogram.
#
# Constraints:
# - 1 <= heights.length <= 10^5
# - 0 <= heights[i] <= 10^4
#
# Examples:
# Input: heights = [2,1,5,6,2,3]
# Output: 10
# Explanation: The largest rectangle is shown in the red area, which has an area = 10 units.
#
# Input: heights = [2,4]
# Output: 4
# ============================================================================

from typing import List, Callable, Tuple

# Comprehensive Test Suite
tests: List[Tuple[List[int], int]] = [
    ([2, 1, 5, 6, 2, 3], 10),      # Example 1: Standard case
    ([2, 4], 4),                   # Example 2: Small case
    ([1], 1),                      # Edge Case: Single element
    ([0], 0),                      # Edge Case: Zero height
    ([1, 1, 1, 1], 4),             # All identical elements
    ([5, 4, 3, 2, 1], 9),          # Strictly decreasing
    ([1, 2, 3, 4, 5], 9),          # Strictly increasing
    ([2, 1, 2], 3),                # "Valley" pattern
    ([1, 10, 1], 10),              # Single tall peak
    ([0, 9, 0], 9),                # Peak surrounded by zeros
    ([2, 1, 4, 5, 1, 3, 3], 8),    # Complex multi-peak
    ([10**4] * 5, 50000),          # Max constraint height
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (heights, expected) in enumerate(tests):
        # Deep copy to prevent mutation issues
        arg_copy = list(heights)
        try:
            result = func(arg_copy)
            if result == expected:
                print(f"Test {i+1:02}: PASSED")
                passed += 1
            else:
                input_str = str(heights) if len(str(heights)) < 50 else f"{str(heights[:5])}..."
                print(f"Test {i+1:02}: FAILED | Input: {input_str} | Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1:02}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nScore: {passed}/{len(tests)}")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def largestRectangleArea(heights: List[int]) -> int:
    """
    Finds the largest rectangular area in a histogram.
    
    Args:
        heights: A list of integers representing bar heights.
    Returns:
        The maximum area of a rectangle.
    """
    stack = []          # mono stack h, inherited index
                        # if cur height is smaller.. pop and calculate
    max_area, n = 0, len(heights) 
                        
    for i, h in enumerate(heights):
        inh_idx = i
        while stack and h <= stack[-1][0]:
            ph, pidx = stack.pop()
            max_area = max(max_area, (i - pidx) * ph)
            inh_idx = pidx
        stack.append((h, inh_idx))
        
    while stack:
        ph, pidx = stack.pop()
        max_area = max(max_area, (n - pidx) * ph)
            
            
    return max_area

harness(largestRectangleArea)