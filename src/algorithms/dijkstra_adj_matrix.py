def convert_graph_to_matrix(graph):
    """
    This function outputs the adjacency matrix of the input graph
    """
    nodes = list(graph.nodes())
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    num_nodes = len(nodes)

    matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        matrix[i][i] = 0

    is_directed = graph.is_directed()

    for u, v, data in graph.edges(data=True):
        weight = data.get('weight', 1.0)
        u_idx, v_idx = node_to_idx[u], node_to_idx[v]

        # Only set the outgoing edge
        matrix[u_idx][v_idx] = weight

        # If the graph is NOT directed, add the symmetric edge
        if not is_directed:
            matrix[v_idx][u_idx] = weight

    return matrix, node_to_idx, nodes

def dijkstra_matrix_simulation(adj_matrix, nodes, start_node_idx):
    """
    Implements Dijkstra's using a pre-computed adjacency matrix for true O(1) edge checks.
    """
    num_nodes = len(nodes)
    distances = {i: float('inf') for i in range(num_nodes)}
    predecessors_idx = {i: None for i in range(num_nodes)}
    distances[start_node_idx] = 0
    unvisited_nodes_idx = set(range(num_nodes))

    while unvisited_nodes_idx:
        current_min_idx = -1
        min_distance = float('inf')
        for idx in unvisited_nodes_idx:
            if distances[idx] < min_distance:
                min_distance = distances[idx]
                current_min_idx = idx

        if current_min_idx == -1 or distances[current_min_idx] == float('inf'):
            break

        for neighbor_idx in range(num_nodes):
            weight = adj_matrix[current_min_idx][neighbor_idx]
            if weight != float('inf'):
                new_distance = distances[current_min_idx] + weight
                if new_distance < distances[neighbor_idx]:
                    distances[neighbor_idx] = new_distance
                    predecessors_idx[neighbor_idx] = current_min_idx

        unvisited_nodes_idx.remove(current_min_idx)

    final_distances = {nodes[i]: dist for i, dist in distances.items()}
    final_predecessors = {nodes[i]: (nodes[p_idx] if p_idx is not None else None) for i, p_idx in predecessors_idx.items()}

    return final_distances, final_predecessors
