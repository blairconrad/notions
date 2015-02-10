#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared


# Let p_(n) be the nth prime: 2, 3, 5, 7, 11, ..., and let r be the
# remainder when (p_(n)-1)^(n) + (p_(n)+1)^(n) is divided by
# p_(n)^(2).

# For example, when n = 3, p_(3) = 5, and 4^(3) + 6^(3) = 280 ? 5 mod
# 25.

# The least value of n for which the remainder first exceeds 10^(9) is
# 7037.

# Find the least value of n for which the remainder first exceeds
# 10^(10).


expected = 21035

def solve():

    # if n is odd, the sum will be 2 * n * p
    # if even, the sum will be 2, so skip the evens
    to_exceed = 10**10

    n = 0
    for p in shared.prime_generator():
        n += 1
        if not n % 2: continue

        if 2 * n * p  > to_exceed:
            return n
    pass

