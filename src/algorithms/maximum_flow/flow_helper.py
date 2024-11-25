from data_structures.graph import Vertex
from data_structures.directed_graph import EdgeKey, Edge
from data_structures.capacitated_network import CapacitatedNetwork


def compute_feasible_flow(capacitated_network: CapacitatedNetwork):
    is_zero_flow = all([capacitated_network.capacity[e.edge].
                        lower_capacity == 0
                        for e in capacitated_network.edges])
    if is_zero_flow:
        feasible_flow = {edge.edge: 0 for edge in capacitated_network.edges}
        return feasible_flow
    # Aufgabe 6.3.c


def get_predecessors(edges: set[Edge],
                     end_vertex: Vertex):
    predecessors = set()
    for edge in edges:
        if Edge(edge.start, end_vertex.id) in edges:
            predecessors.add(Vertex(edge.start))
    return predecessors


def get_successors(edges: set[Edge],
                   start_vertex: Vertex):
    successors = set()
    for edge in edges:
        if Edge(start_vertex.id, edge.end) in edges:
            successors.add(Vertex(edge.end))
    return successors


def ingoing_flow(flow: dict[EdgeKey, int],
                 edges: set[Edge],
                 end_vertex: Vertex):
    # Summe von phi(j, i), vertex ist i
    inflow = 0
    predecessors = get_predecessors(edges,  end_vertex)
    for predecessor in predecessors:
        if Edge(predecessor.id, end_vertex.id) in edges:
            inflow += flow[(predecessor.id, end_vertex.id)]
    return inflow


def outgoing_flow(flow: dict[EdgeKey, int],
                  edges: set[Edge],
                  start_vertex: Vertex):
    # Summe von phi(i, j), vertex ist i
    outflow = 0
    successors = get_successors(edges,  start_vertex)
    for successor in successors:
        if Edge(start_vertex.id, successor.id) in edges:
            outflow += flow[(start_vertex.id, successor.id)]
    return outflow


def total_flow(flow: dict[EdgeKey, int],
               edges: set[Edge],
               vertex: Vertex):
    return ingoing_flow(flow, edges, vertex) - outgoing_flow(flow, edges, vertex)


# Flusseigenschaft
def is_flow(capacitated_network: CapacitatedNetwork,
            start_vertex: Vertex,
            target_vertex: Vertex,
            flow: dict[EdgeKey, int]):
    # vertex ist i
    valid_flow = True
    for vertex in capacitated_network.vertices - {start_vertex, target_vertex}:
        if total_flow(flow, capacitated_network.edges, vertex) != 0:
            valid_flow = False
            break
    start_flow = total_flow(flow, capacitated_network.edges, start_vertex)
    target_flow = total_flow(flow, capacitated_network.edges, target_vertex)
    return valid_flow and -start_flow == target_flow


# Zulaessiger Fluss
def is_feasible_flow(capacitated_network: CapacitatedNetwork,
                     start_vertex: Vertex,
                     target_vertex: Vertex,
                     flow: dict[EdgeKey, int]):
    valid_flow = is_flow(capacitated_network, start_vertex,
                         target_vertex, flow)
    if valid_flow:
        return all([capacitated_network.capacity[e.edge].lower_capacity
                    <= flow[e.edge]
                    <= capacitated_network.capacity[e.edge].upper_capacity
                    for e in capacitated_network.edges])
    return False
