# LC323 — Number of Connected Components

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: count how many disjoint connected components exist in an undirected graph
- input shape: integer `n`, array of `edges` pairs
- output: integer (number of components)
- constraints (inferred if needed): 0-indexed nodes, no duplicate edges

## Core Pattern
- BFS/DFS or Union-Find
- iterate over all nodes; if unvisited, increment counter and traverse full component
- mark all reachable nodes as visited

## Recognition Triggers
- "number of connected components", "islands"
- undirected graph with isolated clusters
- simple reachability grouping

## Correct Approach Outline
1. Build adjacency list `graph` from `edges`
2. Initialize `visited` set and `count = 0`
3. Iterate `i` from 0 to `n - 1`:
4. If `i` not in `visited`:
5. Increment `count`
6. Run DFS/BFS starting from `i` to add all connected nodes to `visited`
7. Return `count`

## Complexity
- time: O(V + E)
- space: O(V + E)
- why: standard graph building and full traversal bounds

## Common Failure Modes
- Forgetting isolated nodes with no edges (iterating only over `edges` instead of `range(n)`)
- Infinite loops in DFS/BFS (failing to add nodes to `visited` correctly)
- Building a directed graph instead of an undirected one

## Implementation Checklist
- [ ] `adj` builds edges bi-directionally (`adj[u].append(v)` and `adj[v].append(u)`)
- [ ] Loop covers all nodes `0` to `n-1`, regardless of edge presence
- [ ] Pass `visited` reference to traversal function (or use global scope)
- [ ] Inside DFS/BFS, ensure node is added to `visited` before traversing neighbors

## What To Practice Next
- LC547 Number of Provinces (exact same problem, input is adjacency matrix)
- LC200 Number of Islands (grid version)
- LC261 Graph Valid Tree (component count == 1 and edges == n - 1)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: base pattern for graph components/islands

## Pattern Links
- Primary: Graphs (connected components)
- Secondary: DFS/BFS
