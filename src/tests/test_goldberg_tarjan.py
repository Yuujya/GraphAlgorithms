import unittest
from algorithms.maximum_flow.goldberg_tarjan import compute_maximum_flow
from data_structures.directed_graph import Edge
from data_structures.capacitated_network import CapacitatedNetwork, Capacity
from data_structures.graph import Vertex


class TestEdmondsKarp(unittest.TestCase):
    def test_compute_maximum_flow(self):
        vertices = {Vertex('s'), Vertex('A'), Vertex('C'),
                    Vertex('B'), Vertex('D'), Vertex('t')}
        edges = {Edge('s', 'A', 13), Edge('s', 'C', 7), Edge('C', 'A', 6),
                 Edge('C', 'B', 6), Edge('C', 't', 4), Edge('A', 'B', 7),
                 Edge('A', 'D', 10), Edge('B', 'D', 8), Edge('B', 't', 3),
                 Edge('D', 't', 12)}
        capacity = {('s', 'A'): Capacity(0, 13), ('s', 'C'): Capacity(0, 7),
                    ('A', 'B'): Capacity(0, 7), ('C', 'A'): Capacity(0, 6),
                    ('C', 'B'): Capacity(0, 6), ('C', 't'): Capacity(0, 4),
                    ('B', 't'): Capacity(0, 3), ('B', 'D'): Capacity(0, 8),
                    ('A', 'D'): Capacity(0, 10), ('D', 't'): Capacity(0, 12)}
        capacitated_network = CapacitatedNetwork(vertices, edges, capacity)
        start_vertex = Vertex('s')
        target_vertex = Vertex('t')
        maximum_flow = compute_maximum_flow(capacitated_network,
                                            start_vertex,
                                            target_vertex)
        expected_flow = 19
        self.assertEqual(maximum_flow, expected_flow)


if __name__ == "__main__":
    unittest.main()
