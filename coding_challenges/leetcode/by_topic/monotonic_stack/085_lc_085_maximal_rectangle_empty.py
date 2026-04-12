"""
id: lc_0085
title: Maximal Rectangle
source: leetcode
difficulty: hard
primary: stack
tags: [stack, monotonic-stack, dynamic-programming, matrix]
leetcode_url: https://leetcode.com/problems/maximal-rectangle/
status: draft
last_updated: 2026-04-12
notes:
- key idea: For each row, compute the histogram of heights (consecutive 1s above).
            Then run Largest Rectangle in Histogram (LC 84) on each row's heights.
- time: O(rows * cols)
- space: O(cols)
"""

# ============================================================================
# File: 085_lc_085_maximal_rectangle_empty.py
# Problem 85: Maximal Rectangle (Hard)
#
# PROBLEM STATEMENT:
# Given a rows x cols binary matrix filled with '0's and '1's, find the
# largest rectangle containing only '1's and return its area.
#
# EXAMPLES:
# Input: matrix = [["1","0","1","0","0"],
#                  ["1","0","1","1","1"],
#                  ["1","1","1","1","1"],
#                  ["1","0","0","1","0"]]
# Output: 6
#
# Input: matrix = [["0"]]
# Output: 0
#
# Constraints:
# - rows == matrix.length, cols == matrix[i].length
# - 1 <= rows, cols <= 200
# - matrix[i][j] is '0' or '1'
# ============================================================================

from typing import List, Tuple, Callable

# Test Cases: List[Tuple[matrix, expected]]
tests: List[Tuple[List[List[str]], int]] = [
    (                                                           # Standard LeetCode example
        [["1","0","1","0","0"],
         ["1","0","1","1","1"],
         ["1","1","1","1","1"],
         ["1","0","0","1","0"]],
        6
    ),
    (                                                           # All 1s 2x2 → full grid
        [["1","1"],
         ["1","1"]],
        4
    ),
    (                                                           # All 1s 3x3 → full grid
        [["1","1","1"],
         ["1","1","1"],
         ["1","1","1"]],
        9
    ),
    (                                                           # All 0s → no rectangle
        [["0","0"],
         ["0","0"]],
        0
    ),
    (                                                           # Single cell 1
        [["1"]],
        1
    ),
    (                                                           # Single cell 0
        [["0"]],
        0
    ),
    (                                                           # Single row of all 1s
        [["1","1","1","1"]],
        4
    ),
    (                                                           # Single column of all 1s
        [["1"],["1"],["1"],["1"]],
        4
    ),
    (                                                           # Wide top, blocked bottom → best is top row
        [["1","1","1","1","1"],
         ["0","0","0","0","0"]],
        5
    ),
    (                                                           # Growing then shrinking → best is middle rows
        [["0","1","1","0"],
         ["1","1","1","1"],
         ["1","1","1","1"],
         ["0","1","1","0"]],
        8
    ),
    (                                                           # Two islands, no bridge → best is one island
        [["1","1","0","1","1"],
         ["1","1","0","1","1"],
         ["0","0","0","0","0"],
         ["1","1","0","1","1"]],
        4
    ),
    (                                                           # Staircase up → row 3 heights=[4,3,2,1], best rect is 3x2 or 2x3=6
        [["1","0","0","0"],
         ["1","1","0","0"],
         ["1","1","1","0"],
         ["1","1","1","1"]],
        6
    ),
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0

    print(f"\n--- Testing: {func.__name__} ---")

    for i, (matrix, expected) in enumerate(tests):
        # Deep copy matrix to prevent mutation
        matrix_copy = [row[:] for row in matrix]

        try:
            result = func(matrix_copy)

            rows = len(matrix)
            cols = len(matrix[0])
            display = f"{rows}x{cols} matrix"

            if result == expected:
                print(f"Test {i+1:02d}: PASSED | {display}")
                passed += 1
            else:
                print(f"Test {i+1:02d}: FAILED | {display}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1:02d}: ERROR  | matrix={matrix}")
            print(f"   Exception: {e}")
            failed += 1

    print(f"\n--- Result: {passed} Passed, {failed} Failed ---\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def maximalRectangle(matrix: List[List[str]]) -> int:
    def pass_one():
        out = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == "1":       # ← cell is 1
                    val = 1
                    if r > 0:
                        val += out[r-1][c]
                else:                          # ← cell is 0, same indent as outer if
                    val = 0
                out[r][c] = val
        return (out)
        
    def largestRecInHistogram(heights: List[int]) -> int:
        """
        Calculates the largest rectangle area in the histogram using a monotonic stack.
        """
        #mono increasing array .. evict when cur is smaller .. inherit the evicted indexes
        stack = []
        max_area = 0
        for i, h in enumerate(heights):
            idx = i
            while stack and h <= stack[-1][0]:
                ph, p_id = stack.pop()
                idx = p_id
                max_area = max(max_area, ph * (i - p_id))
                
            stack.append((h,idx))
        while stack:
            p_h , p_id = stack.pop()
            max_area = max(max_area, p_h * (len(heights) - p_id))
        return max_area
    max_area = 0    
    histograms = pass_one()    
    for histo in histograms:
        max_area = max(max_area, largestRecInHistogram(histo))
    return (max_area)
        
        

harness(maximalRectangle)
