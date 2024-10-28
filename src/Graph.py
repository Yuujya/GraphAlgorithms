class Node:
    def __init__(self, id):
        self.id = id

    def __str__(self) -> str:
        return f"<{self.id}>"


class Edge:
    def __init__(self, start, end, d=0, directed=True):
        self.start = start
        self.end = end
        self.edge = (start, end)
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
        return hash((self.start, self.end, self.directed))

    def __str__(self):
        repr = f"{self.start},{self.end}"
        repr = f"({repr})" if self.directed else f"{{{repr}}}"
        return repr


class Graph:
    def __init__(self, V, E):
        self.V = V
        self.E = E

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


def create_undirected_graph(G: Graph):
    new_edges = set()
    for edge in G.E:
        if edge.directed:
            new_edges.add(Edge(edge.start, edge.end, directed=False))
        else:
            new_edges.add(edge)
    return Graph(G.V, new_edges)


def main():
    V = set()
    E = set()

    # Knoten hinzufuegen
    for i in range(1, 9):
        V.add(Node(i))

    # Kanten hinzufuegen
    # E.add(Edge(5, 1))
    # E.add(Edge(2, 3))
    # E.add(Edge(2, 6))
    # E.add(Edge(3, 7))
    # E.add(Edge(6, 7))
    # E.add(Edge(7, 4))

    E.add(Edge(1, 2, False))
    E.add(Edge(2, 7, False))
    E.add(Edge(5, 8))
    E.add(Edge(8, 6))
    E.add(Edge(8, 4))
    E.add(Edge(6, 4))

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


if __name__ == "__main__":
    main()
