import random

def generate_maze(rows, cols, extra_paths=40):
    """
    Trả về ma trận maze[rows][cols]: 0 = đường, 1 = tường
    Sử dụng recursive backtracker (carve với bước 2) để tạo maze connected.
    """
    # ensure odd sizes could be nicer, but we accept any size
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    def in_bounds(x, y):
        return 0 <= x < cols and 0 <= y < rows

    def carve(x, y):
        maze[y][x] = 0
        dirs = directions[:]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx*2, y + dy*2
            if in_bounds(nx, ny) and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0
                carve(nx, ny)

    # start carving from (0,0)
    carve(0, 0)
    # ensure goal open
    if rows > 0 and cols > 0:
        maze[rows-1][cols-1] = 0

    # make sure the goal has at least one neighbor open (avoid isolated goal)
    if rows > 1 and cols > 1 and maze[rows-2][cols-1] == 1 and maze[rows-1][cols-2] == 1:
        maze[rows-2][cols-1] = 0

    # open some random walls to create multiple branches
    open_cells = [(y, x) for y in range(1, rows-1) for x in range(1, cols-1) if maze[y][x] == 1]
    random.shuffle(open_cells)
    for (y, x) in open_cells[:extra_paths]:
        maze[y][x] = 0

    return maze


# quick debug runner
if __name__ == "__main__":
    m = generate_maze(21, 21, extra_paths=30)
    for row in m:
        print("".join("  " if c == 0 else "██" for c in row))
