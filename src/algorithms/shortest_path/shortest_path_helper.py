import math
from data_structures.graph import Vertex
from data_structures.mixed_graph import MixedGraph, Edge
from util.graph_errors import VertexNotFoundError


def distance(mixed_graph: MixedGraph,
             start_vertex: Vertex,
             end_vertex: Vertex,
             directed: bool):
    if start_vertex not in mixed_graph.vertices:
        raise VertexNotFoundError(start_vertex)
    if end_vertex not in mixed_graph.vertices:
        raise VertexNotFoundError(end_vertex)
    for edge in mixed_graph.edges:
        if Edge(start_vertex.id, end_vertex.id, directed) == edge:
            return edge.weight


def init_distance_table(self, start_vertex: Vertex):
    distances = {}
    predecessors = {}
    for vertex in self.vertices:
        if vertex.id != start_vertex.id:
            distances[vertex.id] = math.inf
            predecessors[vertex.id] = None
    distances[start_vertex.id] = 0
    predecessors[start_vertex.id] = 0
    return predecessors, distances


def distance_argmin(distances, vertices: set[Vertex]):
    min_index = next(iter(vertices))
    for vertex in vertices:
        if distances[vertex.id] < distances[min_index.id]:
            min_index = vertex
    return min_index.id


def build_shortest_path(predecessors, distances, target_vertex: Vertex):
    if not target_vertex:
        return predecessors, distances, []
    # Weg bis target_vertex zusammenbauen
    shortest_path = [target_vertex]
    k = target_vertex
    if predecessors[k.id] is None:
        return predecessors, distances, shortest_path
    while predecessors[k.id] != 0:
        k = Vertex(predecessors[k.id])
        shortest_path.insert(0, k)
    return predecessors, distances, shortest_path
