from .data_structures import fib_heap
import math

def dijkstra_fibonacci_heap(graph, start_node):
    distances = {}
    predecessors = {}
    
    # heap_nodes maps graph vertices to their corresponding Node objects
    # in the Fibonacci heap. This is crucial for decrease_key.
    heap_nodes = {}
    
    pq = fib_heap.FibonacciHeap()

    for node in graph.nodes():
        if node == start_node:
            distances[node] = 0.0
            heap_nodes[node] = pq.insert(0.0, node)
        else:
            distances[node] = math.inf
            heap_nodes[node] = pq.insert(math.inf, node)

        predecessors[node] = None

    while pq.total_nodes > 0:
        min_heap_node = pq.extract_min()
        if min_heap_node is None:
            break # Heap is empty

        u = min_heap_node.value
        u_dist = min_heap_node.key

        if u_dist == math.inf:
            break

        # Relax all edges outgoing from u
        for v, edge_data in graph[u].items():
            # Get edge weight, default to 1.0 if not specified
            weight = edge_data.get('weight', 1.0)
            
            new_dist = u_dist + weight

            # If we found a shorter path to v
            if new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u

                # Update v's priority in the Fibonacci heap
                v_heap_node = heap_nodes[v]
                pq.decrease_key(v_heap_node, new_dist)

    return distances, predecessors