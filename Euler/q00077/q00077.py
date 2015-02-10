#!/usr/bin/env python

# It is possible to write ten as the sum of primes in exactly five different ways:

# 7 + 3
# 5 + 5
# 5 + 3 + 2
# 3 + 3 + 2 + 2
# 2 + 2 + 2 + 2 + 2

# What is the first value which can be written as the sum of primes in over five thousand different ways?

import shared
import collections

expected = 71

SMALLEST = 0
COUNT = 1

def solve():
    counts = collections.defaultdict(list)
    n = 2
    while True:
        g = shared.prime_generator()
        for p in g:
            if p > n:
                break
            elif p == n:
                counts[n].append((n, 1))
            else:
                old_n = n - p
                count_for_p = 0
                for old_count in counts[old_n]:
                    if old_count[SMALLEST] >= p:
                        count_for_p += old_count[COUNT]
                if count_for_p:
                    counts[n].append((p, count_for_p))
        if sum((record[COUNT] for record in counts[n])) > 5000:
            return n
        n += 1

        

