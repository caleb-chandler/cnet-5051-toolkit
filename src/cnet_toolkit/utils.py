# imports
import random
import networkx as nx
import math
import numpy as np

def random_edge(G):
    '''
    selects one edge at random from graph G and returns its two nodes

    Args:
        G (nx.Graph): the graph to be referenced

    Returns:
        list: a list of the two nodes from selected edge
    '''
    edges = list(G.edges())

    random_edge = random.choice(edges)

    return list(random_edge)

def random_node(G):
    ''' 
    selects a random node from graph G
    '''
    return random.choice(list(G.nodes()))

def centrality_function_tester(user_func, nx_func):
    ''' 
    When given a function which is intended to calculate a centrality metric, tests
    it by exposing it to a variety of edge cases and comparing its output with its
    corresponding in-built NetworkX function. User function must return single int.

    Args:
        user_func (function): user's function
        nx_func (NetworkX function)
    
    Returns:
        str: message declaring results of test
    '''
    # init list of failures to potentially be appended later
    failures = []

    # testing normal graph (erdos renyi)
    G = nx.erdos_renyi_graph(50, 0.5)
    k = random_node(G)
    user_output = user_func(G, k)
    nx_output = nx_func(G, k)
    # using math.isclose function to account for negligible differences
    if not math.isclose(user_output, nx_output[k]):
        failures.append('Basic functionality')
    else:
        pass

    # testing disconnected graph
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    G.add_node(3)
    k = 0
    user_output = user_func(G, k)
    nx_output = nx_func(G, k)
    if not math.isclose(user_output, nx_output[k]):
        failures.append('Disconnected graph')
    else:
        pass

    # testing complete graph
    G = nx.complete_graph(50)
    k = random_node(G)
    user_output = user_func(G, k)
    nx_output = nx_func(G, k)
    if not math.isclose(user_output, nx_output[k]):
        failures.append('Complete graph')
    else:
        pass

    # testing non-networkx graph input
    try:
        user_output = user_func(12, 0)
        if user_output is not None:
            failures.append('Non-NetworkX graph input (did not return None)')
    except:
        failures.append('Non-NetworkX graph input (crashed)')

    # testing empty graph
    try:
        user_output = user_func(nx.empty_graph(), 0)
        if user_output is not None:
            failures.append('Empty graph (did not return None)')
    except:
        failures.append('Empty graph (crashed)')

    # testing graph with no edges
    G = nx.empty_graph(50)
    k = random_node(G)
    user_output = user_func(G, k)
    nx_output = nx_func(G, k)
    if not math.isclose(user_output, nx_output[k]):
        failures.append('Edgeless graph')
    else:
        pass

    # testing node not in G
    try:
        user_output = user_func(nx.path_graph(5), 50)
        if user_output is not None:
            failures.append('Node not in graph (did not return None)')
    except:
        failures.append('Node not in graph (crashed)')

    # check if there were any failures and return result based on that
    if not failures:
        return "All scenarios passed. Test successful."
    else:
        return f"Test failed at edge case(s): {[failures]} "
    
def avg_adj_matrix(sample, degrees): # function to calculate avg adjacency matrix
    n = len(degrees)
    sum_matrix = np.zeros((n, n)) # zero matrix to act as "running total"
    for g in sample:
        sum_matrix += nx.to_numpy_array(g) # convert to array and add to sum
    avg_matrix = sum_matrix / len(sample)
    return avg_matrix

def randomWalkGenerator(n, p):
    G = nx.Graph()
    G.add_node(0)

    # section to deal with n=1 edge case
    if n == 1:
        return G
    G.add_edge(0, 1)

    for i in range(2, n):
        existing_nodes = list(range(i))
        G.add_node(i)
        j = random.choice(existing_nodes) # choosing random existing node
        G.add_edge(i, j)
        x = random.choice(existing_nodes) # choosing another random existing node
        if random.random() < p:
            j_neighbors = list(G.neighbors(j))
            j_neighbors.remove(i) # avoiding connection to i itself
            if len(j_neighbors) > 0:
                v = random.choice(j_neighbors)
                G.add_edge(i, v)
            else:
                G.add_edge(i, x) # fallback to random node if no valid neighbors
        else:
            G.add_edge(i, x) # adding to a different random node
    return G

def induce_estimated_subgraph(G, size=500):
    """
    Given a graph G, return the subgraph induced by snowball sampling from G.
    Sampling starts from 10 random nodes and expands until 500.
    """
    startnodes = random.sample(list(G.nodes()), 10)
    sample_nodes = set(startnodes)
    frontier = set(startnodes)
    while len(sample_nodes) < 500:
        next_frontier = set()
        for node in frontier:
            for neighbor in G.neighbors(node):
                if neighbor not in sample_nodes:
                    next_frontier.add(neighbor)
        size_remaining = 500 - len(sample_nodes)
        if len(next_frontier) <= size_remaining:
            sample_nodes.update(next_frontier)
            frontier = next_frontier
        else:
            nodes_to_add = random.sample(list(next_frontier), size_remaining)
            sample_nodes.update(nodes_to_add)
            break
    
    G_sample = G.subgraph(sample_nodes)
    return G_sample

def rnes(G):
    ''' 
    Returns a random sample of 500 nodes and 500 of their neighbors 
    from graph G.
    '''
    sample = set()
    while len(sample) < 1000:
        node1 = random.choice(list(G.nodes()))
        edges = list(G.neighbors(node1))
        if edges:
            node2 = random.choice(edges)
        sample.add(node1)
        sample.add(node2)
    return list(sample)

def all_shortest_from(G, node_i):
    """
    For a given node_i in the network, construct a dictionary containing
    the length of the shortest path between that node and all others in
    the network. Values of -1 correspond to nodes where no paths connect
    to node_i.
    
    Parameters
    ----------
    G (nx.Graph)
        the graph in question
    
    node_i (int or str)
        the label of the "source" node
    
    Returns
    -------
    distances (dict)
        dictionary where the key corresponds to other nodes in the network
        and the values indicate the shortest path length between that node
        and the original node_i source.
    
    """
    queue = [node_i]
    
    distances = {i: -1 for i in G.nodes()}
    
    distances[node_i] = 0
    
    while(queue):
        current_node = queue.pop(0)
        neighbors = G.neighbors(current_node)
        for next_node in neighbors:
            if distances[next_node] < 0:
                distances[next_node] = distances[current_node] + 1
                queue.append(next_node)

    return distances

def remap_partition(partition):
    """
    Converts and remaps a partition to a list-of-lists structure suitable for modularity calculations.

    This function remaps the input partition (whether it's in dictionary form or a flat list of community labels) 
    to a list-of-lists format, where each list represents a community and contains the nodes in that community. 
    The function also ensures that community labels are contiguous integers starting from 0, which is typically 
    required for modularity-based algorithms.
    """

    # if partition is a dictionary where the keys are nodes and values communities
    if type(partition)==dict:
        unique_comms = np.unique(list(partition.values()))
        comm_mapping = {i:ix for ix,i in enumerate(unique_comms)}
        for i,j in partition.items():
            partition[i] = comm_mapping[j]

        unique_comms = np.unique(list(partition.values()))
        communities = [[] for i in unique_comms]
        for i,j in partition.items():
            communities[j].append(i)
            
        return communities

    # if partition is a list of community assignments
    elif type(partition)==list and\
            not any(isinstance(el, list) for el in partition):
        unique_comms = np.unique(partition)
        comm_mapping = {i:ix for ix,i in enumerate(unique_comms)}
        for i,j in enumerate(partition):
            partition[i] = comm_mapping[j]

        unique_comms = np.unique(partition)
        communities = [[] for i in np.unique(partition)]
        for i,j in enumerate(partition):
            communities[j].append(i)

        return communities

    # otherwise assume input is a properly-formatted list of lists
    else:
        communities = partition.copy()
        return communities