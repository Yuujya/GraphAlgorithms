from data_structures.graph import Vertex
from data_structures.mixed_graph import MixedGraph, Edge
from data_structures.undirected__graph import UndirectedGraph
from algorithms.connectivity.reachability_set import reachability_set


def create_undirected_graph(mixed_graph: MixedGraph):
    new_edges = set()
    for edge in mixed_graph.edges:
        if edge.directed:
            new_edges.add(Edge(edge.start, edge.end, directed=False))
        else:
            new_edges.add(edge)
    return UndirectedGraph(mixed_graph.vertices, new_edges)


def connected_components(undirected_graph: UndirectedGraph) -> \
     list[set[Vertex]]:
    vertices_to_check = undirected_graph.vertices
    connected_components = []

    while vertices_to_check:
        k = next(iter(vertices_to_check))
        reachable_vertices = reachability_set(undirected_graph, k)
        connected_components.append(reachable_vertices)
        vertices_to_check = vertices_to_check.\
            difference(reachable_vertices)
    return connected_components
