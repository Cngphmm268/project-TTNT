from collections import deque
import heapq
import time

def bfs_generator(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    q = deque([start])
    came_from = {start: None}
    yield ("visit", start)
    while q:
        cur = q.popleft()
        yield ("expand", cur)
        if cur == goal:
            break
        r, c = cur
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in came_from:
                came_from[(nr, nc)] = cur
                q.append((nr, nc))
                yield ("visit", (nr, nc))
    # reconstruct
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


def dfs_generator(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    came_from = {start: None}
    yield ("visit", start)
    while stack:
        cur = stack.pop()
        yield ("expand", cur)
        if cur == goal:
            break
        r, c = cur
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in came_from:
                came_from[(nr, nc)] = cur
                stack.append((nr, nc))
                yield ("visit", (nr, nc))
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


def dijkstra_generator(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    heap = [(0, start)]
    dist = {start: 0}
    came_from = {start: None}
    yield ("visit", start)
    while heap:
        d, cur = heapq.heappop(heap)
        yield ("expand", cur)
        if cur == goal:
            break
        r, c = cur
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                nd = d + 1
                if (nr, nc) not in dist or nd < dist[(nr, nc)]:
                    dist[(nr, nc)] = nd
                    came_from[(nr, nc)] = cur
                    heapq.heappush(heap, (nd, (nr, nc)))
                    yield ("visit", (nr, nc))
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


def astar_generator(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
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
        r, c = cur
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                tentative_g = gscore[cur] + 1
                if (nr, nc) not in gscore or tentative_g < gscore[(nr, nc)]:
                    gscore[(nr, nc)] = tentative_g
                    f = tentative_g + h((nr, nc), goal)
                    came_from[(nr, nc)] = cur
                    heapq.heappush(heap, (f, tentative_g, (nr, nc)))
                    yield ("visit", (nr, nc))
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


def get_solver_generator(name, maze, start, goal):
    name = name.lower()
    if name == "bfs":
        return bfs_generator(maze, start, goal)
    elif name == "dfs":
        return dfs_generator(maze, start, goal)
    elif name == "dijkstra":
        return dijkstra_generator(maze, start, goal)
    elif name == "a*":
        return astar_generator(maze, start, goal)
    else:
        return None
