# maze/maze_generator.py
import random

def generate_maze(rows, cols, extra_paths=10):
    """
    Sinh mê cung có thể giải được và có nhiều đường rẽ.
    Trả về ma trận 0 (đường) và 1 (tường).
    """
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def in_bounds(x, y):
        return 0 <= x < cols and 0 <= y < rows

    def carve(x, y):
        maze[y][x] = 0
        dirs = directions[:]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx * 2, y + dy * 2
            if in_bounds(nx, ny) and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0
                carve(nx, ny)

    # Bắt đầu từ (0, 0)
    maze[0][0] = 0
    carve(0, 0)
    maze[rows - 1][cols - 1] = 0  # đảm bảo đích mở

    # Mở thêm đường ngẫu nhiên để có nhiều hướng rẽ
    open_cells = [
        (y, x) for y in range(1, rows - 1)
        for x in range(1, cols - 1)
        if maze[y][x] == 1
    ]

    random.shuffle(open_cells)
    for i, (y, x) in enumerate(open_cells[:extra_paths]):
        maze[y][x] = 0

    return maze


# --- Kiểm thử nhanh ---
if __name__ == "__main__":
    m = generate_maze(15, 15, extra_paths=10)
    for row in m:
        print("".join("  " if c == 0 else "██" for c in row))
