"""
id: lc_0064
title: Minimum Path Sum
source: leetcode
difficulty: medium
primary: dynamic programming
tags: [arrays, dynamic-programming, matrix]
leetcode_url: https://leetcode.com/problems/minimum-path-sum/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 064_lc_0064_minimum_path_sum.py
# LC064: Minimum Path Sum (Medium)
# 
# PROBLEM STATEMENT:
# Given a m x n grid filled with non-negative numbers, find a path from top 
# left to bottom right, which minimizes the sum of all numbers along its path.
# 
# Note: You can only move either down or right at any point in time.
#
# EXAMPLES:
# Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
# Output: 7
# Explanation: Because the path 1 -> 3 -> 1 -> 1 -> 1 minimizes the sum.
#
# Input: grid = [[1,2,3],[4,5,6]]
# Output: 12
# ============================================================================

from typing import List, Tuple, Callable

# Test cases: (grid, expected_output, description)
tests: List[Tuple[List[List[int]], int, str]] = [
    ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7, "Standard 3x3 grid"),
    ([[1, 2, 3], [4, 5, 6]], 12, "Standard 2x3 rectangle"),
    ([[1]], 1, "Edge Case: 1x1 grid"),
    ([[1, 2, 5]], 8, "Edge Case: Single row"),
    ([[1], [2], [5]], 8, "Edge Case: Single column"),
    ([[1, 1], [1, 1]], 3, "Boundary: All elements identical"),
    ([[0, 0], [0, 0]], 0, "Boundary: All elements zero"),
    ([[1, 9, 1], [1, 9, 1], [1, 1, 1]], 5, "Path involving non-obvious greedy choice"),
    ([[1, 2], [1, 1], [4, 1]], 4, "Tall grid 3x2"),
    ([[1, 5, 1], [1, 1, 1], [5, 5, 1]], 5, "Path along bottom and right edges"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (grid, expected, desc) in enumerate(tests):
        # Deep copy the grid to prevent mutations during testing
        grid_copy = [row[:] for row in grid]
        
        try:
            result = func(grid_copy)
            if result == expected:
                print(f"Test Case {i+1} [PASSED]: {desc}")
                passed += 1
            else:
                print(f"Test Case {i+1} [FAILED]: {desc}")
                print(f"   Input: {grid}")
                print(f"   Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test Case {i+1} [ERROR]: {desc}")
            print(f"   Exception: {e}")

    print(f"\n--- Result: {passed}/{len(tests)} cases passed ---")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def minPathSum(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    rr, rc = range(rows), range(cols)
    
    for r in rr:
        for c in rc:
            if r == 0 and c == 0:
                continue
            elif r == 0:
                grid[r][c] += grid[r][c-1]
            elif c == 0:
                grid[r][c] += grid[r-1][c]
            else:
                grid[r][c] += min(grid[r-1][c], grid[r][c-1])
    return grid[-1][-1]

harness(minPathSum)