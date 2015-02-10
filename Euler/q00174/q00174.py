#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shared

# We shall define a square lamina to be a square outline with a square "hole" so that the shape possesses vertical and horizontal symmetry.
# Given eight tiles it is possible to form a lamina in only one way: 3x3 square with a 1x1 hole in the middle. However, using thirty-two tiles it is possible to form two distinct laminae.
# # If t represents the number of tiles used, we shall say that t = 8 is type L(1) and t = 32 is type L(2).
# Let N(n) be the number of t <= 1000000 such that t is type L(n); for example, N(15) = 832.
# What is Sum(N(n)) for 1 <= n <= 10?

expected = 209566


def L(t):
    count = 0
    one_side_uses = t/4
    short_side = 1
    while short_side < one_side_uses/short_side:
        if one_side_uses % short_side == 0:
            count += 1
        short_side += 1
    return count

def N(n):
    count = 0
    for t in range(8, 1000000 +1, 4):
        if L(t) == n:
            count += 1
    print n, count
    return count

def solve():
    count = 0
    for t in range(8, 1000000 + 1, 4):
        if L(t) <= 10:
            count += 1
    return count

