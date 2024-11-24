from algorithms.shortest_path.shortest_path_helper \
    import init_distance_table, distance, build_shortest_path
from data_structures.graph import Vertex
from data_structures.mixed_graph import MixedGraph, Edge


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

    return build_shortest_path(mixed_graph, predecessors, distances, target_vertex)


edges = {Edge(1, 2, True, 4), Edge(2, 1, True, 3),
         Edge(1, 4, True, -2), Edge(4, 2, True, 2),
         Edge(2, 4, True, 2), Edge(2, 3, True, 2),
         Edge(3, 5, True, 1), Edge(5, 3, True, 3),
         Edge(4, 5, True, 2), Edge(5, 4, True, 3), Edge(4, 3, True, 6)}
vertices = {Vertex(i) for i in range(1, 5+1)}
mixed_graph = MixedGraph(vertices, edges, True)
start_vertex = Vertex(2)
target_vertex = Vertex(5)
expected_path = [Vertex(2), Vertex(1), Vertex(4), Vertex(5)]
shortest_path, _ = bellman_ford(mixed_graph,
                                start_vertex,
                                target_vertex)
print("done")
