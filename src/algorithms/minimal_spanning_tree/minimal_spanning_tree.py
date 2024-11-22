import copy
from data_structures.undirected__graph import UndirectedGraph
from algorithms.connectivity.connected_components import connected_components


def compute_mst(undirected_graph: UndirectedGraph):
    sorted_edges = sorted(undirected_graph.edges,
                          key=lambda e: e.weight, reverse=True)
    i = 0
    graph = copy.deepcopy(undirected_graph)

    while i != len(sorted_edges)-1:
        edge = sorted_edges[i]
        graph.remove_edge(edge)
        if len(connected_components(graph)) == 1:
            graph.edges = graph.edges - {edge}
        else:
            graph.add_edge(edge)
        if i < len(sorted_edges)-1:
            i += 1

    total_weight = sum([edge.weight for edge in graph.edges])
    return UndirectedGraph(graph.vertices, graph.edges), total_weight
