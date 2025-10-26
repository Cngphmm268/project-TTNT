# maze/maze_solver.py
from collections import deque
import heapq

def bfs_on_graph(graph, start, goal):
    q = deque([start])
    came_from = {start: None}
    yield ("visit", start)
    while q:
        cur = q.popleft()
        yield ("expand", cur)
        if cur == goal:
            break
        for (nbr, _) in graph.neighbors(cur):
            if nbr not in came_from:
                came_from[nbr] = cur
                q.append(nbr)
                yield ("visit", nbr)
    if goal in came_from:
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        yield ("path", path)
    else:
        yield ("path", None)


def dfs_on_graph(graph, start, goal):
    stack = [start]
    came_from = {start: None}
    yield ("visit", start)
    while stack:
        cur = stack.pop()
        yield ("expand", cur)
        if cur == goal:
            break
        for (nbr, _) in graph.neighbors(cur):
            if nbr not in came_from:
                came_from[nbr] = cur
                stack.append(nbr)
                yield ("visit", nbr)
    if goal in came_from:
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        yield ("path", path)
    else:
        yield ("path", None)


def dijkstra_on_graph(graph, start, goal):
    heap = [(0, start)]
    dist = {start: 0}
    came_from = {start: None}
    yield ("visit", start)
    while heap:
        d, cur = heapq.heappop(heap)
        yield ("expand", cur)
        if cur == goal:
            break
        for (nbr, w) in graph.neighbors(cur):
            nd = d + w
            if nbr not in dist or nd < dist[nbr]:
                dist[nbr] = nd
                came_from[nbr] = cur
                heapq.heappush(heap, (nd, nbr))
                yield ("visit", nbr)
    if goal in came_from:
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        yield ("path", path)
    else:
        yield ("path", None)


def astar_on_graph(graph, start, goal):
    def h(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    heap = [(h(start, goal), 0, start)]
    gscore = {start: 0}
    came_from = {start: None}
    yield ("visit", start)
    while heap:
        _, curg, cur = heapq.heappop(heap)
        yield ("expand", cur)
        if cur == goal:
            break
        for (nbr, w) in graph.neighbors(cur):
            tentative_g = gscore[cur] + w
            if nbr not in gscore or tentative_g < gscore[nbr]:
                gscore[nbr] = tentative_g
                f = tentative_g + h(nbr, goal)
                came_from[nbr] = cur
                heapq.heappush(heap, (f, tentative_g, nbr))
                yield ("visit", nbr)
    if goal in came_from:
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        yield ("path", path)
    else:
        yield ("path", None)


def get_solver_generator(name, graph, start, goal):
    key = name.strip().lower()
    if key == "bfs":
        return bfs_on_graph(graph, start, goal)
    elif key == "dfs":
        return dfs_on_graph(graph, start, goal)
    elif key == "dijkstra":
        return dijkstra_on_graph(graph, start, goal)
    elif key in ("a*", "astar", "a star"):
        return astar_on_graph(graph, start, goal)
    else:
        return None
