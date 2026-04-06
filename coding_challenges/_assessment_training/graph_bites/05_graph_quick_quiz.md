# 05: Graph Quick Quiz

Try answering without looking up:

1. Number of Islands:
- Why do we increment count only when we first see a `'1'` before DFS?

2. Clone Graph:
- Why do we need an old->new map before cloning neighbors?

3. Course Schedule:
- What does `visiting` state mean in DFS cycle detection?

4. DFS vs BFS:
- If you need shortest path in an unweighted graph, which one is usually preferred?

5. Grid as graph:
- In 4-direction traversal, what are the 4 neighbor moves?

Expected short answers:
1. Because that cell starts a new component; DFS marks whole component visited.
2. To avoid re-cloning nodes and to handle cycles.
3. Node is currently in recursion path; seeing it again means a cycle.
4. BFS.
5. `(r+1,c), (r-1,c), (r,c+1), (r,c-1)`.

