# LC210 — Course Schedule II

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: find a valid ordering of courses given prerequisite pairs
- input shape: numCourses, prerequisites pairs `[course, prereq]`
- output: array of course ordering (or empty array if impossible)
- constraints (inferred if needed): numCourses <= 2000, may contain cycles

## Core Pattern
- topological sort (Kahn's algorithm using BFS)
- track in-degrees of all nodes
- process nodes with 0 in-degree using a queue

## Recognition Triggers
- dependencies, prerequisites, ordering, scheduling
- directed graph structures
- needs to detect cycles (impossible to complete all courses)

## Correct Approach Outline
1. Build adjacency list `graph` and `in_degree` array
2. Find all courses with 0 in-degree and add to `queue`
3. While `queue` is not empty, pop `node` and append to `result`
4. For each neighbor of `node`, decrement its in-degree
5. If neighbor's in-degree becomes 0, add to `queue`
6. Return `result` if its length equals numCourses, else `[]`

## Complexity
- time: O(V + E)
- space: O(V + E)
- why: visits every node and edge once to build graph and process queue

## Common Failure Modes
- Building the adjacency list backwards (e.g., `course -> prereq` instead of `prereq -> course`)
- Forgetting to check if `len(result) == numCourses` at the end (for cycle detection)
- Not initializing the graphs and in-degrees correctly for independent nodes

## Implementation Checklist
- [ ] `adj_list` maps prerequisite to its dependent courses
- [ ] `in_degree` counts incoming edges correctly
- [ ] Initialize queue with *all* 0 in-degree nodes
- [ ] Check `result` size equals `numCourses` before returning

## What To Practice Next
- LC207 Course Schedule (boolean cycle check only)
- LC269 Alien Dictionary (topo sort with string comparison logic)
- LC329 Longest Increasing Path in a Matrix (topo sort on grid)

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic Kahn's algorithm topological sort

## Pattern Links
- Primary: Graphs (topological sort)
- Secondary: BFS (Kahn's algorithm)
