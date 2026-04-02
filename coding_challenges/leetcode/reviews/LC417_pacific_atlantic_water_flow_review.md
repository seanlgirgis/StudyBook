# LC417 — Pacific Atlantic Water Flow

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find all grid coordinates where water can flow to BOTH the Pacific and Atlantic oceans
- input shape: 2D integer array `heights`
- output: list of coordinate pairs `[r, c]`
- constraints (inferred if needed): water flows to equal or lower height adjacent cells

## Core Pattern
- multi-source BFS/DFS from the borders *inward* (reverse flow)
- find all cells reachable from Pacific border (flowing *up* hill)
- find all cells reachable from Atlantic border
- return intersection of both reachable sets

## Recognition Triggers
- "flows to both boundaries"
- checking reachability from an interior cell to a boundary (often O(N^2) if done naively)
- optimizing by starting at the boundary and going backwards

## Correct Approach Outline
1. Create `pac_visited` and `atl_visited` sets
2. Run DFS/BFS from top/left borders (Pacific) and add reachable cells to `pac_visited`
3. Run DFS/BFS from bottom/right borders (Atlantic) and add to `atl_visited`
4. Reversing flow condition: neighbor is valid if `heights[nr][nc] >= heights[r][c]`
5. Identify intersection: iterate through all cells and return those in both sets

## Complexity
- time: O(R * C)
- space: O(R * C)
- why: touching each cell a constant number of times via traversals

## Common Failure Modes
- Running DFS from every single cell outward (causing O((R*C)^2) TLE)
- Messing up the "reverse flow" condition (must check `>=` instead of `<=`)
- Mishandling the overlap at the corners (where a cell touches both oceans instantly)

## Implementation Checklist
- [ ] Seeds for Pacific: row 0, col 0
- [ ] Seeds for Atlantic: row `R-1`, col `C-1`
- [ ] Traversal rule: `valid range` AND `unvisited` AND `next_height >= curr_height`
- [ ] Find cells present in *both* visited reachability sets

## What To Practice Next
- LC130 Surrounded Regions (also uses boundary-first reverse search)
- LC994 Rotting Oranges (multi-source BFS)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: quintessential reverse-reachability graph problem

## Pattern Links
- Primary: Graphs (multi-source BFS/DFS)
