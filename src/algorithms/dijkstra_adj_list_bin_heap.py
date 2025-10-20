import heapq

def dijkstra_binary_heap(graph, start_node):
    distances = {node: float('inf') for node in graph.nodes()}
    predecessors = {node: [] for node in graph.nodes()}
    distances[start_node] = 0
    pq = [(0, start_node)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            new_distance = distances[current_node] + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = [current_node]
                heapq.heappush(pq, (new_distance, neighbor))

    return distances, predecessors
