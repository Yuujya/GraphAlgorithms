from data_structures.graph import Vertex
from data_structures.directed_graph import DirectedGraph, Edge, EdgeKey


class Capacity:
    def __init__(self, lower_capacity: int, upper_capacity: int):
        if lower_capacity <= upper_capacity:
            self.lower_capacity = lower_capacity
            self.upper_capacity = upper_capacity


# Hier werden antiparallele Kanten bestimmt und mit Hilfsknoten augmentiert
# Hilfsknoten werden der Knotenmenge hinzugefuegt
# Kanten ueber Knoten, die Hilfsknoten benoetigt hatten, werden ersetzt
# Analog mit Kapazitaeten dieser Art
class CapacitatedNetwork(DirectedGraph):
    def __init__(self, vertices: set[Vertex], edges: set[Edge],
                 capacity: dict[EdgeKey, Capacity],
                 source: Vertex, sink: Vertex):
        next_vertex = compute_next_vertex(vertices, source, sink)
        # Neue Knoten, Kanten und Kapazitaeten von Hilfsknoten bestimmen
        new_vertices, new_edges, new_capacity = compute(vertices,
                                                        edges,
                                                        capacity,
                                                        next_vertex)
        self.vertices = new_vertices
        self.edges = new_edges
        self.capacity = new_capacity


def compute(vertices: set[Vertex],
            edges: set[Edge],
            capacity: dict[EdgeKey, Capacity],
            next_vertex):
    new_vertices = set()
    new_edges = set()
    new_capacity = {}
    visited = set()
    # Suche Paare von Kanten mit antiparallelen Kanten
    for edge in edges:
        if Edge(edge.end, edge.start) in edges and \
             Edge(edge.end, edge.start) not in visited:
            visited.add(Edge(edge.start, edge.end))

    # Parallele Kante ueber Hilfsknoten aufteilen
    for edge in visited:
        helper_vertex = Vertex(next_vertex)
        new_vertices.add(helper_vertex)
        to_helper = Edge(edge.start, helper_vertex.id)
        from_helper = Edge(helper_vertex.id,
                           edge.end)
        new_edges.add(to_helper)
        new_edges.add(from_helper)
        new_capacity[(to_helper.start, to_helper.end)] = \
            Capacity(capacity[edge.edge].lower_capacity,
                     capacity[edge.edge].upper_capacity)
        new_capacity[(from_helper.start, from_helper.end)] = \
            Capacity(capacity[edge.edge].lower_capacity,
                     capacity[edge.edge].upper_capacity)
        next_vertex = chr(ord(next_vertex) + 1)
        # Alte Kanten und Kapazitaeten entfernen
        edges.remove(edge)
        del capacity[edge.edge]
    return new_vertices | vertices, new_edges | edges, new_capacity | capacity


def compute_next_vertex(vertices: set[Vertex], source: Vertex, sink: Vertex):
    temp_vertices = vertices - {source, sink}
    next_vertex = max({ord(v.id) for v in temp_vertices}) + 1
    return chr(next_vertex)
