from Graph import Graph, Vertex
from util.graph_errors import VertexNotFoundError


# Ungerichtete Kante {i,j} induziert gerichtete Kanten (i,j) und (j,i)
class Edge:
    def __init__(self, start, end, weight=0):
        self.start = min(start, end)
        self.end = max(start, end)
        self.directed = False
        self.weight = weight

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other):
        return (self.start == other.start and self.end == other.end) \
                or (self.start == other.end and self.end == other.start)

    def __str__(self):
        return f"{{{self.start}, {self.end}}}"


class UndirectedGraph(Graph):
    def __init__(self, vertices: set[Vertex], edges: set[Edge]):
        super().__init__(vertices, edges)
        self.directed = False

    def __eq__(self, other):
        return self.vertices == other.vertices and self.edges == other.edges

    def undirected_degree(self, vertex: Vertex):
        if vertex not in self.vertices:
            raise VertexNotFoundError(vertex)
        degree = 0
        for edge in self.edges:
            if vertex.id == edge.start or vertex.id == edge.end:
                degree += 1
        return degree
