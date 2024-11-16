import random
import time
import math


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

    def is_adjacent(self, first_vertex, second_vertex):
        if first_vertex in self.vertices and second_vertex in self.vertices:
            return Edge(first_vertex.id, second_vertex.id, True) in self.edges
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

    def connected_components(self):
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

    def dijkstra(self, start_vertex, target_vertex=None):
        distances = {}
        predecessors = {}
        for vertex in self.vertices:
            if vertex.id != start_vertex.id:
                distances[vertex.id] = math.inf
                predecessors[vertex.id] = None
        distances[start_vertex.id] = 0
        predecessors[start_vertex.id] = 0

        remaining_vertices = self.vertices
        while remaining_vertices:
            i = Vertex(distance_argmin(distances, remaining_vertices))
            remaining_vertices = remaining_vertices - {i}

            adjacent_vertices = self.adjacent_vertices(i)
            for adjacent_vertex in adjacent_vertices:
                if adjacent_vertex in remaining_vertices and (distances[adjacent_vertex.id] > distances[i.id] + self.distance(i, adjacent_vertex, False)):
                    distances[adjacent_vertex.id] = distances[i.id] + self.distance(i, adjacent_vertex, False)
                    predecessors[adjacent_vertex.id] = i.id

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


# Zufaelliger Graph generieren mit n Knoten und m Kanten
def create_random_graph(n, m):
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
    E3 = {Edge(1, 2, False), Edge(2, 7, False), Edge(5, 8, True), Edge(8, 6, True), Edge(8, 4, True), Edge(6, 4, True)}
    e1 = Edge(8, 6, False)
    print(e1 in E3)
    V3 = {Vertex(i) for i in range(1, 8+1)}
    G3 = Graph(V3, E3, True)
    start_vertex = Vertex(5)
    reachable_vertices = G3.reachability_set(start_vertex)
    print(f"Erreichbarkeitsmenge von {start_vertex}:")
    reachable_set = "{" + ','.join([str(r) for r in reachable_vertices]) + "}"
    print(f"{reachable_set}")

    # Aufgabe 2.2.b
    G4 = create_undirected_graph(G3)
    connected_components = G4.connected_components()
    print("Zusammenhangskomponente von G berechnen:")
    for count, component in enumerate(connected_components):
        print(f"{count+1}-te Zusammenhangskomponente:")
        components = "{" + ','.join([str(e) for e in component]) + "}"
        print(f"{components}")

    # Aufgabe 3.4
    # n = 100
    # m = 200

    # G2 = create_random_graph(n, m)
    # for i in range(10):
    #     v = random.randint(1, n)
    #     start_r = time.time()
    #     _ = G2.reachability_set(Vertex(v))
    #     end_r = time.time()
    #     print(f"Iteration {i + 1} - Benoetigte Rechenzeit fuer Erreichbarkeitsmenge: {end_r - start_r}")

    # for i in range(10):
    #     G3 = create_random_graph(n, m)
    #     start_c = time.time()
    #     _ = G3.connected_components()
    #     end_c = time.time()
    #     print(f"Iteration {i + 1} - Benoetigte Rechenzeit fuer Zusammenhangskomponente: {end_c - start_c}")

    # Bsp 2.19
    E = {Edge(1, 2, False, 1), Edge(2, 4, False, 3), Edge(4, 3, False, 4), Edge(1, 3, False, 3), Edge(5, 3, False, 3), Edge(5, 4, False, 1)}
    V = {Vertex(i) for i in range(1, 5+1)}
    G = Graph(V, E, False)

    start_vertex = Vertex(1)
    target_vertex = Vertex(5)
    _, _, shortest_path = G.dijkstra(start_vertex, target_vertex)
    print(f"Kuerzester Weg: {[vertex.id for vertex in shortest_path]}")

    # Aufgabe 4.1
    E2 = {Edge(5, 1, True, 5), Edge(2, 3, True, 3), Edge(2, 6, True, 4), Edge(6, 7, True, 1), Edge(7, 4, True, 2)}
    V2 = {Vertex(i) for i in range(1, 7+1)}
    G2 = Graph(V2, E2)
    start_vertex2 = Vertex(2)
    target_vertex2 = Vertex(4)
    _, _, shortest_path2 = G2.dijkstra(start_vertex2, target_vertex2)
    print(f"#2 Kuerzester Weg: {[vertex.id for vertex in shortest_path2]}")
    
    print("done")


if __name__ == "__main__":
    main()
