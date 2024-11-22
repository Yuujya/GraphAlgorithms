from util.graph_errors import VertexNotFoundError, EdgeNotFoundError
from data_structures.edge import Edge


class Vertex:
    def __init__(self, id):
        self.id = id

    def __hash__(self):
        return hash(id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"<{self.id}>"


# Kanten liegen in den jeweiligen Unterklassen
class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def __eq__(self, other):
        return self.vertices == other.vertices and self.edges == other.edges

    def add_vertex(self, vertex):
        self.vertices.add(vertex)

    def add_edge(self, edge):
        if Vertex(edge.start) not in self.vertices:
            raise VertexNotFoundError(Vertex(edge.start))
        if Vertex(edge.end) not in self.vertices:
            raise VertexNotFoundError(Vertex(edge.end))
        self.edges.add(edge)

    def remove_edge(self, edge):
        if edge not in self.edges:
            raise EdgeNotFoundError(edge)
        self.edges.remove(edge)

    def print_vertices(self):
        for vertex in self.vertices:
            print(f"{vertex}")

    def print_edges(self):
        for edge in self.edges:
            print(f"{edge}")

    def print_graph(self):
        self.print_vertices()
        self.print_edges()
        
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
