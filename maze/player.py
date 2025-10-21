class Player:
<<<<<<< HEAD
    def __init__(self, canvas, r, c, cell_size, maze, goal):
        self.canvas = canvas
        self.r = r
        self.c = c
        self.cell_size = cell_size
        self.maze = maze
        self.goal = goal
        # create oval based on cell coords
        pad = 5
        x1 = c * cell_size + pad
        y1 = r * cell_size + pad
        x2 = (c+1) * cell_size - pad
        y2 = (r+1) * cell_size - pad
        self.icon = self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="")

    def move(self, dc, dr):
        # note: move signature as (dc, dr) in some calls; unify usage to (dc, dr)
        # but our app will call (dc, dr) consistent
        new_r = self.r + dr
        new_c = self.c + dc
        rows, cols = len(self.maze), len(self.maze[0])
        if 0 <= new_r < rows and 0 <= new_c < cols and self.maze[new_r][new_c] == 0:
            dx = (new_c - self.c) * self.cell_size
            dy = (new_r - self.r) * self.cell_size
            self.canvas.move(self.icon, dx, dy)
            self.r, self.c = new_r, new_c
            if (self.r, self.c) == self.goal:
                self.canvas.create_text(cols * self.cell_size // 2, rows * self.cell_size // 2,
                                        text="🎉 Bạn đã thắng!", fill="red", font=("Arial", 18, "bold"))
=======
    def __init__(self, canvas, x, y, cell_size, maze, goal):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.maze = maze
        self.goal = goal
        self.icon = self.canvas.create_oval(5, 5, cell_size - 5, cell_size - 5, fill="blue")

    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        rows, cols = len(self.maze), len(self.maze[0])
        if 0 <= nx < cols and 0 <= ny < rows and self.maze[ny][nx] == 0:
            self.x, self.y = nx, ny
            self.canvas.move(self.icon, dx * self.cell_size, dy * self.cell_size)
            if (ny, nx) == self.goal:
                self.canvas.create_text(cols * self.cell_size // 2, rows * self.cell_size // 2,
                                        text="🎉 WIn rồi!", fill="red", font=("Arial", 20, "bold"))
>>>>>>> 81b7f8c56fbafc87a70c3eb4fbe733100dfd6e33
