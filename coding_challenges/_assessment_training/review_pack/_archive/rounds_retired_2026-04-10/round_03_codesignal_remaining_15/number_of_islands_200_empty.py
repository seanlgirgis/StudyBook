# LeetCode 200: Number of Islands (Empty)
#
# PROBLEM STATEMENT
# Given a 2D grid of '1' (land) and '0' (water), return the number of islands.
# Islands are connected horizontally/vertically.
#
# EXAMPLE
# Grid with one connected land mass -> 1
# Grid with three disconnected land masses -> 3
#
# WHAT TO IMPLEMENT
# Implement `numIslands(grid)` (DFS/BFS/Union-Find accepted).
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
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def numIslands(grid: Grid) -> int:
    if not grid or not grid[0]:
        return 0
   
    def dfs(i,j):
        if i< 0 or j<0 or i >= len(grid) or j >= len(grid[0]) or grid[i][j] != '1':
            return
        else:
            grid[i][j] = '0'
            dfs(i, j+1)
            dfs(i, j-1)
            dfs(i-1, j)
            dfs(i+1, j)
            
    
    num_islands = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                num_islands += 1
                dfs(i,j)
    return num_islands
                
    
harness(numIslands)

