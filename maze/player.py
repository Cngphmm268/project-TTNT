class Player:
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
                                        text="🎉 Thắng rồi!", fill="red", font=("Arial", 20, "bold"))
