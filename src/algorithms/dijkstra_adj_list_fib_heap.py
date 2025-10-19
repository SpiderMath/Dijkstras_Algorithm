from .data_structures import fib_heap

def dijkstra_fibonacci_heap(graph, start_node):
    """
    Implements Dijkstra's using an adjacency list concept and a Fibonacci heap.
    """
    distances = {node: float('inf') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    distances[start_node] = 0

    heap = fib_heap.FibonacciHeap()
    entries = {}

    for node in graph.nodes():
        entries[node] = heap.insert(distances[node], node)

    while heap.total_nodes > 0:
        min_entry = heap.extract_min()
        current_node = min_entry.value

        if current_node is None or distances[current_node] == float('inf'):
            break

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            new_distance = distances[current_node] + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                heap.decrease_key(entries[neighbor], new_distance)

    return distances, predecessors
