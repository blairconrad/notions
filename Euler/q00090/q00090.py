#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# Each of the six faces on a cube has a different digit (0 to 9)
# written on it; the same is done to a second cube. By placing the two
# cubes side-by-side in different positions we can form a variety of
# 2-digit numbers.

# For example, the square number 64 could be formed:

# In fact, by carefully choosing the digits on both cubes it is
# possible to display all of the square numbers below one-hundred: 01,
# 04, 09, 16, 25, 36, 49, 64, and 81.

# For example, one way this can be achieved is by placing {0, 5, 6, 7,
# 8, 9} on one cube and {1, 2, 3, 4, 8, 9} on the other cube.

# However, for this problem we shall allow the 6 or 9 to be turned
# upside-down so that an arrangement like {0, 5, 6, 7, 8, 9} and {1,
# 2, 3, 4, 6, 7} allows for all nine square numbers to be displayed;
# otherwise it would be impossible to obtain 09.

# In determining a distinct arrangement we are interested in the
# digits on each cube, not the order.

# {1, 2, 3, 4, 5, 6} is equivalent to {3, 6, 4, 1, 2, 5}
# {1, 2, 3, 4, 5, 6} is distinct from {1, 2, 3, 4, 5, 9}

# But because we are allowing 6 and 9 to be reversed, the two distinct
# sets in the last example both represent the extended set {1, 2, 3,
# 4, 5, 6, 9} for the purpose of forming 2-digit numbers.

# How many distinct arrangements of the two cubes allow for all of the
# square numbers to be displayed?


expected = 1217



def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def works(d1,d2):
    #print d1, d2
    squares = ['01', '04', '06', '16', '25', '36', '64', '81'] # omit 46, as it's 64 backwards

    d1 = d1.replace('9', '6')
    d2 = d2.replace('9', '6')

    for square in squares:
        if ((square[0] not in d1 or square[1] not in d2) and
            (square[0] not in d2 or square[1] not in d1) ):
            return False
    return True

def solve():
    digits = range(10)
    dice = []
    for p in combinations(digits, 6):
        dice.append(''.join((str(f) for f in p)))

    count = 0
    for d1 in dice:
        for d2 in dice:
            if d1 > d2: continue
            if works(d1, d2):
                count += 1

    return count #

