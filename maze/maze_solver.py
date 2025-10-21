from collections import deque
<<<<<<< HEAD
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
=======

def solve_maze(self):
    start = self.start
    goal = self.goal
    queue = deque([start])
    came_from = {start: None}

    while queue:
        y, x = queue.popleft()
        if (y, x) == goal:
            break
        for dy, dx in [(0,1),(1,0),(0,-1),(-1,0)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < ROWS and 0 <= nx < COLS and self.maze[ny][nx] == 0 and (ny, nx) not in came_from:
                came_from[(ny, nx)] = (y, x)
                queue.append((ny, nx))

    # Vẽ đường đi 
    cell = goal
    while cell and cell in came_from:
        y, x = cell
        if (y, x) != goal and (y, x) != start:  # Không vẽ đè lên đích hoặc điểm bắt đầu
            x1, y1 = x*CELL_SIZE, y*CELL_SIZE
            x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="gray")
        cell = came_from[cell]

    self.reset_player()

    # Giữ nguyên đích (xanh lá)
    gx, gy = self.goal[1], self.goal[0]
    self.canvas.create_rectangle(gx*CELL_SIZE, gy*CELL_SIZE,
                                 (gx+1)*CELL_SIZE, (gy+1)*CELL_SIZE, fill="green", outline="gray")

>>>>>>> 81b7f8c56fbafc87a70c3eb4fbe733100dfd6e33
