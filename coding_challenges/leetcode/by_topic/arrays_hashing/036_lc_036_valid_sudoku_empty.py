"""
id: lc_0036
title: Valid Sudoku
source: leetcode
difficulty: medium
primary: hash-table
tags: [hash-table, matrix, set]
leetcode_url: https://leetcode.com/problems/valid-sudoku/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: Use sets to track seen numbers for each row, column, and 3x3 sub-box.
- time: O(1) since the board is always 9x9.
- space: O(1) since the board is always 9x9.
"""

# ============================================================================
# File: 036_lc_036_valid_sudoku_empty.py
# Problem 36: Valid Sudoku (Medium)
# 
# PROBLEM STATEMENT:
# Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be 
# validated according to the following rules:
# 1. Each row must contain the digits 1-9 without repetition.
# 2. Each column must contain the digits 1-9 without repetition.
# 3. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 
#    without repetition.
#
# Note:
# - A Sudoku board (partially filled) could be valid but is not necessarily solvable.
# - Only the filled cells need to be validated according to the mentioned rules.
#
# EXAMPLES:
# Input: board = 
# [["5","3",".",".","7",".",".",".","."]
# ,["6",".",".","1","9","5",".",".","."]
# ,[".","9","8",".",".",".",".","6","."]
# ,["8",".",".",".","6",".",".",".","3"]
# ,["4",".",".","8",".","3",".",".","1"]
# ,["7",".",".",".","2",".",".",".","6"]
# ,[".","6",".",".",".",".","2","8","."]
# ,[".",".",".","4","1","9",".",".","5"]
# ,[".",".",".",".","8",".",".","7","9"]]
# Output: true
# ============================================================================

from typing import List, Tuple, Callable

# Helper to generate a blank 9x9 board
def blank_board():
    return [["." for _ in range(9)] for _ in range(9)]

# Test Cases: List[Tuple[board, expected]]
tests: List[Tuple[List[List[str]], bool]] = []

# Case 1: Standard Valid Example
tc1 = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"]
]
tests.append((tc1, True))

# Case 2: Invalid Row (Two 8s in the first row)
tc2 = [row[:] for row in tc1]
tc2[0][2] = "8"
tc2[0][8] = "8"
tests.append((tc2, False))

# Case 3: Invalid Column (Two 7s in the first column)
tc3 = [row[:] for row in tc1]
tc3[0][0] = "7"
tc3[6][0] = "7"
tests.append((tc3, False))

# Case 4: Invalid Sub-box (Two 3s in the top-left 3x3)
tc4 = [row[:] for row in tc1]
tc4[0][0] = "3"
tc4[2][2] = "3"
tests.append((tc4, False))

# Case 5: Empty Board
tests.append((blank_board(), True))

# Case 6: Single Digit
tc6 = blank_board()
tc6[4][4] = "5"
tests.append((tc6, True))

# Case 7: Full Valid Board (Completed Sudoku)
tc7 = [
    ["5","3","4","6","7","8","9","1","2"],
    ["6","7","2","1","9","5","3","4","8"],
    ["1","9","8","3","4","2","5","6","7"],
    ["8","5","9","7","6","1","4","2","3"],
    ["4","2","6","8","5","3","7","9","1"],
    ["7","1","3","9","2","4","8","5","6"],
    ["9","6","1","5","3","7","2","8","4"],
    ["2","8","7","4","1","9","6","3","5"],
    ["3","4","5","2","8","6","1","7","9"]
]
tests.append((tc7, True))

# Case 8: Duplicate on boundary of sub-boxes
tc8 = blank_board()
tc8[0][2] = "1" # Box 0,0
tc8[0][3] = "1" # Box 0,1 (Valid globally for boxes, but invalid for row)
tests.append((tc8, False))

# Case 9: Numbers 1 and 9 at opposite ends
tc9 = blank_board()
tc9[0][0] = "1"
tc9[8][8] = "9"
tests.append((tc9, True))

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (board, expected) in enumerate(tests):
        # Deep copy the board to prevent mutation
        board_copy = [row[:] for row in board]
        
        try:
            result = func(board_copy)
            
            # Simplified display for large matrix
            display = f"Board {i+1}"
            
            if result == expected:
                print(f"Test {i+1}: PASSED | {display}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | {display}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {display}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
'''
import itertools

# 1. COLUMN ITERATOR (e.g., Column 4)
col_4_iterator = ((r, 3) for r in range(9))

# 2. ROW ITERATOR (e.g., Row 4)
row_4_iterator = ((3, c) for c in range(9))

# 3. INNER 3x3 SQUARE ITERATOR (e.g., starting at 3,3)
r_start, c_start = 3, 3
square_3x3_iterator = itertools.product(range(r_start, r_start + 3), range(c_start, c_start + 3))

# 4. STARTERS OF ALL INNER SQUARES (The 9 top-left corners)
square_starters_iterator = itertools.product(range(0, 9, 3), range(0, 9, 3))

'''
import itertools

def isValidSudoku(board: List[List[str]]) -> bool:
    """
    Validates a 9x9 Sudoku board based on rows, columns, and 3x3 boxes.
    """
    def is_valid(coords_iterator):
        seen = set()
        for r, c in coords_iterator:
            if board[r][c] in seen:
                return False
            if board[r][c] != ".":
                seen.add(board[r][c])
        return True
    # rows and columns
    for i in range(9):
        iterator = ((i, x) for x in range(9))
        if not is_valid(iterator):
            return False
        iterator = ((x, i) for x in range(9))
        if not is_valid(iterator):
            return False
    square_starters_iterator = itertools.product(range(0, 9, 3), range(0, 9, 3))
    
    for r,c in square_starters_iterator:
        square_3x3_iterator = itertools.product(range(r, r + 3), range(c, c + 3))
        if not is_valid(square_3x3_iterator):
            return False
    return True

harness(isValidSudoku)