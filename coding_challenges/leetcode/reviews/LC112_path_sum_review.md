# LC112 — Path Sum

## Why It Is Priority
- repeat count: 3
- bucket: Trees
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: determine if tree has a root-to-leaf path summing exactly to `targetSum`
- input shape: root of binary tree, integer `targetSum`
- output: boolean
- constraints (inferred if needed): node values can be negative; path must end at a leaf

## Core Pattern
- pre-order traversal / DFS recursion
- subtract current node's value from targetSum as you descend
- check if remaining target is 0 upon reaching a leaf node

## Recognition Triggers
- "root-to-leaf path"
- exact sum matching
- boolean sequence checking top-down

## Correct Approach Outline
1. Base case: If `root` is None, return False
2. Subtract `root.val` from `targetSum`
3. If node is a leaf (`not root.left and not root.right`), return `targetSum == 0`
4. Recursively check `root.left` and `root.right` with updated `targetSum`
5. Return True if either child path works (`left_res or right_res`)

## Complexity
- time: O(N)
- space: O(H) (height of the tree for recursion stack)
- why: worst case visits all nodes if path not found

## Common Failure Modes
- Mistaking a node with only one child as a leaf (leaf strictly has 0 children)
- Returning True when `targetSum == 0` but *not* at a leaf node
- Mishandling negative node values (early exit optimization fails here)

## Implementation Checklist
- [ ] Check `root is None` early
- [ ] Ensure leaf condition checks BOTH `.left` and `.right` are None
- [ ] Pass the updated (subtracted) target down to children
- [ ] Use `or` to combine boolean results from children

## What To Practice Next
- LC113 Path Sum II (requires returning the actual paths via backtracking)
- LC437 Path Sum III (paths don't need to start at root or end at leaf)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic top-down state-passing tree pattern

## Pattern Links
- Primary: Trees (DFS recursion)
