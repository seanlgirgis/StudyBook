# LC226 — Invert Binary Tree

## Why It Is Priority
- repeat count: 3
- bucket: Trees
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: invert a binary tree (mirror horizontally)
- input shape: root of a binary tree
- output: root of the inverted tree
- constraints (inferred if needed): in-place modification of pointers

## Core Pattern
- post-order or pre-order DFS recursion
- swap left and right pointers at every node
- recursion handles swapping subtrees

## Recognition Triggers
- "invert", "mirror", "symmetric"
- structural modification of every node
- top-down or bottom-up independent swaps

## Correct Approach Outline
1. Base case: if `root` is None, return None
2. Recursively invert the left subtree
3. Recursively invert the right subtree
4. Swap `root.left` and `root.right`
5. Return `root`

## Complexity
- time: O(N)
- space: O(H) (height of tree for recursion stack)
- why: visits every node to perform O(1) swap

## Common Failure Modes
- Overwriting a child pointer before saving it to swap it
- Trying to swap node *values* instead of *pointers* (breaks subtrees)
- Missing the leaf node edge case (handled safely by Base Case)

## Implementation Checklist
- [ ] Safe `None` base case check
- [ ] Standard python swap: `root.left, root.right = root.right, root.left` (or recursive calls directly in the swap)
- [ ] Return the original root parameter

## What To Practice Next
- LC101 Symmetric Tree (checks if a tree is equal to its inverse)
- LC617 Merge Two Binary Trees (concurrent tree modification)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: fundamental structural tree modification

## Pattern Links
- Primary: Trees (DFS recursion)
