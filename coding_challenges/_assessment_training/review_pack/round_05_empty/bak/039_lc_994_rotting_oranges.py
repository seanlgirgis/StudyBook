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
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    minutes = 0
    while q and fresh > 0:
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1

    return minutes if fresh == 0 else -1


harness(orangesRotting)

