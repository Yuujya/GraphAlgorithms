from data_structures.graph import Vertex
from data_structures.directed_graph import DirectedGraph
from data_structures.undirected__graph import UndirectedGraph
from data_structures.edge import Edge
from util.graph_errors import VertexNotFoundError


class MixedGraph(DirectedGraph, UndirectedGraph):
    def __init__(self, vertices: set[Vertex], edges: set[Edge], directed):
        super().__init__(vertices, edges)
        self.directed = directed

    # Unterscheidung zwischen Graphentypen
    def degree(self, vertex: Vertex):
        if vertex not in self.vertices:
            raise VertexNotFoundError(vertex)
        if self.directed:
            degree = self.directed_degree(vertex)
        else:
            degree = self.undirected_degree(vertex)
        return degree
