from heapq import heappop, heappush
import math
import networkx as nx

def dijkstra(graph: nx.Graph, source_node: int):
    distances = { node: math.inf for node in graph.nodes }
    predecessors = { node: None for node in graph.nodes }
    distances[source_node] = 0

    visited = set()

    priority_queue = [(0, source_node)]

    while priority_queue:
        current_distance, current_node = heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbour in graph.neighbours(current_node):
            if neighbour not in visited:
                weight = graph[current_node][neighbour].get('weight', 1)
                new_distance = current_distance + weight

                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    predecessors[neighbour] = current_node
                    heappush(priority_queue, (new_distance, neighbour))

    return distances, predecessors
