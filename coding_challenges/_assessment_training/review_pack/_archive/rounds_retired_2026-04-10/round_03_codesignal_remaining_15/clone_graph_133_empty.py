# LeetCode 133: Clone Graph

from typing import Callable, Dict, List, Optional, Tuple


# --- NODE DEFINITION ---
class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List['Node']] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

# --- GRAPH BUILDER & VERIFIER HELPER ---
def build_graph(adjList: List[List[int]]) -> Optional[Node]:
    """Builds a graph from a 1-indexed adjacency list."""
    if not adjList:
        return None
    # Empty list inside list `[[]]` means 1 node with no neighbors
    if len(adjList) == 1 and not adjList[0]:
        return Node(1)
        
    nodes = {i: Node(i) for i in range(1, len(adjList) + 1)}
    for i, neighbors in enumerate(adjList, 1):
        nodes[i].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]

def verify_clone(node1: Optional[Node], node2: Optional[Node], visited: Optional[set] = None) -> bool:
    """Recursively verifies structural match AND strict memory separation."""
    if not node1 and not node2: return True
    if not node1 or not node2: return False
    
    if visited is None: 
        visited = set()
        
    if node1.val in visited: 
        return True
        
    # STRICT CHECK: Ensure it is actually cloned and not the same memory address
    if id(node1) == id(node2): 
        return False 
    if node1.val != node2.val: 
        return False
    if len(node1.neighbors) != len(node2.neighbors): 
        return False
        
    visited.add(node1.val)
    for n1, n2 in zip(node1.neighbors, node2.neighbors):
        if not verify_clone(n1, n2, visited):
            return False
    return True

# --- TEST CASES ---
# Format: (adjacency_list)
clone_graph_tests: List[List[List[int]]] = [
    [[2, 4], [1, 3], [2, 4], [1, 3]], # 1. Standard LC Example 1 (Square)
    [[]],                             # 2. Standard LC Example 2 (Single node)
    [],                               # 3. Standard LC Example 3 (Empty graph)
    [[2], [1]],                       # 4. Two connected nodes
    [[2, 3], [1, 3], [1, 2]],         # 5. Triangle (Complete graph of 3)
    [[2, 5], [1, 3], [2, 4], [3, 5], [1, 4]], # 6. Pentagon (Cycle of 5)
    [[2], [1, 3], [2]],               # 7. Linear chain of 3
    [[2, 3, 4], [1], [1], [1]]        # 8. Star graph (1 central node connected to 3)
]

# --- TEST HARNESS ---
def test_harness(func: Callable[[Optional[Node]], Optional[Node]], test_cases: List[List[List[int]]]) -> None:
    """
    Test harness for LeetCode #133: Clone Graph.
    Validates Graph DFS/BFS traversal and Deep Copy hash mapping.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    for i, adjList in enumerate(test_cases):
        try:
            original_graph = build_graph(adjList)
            
            # Strict typed execution
            cloned_graph: Optional[Node] = func(original_graph)
            
            if verify_clone(original_graph, cloned_graph):
                display_adj = f"{adjList[:3]}..." if len(adjList) > 3 else f"{adjList}"
                print(f"Test {i+1}: PASSED (adjList={display_adj})")
                passed += 1
            else:
                display_adj = f"{adjList[:3]}..." if len(adjList) > 3 else f"{adjList}"
                print(f"Test {i+1}: FAILED | adjList={display_adj}")
                print(f"    Validation failed: Mismatched structure or shallow copy detected.")
        except Exception as e:
            display_adj = f"{adjList[:3]}..." if len(adjList) > 3 else f"{adjList}"
            print(f"Test {i+1}: ERROR  | adjList={display_adj} | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")
    
    
    




# --- USER TO IMPLEMENT SOLUTION BELOW ---
def cloneGraph(node: Optional['Node']) -> Optional['Node']:

    if node is None:
        return None

    old_to_new: Dict[Node, Node] = {}

    def dfs(cur: Node) -> Node:
        if cur in old_to_new:
            return old_to_new[cur]

        copy = Node(cur.val)
        old_to_new[cur] = copy

        for nei in cur.neighbors:
            copy.neighbors.append(dfs(nei))

        return copy

    return dfs(node)
        
 

# Execute harness without __main__ block
test_harness(cloneGraph, clone_graph_tests)

