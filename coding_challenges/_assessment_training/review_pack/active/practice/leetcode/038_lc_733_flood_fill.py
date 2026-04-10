# ============================================================================
# File: 038_lc_733_flood_fill.py
#
# LeetCode 733: Flood Fill
# ============================================================================

from collections import deque
from typing import Callable, List, Tuple

Grid = List[List[int]]

tests: List[Tuple[Grid, int, int, int, Grid]] = [
    ([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2, [[2, 2, 2], [2, 2, 0], [2, 0, 1]]),
    ([[0, 0, 0], [0, 0, 0]], 0, 0, 0, [[0, 0, 0], [0, 0, 0]]),
    ([[1]], 0, 0, 2, [[2]]),
    ([[0, 1, 1], [1, 1, 0]], 1, 1, 3, [[0, 3, 3], [3, 3, 0]]),
    ([[0, 0, 0], [0, 1, 1]], 0, 0, 2, [[2, 2, 2], [2, 1, 1]]),  # Fails if logic hardcodes fill-color source as 1
    ([[2, 2, 2], [2, 3, 3]], 0, 0, 9, [[9, 9, 9], [9, 3, 3]]),  # Fails if logic only spreads through value 1
]


def harness(func: Callable[[Grid, int, int, int], Grid]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (image, sr, sc, color, expected) in enumerate(tests, 1):
        try:
            got = func([row[:] for row in image], sr, sc, color)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


def floodFill(image: Grid, sr: int, sc: int, color: int) -> Grid:
    clr = image[sr][sc]
    if clr == color : return image
    rows, cols = len(image), len(image[0])
    q = deque()
    q.append((sr,sc))
    
    while(q):
        _in_q = len(q)
        r, c = q.popleft()
        if image[r][c] == clr:
            image[r][c] = color
            
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))  :
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == clr:
                q.append((nr, nc))
    return image
            


harness(floodFill)
