# LC102 — Binary Tree Level Order Traversal

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: return the level order traversal of a binary tree's nodes' values
- input shape: root of a binary tree
- output: list of lists of integers (each inner list is one level)
- constraints (inferred if needed): number of nodes 0 to 2000

## Core Pattern
- BFS using a queue
- track level size before processing nodes in that level
- append current level's values to a sublist, then push children to queue

## Recognition Triggers
- "level order", "level by level", "shortest path"
- need to group nodes by their depth from root
- tree traversal without deep recursion (avoiding implicit stack overhead for depth grouping)

## Correct Approach Outline
1. If root is None, return `[]`
2. Initialize `queue = deque([root])` and `result = []`
3. While `queue` is not empty:
4. Get `level_size = len(queue)` and initialize `current_level = []`
5. Loop exactly `level_size` times: pop node, append value, push left/right children
6. Append `current_level` to `result`

## Complexity
- time: O(N)
- space: O(N)
- why: visits each node exactly once; queue can hold up to N/2 nodes at the bottom level

## Common Failure Modes
- Forgetting to capture `len(queue)` before the inner loop (queue size changes during loop)
- Mishandling the empty tree edge case (`root == None`)
- Appending nodes instead of their values to the result list

## Implementation Checklist
- [ ] check if root is None
- [ ] capture `level_size` out of the loop condition (`for _ in range(len(queue))`)
- [ ] only append non-None children to the queue
- [ ] append the built `current_level` list to `result` after the inner loop

## What To Practice Next
- LC103 Binary Tree Zigzag Level Order Traversal (variation using deque for level reversal)
- LC199 Binary Tree Right Side View (level order but only keeping the last element)
- LC515 Find Largest Value in Each Tree Row (level order max)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic BFS tree pattern template


## Pattern Links
- Primary: Trees (level-order BFS)
- Secondary: BFS
