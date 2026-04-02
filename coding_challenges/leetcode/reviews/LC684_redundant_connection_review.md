# LC684 — Redundant Connection

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the one edge that creates a cycle in a tree (returning it)
- input shape: 2D array of edges
- output: 1D array of the redundant edge `[u, v]`
- constraints (inferred if needed): exactly N nodes and N edges, 1-indexed

## Core Pattern
- Union-Find (Disjoint Set)
- iterate over edges and union their nodes
- if two nodes of an edge are already in the same set, that edge creates the cycle

## Recognition Triggers
- "tree plus one additional edge"
- "return an edge that can be removed to make a tree"
- detecting cycles in an undirected graph dynamically

## Correct Approach Outline
1. Initialize `parent` array where `parent[i] = i` for 1 to N
2. Define `find(x)` with path compression
3. Define `union(u, v)` with union by rank (or simple merge)
4. Iterate through each `[u, v]` in edges
5. If `find(u) == find(v)`, return `[u, v]` immediately
6. Else, `union(u, v)`

## Complexity
- time: ~O(N) (specifically O(N * α(N)) with path compression and rank)
- space: O(N)
- why: processing N edges, Union-Find operations take nearly constant amortized time

## Common Failure Modes
- Using standard DFS/BFS cycle detection which is harder to implement and track the exact last edge forming the cycle
- Forgetting path compression in `find()`, causing O(N) worst-case lookups
- 0-indexing the parent array when nodes are 1-indexed

## Implementation Checklist
- [ ] `parent` array sized `N + 1` to handle 1-indexed nodes
- [ ] `find(x)` recursively sets `parent[x] = find(parent[x])`
- [ ] `union(x, y)` links the root of `x` to the root of `y`
- [ ] early exit and return when `find(u) == find(v)`

## What To Practice Next
- LC685 Redundant Connection II (directed version, much harder)
- LC323 Number of Connected Components in an Undirected Graph (basic UF application)
- LC1319 Number of Operations to Make Network Connected (counting components)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: quintessential Union-Find problem for cycle detection


## Pattern Links
- Primary: Graphs (Union-Find / cycle detection)
- Secondary: Union-Find
