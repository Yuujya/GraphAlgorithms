# Kante in Graphen mit gerichteten und ungerichteten Kanten
class Edge:
    def __init__(self, start, end, directed=True, weight=0):
        if directed:
            self.start = start
            self.end = end
        # ungerichtete Kanten werden sortiert mit i<j in {i,j}
        else:
            self.start = min(start, end)
            self.end = max(start, end)
        self.directed = directed
        self.weight = weight

    def __hash__(self):
        if self.directed:
            return hash((min(self.start, self.end), max(self.start, self.end)))
        return hash((self.start, self.end))

    def __eq__(self, other):
        if not self.directed:
            return (self.start == other.start and self.end == other.end) \
                or (self.start == other.end and self.end == other.start)
        return self.start == other.start and self.end == other.end

    def __str__(self):
        if self.directed:
            return f"({self.start}, {self.end})"
        return f"{{{self.start}, {self.end}}}"
