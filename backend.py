import sys

# 간선 정의
class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

def bellman_ford(vertices, edges, start):
    dist = [float('inf')] * vertices
    dist[start] = 0

    # V-1 번 반복
    for _ in range(vertices - 1):
        for edge in edges:
            if dist[edge.src] != float('inf') and dist[edge.src] + edge.weight < dist[edge.dest]:
                dist[edge.dest] = dist[edge.src] + edge.weight

    return dist

def find_nearest_station(stations, dist):
    min_dist = float('inf')
    nearest_station = -1
    for station in stations:
        if dist[station] < min_dist:
            min_dist = dist[station]
            nearest_station = station
    return nearest_station, min_dist
