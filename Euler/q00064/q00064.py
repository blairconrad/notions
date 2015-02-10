#!/usr/bin/env python

import math
import shared

# Exactly four continued fractions, for N <= 13, have an odd period.
# How many continued fractions for N <= 10000 have an odd period?


expected = 1322

def solve():
    N = 10000
    count = 0

    for base in range(N+1):
        root = base**0.5
        if int(root) == root:
            continue

        # calculate the first term, which won't be part of the cycle
        denom = 1
        n = int(math.floor(root))
        plus = -n



        i = 0
        while True:
            new_denom = base - plus*plus
            common = shared.gcd(new_denom, denom)

            top = (denom * (root - plus))/common
            denom = new_denom/common        

            n = int(math.floor(top/denom))
            plus = -plus - denom * n

            this_tuple = (n,denom, plus)

            if i == 0:
                saved = this_tuple
            elif saved == this_tuple:
                count += i % 2
                break
            i += 1

    return count

