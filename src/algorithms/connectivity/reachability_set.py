from data_structures.graph import Vertex
from data_structures.mixed_graph import MixedGraph, Edge
from util.graph_errors import VertexNotFoundError


def reachability_set(mixed_graph: MixedGraph, start_vertex: Vertex):
    if start_vertex not in mixed_graph.vertices:
        raise VertexNotFoundError(start_vertex)
    vertices_to_check = {start_vertex}
    reachable_vertices = set()

    while vertices_to_check:
        k = vertices_to_check.pop()
        reachable_vertices = reachable_vertices | {k}
        reachable_vertices_from_k = mixed_graph.adjacent_vertices(k)
        for j in reachable_vertices_from_k:
            if Edge(k.id, j.id, True) in mixed_graph.edges and \
                    j not in reachable_vertices:
                vertices_to_check = vertices_to_check | {j}
    return reachable_vertices


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
