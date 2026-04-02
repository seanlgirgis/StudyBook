# LC200 — Number of Islands

## Why It Is Priority
- repeat count: 4
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: count connected components of land cells in a 2D grid
- input shape: `m x n` grid of `'1'` (land) and `'0'` (water)
- output: number of distinct islands
- constraints (inferred if needed): connectivity is 4-directional (up/down/left/right)

## Core Pattern
- Grid traversal as connected-components counting.
- On each unseen land cell, launch DFS/BFS flood fill.
- Mark visited cells so each land cell is processed once.

## Recognition Triggers
- 2D grid with land/water and need to count separate groups.
- Connectivity is directional (usually 4-neighbor) and component-based.
- "Count islands/regions/clusters" language appears explicitly.
- Repeated exploration from every cell is too slow without visited control.

## Correct Approach Outline
1. Iterate every grid cell; when an unvisited land cell is found, increment island count.
2. Start DFS/BFS flood-fill from that cell.
3. Mark all reachable land cells in that component as visited.
4. Continue scan; each new unvisited land start represents a new island.

## Complexity
- time: O(m * n)
- space: O(m * n) worst case (visited set/recursion/queue)
- why: each cell is visited at most once during scan + traversal.

## Common Failure Modes
- forgetting to mark visited immediately, causing duplicate traversal
- counting each land cell instead of each new component start
- using 8-direction neighbors when problem requires 4-direction
- missing boundary guards and causing out-of-range access

## Implementation Checklist
- [ ] only start traversal from unvisited land cells
- [ ] enforce bounds checks before exploring neighbors
- [ ] mark visited immediately to avoid duplicate enqueues/recursion loops
- [ ] use consistent 4-direction neighbor set
- [ ] test empty grid, all water, all land, and single-cell cases

## What To Practice Next
- [LC695 Max Area of Island](https://leetcode.com/problems/max-area-of-island/)
- [LC994 Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)
- [LC130 Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: priority pass filled for BFS/DFS component-recognition signals


## Pattern Links
- Primary: BFS/DFS grid
