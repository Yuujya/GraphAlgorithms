import unittest
from algorithms.minimal_spanning_tree.kruskal import kruskal
from data_structures.undirected__graph import UndirectedGraph, Edge
from data_structures.graph import Vertex


class TestKruskal(unittest.TestCase):
    def test_kruskal_total_weight(self):
        edges = {Edge('A', 'B', 13), Edge('A', 'C', 6),
                 Edge('B', 'C', 7), Edge('B', 'D', 1),
                 Edge('C', 'D', 14), Edge('C', 'E', 8),
                 Edge('D', 'E', 9), Edge('D', 'F', 3),
                 Edge('E', 'F', 2), Edge('C', 'H', 20),
                 Edge('E', 'J', 18), Edge('G', 'H', 15),
                 Edge('G', 'I', 5), Edge('G', 'J', 19),
                 Edge('G', 'K', 10), Edge('H', 'J', 17),
                 Edge('I', 'K', 11), Edge('J', 'K', 16),
                 Edge('J', 'L', 4), Edge('K', 'L', 12)}
        vertices = {Vertex(chr(letter))
                    for letter in range(ord('A'), ord('L')+1, 1)}
        undirected_graph = UndirectedGraph(vertices, edges)
        _, total_weight = kruskal(undirected_graph)
        expected_weight = 83
        self.assertEqual(total_weight, expected_weight)


if __name__ == "__main__":
    unittest.main()
