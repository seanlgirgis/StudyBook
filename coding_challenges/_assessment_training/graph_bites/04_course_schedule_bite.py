# 04: Course Schedule Bite
#
# Pattern:
# - Build directed graph from prerequisites.
# - Detect cycle (cannot finish if cycle exists).
#
# One-line memory:
# "DAG is finishable; cycle is not."

from typing import List, Tuple

tests: List[Tuple[int, List[List[int]], bool]] = [
    (2, [[1, 0]], True),
    (2, [[1, 0], [0, 1]], False),
    (4, [[1, 0], [2, 1], [3, 2]], True),
]


def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    adj = [[] for _ in range(num_courses)]
    for course, pre in prerequisites:
        adj[pre].append(course)

    # 0=unvisited, 1=visiting, 2=done
    state = [0] * num_courses

    def dfs(node: int) -> bool:
        if state[node] == 1:
            return False
        if state[node] == 2:
            return True
        state[node] = 1
        for nei in adj[node]:
            if not dfs(nei):
                return False
        state[node] = 2
        return True

    for c in range(num_courses):
        if not dfs(c):
            return False
    return True


def harness() -> None:
    print("--- Course Schedule Bite ---")
    passed = 0
    for i, (n, pre, expected) in enumerate(tests, 1):
        got = can_finish(n, [x[:] for x in pre])
        if got == expected:
            print(f"Test {i}: PASSED")
            passed += 1
        else:
            print(f"Test {i}: FAILED | expected={expected}, got={got}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    harness()

