# LC199 — Binary Tree Right Side View

## Why It Is Priority
- repeat count: 3
- bucket: Trees
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: return values of nodes you can see from the right side of the tree
- input shape: root of a binary tree
- output: list of node values
- constraints (inferred if needed): ordered from top to bottom

## Core Pattern
- level-order traversal (BFS)
- capture the last element of the queue on every level
- can also be done via DFS (right-first, tracking depth), but BFS is intuitive

## Recognition Triggers
- "right side view", "left side view"
- need the last/first element of each depth level
- visualizing tree from a specific horizontal direction

## Correct Approach Outline
1. If `root` is None, return `[]`
2. Initialize `queue = deque([root])` and `result = []`
3. While `queue` is not empty:
4. Get `level_size = len(queue)`
5. Loop exactly `level_size` times: pop node, add children to queue
6. On the last iteration of the loop (`i == level_size - 1`), append node value to `result`

## Complexity
- time: O(N)
- space: O(D) (max queue width; up to N/2)
- why: visits every node exactly once to construct levels

## Common Failure Modes
- Thinking the right side view is strictly the `root.right` path (it includes left children if they extend deeper)
- Appending the wrong item from the queue
- Forgetting `level_size` extraction

## Implementation Checklist
- [ ] BFS template with `level_size = len(queue)`
- [ ] Push `.left` then `.right` children
- [ ] Append the value of the last processed node in the level loop to `result`

## What To Practice Next
- LC102 Binary Tree Level Order Traversal (the foundation)
- LC515 Find Largest Value in Each Tree Row (level extraction)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: BFS level extraction application

## Pattern Links
- Primary: Trees (level-order BFS)
