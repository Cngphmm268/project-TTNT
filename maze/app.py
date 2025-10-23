import tkinter as tk
from tkinter import ttk
import time

from maze.maze_generator import generate_maze
from maze.maze_solver import get_solver_generator
from maze.player import Player

# Kích thước hiển thị
ROWS, COLS = 20, 25
CELL_SIZE = 30

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Visualizer — BFS/DFS/Dijkstra/A*")

        # Canvas hiển thị mê cung (bên trái)
        self.canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=4, padx=10, pady=10)

        # Khung điều khiển (bên phải, sắp dọc)
        control_frame = tk.Frame(root)
        control_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        # Các nút điều khiển
        button_width = 20
        tk.Button(control_frame, text="🌀 Tạo mê cung mới", command=self.create_maze, width=button_width).pack(pady=6)
        tk.Button(control_frame, text="▶ Bắt đầu", command=self.start_solving, width=button_width).pack(pady=6)
        tk.Button(control_frame, text="■ Dừng", command=self.stop_solving, width=button_width).pack(pady=6)
        tk.Button(control_frame, text="🔄 Đặt lại", command=self.reset_player, width=button_width).pack(pady=6)

        # Chọn thuật toán
        tk.Label(control_frame, text="Thuật toán:").pack(pady=(15, 2))
        self.algo_var = tk.StringVar(value="BFS")
        self.algo_combo = ttk.Combobox(control_frame, textvariable=self.algo_var,
                                       values=["BFS", "DFS", "Dijkstra", "A*"],
                                       state="readonly", width=button_width - 4)
        self.algo_combo.pack()

        # Thanh tốc độ
        tk.Label(control_frame, text="Tốc độ:").pack(pady=(15, 2))
        self.speed_var = tk.IntVar(value=60)
        self.speed_scale = tk.Scale(control_frame, from_=1, to=100, orient="horizontal",
                                    variable=self.speed_var, length=180)
        self.speed_scale.pack()

        # Nhãn hiển thị kết quả
        self.info_label = tk.Label(control_frame, text="Kết quả: Chưa có", justify="center", wraplength=200)
        self.info_label.pack(pady=(20, 0))

        # Trạng thái
        self.maze = []
        self.player = None
        self.start = (0, 0)
        self.goal = (ROWS - 1, COLS - 1)
        self.solver_gen = None
        self.running = False
        self.visited_set = set()
        self.expanded_set = set()
        self.path_cells = []

        # Gán sự kiện click
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        # Di chuyển bằng phím mũi tên
        root.bind("<Up>", lambda e: self._move_player(0, -1))
        root.bind("<Down>", lambda e: self._move_player(0, 1))
        root.bind("<Left>", lambda e: self._move_player(-1, 0))
        root.bind("<Right>", lambda e: self._move_player(1, 0))

        # Khởi tạo mê cung & người chơi
        self.create_maze()

    # ---------------- Maze Drawing ----------------
    def create_maze(self):
        self.maze = generate_maze(ROWS, COLS, extra_paths=int(ROWS * COLS * 0.08))
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                if self.maze[r][c] == 1:
                    shade = 60 + ((r * 7 + c * 13) % 80)
                    color = "#%02x%02x%02x" % (shade, shade - 10 if shade > 10 else shade,
                                               shade - 20 if shade > 20 else shade)
                else:
                    color = "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        self._draw_goal()
        self._draw_start()
        self.reset_state()

    def _cell_top_left(self, r, c):
        return c * CELL_SIZE, r * CELL_SIZE

    def _draw_start(self):
        r, c = self.start
        x1, y1 = self._cell_top_left(r, c)
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#88ddff", outline="blue", width=2, tags="start_cell")
        if self.player:
            self.canvas.delete(self.player.icon)
        self.player = Player(self.canvas, r, c, CELL_SIZE, self.maze, self.goal)

    def _draw_goal(self):
        r, c = self.goal
        x1, y1 = self._cell_top_left(r, c)
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#7CFC00", outline="darkgreen", width=2, tags="goal_cell")

    def reset_state(self):
        self.running = False
        self.solver_gen = None
        self.visited_set.clear()
        self.expanded_set.clear()
        self.path_cells.clear()
        self.info_label.config(text="Kết quả: Chưa có")
        self.canvas.delete("visit")
        self.canvas.delete("expand")
        self.canvas.delete("path")
        self.canvas.delete("start_cell")
        self.canvas.delete("goal_cell")
        self._draw_goal()
        self._draw_start()

    # ---------------- Mouse Handlers ----------------
    def on_left_click(self, event):
        c, r = event.x // CELL_SIZE, event.y // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS and self.maze[r][c] == 0:
            self.start = (r, c)
            self.canvas.delete("start_cell")
            self._draw_start()
            self.reset_state()

    def on_right_click(self, event):
        c, r = event.x // CELL_SIZE, event.y // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS and self.maze[r][c] == 0:
            self.goal = (r, c)
            self.canvas.delete("goal_cell")
            self._draw_goal()
            self.reset_state()

    # ---------------- Player ----------------
    def _move_player(self, dc, dr):
        if self.player:
            self.player.move(dc, dr)

    # ---------------- Solving ----------------
    def start_solving(self):
        if self.running:
            return
        solver_name = self.algo_var.get()
        solver_gen = get_solver_generator(solver_name, self.maze, self.start, self.goal)
        if solver_gen is None:
            self.info_label.config(text="Kết quả: Thuật toán không hợp lệ", fg="red")
            return
        self.canvas.delete("visit")
        self.canvas.delete("expand")
        self.canvas.delete("path")
        self.visited_set.clear()
        self.expanded_set.clear()
        self.path_cells.clear()
        self.solver_gen = solver_gen
        self.running = True
        self.solve_start_time = time.time()
        self._step_solver()

    def stop_solving(self):
        self.running = False
        self.solver_gen = None

    def _step_solver(self):
        if not self.running or self.solver_gen is None:
            return
        try:
            op, payload = next(self.solver_gen)
            if op == "visit":
                r, c = payload
                if (r, c) not in self.visited_set:
                    self.visited_set.add((r, c))
                    self._draw_cell(r, c, tag="visit", fill="#ffee88")
            elif op == "expand":
                r, c = payload
                if (r, c) not in self.expanded_set:
                    self.expanded_set.add((r, c))
                    self._draw_cell(r, c, tag="expand", fill="#ffd27f")
            elif op == "path":
                path = payload
                self.running = False
                self.solver_gen = None
                if path:
                    self.path_cells = path
                    for (r, c) in path:
                        if (r, c) == self.start or (r, c) == self.goal:
                            continue
                        self._draw_cell(r, c, tag="path", fill="#66ff66")
                    elapsed = time.time() - self.solve_start_time
                    self.info_label.config(text=f"Kết quả: Tìm thấy - độ dài {len(path)} | {elapsed:.3f}s", fg="green")
                else:
                    elapsed = time.time() - self.solve_start_time
                    self.info_label.config(text=f"Kết quả: Không tìm thấy ({self.algo_var.get()}) | {elapsed:.3f}s", fg="red")
                return
            speed = self.speed_var.get()
            delay = max(5, int(500 * (1 - speed / 100.0)))
            self.root.after(delay, self._step_solver)
        except StopIteration:
            self.running = False
            self.solver_gen = None
            self.info_label.config(text="Kết quả: Kết thúc", fg="black")

    # ---------------- Helper ----------------
    def _draw_cell(self, r, c, tag=None, fill=None):
        x1, y1 = c * CELL_SIZE + 1, r * CELL_SIZE + 1
        x2, y2 = x1 + CELL_SIZE - 2, y1 + CELL_SIZE - 2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill or "yellow", outline="", tags=(tag or "vis"))
        self.canvas.delete("start_cell")
        self.canvas.delete("goal_cell")
        self._draw_goal()
        self._draw_start()

    def reset_player(self):
        if self.player:
            try:
                self.canvas.delete(self.player.icon)
            except Exception:
                pass
        r, c = self.start
        self.player = Player(self.canvas, r, c, CELL_SIZE, self.maze, self.goal)
