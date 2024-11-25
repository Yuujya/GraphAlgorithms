from data_structures.graph import Vertex
from data_structures.directed_graph import Edge, DirectedGraph
from data_structures.capacitated_network import CapacitatedNetwork
from data_structures.residual_graph import ResidualGraph
from algorithms.shortest_path.dijkstra import dijkstra
from algorithms.maximum_flow.flow_helper \
    import compute_feasible_flow, is_feasible_flow, ingoing_flow


def goldberg_tarjan(capacitated_network: CapacitatedNetwork,
                    start_vertex: Vertex,
                    target_vertex: Vertex):
    # Initial ein zulaessiger Fluss, am Ende ein maximaler Fluss
    flow = compute_feasible_flow(capacitated_network)

    # Schritt 0 Abstandstabelle h bis zur Senke t in rot
    distances_to_target = {start_vertex.id: len(capacitated_network.vertices)}
    edges = {Edge(e.start, e.end) for e in capacitated_network.edges}
    temp_graph = DirectedGraph(capacitated_network.vertices, edges)
    for vertex in capacitated_network.vertices - {start_vertex}:
        _, distances_to_target[vertex.id] =\
            dijkstra(temp_graph,
                     vertex,
                     target_vertex)
    adjacent_vertices = \
        capacitated_network.adjacent_vertices(start_vertex) - {target_vertex}
    # Q ist die Menge mit den Knoten, die noch Ueberschuss besitzen
    vertices_with_excess = set()
    # Ueberschuss ex in orange
    excess = {v.id: 0
              for v in capacitated_network.vertices -
              {start_vertex, target_vertex}}

    for vertex in adjacent_vertices:
        edge = (start_vertex.id, vertex.id)
        if flow[edge] < capacitated_network.capacity[edge].upper_capacity:
            flow[edge] = capacitated_network.capacity[edge].upper_capacity
            vertices_with_excess = vertices_with_excess | {vertex}
            excess[vertex.id] = flow[edge]
    residual_graph = ResidualGraph(capacitated_network, flow)

    # Schritt 1
    while vertices_with_excess:
        v = next(iter(vertices_with_excess))
        next_vertices = {w for w in capacitated_network.vertices
                         if Edge(v.id, w.id) in residual_graph.total_edges and
                         distances_to_target[v.id] == distances_to_target[w.id]
                         + 1}
        # Schritt 2 Relabel
        if not next_vertices:
            distances_to_target[v.id] = \
                min({distances_to_target[w.id]
                     for w in capacitated_network.vertices
                     if Edge(v.id, w.id) in residual_graph.total_edges}) + 1
            continue
        # Schritt 3 Push
        w = next(iter(next_vertices))
        if Edge(v.id, w.id) in residual_graph.edges:
            diff = min({excess[v.id],
                        residual_graph.capacity[(v.id, w.id)].upper_capacity})
            flow[(v.id, w.id)] += diff
            # Ueberschuss ex updaten
            excess[v.id] -= diff
            if w.id != target_vertex.id:
                excess[w.id] += diff
                vertices_with_excess.add(w)
        if Edge(v.id, w.id) in residual_graph.back_edges:
            diff = min({excess[v.id],
                        residual_graph.capacity[(v.id, w.id)].upper_capacity})
            flow[(w.id, v.id)] -= diff
            excess[v.id] -= diff
            if w.id != target_vertex.id and w.id != start_vertex.id:
                excess[w.id] += diff
                vertices_with_excess.add(w)
        if excess[v.id] == 0:
            vertices_with_excess -= {v}
        residual_graph = ResidualGraph(capacitated_network, flow)
    return flow


def compute_maximum_flow(capacitated_network: CapacitatedNetwork,
                         start_vertex: Vertex, target_vertex: Vertex):
    maximum_flow = goldberg_tarjan(capacitated_network,
                                   start_vertex,
                                   target_vertex)
    if is_feasible_flow(capacitated_network,
                        start_vertex,
                        target_vertex,
                        maximum_flow):
        return ingoing_flow(maximum_flow,
                            capacitated_network.edges,
                            target_vertex)
    return -1
