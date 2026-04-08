# ============================================================================
# File: clone_graph_133_empty.py
#
# LeetCode 133: Clone Graph (Medium)
#
# PROBLEM STATEMENT:
# Given a reference of a node in a connected undirected graph.
# Return a deep copy (clone) of the graph.
#
# Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.
# class Node:
#     def __init__(self, val = 0, neighbors = None):
#         self.val = val
#         self.neighbors = neighbors if neighbors is not None else []
#
# Test case format:
# For simplicity, each node's value is the same as the node's index (1-indexed). 
# For example, the first node with val == 1, the second node with val == 2, and so on. 
# The graph is represented in the test case using an adjacency list.
#
# EXAMPLES:
# 1) adjList = [[2,4],[1,3],[2,4],[1,3]] -> Expected: [[2,4],[1,3],[2,4],[1,3]]
# 2) adjList = [[]] -> Expected: [[]] (Single node, no neighbors)
# 3) adjList = [] -> Expected: [] (Empty graph)
# ============================================================================

from typing import Callable, Dict, List, Tuple, Optional, Set

# --- NODE DEFINITION ---
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

# --- TEST CASES ---
# Format: (adjList_representing_graph)
# Since the cloned graph should have the exact same adjacency list, we only need the input.
tests: List[Tuple[List[List[int]]]] = [
    ([[2, 4], [1, 3], [2, 4], [1, 3]],),       # 1. Standard square graph
    ([[]],),                                   # 2. Single node, no edges
    ([],),                                     # 3. Empty graph
    ([[2], [1]],),                             # 4. Two nodes connected to each other
    ([[2, 3], [1, 3], [1, 2]],),               # 5. Triangle graph (all connected)
    ([[2,3,4], [1,3,4], [1,2,4], [1,2,3]],),   # 6. Complete graph (K4)
    ([[2], [1, 3], [2, 4], [3, 5], [4]],),     # 7. Linear chain graph
]

# --- HARNESS HELPERS ---
def build_graph(adjList: List[List[int]]) -> Optional['Node']:
    """Builds a graph from an adjacency list and returns the first node."""
    if not adjList:
        return None
    nodes = {i + 1: Node(i + 1) for i in range(len(adjList))}
    for i, neighbors in enumerate(adjList):
        nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
    return nodes[1] if nodes else None

def get_all_nodes(node: Optional['Node']) -> Set['Node']:
    """Returns a set of all nodes in the graph starting from 'node'."""
    if not node:
        return set()
    visited = set()
    stack = [node]
    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            for neighbor in curr.neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
    return visited

def graph_to_adjList(node: Optional['Node']) -> List[List[int]]:
    """Converts a graph back to an adjacency list for easy comparison."""
    if not node:
        return []
    nodes = get_all_nodes(node)
    max_val = max(n.val for n in nodes)
    adj = [[] for _ in range(max_val)]
    for n in nodes:
        adj[n.val - 1] = sorted([neighbor.val for neighbor in n.neighbors])
    return adj

# --- TEST HARNESS ---
def harness(func: Callable[[Optional['Node']], Optional['Node']]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (adjList,) in enumerate(tests, 1):
        try:
            # Setup
            original_start_node = build_graph(adjList)
            original_nodes = get_all_nodes(original_start_node)
            original_ids = {id(n) for n in original_nodes}
            
            # Execute
            cloned_start_node = func(original_start_node)
            
            # Validate Structural Equality
            expected_adjList = adjList
            got_adjList = graph_to_adjList(cloned_start_node)
            
            if got_adjList != expected_adjList:
                print(f"Test {i}: FAILED | Structure mismatch.")
                print(f"    Expected adjList: {expected_adjList}")
                print(f"    Got adjList:      {got_adjList}")
                continue
                
            # Validate Deep Copy (Ensure no node references were reused)
            cloned_nodes = get_all_nodes(cloned_start_node)
            cloned_ids = {id(n) for n in cloned_nodes}
            
            if original_ids.intersection(cloned_ids):
                print(f"Test {i}: FAILED | Shallow copy detected. Reused original node objects.")
                continue
                
            print(f"Test {i}: PASSED")
            passed += 1
                
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | adjList={adjList}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def cloneGraph(node: Optional['Node']) -> Optional['Node']:

    # Sean style visual:
    # Think of each original node as a "house" and each neighbor edge as a "road".
    # We must build a brand-new city with the same house numbers and same roads,
    # but NONE of the original house objects can be reused.
    #
    # Main trick:
    # Keep a dictionary that answers:
    # "If I see original house X again, what cloned house did I already build for it?"
    #
    # This avoids:
    # 1) cloning the same node multiple times
    # 2) infinite recursion on cycles (A -> B -> A)
    if node is None:
        return None

    # Sean style mental model:
    # old_to_new maps each original node object -> cloned node object.
    # This is the key to both deep-copy correctness and cycle handling.
    old_to_new: Dict[Node, Node] = {}

    def dfs(cur: Node) -> Node:
        # If current original node was seen before, immediately return its clone.
        # This is the cycle breaker.
        # If already cloned, reuse clone reference (prevents infinite loops on cycles).
        if cur in old_to_new:
            return old_to_new[cur]

        # Step 1: create clone shell (value only for now).
        # Create clone first and register it BEFORE exploring neighbors.
        # That way, any back-edge can reuse this clone immediately.
        copy = Node(cur.val)
        old_to_new[cur] = copy

        # Step 2: recursively clone each neighbor and connect cloned edges.
        # "Clone my neighbor, then point to neighbor's clone."
        # Clone neighbor links recursively.
        for nei in cur.neighbors:
            copy.neighbors.append(dfs(nei))

        # Return cloned version of current node (with cloned neighbor links).
        return copy

    # Start DFS from entry node; this returns the cloned graph's entry node.
    return dfs(node)


# Execute harness without __main__ block
harness(cloneGraph)
