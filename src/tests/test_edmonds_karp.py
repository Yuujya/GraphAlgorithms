import unittest
from algorithms.maximum_flow.edmonds_karp import compute_maximum_flow
from data_structures.directed_graph import Edge
from data_structures.capacitated_network import CapacitatedNetwork, Capacity
from data_structures.graph import Vertex


class TestEdmondsKarp(unittest.TestCase):
    def test_compute_maximum_flow(self):
        vertices = {Vertex('s'), Vertex('A'), Vertex('C'),
                    Vertex('B'), Vertex('D'), Vertex('t')}
        edges = {Edge('s', 'A'), Edge('s', 'C'), Edge('C', 'A'),
                 Edge('C', 'B'), Edge('C', 't'), Edge('A', 'B'),
                 Edge('A', 'D'), Edge('B', 'D'), Edge('B', 't'),
                 Edge('D', 't')}
        capacity = {('s', 'A'): Capacity(0, 13), ('s', 'C'): Capacity(0, 7),
                    ('A', 'B'): Capacity(0, 7), ('C', 'A'): Capacity(0, 6),
                    ('C', 'B'): Capacity(0, 6), ('C', 't'): Capacity(0, 4),
                    ('B', 't'): Capacity(0, 3), ('B', 'D'): Capacity(0, 8),
                    ('A', 'D'): Capacity(0, 10), ('D', 't'): Capacity(0, 12)}
        source = Vertex('s')
        sink = Vertex('t')
        capacitated_network = CapacitatedNetwork(vertices, edges, capacity,
                                                 source, sink)
        maximum_flow_value = compute_maximum_flow(capacitated_network,
                                                  source,
                                                  sink)
        expected_flow = 19
        self.assertEqual(maximum_flow_value, expected_flow)

    def test_compute_maximum_flow2(self):
        vertices = {Vertex('s'), Vertex('A'), Vertex('C'),
                    Vertex('B'), Vertex('D'), Vertex('t')}
        edges = {Edge('s', 'A'), Edge('s', 'B'), Edge('B', 'A'),
                 Edge('A', 'B'), Edge('C', 'B'), Edge('A', 'C'),
                 Edge('B', 'D'), Edge('D', 'C'), Edge('C', 't'),
                 Edge('D', 't')}
        capacity = {('s', 'A'): Capacity(0, 16), ('s', 'B'): Capacity(0, 13),
                    ('B', 'A'): Capacity(0, 4), ('A', 'B'): Capacity(0, 10),
                    ('C', 'B'): Capacity(0, 9), ('A', 'C'): Capacity(0, 12),
                    ('B', 'D'): Capacity(0, 14), ('D', 'C'): Capacity(0, 7),
                    ('C', 't'): Capacity(0, 20), ('D', 't'): Capacity(0, 4)}
        source = Vertex('s')
        sink = Vertex('t')
        capacitated_network = CapacitatedNetwork(vertices, edges, capacity,
                                                 source, sink)
        maximum_flow = compute_maximum_flow(capacitated_network,
                                            source,
                                            sink)
        expected_flow = 23
        self.assertEqual(maximum_flow, expected_flow)


if __name__ == "__main__":
    unittest.main()
