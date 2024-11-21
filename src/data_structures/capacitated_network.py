from data_structures.directed_graph import DirectedGraph


class CapacitatedNetwork(DirectedGraph):
    def __init__(self, vertices, edges, source, sink):
        self.directed_graph = DirectedGraph(vertices, edges)
        self.source = source
        self.sink = sink
