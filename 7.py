INF = float("inf")


class Graph:
    def __init__(self, names):
        self.names = names
        self.n = len(names)
        self.matrix = [[0] * self.n for _ in range(self.n)]     # 0 means no edge
        self.adj = {i: [] for i in range(self.n)}                # adjacency list

    def add_edge(self, u, v, w):
        self.matrix[u][v] = w
        self.matrix[v][u] = w                                    # undirected graph
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    # Representation 1: adjacency matrix
    def show_matrix(self):
        print("Adjacency Matrix (distance in metres, 0 = no direct path):")
        print(" " * 7 + "".join(f"{name:>7}" for name in self.names))
        for i in range(self.n):
            row = "".join(f"{self.matrix[i][j]:>7}" for j in range(self.n))
            print(f"{self.names[i]:<7}{row}")

    # Representation 2: adjacency list
    def show_list(self):
        print("Adjacency List (neighbour, distance):")
        for i in range(self.n):
            items = " -> ".join(f"{self.names[v]}({w})" for v, w in self.adj[i])
            print(f"{self.names[i]:<6}-> {items}")

    def show_mst(self, mst, total):
        print("Edges in Minimum Spanning Tree:")
        for u, v, w in mst:
            print(f"  {self.names[u]} - {self.names[v]} : {w} m")
        print(f"Total minimum distance = {total} m")

    # Prim's algorithm (adjacency matrix / key array method)
    def prim(self, start=0):
        key = [INF] * self.n
        parent = [-1] * self.n
        in_mst = [False] * self.n
        key[start] = 0
        mst, total = [], 0

        for step in range(1, self.n + 1):
            u = -1
            for v in range(self.n):                              # min key vertex
                if not in_mst[v] and (u == -1 or key[v] < key[u]):
                    u = v
            if key[u] == INF:
                print("Graph is disconnected. MST not possible.")
                return
            in_mst[u] = True
            if parent[u] == -1:
                print(f"Step {step}: Start at {self.names[u]}")
            else:
                mst.append((parent[u], u, key[u]))
                total += key[u]
                print(f"Step {step}: Add {self.names[parent[u]]}-{self.names[u]} ({key[u]})")
            for v in range(self.n):                              # update keys
                w = self.matrix[u][v]
                if w and not in_mst[v] and w < key[v]:
                    key[v] = w
                    parent[v] = u
        self.show_mst(mst, total)


def campus_graph():
    names = ["ADM", "LIB", "COMP", "IT", "ENTC", "MECH", "CIVIL"]
    g = Graph(names)
    paths = [("ADM", "LIB", 120), ("ADM", "COMP", 250), ("ADM", "MECH", 300),
             ("LIB", "COMP", 150), ("LIB", "IT", 200), ("COMP", "IT", 80),
             ("COMP", "ENTC", 180), ("IT", "ENTC", 110), ("ENTC", "MECH", 220),
             ("ENTC", "CIVIL", 260), ("MECH", "CIVIL", 90)]
    for a, b, w in paths:
        g.add_edge(names.index(a), names.index(b), w)
    return g


def read_graph():
    n = int(input("Number of departments: "))
    names = input(f"Enter {n} short names separated by space: ").upper().split()
    if len(names) != n or len(set(names)) != n:
        print("Names must be unique and exactly", n, "in number.")
        return None
    g = Graph(names)
    e = int(input("Number of paths (edges): "))
    for i in range(e):
        a, b, w = input(f"Edge {i + 1} (from to distance): ").upper().split()
        w = int(w)
        if a not in names or b not in names or a == b or w <= 0:
            print("Invalid edge, skipped.")
            continue
        g.add_edge(names.index(a), names.index(b), w)
    return g


def main():
    g = campus_graph()
    while True:
        print("\n===== Campus Graph: MST using Prim's Algorithm =====")
        print("1. Display adjacency matrix")
        print("2. Display adjacency list")
        print("3. MST using Prim's algorithm")
        print("4. Enter a new graph")
        print("5. Exit")
        try:
            ch = int(input("Enter your choice: "))
            if ch == 1:
                g.show_matrix()
            elif ch == 2:
                g.show_list()
            elif ch == 3:
                s = input(f"Start department (Enter for {g.names[0]}): ").upper()
                if s and s not in g.names:
                    print("Unknown department.")
                else:
                    g.prim(g.names.index(s) if s else 0)
            elif ch == 4:
                new = read_graph()
                if new:
                    g = new
                    print("New graph stored.")
            elif ch == 5:
                print("Exiting program.")
                break
            else:
                print("Invalid choice! Try again.")
        except ValueError:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
