import unittest
from algorithms.connectivity.reachability_set import reachability_set
from data_structures.mixed_graph import MixedGraph, Edge
from data_structures.graph import Vertex


class TestReachabilitySet(unittest.TestCase):
    # Der Test ist noch falsch!
    def test_reachability_set(self):
        edges = {Edge(1, 2, False), Edge(2, 7, False), Edge(5, 8, True),
                 Edge(8, 6, True), Edge(8, 4, True), Edge(6, 4, True)}
        vertices = {Vertex(i) for i in range(1, 8+1)}
        expected_vertices = {Vertex(5), Vertex(4), Vertex(8), Vertex(6)}
        mixed_graph = MixedGraph(vertices, edges, True)
        start_vertex = Vertex(5)
        self.assertSetEqual(reachability_set(mixed_graph, start_vertex),
                            expected_vertices)


if __name__ == "__main__":
    unittest.main()
