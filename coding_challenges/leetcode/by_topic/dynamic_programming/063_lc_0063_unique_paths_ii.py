"""
id: lc_0063
title: Unique Paths II
source: leetcode
difficulty: medium
primary: dynamic-programming
tags: [array, dynamic-programming, matrix]
leetcode_url: https://leetcode.com/problems/unique-paths-ii/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 063_lc_0063_unique_paths_ii.py
# LeetCode 63: Unique Paths II (Medium)
# 
# PROBLEM STATEMENT:
# You are given an m x n integer array grid. There is a robot initially located 
# at the top-left corner (i.e., grid[0][0]). The robot tries to move to the 
# bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move 
# either down or right at any point in time.
#
# An obstacle and space are marked as 1 or 0 respectively in grid. A path that 
# the robot takes cannot include any square that is an obstacle.
#
# Return the number of possible unique paths that the robot can take to reach 
# the bottom-right corner.
#
# EXAMPLES:
# Example 1:
# Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
# Output: 2
#
# Example 2:
# Input: obstacleGrid = [[0,1],[0,0]]
# Output: 1
# ============================================================================

from typing import List, Tuple, Callable
import copy

# (obstacleGrid, expected_output, description)
tests: List[Tuple[List[List[int]], int, str]] = [
    ([[0,0,0],[0,1,0],[0,0,0]], 2, "Standard 3x3 with middle obstacle"),
    ([[0,1],[0,0]], 1, "Small 2x2 with one obstacle"),
    ([[0,0],[0,0]], 2, "Small 2x2 with no obstacles"),
    ([[1,0]], 0, "Start is an obstacle"),
    ([[0,0],[0,1]], 0, "End is an obstacle"),
    ([[0]], 1, "Single cell, no obstacle"),
    ([[1]], 0, "Single cell, with obstacle"),
    ([[0,0,0],[0,0,0],[0,0,0]], 6, "3x3 grid with no obstacles"),
    ([[0,1,0],[0,1,0],[0,1,0]], 0, "Vertical wall blocking path"),
    ([[0,0,0],[1,1,1],[0,0,0]], 0, "Horizontal wall blocking path"),
    ([[0,0,1,0],[0,0,0,0],[1,1,0,0]], 4, "Larger grid with multiple scattered obstacles"),
    ([[0 for _ in range(10)] for _ in range(1)], 1, "1x10 row grid"),
    ([[0] for _ in range(10)], 1, "10x1 column grid"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (grid, expected, desc) in enumerate(tests):
        # Deep copy to prevent mutation of the test cases
        grid_copy = copy.deepcopy(grid)
        try:
            result = func(grid_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED | {desc}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | {desc}")
                print(f"   Input:    {grid if len(grid) < 5 else 'Long Input'}")
                print(f"   Expected: {expected}")
                print(f"   Actual:   {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {desc}")
            print(f"   Message:  {e}")
    
    print(f"\nFinal Result: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
from typing import   List
def uniquePathsWithObstacles(grid: List[List[int]]) -> int:
    """
    Calculates unique paths from top-left to bottom-right avoiding obstacles.
    """
    # maping all obstacles to -1 and setting top row and left col to 1s
    m, n = len(grid), len(grid[0])
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1: grid[r][c] = -1
    r = 0 
    for c in range(len(grid[0])): 
        if grid[r][c] != -1: 
            grid[r][c] = 1
        else:
            break
    c = 0
    for r in range(len(grid)): 
        if grid[r][c] != -1: 
            grid[r][c] = 1
        else:
            break
    for i in range(1,m):
        for j in range(1,n):
            if grid[i][j] == -1: continue
            if grid[i-1][j] == -1:
               grid[i][j] = grid[i][j-1]
            elif grid[i][j-1] == -1:
                grid[i][j] = grid[i-1][j]
            else:              
                grid[i][j] = grid[i-1][j] + grid[i][j-1]
    return grid[-1][-1]  if grid[-1][-1] != -1 else 0

harness(uniquePathsWithObstacles)