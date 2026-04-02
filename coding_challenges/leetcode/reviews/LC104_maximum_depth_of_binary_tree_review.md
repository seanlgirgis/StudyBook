# LC104 — Maximum Depth of Binary Tree

## Why It Is Priority
- repeat count: 3
- bucket: Trees
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the maximum depth (number of nodes along the longest path from root to leaf)
- input shape: root of a binary tree
- output: integer representing max depth
- constraints (inferred if needed): number of nodes 0 to 10^4

## Core Pattern
- post-order traversal / DFS recursion
- depth of a node is 1 + max(depth of left child, depth of right child)
- surface the maximum depth upwards

## Recognition Triggers
- "maximum depth", "deepest node"
- need to aggregate properties from subtrees
- tree traversal without complex state passing

## Correct Approach Outline
1. Base case: if `root` is None, return 0
2. Recursively find `left_depth = dfs(root.left)`
3. Recursively find `right_depth = dfs(root.right)`
4. Return `1 + max(left_depth, right_depth)`

## Complexity
- time: O(N)
- space: O(H) (height of the tree for recursion stack)
- why: exactly one visit per node

## Common Failure Modes
- Forgetting the base case (None node)
- Counting edges instead of nodes (problem asks for nodes, typically)
- Overcomplicating with iterative BFS when a 2-line DFS suffices

## Implementation Checklist
- [ ] Base case: `root is None`
- [ ] Recursive calls on `.left` and `.right`
- [ ] Add 1 to the max of the children

## What To Practice Next
- LC111 Minimum Depth of Binary Tree (needs careful handling of single-child nodes)
- LC110 Balanced Binary Tree (uses max depth internally)
- LC543 Diameter of Binary Tree (computes paths using depths)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: fundamental tree recursion pattern

## Pattern Links
- Primary: Trees (DFS recursion)
