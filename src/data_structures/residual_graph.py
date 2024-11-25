from data_structures.graph import Vertex
from data_structures.directed_graph import DirectedGraph, Edge, EdgeKey
from data_structures.capacitated_network import CapacitatedNetwork, Capacity


class ResidualGraph(DirectedGraph):
    def __init__(self, capacitated_network: CapacitatedNetwork,
                 flow: dict[EdgeKey, int]):
        self.vertices = capacitated_network.vertices
        self.edges = self.compute_edges(capacitated_network, flow)
        self.back_edges = self.compute_back_edges(capacitated_network, flow)
        self.total_edges = self.edges | self.back_edges
        self.capacity = self.compute_capacities(capacitated_network, flow)

    def get_edge(self, start_vertex, end_vertex):
        for edge in self.edges:
            if edge == Edge(start_vertex.id, end_vertex.id):
                return edge
        return None

    def get_edge_weight(self, start_vertex, end_vertex):
        edge = self.get_edge(start_vertex, end_vertex)
        if edge is None:
            return 0
        return edge.weight

    def get_upper_capacity(self, edge: Edge):
        edge = self.get_edge(Vertex(edge.start), Vertex(edge.end))
        if edge is None:
            return 0
        return self.capacity[edge.edge].upper_capacity

    def compute_edges(self, capacitated_network: CapacitatedNetwork,
                      flow: dict[EdgeKey, int]):
        edges = set()
        for edge in capacitated_network.edges:
            if flow[edge.edge] < capacitated_network.\
                 capacity[edge.edge].upper_capacity:
                # Kante mit Kantenbewertung von eins
                edges.add(Edge(edge.start, edge.end))
        return edges

    def compute_back_edges(self, capacitated_network: CapacitatedNetwork,
                           flow: dict[EdgeKey, int]):
        back_edges = set()
        for edge in capacitated_network.edges:
            if flow[edge.edge] > capacitated_network.\
                 capacity[edge.edge].lower_capacity:
                # Kante mit Kantenbewertung von eins
                back_edges.add(conjugate_edge(edge))
        return back_edges

    # Kapazitaeten zu neu berechneten Kanten bestimmen
    def compute_capacities(self, capacitated_network: CapacitatedNetwork,
                           flow: dict[EdgeKey, int]):
        capacity = {}
        for edge in self.edges:
            # hier ist phi(e) < u(e), also u(e) - phi(e) > 0
            u = capacitated_network.capacity[edge.edge]\
                .upper_capacity - flow[edge.edge]
            capacity[edge.edge] = Capacity(0, u)
        for edge in self.back_edges:
            conjugated_edge = conjugate_edge(edge)
            # hier ist phi(e) > l(e), also phi(e) - l(e) > 0
            u = flow[conjugated_edge.edge] - capacitated_network.\
                capacity[conjugated_edge.edge].lower_capacity
            capacity[edge.edge] = Capacity(0, u)
        return capacity


def conjugate_edge(edge: Edge):
    return Edge(edge.end, edge.start)
