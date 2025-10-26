# maze/player.py
class Player:
    def __init__(self, canvas, r, c, cell_size, maze, goal):
        self.canvas = canvas
        self.r = r
        self.c = c
        self.cell_size = cell_size
        self.maze = maze
        self.goal = goal
        pad = 5
        x1 = c * cell_size + pad
        y1 = r * cell_size + pad
        x2 = (c+1) * cell_size - pad
        y2 = (r+1) * cell_size - pad
        self.icon = self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="")

    def move(self, dc, dr):
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
