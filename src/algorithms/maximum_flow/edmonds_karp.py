from data_structures.graph import Vertex
from data_structures.directed_graph import Edge
from data_structures.capacitated_network import CapacitatedNetwork, Capacity
from data_structures.residual_graph import ResidualGraph, conjugate_edge
from algorithms.shortest_path.dijkstra import dijkstra


def edmonds_karps(capacitated_network: CapacitatedNetwork,
                  start_vertex: Vertex, target_vertex: Vertex):
    # Schritt 0: Initial: zulaessiger Fluss
    maximum_flow = compute_feasible_flow(capacitated_network)
    # Schritt 1
    while True:
        residual_graph = ResidualGraph(capacitated_network, maximum_flow)
        shortest_path, _ = dijkstra(residual_graph,
                                    start_vertex, target_vertex)
        print(shortest_path)
        if not shortest_path:
            break
        # Kantenmenge vom kuerzesten Weg bestimmen
        p = {residual_graph.get_edge(shortest_path[k], shortest_path[k+1])
             for k in range(len(shortest_path)-1)}
        # update flow
        for edge in p & residual_graph.edges:
            maximum_flow[edge.edge] += min([residual_graph.get_upper_capacity(e) for e in p])
        for edge in p & residual_graph.back_edges:
            conjugated_edge = conjugate_edge(edge)
            maximum_flow[conjugated_edge.edge] -=\
                min([residual_graph.get_upper_capacity(e) for e in p])
    return maximum_flow


def compute_feasible_flow(capacitated_network: CapacitatedNetwork):
    is_zero_flow = all([capacitated_network.capacity[e.edge].lower_capacity == 0 for e in capacitated_network.edges])
    if is_zero_flow:
        feasible_flow = {edge.edge: 0 for edge in capacitated_network.edges}
        return feasible_flow
    # Aufgabe 6.3.c


# Bsp 4.7
# vertices = {Vertex(i) for i in range(1, 4+1)}
# edges = {Edge(1, 2), Edge(1, 3), Edge(3, 2), Edge(3, 4), Edge(2, 4)}
# capacity = {(1, 2): Capacity(0, 1), (1, 3): Capacity(1, 2),
#             (3, 2): Capacity(1, 3), (3, 4): Capacity(0, 4),
#             (2, 4): Capacity(0, 3)}
# capacitated_network = CapacitatedNetwork(vertices, edges, capacity)
# flow = {(1, 2): 0, (1, 3): 2,
#         (3, 2): 1, (3, 4): 1, (2, 4): 1}
# residual_graph = ResidualGraph(capacitated_network, flow)

# Bsp 4.12
# vertices = {Vertex('s'), Vertex('A'), Vertex('C'),
#             Vertex('B'), Vertex('D'), Vertex('t')}
# edges = {Edge('s', 'A', 13), Edge('s', 'C', 7), Edge('C', 'A', 6),
#          Edge('C', 'B', 6), Edge('C', 't', 4), Edge('A', 'B', 7),
#          Edge('A', 'D', 10), Edge('B', 'D', 8), Edge('B', 't', 3),
#          Edge('D', 't', 12)}
# capacity = {('s', 'A'): Capacity(0, 13), ('s', 'C'): Capacity(0, 7),
#             ('A', 'B'): Capacity(0, 7), ('C', 'A'): Capacity(0, 6),
#             ('C', 'B'): Capacity(0, 6), ('C', 't'): Capacity(0, 4),
#             ('B', 't'): Capacity(0, 3), ('B', 'D'): Capacity(0, 8),
#             ('A', 'D'): Capacity(0, 10), ('D', 't'): Capacity(0, 12)}
# capacitated_network = CapacitatedNetwork(vertices, edges, capacity)
# start_vertex = Vertex('s')
# target_vertex = Vertex('t')
# maximum_flow = edmonds_karps(capacitated_network, start_vertex, target_vertex)
# print("done")
