from util.graph_errors import VertexNotFoundError, EdgeNotFoundError


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
