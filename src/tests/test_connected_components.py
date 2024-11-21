import unittest
from algorithms.connectivity.connected_components \
    import create_undirected_graph, connected_components
from data_structures.mixed_graph import MixedGraph, Edge
from data_structures.graph import Vertex
from data_structures.undirected__graph import UndirectedGraph


class TestConnectedComponents(unittest.TestCase):

    def test_create_undirected_graph(self):
        edges = {Edge(1, 2, False), Edge(2, 7, False), Edge(5, 8, True),
                 Edge(8, 6, True), Edge(8, 4, True), Edge(6, 4, True)}
        vertices = {Vertex(i) for i in range(1, 8+1)}

        asserted_edges = {Edge(1, 2, False), Edge(2, 7, False),
                          Edge(5, 8, False), Edge(8, 6, False),
                          Edge(8, 4, False), Edge(6, 4, False)}
        mixed_graph = MixedGraph(vertices, edges, True)
        self.assertEqual(create_undirected_graph(mixed_graph),
                         UndirectedGraph(vertices, asserted_edges))

    def test_connected_components(self):
        edges = {Edge(1, 2, False), Edge(2, 7, False), Edge(5, 8, True),
                 Edge(8, 6, True), Edge(8, 4, True), Edge(6, 4, True)}
        vertices = {Vertex(i) for i in range(1, 8+1)}
        mixed_graph = MixedGraph(vertices, edges, True)
        undirected_graph = create_undirected_graph(mixed_graph)
        asserted_components = [{Vertex(6), Vertex(5), Vertex(8), Vertex(4)},
                               {Vertex(7), Vertex(2), Vertex(1)}, {Vertex(3)}]
        self.assertCountEqual(connected_components(undirected_graph),
                              asserted_components)


if __name__ == "__main__":
    unittest.main()
