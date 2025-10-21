from collections import deque

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

