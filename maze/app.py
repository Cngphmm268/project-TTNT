import tkinter as tk
from maze.maze_generator import generate_maze
from maze.maze_solver import solve_maze
from maze.player import Player

ROWS, COLS = 15, 15
CELL_SIZE = 35

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game 🌀")

        self.canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white")
        self.canvas.pack(padx=10, pady=10)

        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Button(control_frame, text="Tạo mê cung mới", command=self.create_maze).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Giải mê cung", command=self.solve).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Đặt lại", command=self.reset_player).grid(row=0, column=2, padx=5)

        self.player = None
        self.start = (0, 0)
        self.goal = (ROWS - 1, COLS - 1)
        self.maze = []

        self.create_maze()
        self.reset_player()

        self.root.bind("<Up>", lambda e: self.player.move(0, -1))
        self.root.bind("<Down>", lambda e: self.player.move(0, 1))
        self.root.bind("<Left>", lambda e: self.player.move(-1, 0))
        self.root.bind("<Right>", lambda e: self.player.move(1, 0))

    def create_maze(self):
        self.maze = generate_maze(ROWS, COLS)
        self.canvas.delete("all")

        for i in range(ROWS):
            for j in range(COLS):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "black" if self.maze[i][j] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

        self.canvas.create_rectangle((COLS - 1) * CELL_SIZE, (ROWS - 1) * CELL_SIZE,
                                     COLS * CELL_SIZE, ROWS * CELL_SIZE, fill="green")

    def reset_player(self):
        if self.player:
            self.canvas.delete(self.player.icon)
        self.player = Player(self.canvas, 0, 0, CELL_SIZE, self.maze, self.goal)

    def solve(self):
        path = solve_maze(self.maze, self.start, self.goal)
        if not path:
            return
        for (y, x) in path:
            x1, y1 = x * CELL_SIZE, y * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="gray")

        self.reset_player()
