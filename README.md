# Welcome to cnet_toolkit

| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |


cnet_toolkit is a simple package containing a set of 9 functions for use in network analysis and network analysis coursework. Content sourced from CNET5051 coursework at Northeastern University.

## Get started

You can install this package into your preferred Python environment using pip:

```bash
$ pip install cnet_toolkit
```

Example:

```python
import cnet_toolkit as cnet
graphs = []
for i in range(1000):
    G = erdos_renyi_graph(500, 0.3)
    graphs.append(G)
cnet.avg_adj_matrix(graphs)
```

## Contents

### ***random_edge***
Selects a random edge from graph G.

### ***random_node***
Selects a random node from graph G.

### ***centrality_function_tester***
Tests a provided centrality function against its corresponding NetworkX function and a set of potential edge cases.

### ***avg_adj_matrix***
Returns the average adjacency matrix from a list of graphs of identical dimension.

### ***randomWalkGenerator***
Generates a graph using the random walk method. New nodes are connected to two existing nodes: one random and, with probability p,
one of that random node's neighbors, or else another random node.

### ***induce_estimated_subgraph***
Given a graph G, return the subgraph induced by snowball sampling from G. Sampling starts from 10 random nodes and expands until 500.

### ***rnes***
Returns a random sample of 500 node-neighbor pairs from graph G.

### ***all_shortest_from***
For a given node_i in the network, constructs a dictionary containing the length of the shortest path between that node and all others 
in the network.

### ***remap_partition***
Converts a partition into a list-of-lists structure suitable for modularity calculations.

## Copyright

- Copyright © 2025 Caleb Chandler.
- Free software distributed under the [MIT License](./LICENSE).
