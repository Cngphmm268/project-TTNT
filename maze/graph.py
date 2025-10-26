# maze/graph.py
"""
Graph utilities cho project maze -> chuyển grid 2D (r,c) thành đồ thị
Node: dùng tuple (r, c)
Edge: (u, v, weight) với weight mặc định = 1
"""

from collections import defaultdict
import json


class Graph:
    def __init__(self):
        self.adj = defaultdict(list)

    def add_node(self, node):
        _ = self.adj[node]

    def add_edge(self, u, v, w=1):
        if u == v:
            return
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def neighbors(self, node):
        return list(self.adj.get(node, []))

    def has_node(self, node):
        return node in self.adj

    def nodes(self):
        return list(self.adj.keys())

    def remove_edges_of_node(self, node):
        if node not in self.adj:
            return
        for nbr, _ in list(self.adj[node]):
            self.adj[nbr] = [(n, w) for (n, w) in self.adj[nbr] if n != node]
        self.adj[node] = []

    def clear(self):
        self.adj.clear()

    def to_dict(self):
        out = {}
        for node, nbrs in self.adj.items():
            key = f"{node[0]},{node[1]}"
            out[key] = [[f"{n[0]},{n[1]}", w] for (n, w) in nbrs]
        return out

    def save_json(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def from_dict(d):
        g = Graph()
        for key, nbrs in d.items():
            r, c = map(int, key.split(","))
            u = (r, c)
            g.add_node(u)
        for key, nbrs in d.items():
            r, c = map(int, key.split(","))
            u = (r, c)
            for nkey, w in nbrs:
                nr, nc = map(int, nkey.split(","))
                v = (nr, nc)
                if all(n != v for (n, _) in g.adj[u]):
                    g.adj[u].append((v, w))
        return g

    @staticmethod
    def load_json(path):
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return Graph.from_dict(d)


def grid_to_graph(maze):
    if not maze or not maze[0]:
        return Graph()
    rows = len(maze)
    cols = len(maze[0])

    g = Graph()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 0:
                u = (r, c)
                g.add_node(u)
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                        v = (nr, nc)
                        g.add_edge(u, v, 1)
    return g


if __name__ == "__main__":
    sample = [
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0]
    ]
    g = grid_to_graph(sample)
    print("Nodes:", g.nodes())
    for n in g.nodes():
        print(f"{n} -> {g.neighbors(n)}")
    g.save_json("sample_graph.json")
    print("Saved sample_graph.json")
