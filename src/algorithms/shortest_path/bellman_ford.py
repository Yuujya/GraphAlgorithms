from shortest_path_helper import init_distance_table, \
                                 distance, \
                                 build_shortest_path
from data_structures.graph import Vertex
from data_structures.mixed_graph import MixedGraph


def bellman_ford(mixed_graph: MixedGraph,
                 start_vertex: Vertex,
                 target_vertex: Vertex = None):
    predecessors, distances = init_distance_table(mixed_graph, start_vertex)

    for _ in range(len(mixed_graph.vertices)-1):
        for edge in mixed_graph.edges:
            rhs = distances[edge.start] + \
                distance(mixed_graph,
                         Vertex(edge.start),
                         Vertex(edge.end),
                         True)
            if predecessors[edge.start] != edge.end and \
                    distances[edge.end] > rhs:
                distances[edge.end] = rhs
                predecessors[edge.end] = edge.start

    for edge in mixed_graph.edges:
        rhs = distances[edge.start] + \
                distance(mixed_graph,
                         Vertex(edge.start),
                         Vertex(edge.end),
                         True)
        if distances[edge.end] > rhs:
            print("Kreis mit negativer Laenge existiert")
            return {}, {}, []

    return build_shortest_path(predecessors, distances, target_vertex)
