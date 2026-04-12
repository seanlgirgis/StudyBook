"""
id: lc_0739
title: Daily Temperatures
source: leetcode
difficulty: medium
primary: stack
tags: [stack, monotonic-stack, arrays]
leetcode_url: https://leetcode.com/problems/daily-temperatures/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use a monotonic decreasing stack to store indices of days whose next warmer day hasn't been found.
- time: O(n) - each index is pushed/popped once.
- space: O(n) - for the result array and the stack in the worst case.
"""

# ============================================================================
# File: 739_lc_0739_daily_temperatures_empty.py
#
# LeetCode 739: Daily Temperatures
# Difficulty: Medium
#
# PROBLEM STATEMENT:
# Given an array of integers `temperatures` represents the daily temperatures, 
# return an array `answer` such that `answer[i]` is the number of days you 
# have to wait after the i-th day to get a warmer temperature. 
#
# If there is no future day for which this is possible, keep `answer[i] == 0` 
# instead.
#
# EXAMPLES:
# 1) temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
#    Output: [1, 1, 4, 2, 1, 1, 0, 0]
# 2) temperatures = [30, 40, 50, 60]
#    Output: [1, 1, 1, 0]
# 3) temperatures = [30, 60, 90]
#    Output: [1, 1, 0]
# ============================================================================

from typing import Callable, List, Tuple
import copy

# --- TEST CASES ---
# Format: (temperatures, expected_output)
tests: List[Tuple[List[int], List[int]]] = [
    ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]), # Example 1
    ([30, 40, 50, 60], [1, 1, 1, 0]),                             # Example 2
    ([30, 60, 90], [1, 1, 0]),                                    # Example 3
    ([90, 80, 70, 60], [0, 0, 0, 0]),                             # Boundary: Strictly decreasing
    ([60, 70, 80, 90], [1, 1, 1, 0]),                             # Boundary: Strictly increasing
    ([50, 50, 50, 50], [0, 0, 0, 0]),                             # Boundary: All identical
    ([30], [0]),                                                  # Edge Case: Single element
    ([30, 100], [1, 0]),                                          # Edge Case: Two elements
    ([89, 62, 70, 58, 47, 47, 46, 76, 100, 70], [8, 1, 5, 4, 3, 2, 1, 1, 0, 0]), # Complex pattern
    ([30, 30, 31, 30, 30, 32], [2, 1, 3, 2, 1, 0]),               # Flat sections with jumps
    ([40, 35, 30, 45], [3, 2, 1, 0]),                             # Large jump after long decline
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (temperatures, expected) in enumerate(tests):
        # Deep copy to protect the test suite
        input_copy = copy.deepcopy(temperatures)
        try:
            result = func(input_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                input_disp = str(temperatures) if len(str(temperatures)) < 50 else str(temperatures)[:47] + "..."
                print(f"Test {i+1}: FAILED | Input: {input_disp} | Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {temperatures} | Exception: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def dailyTemperatures(temperatures: List[int]) -> List[int]:
    temps = temperatures
    n = len(temps)
    # pattern is mono increasing stack .. evict smaller items from stack as larger ones arrive
    stack = []
    out = [0] * n
    for i, val in enumerate(temps):
        while stack and stack[-1][1] < val:
            idx, _ = stack.pop()
            out [idx] = i - idx
        stack.append((i, val))
    
    return out

harness(dailyTemperatures)