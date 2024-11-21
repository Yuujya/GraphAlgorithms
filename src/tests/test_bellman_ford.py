import unittest
from algorithms.shortest_path.bellman_ford import bellman_ford
from data_structures.mixed_graph import MixedGraph, Edge
from data_structures.graph import Vertex


class TestBellmanFord(unittest.TestCase):
    def test_bellman_ford(self):
        edges = {Edge(1, 2, True, 4), Edge(2, 1, True, 3),
                 Edge(1, 4, True, -2), Edge(4, 2, True, 2),
                 Edge(2, 4, True, 2), Edge(2, 3, True, 2),
                 Edge(3, 5, True, 1), Edge(5, 3, True, 3),
                 Edge(4, 5, True, 2), Edge(5, 4, True, 3), Edge(4, 3, True, 6)}
        vertices = {Vertex(i) for i in range(1, 5+1)}
        mixed_graph = MixedGraph(vertices, edges, True)
        start_vertex = Vertex(2)
        target_vertex = Vertex(5)
        expected_path = [Vertex(2), Vertex(1), Vertex(4), Vertex(5)]
        _, _, shortest_path = bellman_ford(mixed_graph,
                                           start_vertex,
                                           target_vertex)
        self.assertEqual(shortest_path, expected_path)

    def test_bellman_ford_predecessors(self):
        edges = {Edge(1, 2, True, 4), Edge(2, 1, True, 3),
                 Edge(1, 4, True, -2), Edge(4, 2, True, 2),
                 Edge(2, 4, True, 2), Edge(2, 3, True, 2),
                 Edge(3, 5, True, 1), Edge(5, 3, True, 3),
                 Edge(4, 5, True, 2), Edge(5, 4, True, 3), Edge(4, 3, True, 6)}
        vertices = {Vertex(i) for i in range(1, 5+1)}
        mixed_graph = MixedGraph(vertices, edges, True)
        start_vertex = Vertex(2)
        expected_predecessors = {5: 4, 3: 2, 1: 2, 4: 1, 2: 0}
        predecessors, _, _ = bellman_ford(mixed_graph,
                                          start_vertex)
        self.assertEqual(predecessors, expected_predecessors)

    def test_bellman_ford_distances(self):
        edges = {Edge(1, 2, True, 4), Edge(2, 1, True, 3),
                 Edge(1, 4, True, -2), Edge(4, 2, True, 2),
                 Edge(2, 4, True, 2), Edge(2, 3, True, 2),
                 Edge(3, 5, True, 1), Edge(5, 3, True, 3),
                 Edge(4, 5, True, 2), Edge(5, 4, True, 3), Edge(4, 3, True, 6)}
        vertices = {Vertex(i) for i in range(1, 5+1)}
        mixed_graph = MixedGraph(vertices, edges, True)
        start_vertex = Vertex(2)
        expected_distances = {5: 3, 3: 2, 1: 3, 4: 1, 2: 0}
        _, distances, _ = bellman_ford(mixed_graph,
                                       start_vertex)
        self.assertEqual(distances, expected_distances)

    def test_bellman_ford_no_target(self):
        edges = {Edge(1, 2, True, 4), Edge(2, 1, True, 3),
                 Edge(1, 4, True, -2), Edge(4, 2, True, 2),
                 Edge(2, 4, True, 2), Edge(2, 3, True, 2),
                 Edge(3, 5, True, 1), Edge(5, 3, True, 3),
                 Edge(4, 5, True, 2), Edge(5, 4, True, 3), Edge(4, 3, True, 6)}
        vertices = {Vertex(i) for i in range(1, 5+1)}
        mixed_graph = MixedGraph(vertices, edges, True)
        start_vertex = Vertex(2)
        _, _, shortest_path = bellman_ford(mixed_graph,
                                           start_vertex)
        self.assertEqual(shortest_path, [])


if __name__ == "__main__":
    unittest.main()
