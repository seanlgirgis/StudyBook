"""
id: lc_0062
title: Unique Paths
source: leetcode
difficulty: medium
primary: dynamic-programming
tags: [dynamic-programming, combinatorics, math]
leetcode_url: https://leetcode.com/problems/unique-paths/
status: draft
last_updated: 2026-04-16
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 062_lc_0062_unique_paths.py
# LeetCode 62: Unique Paths (Medium)
#
# There is a robot on an m x n grid. The robot is initially located at the 
# top-left corner (i.e., grid[0][0]). The robot tries to move to the 
# bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move 
# either down or right at any point in time.
#
# Given the two integers m and n, return the number of possible unique paths 
# that the robot can take to reach the bottom-right corner.
#
# Constraints:
# - 1 <= m, n <= 100
#
# Example 1:
# Input: m = 3, n = 7
# Output: 28
#
# Example 2:
# Input: m = 3, n = 2
# Output: 3
# Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
# 1. Right -> Down -> Down
# 2. Down -> Down -> Right
# 3. Down -> Right -> Down
# ============================================================================

from typing import Callable, List, Tuple

# Tests format: (m, n, expected_output, description)
tests: List[Tuple[int, int, int, str]] = [
    (3, 7, 28, "Example 1: Standard rectangle"),
    (3, 2, 3, "Example 2: Small rectangle"),
    (1, 1, 1, "Edge Case: Single cell grid"),
    (1, 10, 1, "Edge Case: Single row"),
    (10, 1, 1, "Edge Case: Single column"),
    (2, 2, 2, "Boundary: Smallest square > 1x1"),
    (3, 3, 6, "Standard: 3x3 square"),
    (7, 3, 28, "Symmetry Check: Flipped m and n from Example 1"),
    (10, 10, 48620, "Complexity: Medium-sized square"),
    (23, 12, 193536720, "Complexity: Larger grid"),
    (1, 1, 1, "Boundary: 1x1 grid"),
    (13, 5, 1820, "Standard: Random medium dimensions"),
]

def harness(func: Callable) -> None:
    print(f"\n--- Running Harness for: {func.__name__} ---")
    passed = 0
    for m, n, expected, desc in tests:
        try:
            # Integers are immutable, no deep copy needed for m, n
            result = func(m, n)
            if result == expected:
                print(f"✅ PASSED: {desc}")
                passed += 1
            else:
                print(f"❌ FAILED: {desc}")
                print(f"    Input: m={m}, n={n}")
                print(f"    Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"🔥 ERROR: {desc}")
            print(f"    Input: m={m}, n={n}")
            print(f"    Exception: {e}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def unique_paths(m: int, n: int) -> int:
    grid: list[list[int]] = []
    for i in range(m):
        grid.append([1 for _ in range(n)])
    for i in range(1,m):
        for j in range(1,n):
            grid[i][j] = grid[i-1][j] + grid[i][j-1]
    return grid[-1][-1]
            
    

harness(unique_paths)