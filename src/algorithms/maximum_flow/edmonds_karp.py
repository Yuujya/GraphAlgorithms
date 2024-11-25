from data_structures.graph import Vertex
from data_structures.capacitated_network import CapacitatedNetwork
from data_structures.residual_graph import ResidualGraph, conjugate_edge
from algorithms.shortest_path.dijkstra import dijkstra
from algorithms.maximum_flow.flow_helper \
    import compute_feasible_flow, is_feasible_flow, outgoing_flow


def edmonds_karp(capacitated_network: CapacitatedNetwork,
                 start_vertex: Vertex, target_vertex: Vertex):
    # Schritt 0: Initial: zulaessiger Fluss
    flow = compute_feasible_flow(capacitated_network)
    # Schritt 1
    while True:
        residual_graph = ResidualGraph(capacitated_network, flow)
        shortest_path, _ = dijkstra(residual_graph,
                                    start_vertex, target_vertex)
        if not shortest_path:
            break
        # Kantenmenge vom kuerzesten Weg bestimmen
        p = {residual_graph.get_edge(shortest_path[k], shortest_path[k+1])
             for k in range(len(shortest_path)-1)}
        # update flow
        for edge in p & residual_graph.edges:
            flow[edge.edge] += min([residual_graph.
                                    get_upper_capacity(e) for e in p])
        for edge in p & residual_graph.back_edges:
            conjugated_edge = conjugate_edge(edge)
            flow[conjugated_edge.edge] -=\
                min([residual_graph.get_upper_capacity(e) for e in p])
    return flow


def compute_maximum_flow(capacitated_network: CapacitatedNetwork,
                         start_vertex: Vertex, target_vertex: Vertex):
    flow = edmonds_karp(capacitated_network,
                        start_vertex,
                        target_vertex)
    if is_feasible_flow(capacitated_network,
                        start_vertex,
                        target_vertex,
                        flow):
        return outgoing_flow(flow,
                             capacitated_network.edges,
                             start_vertex)
    return -1
