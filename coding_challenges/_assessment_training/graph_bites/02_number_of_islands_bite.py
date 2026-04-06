# 02: Number of Islands Bite
#
# Pattern:
# - Scan grid.
# - When you see unvisited land ('1'), that's a new island.
# - DFS/BFS to sink/mark all connected land.
#
# One-line memory:
# "Count starts of components, flood-fill each component once."

from typing import List, Tuple

Grid = List[List[str]]

tests: List[Tuple[Grid, int]] = [
    ([["1", "1", "0"], ["0", "1", "0"], ["1", "0", "1"]], 3),
    ([["1", "1"], ["1", "1"]], 1),
    ([["0", "0"], ["0", "0"]], 0),
    ([], 0),
]


def num_islands(grid: Grid) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count


def harness() -> None:
    print("--- Number of Islands Bite ---")
    passed = 0
    for i, (grid, expected) in enumerate(tests, 1):
        got = num_islands([row[:] for row in grid])
        if got == expected:
            print(f"Test {i}: PASSED")
            passed += 1
        else:
            print(f"Test {i}: FAILED | expected={expected}, got={got}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    harness()

