from heapq import heappop, heappush
import math
import networkx as nx

def dijkstra_visual(graph: nx.Graph, source_node: int):
    distances = { node: math.inf for node in graph.nodes }
    predecessors = { node: None for node in graph.nodes }
    visited = set()

    priority_queue = [(0, source_node)]
    distances[source_node] = 0

    while priority_queue:
        current_distance, current_node = heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        yield {
            "current_node": current_node,
            "visited_nodes": visited.copy(),
            "distances": distances.copy(),
            "predecessors": predecessors.copy(),
        }

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                weight = graph[current_node][neighbor].get('weight', 1)
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    heappush(priority_queue, (new_distance, neighbor))

        yield {
            "current_node": current_node,
            "visited_nodes": visited.copy(),
            "distances": distances.copy(),
            "predecessors": predecessors.copy(),
        }
