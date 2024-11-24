from algorithms.shortest_path.shortest_path_helper \
    import init_distance_table, distance_argmin, distance, build_shortest_path
from data_structures.graph import Vertex
from data_structures.mixed_graph import MixedGraph


# Funktioniert sowohl fuer ungerichtete als auch gerichtete Graphen
# TODO: noch nicht an ungerichteten Graphen getestet
def dijkstra(mixed_graph: MixedGraph,
             start_vertex: Vertex,
             target_vertex: Vertex = None):
    predecessors, distances = init_distance_table(mixed_graph,
                                                  start_vertex)

    remaining_vertices = mixed_graph.vertices
    while remaining_vertices:
        i = Vertex(distance_argmin(distances, remaining_vertices))
        remaining_vertices = remaining_vertices - {i}

        adjacent_vertices = mixed_graph.adjacent_vertices(i)
        for adjacent_vertex in adjacent_vertices:
            rhs = distances[i.id] + \
                distance(mixed_graph, i, adjacent_vertex, False)
            if adjacent_vertex in remaining_vertices and \
                    (distances[adjacent_vertex.id] > rhs):
                distances[adjacent_vertex.id] = rhs
                predecessors[adjacent_vertex.id] = i.id

    return build_shortest_path(mixed_graph, predecessors,
                               distances, target_vertex)
