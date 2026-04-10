# ============================================================================
# File: 017_lc_200_number_of_islands.py
#
# LeetCode 200: Number of Islands
#
# PROBLEM STATEMENT:
# You are given a grid where:
# - '1' = land
# - '0' = water
#
# An island is a connected component of land cells connected only in
# 4 directions (up/down/left/right).
#
# GOAL:
# Return how many islands exist in the grid.
#
# HOW TO THINK:
# Scan every cell.
# When you find unvisited land ('1'):
# 1) count one new island
# 2) run DFS/BFS to "sink" all connected land to '0'
# This prevents counting the same island multiple times.
# ============================================================================
from collections import deque
from typing import Callable, List, Tuple
Grid = List[List[str]]

tests: List[Tuple[Grid, int]] = [
    ([['1','1','1','1','0'],['1','1','0','1','0'],['1','1','0','0','0'],['0','0','0','0','0']], 1),
    ([['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']], 3),
    ([], 0),
    ([[]], 0),
    ([['0','0'],['0','0']], 0),
    ([['1','0','1','0','1']], 3),
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
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
def numIslands(grid: List[List[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    ret = 0
    q = deque()
    
    
    def floodIt():

        while q:
            (r,c) = q.popleft()
            # Check 4-direction neighbors from current land cell.
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                # Enqueue only valid neighboring land.
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    q.append((nr, nc))
            
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                q.append((r,c))
                grid[r][c] = '0'
                ret += 1
                floodIt()
    return ret
                
# Execute harness without __main__ block
harness(numIslands)
