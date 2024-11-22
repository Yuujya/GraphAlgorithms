from data_structures.graph import Graph, Vertex
from util.graph_errors import VertexNotFoundError


class Edge:
    def __init__(self, start, end, weight=0):
        self.start = start
        self.end = end
        self.directed = True
        self.weight = weight

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def conjugated_edge(self):
        return Edge(self.end, self.start)

    def __str__(self):
        return f"({self.start}, {self.end})"


class DirectedGraph(Graph):
    def __init__(self, vertices: set[Vertex], edges: set[Edge]):
        super().__init__(vertices, edges)
        self.directed = True

    def directed_degree(self, vertex: Vertex):
        if vertex not in self.vertices:
            raise VertexNotFoundError(vertex)
        return self.__indegree(vertex) + self.__outdegree(vertex)

    def __outdegree(self, vertex: Vertex):
        degree = 0
        for edge in self.edges:
            if vertex.id == edge.start:
                degree += 1
        return degree

    def __indegree(self, vertex: Vertex):
        degree = 0
        for edge in self.edges:
            if vertex.id == edge.end:
                degree += 1
        return degree
