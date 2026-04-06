# 00: Graph Mental Model

What is a graph?
- Nodes (things)
- Edges (connections)

In interview problems, graph is often hidden:
- Grid -> each cell is a node, neighbors are edges.
- Courses with prerequisites -> course is node, prerequisite relation is directed edge.
- Cloning network objects -> each object is a node, neighbor list is edges.

Three core graph questions:
1. Reachability: "Can I get there?"
2. Components: "How many disconnected groups?"
3. Cycles/order: "Can dependencies be completed?"

Two core tools:
- DFS (stack/recursion): go deep first.
- BFS (queue): go level by level.

Golden rule:
- Always track `visited`, or mark in-place.

One-sentence pattern:
"When I see connected/reachable/cycle words, I model nodes+edges and traverse with DFS/BFS plus visited."

