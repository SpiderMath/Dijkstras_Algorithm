import math

def dijkstra_adj_matrix(G, source_node):
    nodes = list(G.nodes())
    V = len(nodes)

    if source_node not in nodes:
        raise ValueError("Source node is not in the graph.")

    node_to_index = {node: i for i, node in enumerate(nodes)}
    adj_matrix = [[0 for _ in range(V)] for _ in range(V)]

    for u, neighbors in G.adj.items():
        u_index = node_to_index[u]
        for v, edge_data in neighbors.items():
            v_index = node_to_index[v]
            adj_matrix[u_index][v_index] = edge_data.get('weight', 1)

    source_index = node_to_index[source_node]

    dist = [math.inf] * V
    visited = [False] * V
    predecessors = [None] * V

    dist[source_index] = 0

    for _ in range(V):
        min_dist = math.inf
        u = -1

        for i in range(V):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        if u == -1:
            break

        visited[u] = True

        for v in range(V):
            edge_weight = adj_matrix[u][v]

            if not visited[v] and edge_weight > 0 and dist[u] != math.inf and dist[u] + edge_weight < dist[v]:

                dist[v] = dist[u] + edge_weight
                predecessors[v] = u

    final_distances = {}
    final_predecessors = {}

    for i in range(V):
        node_label = nodes[i]
        final_distances[node_label] = dist[i]

        pred_index = predecessors[i]
        if pred_index is not None:
            final_predecessors[node_label] = [nodes[pred_index]]
        else:
            final_predecessors[node_label] = []

    return final_distances, final_predecessors
