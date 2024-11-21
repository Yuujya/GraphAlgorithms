from data_structures.graph import Vertex
from data_structures.mixed_graph import UndirectedGraph


def prim(undirected_graph: UndirectedGraph, start_vertex: Vertex):
    sorted_edges = sorted(undirected_graph.edges, key=lambda e: e.weight)
    mst_vertices = {start_vertex}
    mst_edges = set()
    total_weight = 0
    while mst_vertices != undirected_graph.vertices:
        for edge in sorted_edges:
            new_vertices = {Vertex(edge.start), Vertex(edge.end)}
            if len(new_vertices & mst_vertices) == 1:
                mst_vertices = mst_vertices | new_vertices
                mst_edges = mst_edges | {edge}
                total_weight += edge.weight
                sorted_edges.remove(edge)
                break
    return UndirectedGraph(mst_vertices, mst_edges), total_weight
