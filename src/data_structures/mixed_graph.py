from Graph import Vertex, Graph
from data_structures.directed_graph import DirectedGraph
from data_structures.undirected__graph import UndirectedGraph
from util.graph_errors import VertexNotFoundError, EdgeNotFoundError


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


class MixedGraph(DirectedGraph, UndirectedGraph):
    def __init__(self, vertices: set[Vertex], edges: set[Edge], directed):
        super().__init__(vertices, edges)
        self.directed = directed

    def __eq__(self, other):
        return self.vertices == other.vertices and self.edges == other.edges

    # Unterscheidung zwischen Graphentypen
    def degree(self, vertex: Vertex):
        if vertex not in self.vertices:
            raise VertexNotFoundError(vertex)
        if self.directed:
            degree = self.directed_degree(vertex)
        else:
            degree = self.undirected_degree(vertex)
        return degree

    def is_incident(self, vertex, edge):
        if vertex not in self.vertices:
            raise VertexNotFoundError(vertex)
        if edge not in self.edges:
            raise EdgeNotFoundError(edge)
        if vertex.id == edge.start or vertex.id == edge.end:
            return True
        return False

    def is_adjacent(self, start_vertex, end_vertex):
        if start_vertex not in self.vertices:
            raise VertexNotFoundError(start_vertex)
        if end_vertex not in self.vertices:
            raise VertexNotFoundError(end_vertex)
        return Edge(start_vertex.id, end_vertex.id, True) in self.edges

    def is_isolated(self, vertex):
        if vertex not in self.vertices:
            raise VertexNotFoundError(vertex)
        if self.degree(vertex) == 0:
            return True
        return False

    def adjacent_vertices(self, start_vertex):
        if start_vertex not in self.vertices:
            raise VertexNotFoundError(start_vertex)
        adjacent_vertices = set()
        for vertex in self.vertices:
            if self.is_adjacent(start_vertex, vertex):
                adjacent_vertices.add(vertex)
        return adjacent_vertices

    def incident_edges(self, start_vertex):
        if start_vertex not in self.vertices:
            raise VertexNotFoundError(start_vertex)
        incident_edges = set()
        for edge in self.edges:
            if self.is_incident(start_vertex, edge):
                incident_edges.add(edge)
        return incident_edges
