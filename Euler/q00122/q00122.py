#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# The most naive way of computing n**15 requires fourteen multiplications:
# n * n * ... * n = n**15
# But using a "binary" method you can compute it in six multiplications:
# n * n = n**2
# n**2 * n**2 = n**4
# n**4 * n**4 = n**8
# n**8 * n**4 = n**12
# n**12 * n**2 = n**14
# n**14 * n = n**15
# However it is yet possible to compute it in only five multiplications:
# n * n = n**2
# n**2 * n = n**3
# n**3 * n**3 = n**6
# n**6 * n**6 = n**12
# n**12 * n**3 = n**15
# We shall define m(k) to be the minimum number of multiplications to compute n**k; for example m(15) = 5.
# For 1 <= k <= 200, find sum(m(k)).
# 

expected = 1582

def solve():
    highest = 200
    sets = [[1]]
    counts = [0]

    n = 2
    while n <= highest:
        
        # clean out the sets that don't add up to n - save ~7 seconds
        i = 0
        while 2 * sets[i][-1] < n-1:
            i += 1
        sets = sets[i:]        
        
        shortest = n
        new_sets = []
        for p in sets:
            for i in range(len(p)):
                for j in range(i, len(p)):
                    if p[i] + p[j] == n:
                        new_sets.append(p + [n])
                        shortest = min(shortest, len(p)) # len(p) because the 1 doesn't count

        counts.append(shortest)

        for p in new_sets:
            if len(p) == shortest+1:
                sets.append(p)

        n += 1

    return sum(counts)

