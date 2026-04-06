# 01: Traversal Templates (BFS + DFS)
from collections import deque
from typing import Dict, List, Set

# Example adjacency list graph
graph: Dict[int, List[int]] = {
    1: [2, 3],
    2: [4],
    3: [4, 5],
    4: [],
    5: [],
}


def dfs(start: int, adj: Dict[int, List[int]]) -> List[int]:
    order: List[int] = []
    visited: Set[int] = set()

    def go(node: int) -> None:
        if node in visited:
            return
        visited.add(node)
        order.append(node)
        for nei in adj.get(node, []):
            go(nei)

    go(start)
    return order


def bfs(start: int, adj: Dict[int, List[int]]) -> List[int]:
    order: List[int] = []
    visited: Set[int] = {start}
    q = deque([start])

    while q:
        node = q.popleft()
        order.append(node)
        for nei in adj.get(node, []):
            if nei not in visited:
                visited.add(nei)
                q.append(nei)

    return order


if __name__ == "__main__":
    print("DFS from 1:", dfs(1, graph))
    print("BFS from 1:", bfs(1, graph))

