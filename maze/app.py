import tkinter as tk
from tkinter import ttk
import time

from maze.maze_generator import generate_maze
from maze.maze_solver import get_solver_generator
from maze.player import Player

# tùy chỉnh kích thước hiển thị
ROWS, COLS = 20, 25    # bạn có thể thay đổi
CELL_SIZE = 30

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Visualizer — BFS/DFS/Dijkstra/A*")

        # top frame: canvas
        self.canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # right/bottom controls
        control_frame = tk.Frame(root)
        control_frame.grid(row=1, column=0, sticky="w", padx=10)

        tk.Button(control_frame, text="🌀 Tạo mê cung mới", command=self.create_maze).grid(row=0, column=0, padx=4)
        tk.Button(control_frame, text="▶ Bắt đầu", command=self.start_solving).grid(row=0, column=1, padx=4)
        tk.Button(control_frame, text="■ Dừng", command=self.stop_solving).grid(row=0, column=2, padx=4)
        tk.Button(control_frame, text="🔄 Đặt lại", command=self.reset_player).grid(row=0, column=3, padx=4)

        # algorithm selector
        algo_frame = tk.Frame(root)
        algo_frame.grid(row=1, column=1, sticky="w")
        tk.Label(algo_frame, text="Thuật toán:").grid(row=0, column=0, padx=4)
        self.algo_var = tk.StringVar(value="BFS")
        self.algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=["BFS","DFS","Dijkstra","A*"], state="readonly", width=12)
        self.algo_combo.grid(row=0, column=1)

        # speed control
        speed_frame = tk.Frame(root)
        speed_frame.grid(row=1, column=2, sticky="w")
        tk.Label(speed_frame, text="Tốc độ:").grid(row=0, column=0)
        self.speed_var = tk.IntVar(value=60)  # 1..100
        self.speed_scale = tk.Scale(speed_frame, from_=1, to=100, orient="horizontal", variable=self.speed_var, length=200)
        self.speed_scale.grid(row=0, column=1, padx=4)

        # info display (bottom-right)
        info_frame = tk.Frame(root)
        info_frame.grid(row=1, column=3, sticky="e", padx=10)
        self.info_label = tk.Label(info_frame, text="Kết quả: Chưa có", justify="right")
        self.info_label.pack()

        # status vars
        self.maze = []
        self.player = None
        self.start = (0,0)
        self.goal = (ROWS-1, COLS-1)
        self.solver_gen = None
        self.running = False
        self.visited_set = set()
        self.expanded_set = set()
        self.path_cells = []

        # bind events for setting start/goal
        self.canvas.bind("<Button-1>", self.on_left_click)   # left click = set start
        self.canvas.bind("<Button-3>", self.on_right_click)  # right click = set goal

        # arrow keys for player control
        root.bind("<Up>", lambda e: self._move_player(0, -1))
        root.bind("<Down>", lambda e: self._move_player(0, 1))
        root.bind("<Left>", lambda e: self._move_player(-1, 0))
        root.bind("<Right>", lambda e: self._move_player(1, 0))

        # initialize maze & player
        self.create_maze()

    # ---------- Maze drawing ----------
    def create_maze(self):
        self.maze = generate_maze(ROWS, COLS, extra_paths=int(ROWS*COLS*0.08))
        self.canvas.delete("all")
        # draw cells: walls and floors (walls có shading để sinh động)
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if self.maze[r][c] == 1:
                    # shade depends on position for natural variation
                    shade = 60 + ((r*7 + c*13) % 80)
                    color = "#%02x%02x%02x" % (shade, shade-10 if shade>10 else shade, shade-20 if shade>20 else shade)
                else:
                    color = "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        # draw start & goal
        self._draw_goal()
        self._draw_start()
        # reset internal states
        self.reset_state()

    def _cell_top_left(self, r, c):
        return c*CELL_SIZE, r*CELL_SIZE

    def _draw_start(self):
        r,c = self.start
        x1,y1 = self._cell_top_left(r,c)
        x2,y2 = x1+CELL_SIZE, y1+CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#88ddff", outline="blue", width=2, tags="start_cell")
        # player
        if self.player:
            self.canvas.delete(self.player.icon)
        self.player = Player(self.canvas, r, c, CELL_SIZE, self.maze, self.goal)

    def _draw_goal(self):
        r,c = self.goal
        x1,y1 = self._cell_top_left(r,c)
        x2,y2 = x1+CELL_SIZE, y1+CELL_SIZE
        # green rectangle for goal
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#7CFC00", outline="darkgreen", width=2, tags="goal_cell")

    def reset_state(self):
        self.running = False
        self.solver_gen = None
        self.visited_set.clear()
        self.expanded_set.clear()
        self.path_cells.clear()
        self.info_label.config(text="Kết quả: Chưa có")
        # remove any 'visit', 'expand', 'path' tags drawn
        self.canvas.delete("visit")
        self.canvas.delete("expand")
        self.canvas.delete("path")
        # redraw start/goal and player icon
        self.canvas.delete("start_cell")
        self.canvas.delete("goal_cell")
        self._draw_goal()
        self._draw_start()

    # ---------- Mouse handlers ----------
    def on_left_click(self, event):
        # set start to clicked cell if it's a free cell
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS and self.maze[r][c] == 0:
            self.start = (r, c)
            self.canvas.delete("start_cell")
            self._draw_start()
            self.reset_state()

    def on_right_click(self, event):
        # set goal to clicked cell if free
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS and self.maze[r][c] == 0:
            self.goal = (r, c)
            self.canvas.delete("goal_cell")
            self._draw_goal()
            self.reset_state()

    # ---------- Player movement wrapper ----------
    def _move_player(self, dc, dr):
        # player.move expects (dc, dr) to be consistent with earlier player implementation
        if self.player:
            self.player.move(dc, dr)

    # ---------- Solving control ----------
    def start_solving(self):
        if self.running:
            return
        solver_name = self.algo_var.get()
        solver_gen = get_solver_generator(solver_name, self.maze, self.start, self.goal)
        if solver_gen is None:
            self.info_label.config(text="Kết quả: Thuật toán không hợp lệ", fg="red")
            return
        # reset drawing and states
        self.canvas.delete("visit")
        self.canvas.delete("expand")
        self.canvas.delete("path")
        self.visited_set.clear()
        self.expanded_set.clear()
        self.path_cells.clear()
        self.solver_gen = solver_gen
        self.running = True
        # run with timing
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
                r,c = payload
                if (r,c) not in self.visited_set:
                    self.visited_set.add((r,c))
                    self._draw_cell(r, c, tag="visit", fill="#ffee88")
            elif op == "expand":
                r,c = payload
                if (r,c) not in self.expanded_set:
                    self.expanded_set.add((r,c))
                    self._draw_cell(r, c, tag="expand", fill="#ffd27f")
            elif op == "path":
                path = payload
                self.running = False
                self.solver_gen = None
                if path:
                    self.path_cells = path
                    for (r,c) in path:
                        # skip start/goal coloring override
                        if (r,c) == self.start or (r,c) == self.goal:
                            continue
                        self._draw_cell(r, c, tag="path", fill="#66ff66")
                    elapsed = time.time() - self.solve_start_time
                    self.info_label.config(text=f"Kết quả: Tìm thấy - độ dài {len(path)} | {elapsed:.3f}s", fg="green")
                else:
                    elapsed = time.time() - self.solve_start_time
                    self.info_label.config(text=f"Kết quả: Không tìm thấy ({self.algo_var.get()}) | {elapsed:.3f}s", fg="red")
                return
            # schedule next step based on speed slider
            speed = self.speed_var.get()  # 1 .. 100
            delay = max(5, int(500 * (1 - speed/100.0)))  # faster => smaller delay
            self.root.after(delay, self._step_solver)
        except StopIteration:
            self.running = False
            self.solver_gen = None
            self.info_label.config(text="Kết quả: Kết thúc", fg="black")

    # ---------- drawing helper ----------
    def _draw_cell(self, r, c, tag=None, fill=None):
        x1 = c * CELL_SIZE + 1
        y1 = r * CELL_SIZE + 1
        x2 = x1 + CELL_SIZE - 2
        y2 = y1 + CELL_SIZE - 2
        if fill is None:
            fill = "yellow"
        # draw rectangle with a specific tag so we can delete later
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="", tags=(tag if tag else "vis"))
        # re-draw start/goal on top
        self.canvas.delete("start_cell")
        self.canvas.delete("goal_cell")
        self._draw_goal()
        self._draw_start()

    def reset_player(self):
        # move player back to start
        if self.player:
            try:
                # delete player and recreate
                self.canvas.delete(self.player.icon)
            except Exception:
                pass
        r,c = self.start
        self.player = Player(self.canvas, r, c, CELL_SIZE, self.maze, self.goal)

