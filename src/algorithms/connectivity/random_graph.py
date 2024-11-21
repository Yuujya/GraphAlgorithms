import random
from data_structures.graph import Vertex
from data_structures.mixed_graph import MixedGraph, Edge


def create_random_graph(n, m):
    """Zufaelligen Graph generieren mit n Knoten und m Kanten."""
    vertices = {Vertex(i) for i in range(1, n + 1)}
    edges = set()
    done = m
    while done != 0:
        start = random.randint(1, n)
        end = random.randint(1, m)
        direction = random.randint(0, 1)
        if start != end and direction == 0:
            edge = Edge(start, end, False)
        if start != end and direction == 1:
            edge = Edge(start, end)
        if edge not in edges:
            edges.add(edge)
            done -= 1
    return MixedGraph(vertices, edges, True)
