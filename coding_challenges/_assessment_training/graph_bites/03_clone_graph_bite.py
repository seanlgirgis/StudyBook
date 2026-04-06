# 03: Clone Graph Bite
#
# Pattern:
# - Use map old_node -> new_node.
# - DFS/BFS clone neighbors recursively/iteratively.
#
# One-line memory:
# "Create clone once per original node, reuse from map on revisits."

from typing import Dict, List, Optional


class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Optional[Node]) -> Optional[Node]:
    if node is None:
        return None

    seen: Dict[Node, Node] = {}

    def dfs(cur: Node) -> Node:
        if cur in seen:
            return seen[cur]
        copy = Node(cur.val)
        seen[cur] = copy
        for nei in cur.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy

    return dfs(node)


def harness() -> None:
    print("--- Clone Graph Bite ---")
    n1, n2 = Node(1), Node(2)
    n1.neighbors = [n2]
    n2.neighbors = [n1]
    out = clone_graph(n1)
    ok = (
        out is not None
        and out is not n1
        and out.val == 1
        and out.neighbors
        and out.neighbors[0] is not n2
        and out.neighbors[0].neighbors[0] is out
    )
    print("Test 1: PASSED" if ok else "Test 1: FAILED")


if __name__ == "__main__":
    harness()

