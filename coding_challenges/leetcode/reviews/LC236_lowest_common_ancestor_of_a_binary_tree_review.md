# LC236 — Lowest Common Ancestor of a Binary Tree

## Why It Is Priority
- repeat count: 6
- bucket: Trees
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find the lowest common ancestor (LCA) of two given nodes in a binary tree
- input shape: root node, node `p`, node `q`
- output: node that is the LCA
- constraints (inferred if needed): p and q exist in the tree, all node values unique

## Core Pattern
- post-order traversal / recursion
- surface findings from bottom to top
- LCA is the node where both left and right subtrees return a target, or a target matches the node itself

## Recognition Triggers
- "lowest common ancestor"
- binary tree (not necessarily BST)
- need to combine search results from multiple subtrees

## Correct Approach Outline
1. Base case: If `root` is None, return None
2. Base case: If `root` is `p` or `root` is `q`, return `root`
3. Recursively search left subtree: `left_lca = dfs(root.left, p, q)`
4. Recursively search right subtree: `right_lca = dfs(root.right, p, q)`
5. If both `left_lca` and `right_lca` are not None: `root` is the LCA
6. Otherwise, return the non-None child (or None)

## Complexity
- time: O(N)
- space: O(H) (height of tree for recursion stack)
- why: touches every node once in worst case

## Common Failure Modes
- Over-complicating by trying to store paths to p and q and comparing them
- Mishandling the case where `p` is an ancestor of `q` (handled automatically if returning root)
- Storing parent pointers when recursion naturally achieves the same result

## Implementation Checklist
- [ ] Base cases check for `p` and `q` match, returning immediately
- [ ] Process left and right subtrees independently
- [ ] Check if *both* subtrees yielded a result
- [ ] Propagate the single valid result upward if only one matched

## What To Practice Next
- LC235 Lowest Common Ancestor of a Binary Search Tree (can use BST property)
- LC1644 Lowest Common Ancestor of a Binary Tree II (p and q not guaranteed to exist)
- LC2096 Step-By-Step Directions From a Binary Tree Node to Another (uses LCA concept)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: core recursive tree aggregation problem

## Pattern Links
- Primary: Trees (post-order recursion)
- Secondary: DFS