import random
import time
import math
import copy


# Ein Knoten hat einen Namen
class Vertex:
    def __init__(self, id):
        self.id = id

    def __hash__(self):
        return hash(id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"<{self.id}>"


# Eine Kante kann gerichtet sein ODER ungerichtet
# Ungerichtete Kanten sind so sortiert, dass start < end ist
# Ausserdem ist ungerichtete Kante {i,j} gleichbedeutend mit (i,j) und (j,i)
# (i,j) bedeutet ausgehende Kante aus Knoten i und eingehend in Knoten j
class Edge:
    def __init__(self, start, end, directed=True, weight=0):
        if directed:
            self.start = start
            self.end = end
        # ungerichtete Kanten werden sortiert mit i<j in {i,j}
        else:
            self.start = min(start, end)
            self.end = max(start, end)
        self.directed = directed
        self.weight = weight

    def __hash__(self):
        if self.directed:
            return hash((min(self.start, self.end), max(self.start, self.end)))
        return hash((self.start, self.end))

    def __eq__(self, other):
        if not self.directed:
            return (self.start == other.start and self.end == other.end) \
                or (self.start == other.end and self.end == other.start)
        return self.start == other.start and self.end == other.end

    def __str__(self):
        if self.directed:
            return f"({self.start}, {self.end})"
        return f"{{{self.start}, {self.end}}}"


# Falls Knoten oder Kante nicht in der Menge liegt, so gebe bei
# Knotengrad-Berechnungen -1 und bei anderen Methoden None aus
class Graph:
    def __init__(self, vertices, edges, directed=False):
        self.vertices = vertices
        self.edges = edges
        # bei gemischten Graphen nicht mehr aussagekraeftig
        self.directed = directed

    # bei ungerichteten Graphen
    def undirected_degree(self, vertex):
        degree = 0
        if vertex in self.vertices:
            for edge in self.edges:
                if vertex.id == edge.start or vertex.id == edge.end:
                    degree += 1
            return degree
        return -1

    # Unterscheidung zwischen Graphentypen
    def degree(self, vertex: Vertex):
        degree = 0
        if vertex in self.vertices:
            if self.directed:
                degree = self.undirected_degree(vertex)
            else:
                degree = self.indegree(vertex) + self.outdegree(vertex)
            return degree
        return -1

    # bei gerichteten Graphen
    def outdegree(self, vertex):
        degree = 0
        if vertex in self.vertices:
            for edge in self.edges:
                if vertex.id == edge.start:
                    degree += 1
            return degree
        return -1

    def indegree(self, vertex):
        degree = 0
        if vertex in self.vertices:
            for edge in self.edges:
                if vertex.id == edge.end:
                    degree += 1
            return degree
        return -1

    def is_incident(self, vertex, edge):
        if vertex in self.vertices and edge in self.edges:
            if vertex.id == edge.start or vertex.id == edge.end:
                return True
            return False
        return None

    def is_adjacent(self, start_vertex, end_vertex):
        if start_vertex in self.vertices and end_vertex in self.vertices:
            return Edge(start_vertex.id, end_vertex.id, True) in self.edges
        return None

    def is_isolated(self, vertex):
        if vertex in self.vertices:
            if self.degree(vertex) == 0:
                return True
            return False
        return None

    def adjacent_vertices(self, start_vertex):
        adjacent_vertices = set()
        if start_vertex in self.vertices:
            for vertex in self.vertices:
                if self.is_adjacent(start_vertex, vertex):
                    adjacent_vertices.add(vertex)
            return adjacent_vertices
        return None

    def incident_edges(self, start_vertex):
        incident_edges = set()
        if start_vertex in self.vertices:
            for edge in self.edges:
                if self.is_incident(start_vertex, edge):
                    incident_edges.add(edge)
            return incident_edges
        return None

    def reachability_set(self, start_vertex):
        if start_vertex in self.vertices:
            vertices_to_check = {start_vertex}
            reachable_vertices = set()

            while vertices_to_check:
                k = vertices_to_check.pop()
                reachable_vertices = reachable_vertices | {k}
                reachable_vertices_from_k = self.adjacent_vertices(k)
                for j in reachable_vertices_from_k:
                    if Edge(k.id, j.id, True) in self.edges and \
                            j not in reachable_vertices:
                        vertices_to_check = vertices_to_check | {j}
            return reachable_vertices
        return None

    def reachability_set_table(self):
        reachability_table = {}
        for vertex in self.vertices:
            reachability_set = self.reachability_set(vertex)
            for reachibility_vertex in reachability_set:
                reachability_table[reachibility_vertex.id] = reachability_set
        return reachability_table

    def connected_components(self) -> list[set[Vertex]]:
        vertices_to_check = self.vertices
        connected_components = []

        while vertices_to_check:
            k = next(iter(vertices_to_check))
            reachable_vertices = self.reachability_set(k)
            connected_components.append(reachable_vertices)
            vertices_to_check = vertices_to_check.\
                difference(reachable_vertices)
        return connected_components

    def distance(self, start_vertex, end_vertex, directed):
        if start_vertex in self.vertices and end_vertex in self.vertices:
            for edge in self.edges:
                if Edge(start_vertex.id, end_vertex.id, directed) == edge:
                    return edge.weight
        return -1

    def init_distance_table(self, start_vertex):
        distances = {}
        predecessors = {}
        for vertex in self.vertices:
            if vertex.id != start_vertex.id:
                distances[vertex.id] = math.inf
                predecessors[vertex.id] = None
        distances[start_vertex.id] = 0
        predecessors[start_vertex.id] = 0
        return predecessors, distances

    # TODO: an ungerichtete Graphen anpassen,
    # funktioniert nur fuer gerichtete Graphen
    def bellman_ford(self, start_vertex, target_vertex=None):
        predecessors, distances = self.init_distance_table(start_vertex)

        for k in range(len(self.vertices)-1):
            for edge in self.edges:
                if predecessors[edge.start] != edge.end and distances[edge.end] > distances[edge.start] + self.distance(Vertex(edge.start), Vertex(edge.end), True):
                    distances[edge.end] = distances[edge.start] + self.distance(Vertex(edge.start), Vertex(edge.end), True)
                    predecessors[edge.end] = edge.start

        for edge in self.edges:
            if distances[edge.end] > distances[edge.start] + self.distance(Vertex(edge.start), Vertex(edge.end), True):
                print("Kreis mit negativer Laenge existiert")
                return {}, {}, []

        return build_shortest_path(predecessors, distances, target_vertex)

    def dijkstra(self, start_vertex, target_vertex=None):
        predecessors, distances = self.init_distance_table(start_vertex)

        remaining_vertices = self.vertices
        while remaining_vertices:
            i = Vertex(distance_argmin(distances, remaining_vertices))
            remaining_vertices = remaining_vertices - {i}

            adjacent_vertices = self.adjacent_vertices(i)
            for adjacent_vertex in adjacent_vertices:
                if adjacent_vertex in remaining_vertices and (distances[adjacent_vertex.id] > distances[i.id] + self.distance(i, adjacent_vertex, False)):
                    distances[adjacent_vertex.id] = distances[i.id] + self.distance(i, adjacent_vertex, False)
                    predecessors[adjacent_vertex.id] = i.id

        return build_shortest_path(predecessors, distances, target_vertex)

    def add_edge(self, edge):
        self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    # TODO: Wie bestimmt man Kreise in dem Graphen?
    # Annahme Nur die Komponenten aus connected_components sind Inputs
    def kruskal(self):
        # MST besitzt alle Knoten, sodass Kanten alle verbinden und minimale Kosten verursachen
        sorted_edges = sorted(self.edges, key=lambda e: e.weight)
        mst = Graph(self.vertices, set())
        mst_prime = copy.deepcopy(mst)
        for edge in sorted_edges:
            mst_prime.add_edge(edge)
            if mst.reachability_set_table() != mst_prime.reachability_set_table():
                mst.add_edge(edge)
            else:
                mst_prime.remove_edge(edge)
        return mst


def build_shortest_path(predecessors, distances, target_vertex):
    if not target_vertex:
        return predecessors, distances, []
    # Weg bis target_vertex zusammenbauen
    shortest_path = [target_vertex]
    k = target_vertex
    while predecessors[k.id] != 0:
        k = Vertex(predecessors[k.id])
        shortest_path.insert(0, k)
    return predecessors, distances, shortest_path


def distance_argmin(distances, vertices):
    min_index = next(iter(vertices))
    for vertex in vertices:
        if distances[vertex.id] < distances[min_index.id]:
            min_index = vertex
    return min_index.id


def create_undirected_graph(graph: Graph):
    new_edges = set()
    for edge in graph.edges:
        if edge.directed:
            new_edges.add(Edge(edge.start, edge.end, directed=False))
        else:
            new_edges.add(edge)
    return Graph(graph.vertices, new_edges, False)


def create_random_graph(n, m):
    """Zufaelligen Graph generieren mit n Knoten und m Kanten."""
    vertices = {Vertex(i) for i in range(1, n + 1)}
    edges = set()
    done = m
    while done != 0:
        start = random.randint(1, n)
        end = random.randint(1, m)
        direction = random.randint(0, 1)
        if start != end and direction == 0:
            edge = Edge(start, end, False)
        if start != end and direction == 1:
            edge = Edge(start, end)
        if edge not in edges:
            edges.add(edge)
            done -= 1
    return Graph(vertices, edges)


def main():
    # Aufgabe 2.2.a
    E1 = {Edge(1, 2, False), Edge(2, 7, False), Edge(5, 8, True), Edge(8, 6, True), Edge(8, 4, True), Edge(6, 4, True)}
    e1 = Edge(8, 6, False)
    print(e1 in E1)
    V1 = {Vertex(i) for i in range(1, 8+1)}
    G1 = Graph(V1, E1, True)
    start_vertex = Vertex(5)
    reachable_vertices = G1.reachability_set(start_vertex)
    print(f"Erreichbarkeitsmenge von {start_vertex}:")
    reachable_set = "{" + ','.join([str(r) for r in reachable_vertices]) + "}"
    print(f"{reachable_set}")

    # Aufgabe 2.2.b
    G2 = create_undirected_graph(G1)
    connected_components = G2.connected_components()
    print("Zusammenhangskomponente von G berechnen:")
    for count, component in enumerate(connected_components):
        print(f"{count+1}-te Zusammenhangskomponente:")
        components = "{" + ','.join([str(e) for e in component]) + "}"
        print(f"{components}")

    # Aufgabe 3.4
    n = 100
    m = 200

    G2 = create_random_graph(n, m)
    for i in range(10):
        v = random.randint(1, n)
        start_r = time.time()
        _ = G2.reachability_set(Vertex(v))
        end_r = time.time()
        print(f"Iteration {i + 1} - Benoetigte Rechenzeit fuer Erreichbarkeitsmenge: {end_r - start_r}")

    for i in range(10):
        G3 = create_random_graph(n, m)
        start_c = time.time()
        _ = G3.connected_components()
        end_c = time.time()
        print(f"Iteration {i + 1} - Benoetigte Rechenzeit fuer Zusammenhangskomponente: {end_c - start_c}")

    # Aufgabe 4.1
    E2 = {Edge(5, 1, True, 5), Edge(2, 3, True, 3), Edge(2, 6, True, 4), Edge(6, 7, True, 1), Edge(7, 4, True, 2)}
    V2 = {Vertex(i) for i in range(1, 7+1)}
    G2 = Graph(V2, E2)
    start_vertex = Vertex(2)
    target_vertex = Vertex(4)
    _, _, shortest_path = G2.dijkstra(start_vertex, target_vertex)
    print(f"Kuerzester Weg von {start_vertex.id} zu {target_vertex.id}: {[v.id for v in shortest_path]}")

    # Aufgabe 4.3
    E4 = {Edge(1, 2, True, 4), Edge(2, 1, True, 3), Edge(1, 4, True, -2),
          Edge(4, 2, True, 2), Edge(2, 4, True, 2), Edge(2, 3, True, 2),
          Edge(3, 5, True, 1), Edge(5, 3, True, 3), Edge(4, 5, True, 2),
          Edge(5, 4, True, 3), Edge(4, 3, True, 6)}
    V4 = {Vertex(i) for i in range(1, 5+1)}
    G4 = Graph(V4, E4)

    start_vertex = Vertex(2)
    for i in range(1, 5+1):
        if i != start_vertex.id:
            target_vertex = Vertex(i)
            _, _, shortest_path = G4.bellman_ford(start_vertex, target_vertex)
            print(f"Kuerzester Weg von {start_vertex.id} zu {target_vertex.id}: {[v.id for v in shortest_path]}")

    sorted_edges4 = sorted(E4, key=lambda e: e.weight)
    for e in sorted_edges4:
        print(f"start={e.start} end={e.end} weight={e.weight}")

    # Bsp 3.8
    # TODO: An Aufgabe 5.5.a pruefen
    E5 = {Edge(1, 6, False, 1), Edge(1, 2, False, 4), Edge(2, 5, False, 2),
          Edge(2, 3, False, 3), Edge(1, 3, False, 5), Edge(2, 6, False, 5),
          Edge(3, 6, False, 4), Edge(4, 3, False, 6), Edge(4, 5, False, 2),
          Edge(3, 5, False, 3)}
    V5 = {Vertex(i) for i in range(1, 6+1)}
    G5 = Graph(V5, E5)
    mst = G5.kruskal()
    total_weight = 0
    for vertex in mst.vertices:
        print(vertex)
    for edge in mst.edges:
        print(edge)
        total_weight += edge.weight
    print(f"MST mit Staerke {total_weight}")
    print("done")


if __name__ == "__main__":
    main()
