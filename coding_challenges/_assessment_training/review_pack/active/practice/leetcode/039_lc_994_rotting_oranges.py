# ============================================================================
# File: 039_lc_994_rotting_oranges.py
#
# LeetCode 994: Rotting Oranges
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
    # Sean style:
    # Multi-source BFS.
    # Start BFS from ALL initially rotten oranges simultaneously.
    # Each BFS layer = 1 minute of spread.
    # 2 Rotten 1 Fresh 0 no Orange
    
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    q = deque()                        #keep Track of rotten Oranges
    fresh = 0                            #keep track of nmber of Fresh oranges
    ret = 0                              #number of minutes .. -1 for left over Fresh Oranges
    
    #prep work
    # Fill q and keep track of Fresh Oranges
    
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
        ret += 1
        
    return ret if fresh == 0 else -1
            
    


harness(orangesRotting)
