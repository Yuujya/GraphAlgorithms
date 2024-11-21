import copy
from data_structures.mixed_graph import UndirectedGraph
from algorithms.connectivity.reachability_set import reachability_set


def __reachability_set_table(undirected_graph: UndirectedGraph, edge=None):
    if edge is not None:
        undirected_graph = copy.deepcopy(undirected_graph)
        undirected_graph.add_edge(edge)
    reachability_table = {}
    for vertex in undirected_graph.vertices:
        rset = reachability_set(undirected_graph, vertex)
        for reachibility_vertex in rset:
            reachability_table[reachibility_vertex.id] = rset
    return reachability_table


def kruskal(undirected_graph: UndirectedGraph):
    sorted_edges = sorted(undirected_graph.edges, key=lambda e: e.weight)
    mst = UndirectedGraph(undirected_graph.vertices, set())
    total_weight = 0
    for edge in sorted_edges:
        if __reachability_set_table(mst) != \
             __reachability_set_table(mst, edge):
            mst.add_edge(edge)
            total_weight += edge.weight
    return mst, total_weight
