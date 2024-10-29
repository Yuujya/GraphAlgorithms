import random
import time

class Node:
    def __init__(self, id):
        self.id = id

    def __str__(self) -> str:
        return f"<{self.id}>"


class Edge:
    def __init__(self, start, end, d=0, directed=True):
        # if directed and start > end:
        #     start, end = end, start
        self.start = start
        self.end = end
        self.edge = (self.start, self.end)
        self.d = d
        # gerichtete oder ungerichtete Kante, gerichtet = True
        self.directed = directed

    def __eq__(self, other):
        # ungerichtete Kante {i,j} vergleichen mit (i,j) oder (j,i)
        if not other.directed:
            return ((self.start, self.end) == (other.start, other.end)) \
                or ((self.end, self.start) == (other.start, other.end))
        # gerichtete Kante (i,j) nur mit (i,j) vergleichen
        return (self.start, self.end) == (other.start, other.end)

    def __hash__(self):
        # TODO: Richtung in hash abdecken
        return hash((self.start, self.end, self.directed))

    # TODO
    def incident(self, directed=True):
        pass

    # TODO
    def adjacent(self, directed=True):
        pass

    def __str__(self):
        repr = f"{self.start},{self.end}"
        repr = f"({repr})" if self.directed else f"{{{repr}}}"
        return repr


class Graph:
    def __init__(self, V, E):
        self.V = V
        self.E = E

    def is_complete_graph(self, directed=True):
        N = (len(self.V) * (len(self.V) - 1))
        if directed:
            return len(self.E) == N
        return len(self.E) == N / 2

    def reachability_set(self, v):
        # Schritt 0
        M = {v}
        R = set()
        edges = [e for e in self.E]  # TODO

        # Schritt 1
        while True:
            k = M.pop()
            # M = M - set(k) # wird schon mit pop gemacht
            R.add(k)
            for j in self.V:
                if any(Edge(k.id, j.id) == e for e in edges):
                    if j not in R:
                        M.add(j)
            if not M:
                break
        return R

    def compute_connected_components(self):
        uG = create_undirected_graph(self)
        # Schritt 0
        M = uG.V
        # Z hat Teilmengen von V
        Z = []

        # Schritt 1
        while M:
            k = next(iter(M))
            R = uG.reachability_set(k)
            # Menge R hinzufuegen und nicht die Elemente von R elementweise zu Z hinzufuegen
            Z.append(R)
            M = M.difference(R)
        return Z


def create_random_graph(n, m):
    """Create random graph with n vertices and m edges."""
    V = {Node(i) for i in range(1, n + 1)}
    E = set()
    done = m
    while done != 0:
        i = random.randint(1, n)
        j = random.randint(1, m)
        k = random.randint(0, 1)
        if i != j and k == 0:
            e = (Edge(i, j, False))
        if i != j and k == 1:
            e = Edge(i, j)
        if e not in E:
            E.add(e)
            done -= 1
    return Graph(V, E)


def create_undirected_graph(G: Graph):
    new_edges = set()
    for edge in G.E:
        if edge.directed:
            new_edges.add(Edge(edge.start, edge.end, directed=False))
        else:
            new_edges.add(edge)
    return Graph(G.V, new_edges)


def main():
    # 2.2 Kanten
    V = {Node(i) for i in range(1, 8)}
    E = {Edge(5, 1), Edge(2, 3), Edge(2, 6), Edge(3, 7), Edge(6, 7), Edge(7, 4)}

    # Bsp aus Skript
    V = {Node(i) for i in range(1, 9)}
    E = {Edge(1, 2, False), Edge(2, 7, False), Edge(5, 8), Edge(8, 6), Edge(8, 4), Edge(6, 4)}

    G = Graph(V, E)

    k = 5
    R = G.reachability_set(Node(k))
    print(f"Erreichbarkeitsmenge von {k} bestimmen:")
    reachable_set = "{" + ','.join([str(r) for r in R]) + "}"
    print(f"{reachable_set}")

    print()

    connectedComponents = G.compute_connected_components()
    print("Zusammenhangskomponente von G berechnen:")
    for count, component in enumerate(connectedComponents):
        print(f"{count+1}-te Zusammenhangskomponente:")
        components = "{" + ','.join([str(e) for e in component]) + "}"
        print(f"{components}")

    n = 100
    m = 100

    G2 = create_random_graph(n, m)
    for i in range(10):
        v = random.randint(1, n)
        start_r = time.time()
        _ = G2.reachability_set(Node(v))
        end_r = time.time()
        print(f"Iteration {i + 1} - Benoetigte Rechenzeit fuer Erreichbarkeitsmenge: {end_r - start_r}")

    for i in range(10):
        G3 = create_random_graph(n, m)
        start_c = time.time()
        _ = G3.compute_connected_components()
        end_c = time.time()
        print(f"Iteration {i + 1} - Benoetigte Rechenzeit fuer Zusammenhangskomponente: {end_c - start_c}")


if __name__ == "__main__":
    main()
