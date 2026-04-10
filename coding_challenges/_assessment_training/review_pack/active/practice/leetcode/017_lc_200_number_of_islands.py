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

# --- USER TO IMPLEMENT SOLUTION BELOW ---
def numIslands(grid: List[List[str]]) -> int:
    if len(grid) == 0 or len(grid[0]) == 0:
        return 0
    ret = 0    
    
    def dfs(r: int, c: int) -> None:
        # If out of bounds or not land, stop DFS.
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return
        if grid[r][c] != '1':
            return
             
        grid[r][c] = '0'
        dfs(r, c - 1)
        dfs(r, c + 1)
        dfs(r - 1, c)
        dfs(r + 1, c)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '1':
                ret += 1
                dfs(r, c)
    return ret

# Execute harness without __main__ block
harness(numIslands)
