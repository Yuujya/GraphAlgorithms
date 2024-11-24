from data_structures.graph import Vertex
from data_structures.directed_graph import DirectedGraph, Edge


class Capacity:
    def __init__(self, lower_capacity: int, upper_capacity: int):
        if lower_capacity <= upper_capacity:
            self.lower_capacity = lower_capacity
            self.upper_capacity = upper_capacity


class CapacitatedNetwork(DirectedGraph):
    def __init__(self, vertices: set[Vertex], edges: set[Edge],
                 capacity: dict[(int, int), Capacity]):
        super().__init__(vertices, edges)
        # Kanten mit unterer und oberer Kapazitaet
        self.capacity = capacity
