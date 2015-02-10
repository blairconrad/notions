#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import collections

# A spider, S, sits in one corner of a cuboid room, measuring 6 by 5
# by 3, and a fly, F, sits in the opposite corner. By travelling on
# the surfaces of the room the shortest "straight line" distance from
# S to F is 10 and the path is shown on the diagram.

# However, there are up to three "shortest" path candidates for any
# given cuboid and the shortest route is not always integer.

# By considering all cuboid rooms with integer dimensions, up to a
# maximum size of M by M by M, there are exactly 2060 cuboids for
# which the shortest distance is integer when M=100, and this is the
# least value of M for which the number of solutions first exceeds two
# thousand; the number of solutions is 1975 when M=99.

# Find the least value of M such that the number of solutions first
# exceeds one million.


expected = 1818

def shortest(w, l, h):
    return math.sqrt(min((w+l)**2 + h**2,
                         (w+h)**2 + l**2,
                         (l+h)**2 + w**2))

def solve():
    short_sides = collections.defaultdict(int)
    count = 0
    M = 1
    while True:
        for ss in range(M+1, 2*M+1):
            short_sides[ss] += 1
        
        #print M, short_sides
        for ss in range(2, 2*M+1):
            #print 'ss', ss, short_sides[ss]
            length = math.sqrt(ss**2 + M*M)
            #print M, ss, length
            if int(length) == length:
                #print 'adding', M, ss, short_sides[ss]
                count += short_sides[ss]

        #print M, count
        if count > 10**6:
            return M
        M += 1

