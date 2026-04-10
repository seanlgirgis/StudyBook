# ============================================================================
# File: 039_lc_994_rotting_oranges.py
#
# LeetCode 994: Rotting Oranges
# 
# PROBLEM STATEMENT:
# You are given a grid where each cell can be:
# - 0 = empty cell
# - 1 = fresh orange
# - 2 = rotten orange
#
# Every minute, any fresh orange (1) that is 4-directionally adjacent
# (up/down/left/right) to a rotten orange (2) becomes rotten.
#
# GOAL:
# Return the minimum number of minutes needed until no fresh oranges remain.
# If it is impossible to rot all fresh oranges, return -1.
# If there are no fresh oranges at the start, return 0.
# 
# HOW TO THINK:
# This is a multi-source BFS:
# - Start BFS from ALL rotten oranges at once.
# - One BFS layer = one minute.
# - Count fresh oranges and decrement as they rot.
# - At the end:
#   - fresh == 0 -> return minutes
#   - fresh > 0  -> return -1
# ============================================================================

from collections import deque
from typing import Callable, List, Tuple

Grid = List[List[int]]

tests: List[Tuple[Grid, int]] = [
    ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4),
    ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1),
    ([[0, 2]], 0),
    ([[1]], -1),
    ([[2]], 0),
    ([[2, 2], [2, 2]], 0),
]


def harness(func: Callable[[Grid], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (grid, expected) in enumerate(tests, 1):
        try:
            got = func([row[:] for row in grid])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got} | grid={grid}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | grid={grid}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


def orangesRotting(grid: Grid) -> int:
    # get number of fresh oranges.
    # build a q or rotton oranges
    
    q = deque()               # where to keep track of rotton oranges
    fresh = 0                 # keep track of Fresh Oranges
    rows, cols = len(grid) , len(grid[0])
    minute = 0                #each level a minute
    
    #prep
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                fresh += 1
            if grid[r][c] == 2:
                q.append((r,c))
    
    while q and fresh > 0:
        level_size = len(q)                        # snapshot of level size. Each Level adds a minute
        for _ in range(level_size):
            r, c = q.popleft()
            # check the 4 directions from this rotten orange
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                #act only if within range and Fresh Orange exist
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                   #make it rotten
                   grid[nr][nc] = 2
                   #decrement Fresh Oranges
                   fresh -= 1
                   #add to q
                   q.append((nr, nc))
        minute += 1
        
    return minute if fresh == 0 else -1
                

            
            
    


harness(orangesRotting)
