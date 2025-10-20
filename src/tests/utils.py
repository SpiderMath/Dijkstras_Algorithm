import random
import math
import networkx as nx

def create_connected_random_graph(n, p):
    G = nx.gnp_random_graph(n, p)

    # check connectedness
    if nx.is_connected(G):
        return G

    # Stitching the components together
    components = list(nx.connected_components(G))
    main_component = list(components[0])

    for comp in components[1:]:
        # Select one random node from the main component
        node_from_main = random.choice(main_component)
        node_from_other = random.choice(list(comp))
        G.add_edge(node_from_main, node_from_other)        
        main_component.extend(list(comp))

    return G


def add_random_weights(graph, w_min=1, w_max=20):
    for (u, v) in graph.edges():
        graph[u][v]['weight'] = random.randint(w_min, w_max)

    return graph


def create_arbitrary_graphs(n, p, w_min=1, w_max=20):
    return add_random_weights(create_connected_random_graph(n, p), w_min, w_max)


def normalise_dijkstra_preds(nx_preds):
    for node, preds in nx_preds.items():
        if preds:
            nx_preds[node] = [preds[0]]

    return nx_preds


def compare_dijkstra_results(g, source, custom_djk_function):
    """This function compares the output of a custom Dijkstra function against the NetworkX implementation"""

    nx_preds, nx_dists = nx.dijkstra_predecessor_and_distance(g, source)
    nx_preds = normalise_dijkstra_preds(nx_preds)
    # Assuming function returns (distances, predecessors)
    custom_dists, custom_preds = custom_djk_function(g, source)

    distances_match = True

    # Check if all reachable nodes in NetworkX are in our results
    for node, nx_dist in nx_dists.items():
        custom_dist = custom_dists.get(node)
        if custom_dist is None:
            distances_match = False
            break
        # Use math.isclose for robust float comparison
        if not math.isclose(nx_dist, custom_dist):
            distances_match = False
            break

    if distances_match and len(nx_dists) != len(custom_dists):
        distances_match = False

    predecessors_match = True

    # NOTE: NetworkX's predecessor dict omits the source node.
    for node, nx_pred in nx_preds.items():
        custom_pred = custom_preds.get(node)

        if custom_pred is None:
            predecessors_match = False
            break
        if custom_pred != nx_pred:
            predecessors_match = False
            break

    return distances_match and predecessors_match
