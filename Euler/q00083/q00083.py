#!/usr/bin/env python

import collections
import heapq

# NOTE: This problem is a significantly more challenging version of Problem 81.

# In the 5 by 5 matrix below, the minimal path sum from the top left
# to the bottom right, by moving left, right, up, and down, is
# indicated in bold red and is equal to 2297.


# 131	673	234	103	18
# 201	96	342	965	150
# 630	803	746	422	111
# 537	699	497	121	956
# 805	732	524	37	331

# Find the minimal path sum, in matrix.txt (right click and 'Save
# Link/Target As...'), a 31K text file containing a 80 by 80 matrix,
# from the top left to the bottom right by moving left, right, up, and
# down.

expected = 425185

COST = 0
POSITION = 1

def step(path, matrix, goal):
    position = path[POSITION]
    new_paths = []
    for move in [(0,-1), (-1,0), (0,1), (1,0)]:
        new_position = (position[0] + move[0], position[1] + move[1])
        new_path = (path[COST] + matrix[new_position], new_position)
        new_paths.append(new_path)
    return new_paths
        
def solve():
    shortest_paths = {}
    matrix = collections.defaultdict(lambda: 999999999)
    row = 0
    for line in file('matrix.txt'):
        col = 0
        for n in line.split(','):
            matrix[(row, col)] = int(n)
            col += 1
        row += 1

    goal = (row-1, col-1)

    # paths - a heapified list of (cost, path) elements
    paths = [(matrix[(0,0)], (0,0))]

    while True:
        shortest_path = heapq.heappop(paths)
        #print len(paths), '\t', shortest_path[COST], shortest_path[YET_TO_GO]
        if shortest_path[POSITION] == goal:
            return shortest_path[COST]

        new_paths = step(shortest_path, matrix, goal)
        for new_path in new_paths:
            position = new_path[POSITION]
            shortest_paths.get(position, new_path[COST])

            # only keep this path if there was no shorter way to get to this
            # position
            if shortest_paths.has_key(position):
                if shortest_paths[position] <= new_path[COST]:
                    continue
            shortest_paths[position] = new_path[COST]
            heapq.heappush(paths, new_path)

        


