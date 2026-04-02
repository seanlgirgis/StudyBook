# LC130 — Surrounded Regions

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: capture all regions surrounded by 'X' by flipping 'O's to 'X's
- input shape: 2D character array `board`
- output: modify `board` in-place
- constraints (inferred if needed): regions on the border are *not* surrounded

## Core Pattern
- BFS/DFS grid via reverse-thinking (boundary outward)
- find 'O's on the borders and mark them as safe
- all remaining 'O's are surrounded and can be flipped to 'X'

## Recognition Triggers
- "regions", "surrounded", "flipping"
- grid problem where the boundary dictates interior states
- reachability from the edge is the defining property

## Correct Approach Outline
1. Scan the 4 borders of the board for 'O's
2. Run DFS/BFS from each border 'O' to mark it and connected 'O's as safe (e.g., change to 'S')
3. Traverse entire board: change remaining 'O' to 'X' (captured)
4. Change 'S' back to 'O' (restoring safe regions)

## Complexity
- time: O(M * N)
- space: O(M * N)
- why: visits every cell a constant number of times; recursion/queue depth at most M*N

## Common Failure Modes
- Running DFS over every interior 'O', comparing to boundaries (TLE/complex)
- Missing corner cells or off-by-one on loop iterations over borders
- Forgetting to revert the safe marker ('S') back to 'O' at the end

## Implementation Checklist
- [ ] loops to find borders: first/last row, first/last col
- [ ] safe-marker DFS state prevents revisiting and infinite loops
- [ ] iterate full board explicitly to map `O -> X` and `S -> O`
- [ ] edge case: empty or 1x1 board (can just return)

## What To Practice Next
- LC200 Number of Islands (basic component counting)
- LC417 Pacific Atlantic Water Flow (similar boundary-inwards approach)
- LC695 Max Area of Island (component size measuring)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic reverse reachability pattern

## Pattern Links
- Primary: Graphs (DFS/BFS on grid)
