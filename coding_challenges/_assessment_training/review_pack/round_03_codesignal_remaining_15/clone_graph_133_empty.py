# LeetCode 133: Clone Graph (Empty)
#
# PROBLEM STATEMENT
# Given a reference to a node in a connected undirected graph, return a deep copy (clone)
# of the graph.
#
# EXAMPLE
# 1--2 (undirected)
# Clone should have same structure/values but all new node objects.
#
# WHAT TO IMPLEMENT
# Implement `Solution.cloneGraph(node)` using DFS/BFS with a map old->new.
from typing import List, Optional

class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List['Node']] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        pass

def harness() -> None:
    print("--- Running Tests for: cloneGraph ---")
    try:
        n1, n2 = Node(1), Node(2)
        n1.neighbors = [n2]
        n2.neighbors = [n1]
        out = Solution().cloneGraph(n1)
        case1 = (
            out is not None
            and out is not n1
            and out.val == 1
            and out.neighbors
            and out.neighbors[0] is not n2
            and out.neighbors[0].neighbors
            and out.neighbors[0].neighbors[0] is out
        )

        # None input should return None.
        case2 = Solution().cloneGraph(None) is None

        # Single node self-loop.
        n3 = Node(3)
        n3.neighbors = [n3]
        c3 = Solution().cloneGraph(n3)
        case3 = c3 is not None and c3 is not n3 and c3.neighbors and c3.neighbors[0] is c3

        ok = case1 and case2 and case3
        print("Test 1: PASSED" if ok else "Test 1: FAILED")
    except Exception as e:
        print(f"Test 1: ERROR | {type(e).__name__}: {e}")

harness()

