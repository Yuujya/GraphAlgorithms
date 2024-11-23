import unittest
import math
from algorithms.shortest_path.dijkstra import dijkstra
from data_structures.directed_graph import DirectedGraph, Edge
from data_structures.graph import Vertex


class TestDijkstra(unittest.TestCase):
    def test_dijsktra(self):
        edges = {Edge(5, 1, 5), Edge(2, 3, 3),
                 Edge(2, 6, 4), Edge(6, 7, 1),
                 Edge(7, 4, 2)}
        vertices = {Vertex(i) for i in range(1, 7+1)}
        directed_graph = DirectedGraph(vertices, edges)
        start_vertex = Vertex(2)
        target_vertex = Vertex(4)
        expected_path = [Vertex(2), Vertex(6), Vertex(7), Vertex(4)]
        _, _, shortest_path = dijkstra(directed_graph,
                                       start_vertex,
                                       target_vertex)
        self.assertEqual(shortest_path, expected_path)

    def test_dijsktra_predecessors(self):
        edges = {Edge(5, 1, 5), Edge(2, 3, 3),
                 Edge(2, 6, 4), Edge(6, 7, 1),
                 Edge(7, 4, 2)}
        vertices = {Vertex(i) for i in range(1, 7+1)}
        directed_graph = DirectedGraph(vertices, edges)
        start_vertex = Vertex(2)
        expected_predecessors = {3: 2, 4: 7, 1: None,
                                 5: None, 6: 2, 7: 6, 2: 0}
        predecessors, _, _ = dijkstra(directed_graph,
                                      start_vertex)
        self.assertEqual(predecessors, expected_predecessors)

    def test_dijsktra_distances(self):
        edges = {Edge(5, 1, 5), Edge(2, 3, 3),
                 Edge(2, 6, 4), Edge(6, 7, 1),
                 Edge(7, 4, 2)}
        vertices = {Vertex(i) for i in range(1, 7+1)}
        directed_graph = DirectedGraph(vertices, edges)
        start_vertex = Vertex(2)
        expected_distances = {3: 3, 4: 7, 1: math.inf,
                              5: math.inf, 6: 4, 7: 5, 2: 0}
        _, distances, _ = dijkstra(directed_graph,
                                   start_vertex)
        self.assertEqual(distances, expected_distances)

    def test_dijsktra_no_target(self):
        edges = {Edge(5, 1, 5), Edge(2, 3, 3),
                 Edge(2, 6, 4), Edge(6, 7, 1),
                 Edge(7, 4, 2)}
        vertices = {Vertex(i) for i in range(1, 7+1)}
        directed_graph = DirectedGraph(vertices, edges)
        start_vertex = Vertex(2)
        _, _, shortest_path = dijkstra(directed_graph,
                                       start_vertex)
        self.assertEqual(shortest_path, [])


if __name__ == "__main__":
    unittest.main()
