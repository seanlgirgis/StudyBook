# ============================================================================
# File: 017_lc_200_number_of_islands_empty.py
#
# LeetCode 200: Number of Islands (Medium)
#
# PROBLEM STATEMENT:
# Given an m x n 2D binary grid grid which represents a map of '1's (land) 
# and '0's (water), return the number of islands.
#
# An island is surrounded by water and is formed by connecting adjacent lands 
# horizontally or vertically. You may assume all four edges of the grid are 
# all surrounded by water.
#
# EXAMPLES:
# 1) grid = [
#      ["1","1","1","1","0"],
#      ["1","1","0","1","0"],
#      ["1","1","0","0","0"],
#      ["0","0","0","0","0"]
#    ] 
#    Expected: 1
#
# 2) grid = [
#      ["1","1","0","0","0"],
#      ["1","1","0","0","0"],
#      ["0","0","1","0","0"],
#      ["0","0","0","1","1"]
#    ]
#    Expected: 3
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (grid, expected_num_islands)
tests: List[Tuple[List[List[str]], int]] = [
    (
        [
            ["1","1","1","1","0"],
            ["1","1","0","1","0"],
            ["1","1","0","0","0"],
            ["0","0","0","0","0"]
        ], 1
    ),                                        # Standard Example 1
    (
        [
            ["1","1","0","0","0"],
            ["1","1","0","0","0"],
            ["0","0","1","0","0"],
            ["0","0","0","1","1"]
        ], 3
    ),                                        # Standard Example 2
    ([], 0),                                  # Edge Case: Empty grid
    ([["1"]], 1),                             # Edge Case: Single element (land)
    ([["0"]], 0),                             # Edge Case: Single element (water)
    ([
        ["1","1"],
        ["1","1"]
    ], 1),                                    # Boundary: All land
    ([
        ["0","0"],
        ["0","0"]
    ], 0),                                    # Boundary: All water
    ([
        ["1","0","1"],
        ["0","1","0"],
        ["1","0","1"]
    ], 5),                                    # Boundary: Checkerboard (diagonals do not connect)
    ([
        ["1","1","1"],
        ["1","0","1"],
        ["1","1","1"]
    ], 1),                                    # Boundary: Ring/O-shape (one continuous island)
    ([
        ["1","0","0","0","0"],
        ["1","1","1","1","0"],
        ["0","0","0","1","0"],
        ["0","1","1","1","0"]
    ], 1),                                    # Boundary: Snaking island
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[List[str]]], int]) -> None:
    """
    Test harness for LeetCode #200: Number of Islands.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (grid, expected) in enumerate(tests, 1):
        try:
            # Pass a deep copy because standard BFS/DFS solutions mutate the grid
            grid_copy = [row[:] for row in grid]
            got = func(grid_copy)
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                grid_disp = f"{len(grid)}x{len(grid[0])} grid" if grid else "Empty grid"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | shape={grid_disp}")
        except Exception as e:
            grid_disp = f"{len(grid)}x{len(grid[0])} grid" if grid else "Empty grid"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | shape={grid_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

from collections import deque
# --- USER TO IMPLEMENT SOLUTION BELOW ---
def numIslands(grid: List[List[str]]) -> int:
    q = deque()
    if len(grid) == 0 or len(grid[0]) == 0: return 0
    rows, cols = len(grid), len(grid[0])
    
    def floodIt():
        while q:
            r, c = q.popleft()
            for nr, nc in ((r,c-1), (r, c+1), (r+1, c), (r-1, c)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = '0'
                    q.append((nr, nc))
                    
    nIslands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                grid[r][c] = '0'
                nIslands += 1
                q.append((r, c))
                floodIt()
    
    return nIslands
                    


# Execute harness without __main__ block
harness(numIslands)
