#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# NOTE: This is a more difficult version of problem 114.

# A row measuring n units in length has red blocks with a minimum
# length of m units placed on it, such that any two red blocks (which
# are allowed to be different lengths) are separated by at least one
# black square.

# Let the fill-count function, F(m, n), represent the number of ways that a row can be filled.
# For example, F(3, 29) = 673135 and F(3, 30) = 1089155.

# That is, for m = 3, it can be seen that n = 30 is the smallest value for which the fill-count function first exceeds one million.

# In the same way, for m = 10, it can be verified that F(10, 56) =
# 880711 and F(10, 57) = 1148904, so n = 57 is the least value for
# which the fill-count function first exceeds one million.

# For m = 50, find the least value of n for which the fill-count function first exceeds one million.

@shared.Memoize
def fit(m, row_size):
    if row_size < 0:
        return 0

    if row_size < m:
        return 1

    result = fit(m, row_size - 1) + \
           sum(fit(m, row_size - tile_size - 1) for tile_size in range(m, row_size+1)) + \
           1
    return result


expected = 168

def solve():
    target = 10**6
    n = 50
    while True:
        if fit(50, n) > target:
            return n
        n += 1

