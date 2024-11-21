class VertexNotFoundError(Exception):
    def __init__(self, vertex):
        self.vertex = vertex
        self.message = f"Following vertex not found in graph: {vertex}"
        super().__init__(self.message)


class EdgeNotFoundError(Exception):
    def __init__(self, edge):
        self.edge = edge
        self.message = f"Following edge not found in graph: {edge}"
        super().__init__(self.message)
