"""
GRAPH PROGRAMMING CHEATSHEET
Run this file to see all templates printed to console.
"""

CHEATSHEET = """
╔══════════════════════════════════════════════════════════════════╗
║              GRAPH PROGRAMMING QUICK REFERENCE                  ║
╚══════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. BUILD GRAPH FROM EDGE LIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from collections import defaultdict

graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # remove for directed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. DFS RECURSIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
visited = set()

def dfs(node):
    if node in visited: return
    visited.add(node)
    for neighbor in graph[node]:
        dfs(neighbor)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. DFS ITERATIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
stack = [start]
visited = set()

while stack:
    node = stack.pop()
    if node in visited: continue
    visited.add(node)
    for neighbor in graph[node]:
        stack.append(neighbor)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. BFS (shortest path / level order)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from collections import deque

queue = deque([start])
visited = {start}
steps = 0

while queue:
    for _ in range(len(queue)):   # level-by-level
        node = queue.popleft()
        if node == target: return steps
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    steps += 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. GRID NEIGHBORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRS = [(0,1),(0,-1),(1,0),(-1,0)]

for dr, dc in DIRS:
    nr, nc = r+dr, c+dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # valid neighbor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. DFS ON GRID (Islands)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def dfs(r, c):
    if r<0 or r>=rows or c<0 or c>=cols or grid[r][c]!='1':
        return
    grid[r][c] = '#'  # mark visited
    dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)

count = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':
            count += 1
            dfs(r, c)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. CYCLE DETECTION DIRECTED (DFS 3-color)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
state = [0] * n  # 0=unvisited 1=in-stack 2=done

def dfs(node):
    if state[node] == 1: return False  # cycle!
    if state[node] == 2: return True
    state[node] = 1
    for neighbor in graph[node]:
        if not dfs(neighbor): return False
    state[node] = 2
    return True

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. TOPOLOGICAL SORT — KAHN'S (BFS + in-degree)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
indegree = [0] * n
for u, v in edges:
    graph[u].append(v)
    indegree[v] += 1

queue = deque([i for i in range(n) if indegree[i] == 0])
order = []

while queue:
    node = queue.popleft()
    order.append(node)
    for neighbor in graph[node]:
        indegree[neighbor] -= 1
        if indegree[neighbor] == 0:
            queue.append(neighbor)

valid = len(order) == n  # False = has cycle

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. DIJKSTRA'S (weighted shortest path)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import heapq

dist = {node: float('inf') for node in graph}
dist[start] = 0
heap = [(0, start)]  # (distance, node)

while heap:
    d, node = heapq.heappop(heap)
    if d > dist[node]: continue
    for neighbor, weight in graph[node]:
        new_d = d + weight
        if new_d < dist[neighbor]:
            dist[neighbor] = new_d
            heapq.heappush(heap, (new_d, neighbor))

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. UNION-FIND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # path compression
    return parent[x]

def union(x, y):
    rx, ry = find(x), find(y)
    if rx == ry: return False
    if rank[rx] < rank[ry]: rx, ry = ry, rx
    parent[ry] = rx
    if rank[rx] == rank[ry]: rank[rx] += 1
    return True

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALGORITHM SELECTOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shortest path (unweighted)     → BFS
Shortest path (weighted)       → Dijkstra
Cycle in directed graph        → DFS 3-color
Cycle in undirected graph      → DFS + track parent
Topological order              → Kahn's BFS
Connected components (count)   → DFS/BFS from each node
Merge/query components fast    → Union-Find
Grid flood-fill, islands       → DFS or BFS on grid
Multi-source spread            → Multi-source BFS (seed all at once)
2-colorable graph              → BFS bipartite check
"""

print(CHEATSHEET)
