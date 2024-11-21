from shortest_path_helper import init_distance_table, \
                                 distance_argmin, distance, build_shortest_path
from data_structures.graph import Vertex
from data_structures.undirected__graph import UndirectedGraph


def dijkstra(undirected_graph: UndirectedGraph,
             start_vertex: Vertex,
             target_vertex: Vertex = None):
    predecessors, distances = init_distance_table(undirected_graph,
                                                  start_vertex)

    remaining_vertices = undirected_graph.vertices
    while remaining_vertices:
        i = Vertex(distance_argmin(distances, remaining_vertices))
        remaining_vertices = remaining_vertices - {i}

        adjacent_vertices = undirected_graph.adjacent_vertices(i)
        for adjacent_vertex in adjacent_vertices:
            rhs = distances[i.id] + \
                distance(undirected_graph, i, adjacent_vertex, False)
            if adjacent_vertex in remaining_vertices and \
                    (distances[adjacent_vertex.id] > rhs):
                distances[adjacent_vertex.id] = rhs
                predecessors[adjacent_vertex.id] = i.id

    return build_shortest_path(predecessors, distances, target_vertex)
