# LC207 — Course Schedule

## Why It Is Priority
- repeat count: 3
- bucket: Graphs
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: determine if all courses can be finished given prerequisite pairs
- input shape: integer `numCourses` and directed edges `prerequisites`
- output: boolean feasibility of completing all courses
- constraints (inferred if needed): cycle in dependency graph makes completion impossible

## Core Pattern
- Directed graph cycle detection via topological processing.
- Kahn's BFS tracks indegree-zero nodes and removes edges.
- Feasible schedule exists iff processed node count equals `numCourses`.

## Recognition Triggers
- Input describes prerequisites/dependencies between tasks.
- Need feasibility, not shortest path or path count.
- Presence of directed edges and cycle implication.
- Wording like \"can finish all\" strongly maps to cycle detection.

## Correct Approach Outline
1. Build adjacency list and indegree array from prerequisites.
2. Push all indegree-zero courses into queue.
3. Pop queue, count processed nodes, and decrement indegrees of neighbors.
4. Return `processed == numCourses`.

## Complexity
- time: O(V + E)
- space: O(V + E)
- why: each node and edge is processed a constant number of times.

## Common Failure Modes
- reversing edge direction and corrupting indegree logic
- forgetting to seed queue with all indegree-zero nodes
- using visited alone in directed graph and missing cycle cases
- comparing queue emptiness instead of processed count for final decision

## Implementation Checklist
- [ ] edge `b -> a` for prerequisite pair `[a, b]`
- [ ] compute indegree per node accurately
- [ ] enqueue every zero-indegree node initially
- [ ] decrement and enqueue neighbor when indegree hits zero
- [ ] test disconnected graph, simple cycle, and no-prerequisite cases

## What To Practice Next
- [LC210 Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)
- [LC269 Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)
- [LC323 Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/)

## Promotion Status
- status: in-progress
- source: PracticeHistory
- notes: promotion draft completed for topo-sort cycle-feasibility pattern


## Pattern Links
- Primary: Graphs (topological sort)
