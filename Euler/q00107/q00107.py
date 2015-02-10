#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Using network.txt (right click and 'Save Link/Target As...'), a 6K
# text file containing a network with forty vertices, and given in
# matrix form, find the maximum saving which can be achieved by
# removing redundant edges whilst ensuring that the network remains
# connected.

expected = 259679


def solve():
    # Build a minimum spanning tree.
    # Sort edges by weight, and put each node in its own component.
    # Pull out shortest edge and if it joins two components, add to the tree.
    # Repeat until there's one component.

    i = 0
    edges = []
    for line in file('network.txt'):
        j = 0
        weights = line.strip().split(',')
        for weight in weights[i:]:
            if weight != '-':
                edges.append((int(weight), i, i+j))
            j += 1
        i += 1
    edges.sort()

    full_cost = sum((e[0] for e in edges))
    spanning_cost = 0
    
    components = [[c] for c in range(i)]

    while len(components) > 1:
        edge = edges.pop(0)
        c1 = [c for c in components if edge[1] in c][0]
        c2 = [c for c in components if edge[2] in c][0]
        if c1 != c2:
            c1.extend(c2)
            components.remove(c2)
            spanning_cost += edge[0]
    return full_cost - spanning_cost
    


