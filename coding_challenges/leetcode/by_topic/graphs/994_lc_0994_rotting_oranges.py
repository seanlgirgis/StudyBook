"""
id: lc_0994
title: Rotting Oranges
source: leetcode
difficulty: medium
primary: arrays
tags: [arrays, bfs, matrix, graph, multi_source_bfs]
leetcode_url: https://leetcode.com/problems/rotting-oranges/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 994_lc_0994_rotting_oranges.py
# Problem: LC 994 - Rotting Oranges (Medium)
# 
# PROBLEM STATEMENT:
# You are given an m x n grid where each cell can have one of three values:
# - 0 representing an empty cell,
# - 1 representing a fresh orange, or
# - 2 representing a rotten orange.
#
# Every minute, any fresh orange that is 4-directionally adjacent to a rotten 
# orange becomes rotten.
#
# Return the minimum number of minutes that must elapse until no cell has a 
# fresh orange. If this is impossible, return -1.
#
# EXAMPLES:
# Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
# Output: 4
#
# Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
# Output: -1
#
# Input: grid = [[0,2]]
# Output: 0
# ============================================================================

from typing import List, Tuple, Callable
import copy

# Test cases: (input_grid, expected_output, description)
tests: List[Tuple[List[List[int]], int, str]] = [
    ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4, "Standard Example 1: Multiple minutes"),
    ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1, "Standard Example 2: Impossible reach"),
    ([[0, 2]], 0, "Standard Example 3: Only empty and rotten"),
    ([[1]], -1, "Edge Case: Single fresh orange"),
    ([[2]], 0, "Edge Case: Single rotten orange"),
    ([[0]], 0, "Edge Case: Single empty cell"),
    ([[1, 2, 1, 1]], 2, "Linear Grid: Rotting from middle"),
    ([[2, 2, 2], [2, 2, 2]], 0, "Boundary: All rotten initially"),
    ([[1, 1, 1], [1, 1, 1]], -1, "Boundary: All fresh (no rotten source)"),
    ([[2, 1], [1, 1]], 2, "Small Grid: 2x2 propagation"),
    ([[2, 0, 1], [0, 0, 0], [1, 0, 2]], -1, "Disconnected Components: Some oranges isolated"),
    ([[2, 1, 1], [1, 1, 1], [0, 1, 2]], 2, "Multiple Sources: Rotting from opposite corners"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for i, (grid, expected, desc) in enumerate(tests):
        # Create a deep copy to prevent mutation during testing
        grid_copy = copy.deepcopy(grid)
        
        try:
            result = func(grid_copy)
            if result == expected:
                print(f"Test {i+1} PASSED: {desc}")
                passed += 1
            else:
                print(f"Test {i+1} FAILED: {desc}")
                print(f"   Input:    {grid}")
                print(f"   Expected: {expected}")
                print(f"   Actual:   {result}")
        except Exception as e:
            print(f"Test {i+1} ERROR: {desc}")
            print(f"   Exception: {e}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
from collections impoort deqeue
def orangesRotting(grid: List[List[int]]) -> int:
    """
    Determine the minimum time until all oranges are rotten.
    """
    pass

harness(orangesRotting)