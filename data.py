class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

vertices = 5
edges = [
    Edge(0, 1, 4), Edge(0, 2, 2), Edge(1, 2, 3), Edge(1, 3, 2),
    Edge(2, 3, 4), Edge(2, 4, 5), Edge(3, 4, 1)
]
bike_stations = [2, 4]  # 자전거 대여소 위치